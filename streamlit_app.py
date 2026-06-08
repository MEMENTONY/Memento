import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide"
)

# =============================
# 디자인 CSS
# =============================
st.markdown(
    """
    <style>
    .main {
        background-color: #0f1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 50%, #0f172a 100%);
        padding: 28px;
        border-radius: 22px;
        border: 1px solid #334155;
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #cbd5e1;
    }

    .card {
        background-color: #111827;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 16px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .card-text {
        color: #cbd5e1;
        font-size: 15px;
    }

    .good {
        color: #22c55e;
        font-weight: 800;
    }

    .warning {
        color: #facc15;
        font-weight: 800;
    }

    .bad {
        color: #ef4444;
        font-weight: 800;
    }

    .neutral {
        color: #38bdf8;
        font-weight: 800;
    }

    .small-caption {
        color: #94a3b8;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# 세션 저장소
# =============================
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

if "market_board" not in st.session_state:
    st.session_state.market_board = []


# =============================
# 기본 함수
# =============================
def money(value):
    return f"${value:,.2f}"


def cents(value):
    return f"{value:.2f}¢"


def pct(value):
    return f"{value:+.2f}%"


def clamp_score(score):
    return max(0, min(100, score))


def judge_edge(edge):
    if edge >= 15:
        return 30, "매우 좋음", "내 예상 승률이 시장 가격보다 크게 높습니다."
    elif edge >= 10:
        return 25, "좋음", "좋은 value 가능성이 있습니다."
    elif edge >= 5:
        return 15, "약간 좋음", "소액 진입은 검토 가능합니다."
    elif edge >= 0:
        return 5, "약함", "edge가 작습니다. 신중해야 합니다."
    else:
        return -25, "나쁨", "내 예상 승률보다 시장 가격이 비쌉니다."


def judge_price(current_price):
    if current_price >= 95:
        return -35, "매우 위험", "95¢ 이상은 신규 진입보다 익절/상환 구간에 가깝습니다."
    elif current_price >= 90:
        return -25, "위험", "90¢ 이상은 신규 매수 손익비가 좋지 않습니다."
    elif current_price >= 80:
        return -12, "주의", "80¢ 이상은 이겨도 수익이 작고, 틀리면 손실이 큽니다."
    elif current_price >= 60:
        return 5, "보통", "가격이 꽤 올라온 구간입니다. edge가 충분해야 합니다."
    elif current_price >= 30:
        return 15, "양호", "가격과 수익비가 비교적 균형 잡힌 구간입니다."
    elif current_price >= 10:
        return 5, "변동성 큼", "저가 구간입니다. 맞으면 크지만 실패 확률도 큽니다."
    elif current_price >= 2:
        return -5, "초저가 역배", "2~10¢ 구간은 bounce trade 소액 전용으로 보는 게 좋습니다."
    else:
        return -15, "극단적 역배", "거의 복권에 가까운 구간입니다."


def judge_position_size(position_pct):
    if position_pct <= 2:
        return 20, "안전", "전체 자산 대비 부담이 작은 포지션입니다."
    elif position_pct <= 5:
        return 12, "보통", "감당 가능한 수준이지만 연속 손실은 조심해야 합니다."
    elif position_pct <= 10:
        return -5, "위험", "전체 자산의 5~10%입니다. 꽤 큰 포지션입니다."
    else:
        return -30, "매우 위험", "전체 자산의 10% 이상입니다. 리스크 위험 상태입니다."


def judge_cap(stake, bet_type, bankroll):
    if bet_type == "확실한 경기":
        fixed_cap = 50
        pct_cap = bankroll * 0.05
        cap_note = "확실한 경기 기본 상한선: $50 또는 계좌의 5%"
    elif bet_type == "중간 확신":
        fixed_cap = 30
        pct_cap = bankroll * 0.03
        cap_note = "중간 확신 기본 상한선: $30 또는 계좌의 3%"
    else:
        fixed_cap = 10
        pct_cap = bankroll * 0.01
        cap_note = "역배/bounce 기본 상한선: $10 또는 계좌의 1%"

    final_cap = min(fixed_cap, pct_cap) if bankroll > 0 else fixed_cap

    if stake <= final_cap:
        return 15, final_cap, "상한선 이내", cap_note
    elif stake <= final_cap * 1.2:
        return 0, final_cap, "상한선 근처", cap_note
    else:
        return -25, final_cap, "상한선 초과", cap_note


def judge_bookmaker(book_prob, current_price):
    if book_prob <= 0:
        return 0, "미입력", "북메이커 기준 승률을 입력하지 않았습니다."

    book_edge = book_prob - current_price

    if book_edge >= 10:
        return 15, "북메이커 대비 저평가", "스포츠 배당 기준으로도 Polymarket 가격이 싸 보입니다."
    elif book_edge >= 5:
        return 8, "약한 저평가", "북메이커 기준으로 약간 싸 보입니다."
    elif book_edge > -5:
        return 0, "비슷함", "북메이커 기준과 큰 차이가 없습니다."
    elif book_edge > -10:
        return -8, "약간 비쌈", "북메이커 기준보다 Polymarket 가격이 비싼 편입니다."
    else:
        return -18, "비쌈", "북메이커 기준으로는 Polymarket 가격이 비싸 보입니다."


def judge_chase_risk(reference_price, current_price):
    price_jump = current_price - reference_price

    if reference_price <= 0:
        return 0, "미입력", "처음 봤던 저평가 가격을 입력하지 않았습니다.", price_jump

    if price_jump <= 0:
        return 10, "추격 아님", "처음 봤던 가격보다 아직 비싸지지 않았습니다.", price_jump
    elif price_jump <= 5:
        return 8, "괜찮음", "처음 봤던 가격보다 조금 올랐지만 아직 추격 위험은 작습니다.", price_jump
    elif price_jump <= 15:
        return 2, "주의", "가격이 꽤 올라왔습니다. 진입 금액을 줄이는 게 좋습니다.", price_jump
    elif price_jump <= 30:
        return -12, "추격 위험", "처음 봤던 저평가 구간을 많이 놓쳤습니다.", price_jump
    else:
        return -25, "FOMO 위험", "30¢ 이상 급등 후 진입은 추격매수 위험이 큽니다.", price_jump


def final_decision(score, edge, current_price, position_pct, stake, cap):
    if current_price >= 95:
        return "강한 비추천", "95¢ 이상은 신규 진입보다 익절/상환 구간입니다."
    if edge < 0:
        return "비추천", "Edge가 음수입니다. 내 판단 기준으로는 비싼 가격입니다."
    if position_pct > 10:
        return "금액 축소 필요", "전체 자산의 10% 이상입니다. 포지션 크기가 너무 큽니다."
    if stake > cap * 1.2:
        return "금액 축소 필요", "배팅 상한선을 초과했습니다."

    if score >= 80:
        return "진입 강함", "조건은 좋지만, 그래도 분할 진입과 손절 기준이 필요합니다."
    elif score >= 65:
        return "진입 약함", "소액 진입은 가능하지만 큰 금액은 조심해야 합니다."
    elif score >= 50:
        return "관망 우선", "edge나 가격 조건이 애매합니다. 더 좋은 가격을 기다리는 게 좋습니다."
    elif score >= 35:
        return "비추천", "리스크 대비 보상이 부족합니다."
    else:
        return "강한 비추천", "여러 평가 항목에서 위험 신호가 많습니다."


# =============================
# 상단 디자인
# =============================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">📊 Memento</div>
        <div class="hero-subtitle">
        Polymarket 배팅 가치 판독기 + 거래 손익 기록장<br>
        자동매매가 아니라, 진입 전 리스크를 숫자로 확인하는 수동 판단 도구입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 메인 판독기",
    "💰 거래 손익 계산기",
    "📈 총수익률",
    "📰 EDGE / NEWS"
])


# =====================================================
# 1. 메인 배팅 가치 판독기
# =====================================================
with tab1:
    st.header("🏠 배팅 가치 판독기")
    st.caption("가격, edge, 배팅금액, 포트폴리오 비율, 북메이커 기준, 추격매수 위험을 종합 평가합니다.")

    st.markdown('<div class="card"><div class="card-title">① 기본 정보</div><div class="card-text">시장 이름과 현재 가격, 내 예상 승률을 입력하세요.</div></div>', unsafe_allow_html=True)

    market_name = st.text_input(
        "시장 이름",
        "T1 vs HLE — Match Winner",
        key="main_market_name"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        current_price = st.number_input(
            "현재 Polymarket 가격(센트)",
            min_value=1.0,
            max_value=99.0,
            value=56.0,
            key="main_current_price"
        )

    with col2:
        my_probability = st.number_input(
            "내가 생각하는 실제 승률(%)",
            min_value=1.0,
            max_value=99.0,
            value=65.0,
            key="main_my_probability"
        )

    with col3:
        reference_price = st.number_input(
            "처음 봤던 저평가 가격(센트)",
            min_value=0.0,
            max_value=99.0,
            value=30.0,
            key="main_reference_price"
        )

    st.markdown('<div class="card"><div class="card-title">② 금액 / 리스크 설정</div><div class="card-text">내 전체 자산 대비 이번 배팅이 얼마나 큰지 확인합니다.</div></div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        bankroll = st.number_input(
            "현재 전체 포트폴리오 / 총자산($)",
            min_value=1.0,
            value=500.0,
            key="main_bankroll"
        )

    with col5:
        stake = st.number_input(
            "이번 투자금($)",
            min_value=1.0,
            value=50.0,
            key="main_stake"
        )

    with col6:
        bet_type = st.selectbox(
            "배팅 성격",
            ["확실한 경기", "중간 확신", "역배/bounce"],
            key="main_bet_type"
        )

    st.markdown('<div class="card"><div class="card-title">③ 목표가 / 손절가 / 스포츠 배당</div><div class="card-text">목표 매도가, 손절가, 북메이커 기준 승률을 입력하면 더 정확하게 평가합니다.</div></div>', unsafe_allow_html=True)

    col7, col8, col9 = st.columns(3)

    with col7:
        target_sell_price = st.number_input(
            "목표 매도가(센트)",
            min_value=1.0,
            max_value=100.0,
            value=75.0,
            key="main_target_sell_price"
        )

    with col8:
        stop_loss_price = st.number_input(
            "손절가(센트)",
            min_value=0.0,
            max_value=99.0,
            value=45.0,
            key="main_stop_loss_price"
        )

    with col9:
        bookmaker_probability = st.number_input(
            "스포츠 북메이커 기준 승률(%)",
            min_value=0.0,
            max_value=99.0,
            value=60.0,
            key="main_bookmaker_probability"
        )

    if st.button("🔍 배팅 가치 판독하기", key="main_analyze_button"):
        price_decimal = current_price / 100
        target_decimal = target_sell_price / 100
        stop_decimal = stop_loss_price / 100

        shares = stake / price_decimal
        payout_if_win = shares
        profit_if_win = payout_if_win - stake
        loss_if_lose = stake

        target_sell_amount = shares * target_decimal
        target_profit = target_sell_amount - stake

        stop_loss_amount = shares * stop_decimal
        stop_loss_result = stop_loss_amount - stake

        risk_amount = stake - stop_loss_amount
        reward_amount = target_profit

        if risk_amount > 0:
            risk_reward = reward_amount / risk_amount
        else:
            risk_reward = 0

        edge = my_probability - current_price
        position_pct = (stake / bankroll) * 100

        edge_score, edge_label, edge_note = judge_edge(edge)
        price_score, price_label, price_note = judge_price(current_price)
        size_score, size_label, size_note = judge_position_size(position_pct)
        cap_score, cap, cap_label, cap_note = judge_cap(stake, bet_type, bankroll)
        book_score, book_label, book_note = judge_bookmaker(bookmaker_probability, current_price)
        chase_score, chase_label, chase_note, price_jump = judge_chase_risk(reference_price, current_price)

        raw_score = 50 + edge_score + price_score + size_score + cap_score + book_score + chase_score
        final_score = clamp_score(raw_score)

        decision, decision_note = final_decision(
            final_score,
            edge,
            current_price,
            position_pct,
            stake,
            cap
        )

        st.divider()
        st.subheader("📌 최종 판정")

        col_result1, col_result2, col_result3 = st.columns(3)

        with col_result1:
            st.metric("최종 점수", f"{final_score}/100")

        with col_result2:
            st.metric("최종 판단", decision)

        with col_result3:
            st.metric("포트폴리오 비중", f"{position_pct:.2f}%")

        st.progress(final_score / 100)

        if decision in ["진입 강함"]:
            st.success(f"{decision}: {decision_note}")
        elif decision in ["진입 약함", "관망 우선", "금액 축소 필요"]:
            st.warning(f"{decision}: {decision_note}")
        else:
            st.error(f"{decision}: {decision_note}")

        st.divider()

        st.subheader("📊 핵심 계산 결과")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("시장 implied probability", f"{current_price:.2f}%")
        m2.metric("내 예상 승률", f"{my_probability:.2f}%")
        m3.metric("Edge", pct(edge))
        m4.metric("보유 수량", f"{shares:.2f}주")

        m5, m6, m7, m8 = st.columns(4)

        m5.metric("승리 시 총 수령액", money(payout_if_win))
        m6.metric("승리 시 순이익", money(profit_if_win))
        m7.metric("패배 시 손실", f"-{money(loss_if_lose)}")
        m8.metric("손익비", f"{risk_reward:.2f} : 1")

        st.divider()

        st.subheader("🧠 평가 항목별 판독")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">1. Edge 평가</div>
                    <div class="card-text">
                    상태: <span class="neutral">{edge_label}</span><br>
                    Edge: <b>{edge:+.2f}%</b><br>
                    설명: {edge_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">2. 진입가격 평가</div>
                    <div class="card-text">
                    상태: <span class="warning">{price_label}</span><br>
                    현재 가격: <b>{current_price:.2f}¢</b><br>
                    설명: {price_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">3. 추격매수 / FOMO 평가</div>
                    <div class="card-text">
                    상태: <span class="warning">{chase_label}</span><br>
                    처음 본 가격: <b>{reference_price:.2f}¢</b><br>
                    현재 가격: <b>{current_price:.2f}¢</b><br>
                    가격 변화: <b>{price_jump:+.2f}¢</b><br>
                    설명: {chase_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_b:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">4. 배팅금액 크기 평가</div>
                    <div class="card-text">
                    상태: <span class="neutral">{size_label}</span><br>
                    이번 투자금: <b>{money(stake)}</b><br>
                    전체 자산: <b>{money(bankroll)}</b><br>
                    포트폴리오 비중: <b>{position_pct:.2f}%</b><br>
                    설명: {size_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">5. 배팅 상한선 평가</div>
                    <div class="card-text">
                    상태: <span class="warning">{cap_label}</span><br>
                    배팅 성격: <b>{bet_type}</b><br>
                    추천 상한선: <b>{money(cap)}</b><br>
                    현재 투자금: <b>{money(stake)}</b><br>
                    기준: {cap_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">6. 스포츠 배당 비교</div>
                    <div class="card-text">
                    상태: <span class="neutral">{book_label}</span><br>
                    북메이커 기준 승률: <b>{bookmaker_probability:.2f}%</b><br>
                    Polymarket 가격: <b>{current_price:.2f}%</b><br>
                    차이: <b>{bookmaker_probability - current_price:+.2f}%</b><br>
                    설명: {book_note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.subheader("🎯 목표가 / 손절가 시나리오")

        s1, s2, s3 = st.columns(3)

        s1.metric("목표가 도달 시 예상 수익", money(target_profit))
        s2.metric("손절가 도달 시 예상 손익", money(stop_loss_result))
        s3.metric("추천 상한선", money(cap))

        st.divider()

        st.subheader("📝 기록용 요약")

        summary = (
            f"{market_name}\n"
            f"현재가: {current_price:.0f}¢ / 내 예상 승률: {my_probability:.1f}% / "
            f"Edge: {edge:+.1f}% / 투자금: ${stake:.2f} / "
            f"포트폴리오 비중: {position_pct:.1f}% / "
            f"북메이커 기준: {bookmaker_probability:.1f}% / "
            f"처음 본 가격: {reference_price:.0f}¢ → 현재 {current_price:.0f}¢ / "
            f"최종판정: {decision} / 점수: {final_score}/100"
        )

        st.code(summary)

        if st.button("이 시장을 EDGE / NEWS 보드에 추가", key="add_main_to_board"):
            st.session_state.market_board.append({
                "날짜": str(date.today()),
                "시장 이름": market_name,
                "현재가": f"{current_price:.2f}¢",
                "내 예상 승률": f"{my_probability:.2f}%",
                "Edge": edge,
                "북메이커 기준": f"{bookmaker_probability:.2f}%",
                "포트폴리오 비중": f"{position_pct:.2f}%",
                "판정": decision,
                "점수": final_score,
                "메모": "메인 판독기에서 추가"
            })
            st.success("EDGE / NEWS 보드에 추가했습니다.")


# =====================================================
# 2. 거래 손익 계산기
# =====================================================
with tab2:
    st.header("💰 거래 손익 계산기")
    st.caption("일반 매도와 부분매도를 계산하고, 워드에 붙여넣기 좋은 요약을 만듭니다.")

    trade_name = st.text_input(
        "거래 이름",
        "Anyone's Legend vs Bilibili Gaming — Game 1 Winner",
        key="trade_name"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        buy_price = st.number_input(
            "매수가(센트)",
            min_value=1.0,
            max_value=99.0,
            value=54.0,
            key="trade_buy_price"
        )

    with col2:
        sell_price = st.number_input(
            "매도가(센트)",
            min_value=0.0,
            max_value=100.0,
            value=87.0,
            key="trade_sell_price"
        )

    with col3:
        trade_stake = st.number_input(
            "투자금($)",
            min_value=1.0,
            value=77.19,
            key="trade_stake"
        )

    use_partial_sell = st.checkbox("부분매도 계산하기", key="use_partial_sell")

    if use_partial_sell:
        col4, col5, col6 = st.columns(3)

        with col4:
            partial_sell_price = st.number_input(
                "부분매도 가격(센트)",
                min_value=0.0,
                max_value=100.0,
                value=73.0,
                key="partial_sell_price"
            )

        with col5:
            partial_sell_shares = st.number_input(
                "부분매도 수량",
                min_value=0.0,
                value=24.5,
                key="partial_sell_shares"
            )

        with col6:
            final_sell_price = st.number_input(
                "남은 포지션 최종 매도가(센트)",
                min_value=0.0,
                max_value=100.0,
                value=100.0,
                key="final_sell_price"
            )

    if st.button("손익 계산하기", key="calculate_trade"):
        buy_decimal = buy_price / 100
        sell_decimal = sell_price / 100

        total_shares = trade_stake / buy_decimal

        if not use_partial_sell:
            sell_amount = total_shares * sell_decimal
            profit = sell_amount - trade_stake
            roi = (profit / trade_stake) * 100

            st.subheader("거래 요약")

            a, b, c, d = st.columns(4)

            a.metric("보유 수량", f"{total_shares:.2f}주")
            b.metric("매도금", money(sell_amount))
            c.metric("실현손익", money(profit))
            d.metric("수익률", f"{roi:+.2f}%")

            summary = (
                f"{trade_name}\n"
                f"매수가: {buy_price:.0f}¢ / "
                f"매도가: {sell_price:.0f}¢ / "
                f"투자금: ${trade_stake:.2f} / "
                f"실현손익: ${profit:+.2f} / "
                f"수익률: {roi:+.1f}%"
            )

            st.markdown("### 워드 기록용 한 줄 요약")
            st.code(summary)

            st.session_state.trade_log.append({
                "날짜": str(date.today()),
                "거래 이름": trade_name,
                "매수가": f"{buy_price:.2f}¢",
                "매도가": f"{sell_price:.2f}¢",
                "투자금": trade_stake,
                "손익": profit,
                "수익률": roi,
                "형태": "일반매도"
            })

        else:
            partial_decimal = partial_sell_price / 100
            final_decimal = final_sell_price / 100

            partial_sell_amount = partial_sell_shares * partial_decimal
            remaining_shares = total_shares - partial_sell_shares

            if remaining_shares < 0:
                st.error("부분매도 수량이 전체 보유 수량보다 큽니다.")
            else:
                remaining_sell_amount = remaining_shares * final_decimal
                total_sell_amount = partial_sell_amount + remaining_sell_amount

                profit = total_sell_amount - trade_stake
                roi = (profit / trade_stake) * 100

                st.subheader("부분매도 거래 요약")

                a, b, c, d = st.columns(4)

                a.metric("전체 수량", f"{total_shares:.2f}주")
                b.metric("총 매도금", money(total_sell_amount))
                c.metric("총손익", money(profit))
                d.metric("수익률", f"{roi:+.2f}%")

                summary = (
                    f"{trade_name}\n"
                    f"매수가: {buy_price:.0f}¢ / "
                    f"부분매도: {partial_sell_price:.0f}¢, {partial_sell_shares:.1f}주, ${partial_sell_amount:.2f} / "
                    f"남은 포지션: {remaining_shares:.1f}주 상환 ${remaining_sell_amount:.2f} / "
                    f"투자금: ${trade_stake:.2f} / "
                    f"총손익: ${profit:+.2f} / "
                    f"수익률: {roi:+.1f}%"
                )

                st.markdown("### 워드 기록용 한 줄 요약")
                st.code(summary)

                st.session_state.trade_log.append({
                    "날짜": str(date.today()),
                    "거래 이름": trade_name,
                    "매수가": f"{buy_price:.2f}¢",
                    "매도가": f"부분 {partial_sell_price:.2f}¢ / 최종 {final_sell_price:.2f}¢",
                    "투자금": trade_stake,
                    "손익": profit,
                    "수익률": roi,
                    "형태": "부분매도"
                })


# =====================================================
# 3. 총수익률
# =====================================================
with tab3:
    st.header("📈 총수익률 / 전체 성과")

    col1, col2, col3 = st.columns(3)

    with col1:
        starting_bankroll = st.number_input(
            "시작 자금($)",
            min_value=0.0,
            value=500.0,
            key="starting_bankroll"
        )

    with col2:
        current_bankroll = st.number_input(
            "현재 총자산($)",
            min_value=0.0,
            value=650.0,
            key="current_bankroll"
        )

    with col3:
        net_deposit = st.number_input(
            "추가 입금 / 출금 조정($)",
            value=0.0,
            key="net_deposit"
        )

    adjusted_start = starting_bankroll + net_deposit
    total_profit = current_bankroll - adjusted_start

    if adjusted_start > 0:
        total_roi = (total_profit / adjusted_start) * 100
    else:
        total_roi = 0

    a, b, c = st.columns(3)

    a.metric("총손익", money(total_profit))
    b.metric("총수익률", f"{total_roi:+.2f}%")
    c.metric("현재 총자산", money(current_bankroll))

    st.divider()

    st.subheader("거래일지 기준")

    if len(st.session_state.trade_log) == 0:
        st.warning("아직 거래 손익 계산기에서 추가된 거래가 없습니다.")
    else:
        total_trade_stake = sum(item["투자금"] for item in st.session_state.trade_log)
        total_trade_profit = sum(item["손익"] for item in st.session_state.trade_log)

        if total_trade_stake > 0:
            trade_roi = (total_trade_profit / total_trade_stake) * 100
        else:
            trade_roi = 0

        c1, c2, c3 = st.columns(3)

        c1.metric("기록된 거래 수", len(st.session_state.trade_log))
        c2.metric("누적 실현손익", money(total_trade_profit))
        c3.metric("거래 기준 ROI", f"{trade_roi:+.2f}%")

        st.dataframe(st.session_state.trade_log, use_container_width=True)

    if st.button("거래일지 초기화", key="clear_trade_log"):
        st.session_state.trade_log = []
        st.success("거래일지를 초기화했습니다.")


# =====================================================
# 4. EDGE / NEWS
# =====================================================
with tab4:
    st.header("📰 EDGE 높은 시장 / NEWS")
    st.caption("나중에 Polymarket API, 스포츠 배당, 뉴스 데이터를 연결할 공간입니다. 현재는 수동 기록 보드입니다.")

    st.subheader("관심 시장 수동 추가")

    news_market_name = st.text_input(
        "시장 이름",
        "Example: T1 vs HLE",
        key="news_market_name"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        news_price = st.number_input(
            "현재 가격(센트)",
            min_value=1.0,
            max_value=99.0,
            value=50.0,
            key="news_price"
        )

    with col2:
        news_my_probability = st.number_input(
            "내 예상 승률(%)",
            min_value=1.0,
            max_value=99.0,
            value=60.0,
            key="news_my_probability"
        )

    with col3:
        news_bookmaker = st.number_input(
            "북메이커 기준 승률(%)",
            min_value=0.0,
            max_value=99.0,
            value=55.0,
            key="news_bookmaker"
        )

    with col4:
        news_importance = st.selectbox(
            "관심도",
            ["낮음", "보통", "높음", "매우 높음"],
            key="news_importance"
        )

    news_note = st.text_area(
        "메모 / 뉴스 / 근거",
        "예: 라인업 변화, 부상, 시장 공포, 과매도, 북메이커와 가격 차이 등",
        key="news_note"
    )

    if st.button("관심 시장 추가", key="add_market_board"):
        news_edge = news_my_probability - news_price
        news_book_gap = news_bookmaker - news_price

        if news_edge >= 10 and news_book_gap >= 5:
            news_score = 90
            news_judge = "강한 저평가 후보"
        elif news_edge >= 10:
            news_score = 80
            news_judge = "저평가 후보"
        elif news_edge >= 5:
            news_score = 65
            news_judge = "소액 관찰 후보"
        elif news_edge >= 0:
            news_score = 50
            news_judge = "관망"
        else:
            news_score = 30
            news_judge = "비추천"

        st.session_state.market_board.append({
            "날짜": str(date.today()),
            "시장 이름": news_market_name,
            "현재가": f"{news_price:.2f}¢",
            "내 예상 승률": f"{news_my_probability:.2f}%",
            "Edge": news_edge,
            "북메이커 차이": news_book_gap,
            "관심도": news_importance,
            "판정": news_judge,
            "점수": news_score,
            "메모": news_note
        })

        st.success("관심 시장에 추가했습니다.")

    st.divider()

    st.subheader("EDGE 높은 시장 보드")

    if len(st.session_state.market_board) == 0:
        st.info("아직 추가한 시장이 없습니다.")
    else:
        sorted_board = sorted(
            st.session_state.market_board,
            key=lambda x: x["점수"],
            reverse=True
        )

        st.dataframe(sorted_board, use_container_width=True)

    if st.button("EDGE / NEWS 보드 초기화", key="clear_market_board"):
        st.session_state.market_board = []
        st.success("보드를 초기화했습니다.")

    st.divider()

    st.subheader("나중에 확장할 기능")
    st.write("✅ Polymarket API 자동 연결")
    st.write("✅ 시장 가격 자동 불러오기")
    st.write("✅ 스포츠 북메이커 배당률 자동 비교")
    st.write("✅ 뉴스 / 부상 / 라인업 자동 감시")
    st.write("✅ Edge 높은 시장 자동 정렬")
    st.write("✅ 텔레그램 / 디스코드 알림")
    st.write("✅ 반자동 주문 보조")