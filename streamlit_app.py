import streamlit as st
from datetime import date

st.set_page_config(page_title="Memento", page_icon="📊", layout="wide")

# =============================
# Design
# =============================
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .hero-box {
        background: linear-gradient(135deg, #111827 0%, #1f2937 55%, #0f172a 100%);
        padding: 28px;
        border-radius: 24px;
        border: 1px solid #334155;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    }
    .hero-title { font-size: 42px; font-weight: 900; color: #f8fafc; margin-bottom: 8px; }
    .hero-subtitle { font-size: 16px; color: #cbd5e1; line-height: 1.65; }
    .card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 18px 20px;
        margin: 12px 0px;
    }
    .card-title { font-size: 19px; font-weight: 800; color: #f8fafc; margin-bottom: 8px; }
    .card-text { color: #cbd5e1; font-size: 15px; line-height: 1.6; }
    .danger-box {
        background: #3f1111;
        border: 1px solid #ef4444;
        border-radius: 18px;
        padding: 18px 20px;
        margin: 12px 0px;
        color: #fee2e2;
    }
    .good { color: #22c55e; font-weight: 800; }
    .warn { color: #facc15; font-weight: 800; }
    .bad { color: #ef4444; font-weight: 800; }
    .info { color: #38bdf8; font-weight: 800; }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# Session storage
# =============================
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []
if "market_board" not in st.session_state:
    st.session_state.market_board = []

# =============================
# Utility functions
# =============================
def money(value):
    return f"${value:,.2f}"


def cents(value):
    return f"{value:.2f}¢"


def signed_pct(value):
    return f"{value:+.2f}%"


def clamp_score(score):
    return max(0, min(100, int(round(score))))


def portfolio_judgement(position_pct):
    if position_pct >= 50:
        return "시스템 실패 — 계좌 생존 리스크", "시스템 실패", -80
    if position_pct >= 20:
        return "진입 금지", "진입 금지", -60
    if position_pct >= 10:
        return "매우 위험", "전체 자산의 10~20%입니다. 이미 계좌 생존에 부담이 큽니다.", -35
    if position_pct >= 5:
        return "위험", "전체 자산의 5~10%입니다. 한 번 틀리면 회복 부담이 큽니다.", -20
    if position_pct >= 3:
        return "주의", "전체 자산의 3~5%입니다. 확신과 근거가 필요합니다.", -8
    return "정상", "전체 자산의 0~3%입니다. 포지션 크기는 비교적 정상입니다.", 12


def duplicate_exposure_judgement(total_exposure_pct):
    if total_exposure_pct >= 20:
        return "진입 금지", "같은 경기/팀/방향 총 노출이 20% 이상입니다.", -50
    if total_exposure_pct >= 10:
        return "위험", "같은 경기/팀/방향 총 노출이 10~20%입니다.", -25
    if total_exposure_pct >= 5:
        return "주의", "같은 경기/팀/방향 총 노출이 5~10%입니다.", -10
    return "정상", "같은 경기/팀/방향 총 노출이 5% 이하입니다.", 8


def confidence_cap(confidence):
    data = {
        "관찰용": (15, "관찰용은 $5~15 소액만 적절합니다."),
        "낮은 확신": (25, "낮은 확신은 $15~25 안에서 보는 게 좋습니다."),
        "중간 확신": (50, "중간 확신은 $25~50 범위가 기본 상한입니다."),
        "높은 확신": (70, "높은 확신도 $50~70을 넘으면 부담이 커집니다."),
        "초고확신": (70, "초고확신이어도 $70 이상은 강한 경고가 필요합니다."),
    }
    return data.get(confidence, (30, "기본 상한선을 적용했습니다."))


def account_cap(bankroll, confidence):
    pct_map = {
        "관찰용": 0.01,
        "낮은 확신": 0.02,
        "중간 확신": 0.03,
        "높은 확신": 0.05,
        "초고확신": 0.07,
    }
    return bankroll * pct_map.get(confidence, 0.03)


def market_type_modifier(market_type):
    if market_type == "Game Winner":
        return 0.50, "Game Winner는 변동성이 커서 추천 금액을 50% 줄입니다."
    if market_type == "Correct Score":
        return 0.30, "Correct Score는 맞히기 어려운 구조입니다. 강한 경고, 소액 전용입니다."
    if market_type in ["정치 선거", "뉴스/이벤트"]:
        return 0.50, "정치/뉴스 이벤트는 조건문과 결과 기준을 반드시 확인해야 합니다."
    if market_type == "99¢ 상환 스캘핑":
        return 0.20, "99¢ 상환 스캘핑은 작은 수익을 위해 큰 금액을 거는 구조입니다. 고액 금지입니다."
    if market_type == "2~5¢ Bounce Trade":
        return 0.20, "2~5¢ Bounce Trade는 소액 전용입니다. 복권처럼 커지면 안 됩니다."
    return 1.00, "시장 유형에 따른 추가 금액 감소는 없습니다."


def high_price_warning(price):
    if price >= 99:
        return "99¢: 사는 가격이 아니라 파는 가격입니다. 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다.", -50
    if price >= 95:
        return "95~98¢: 거의 상환 스캘핑입니다. 신규 고액 매수 금지 구간입니다.", -40
    if price >= 90:
        return "90~95¢: 신규 매수 비추천 구간입니다. 이겨도 추가수익이 작습니다.", -28
    if price >= 85:
        return "85~90¢: 신규 진입 신중 구간입니다. 손익비를 반드시 확인하세요.", -18
    if price >= 80:
        return "80~85¢: 익절 고려 구간입니다. 신규 진입보다 매도 계획이 중요합니다.", -10
    if 2 <= price <= 5:
        return "2~5¢: Bounce Trade 소액 전용입니다. 큰 금액 진입 금지입니다.", -12
    if 5 < price <= 10:
        return "5~10¢: 초저가 역배 구간입니다. 소액만 적절합니다.", -5
    return "가격 구간 자체의 강한 경고는 없습니다.", 5


def edge_judgement(edge):
    if edge >= 15:
        return "매우 좋음", "내 예상 승률 기준으로는 큰 저평가입니다.", 28
    if edge >= 10:
        return "좋음", "좋은 value 가능성이 있습니다.", 22
    if edge >= 5:
        return "약간 좋음", "소액 진입은 검토 가능합니다.", 12
    if edge >= 0:
        return "약함", "edge가 작습니다. 신중해야 합니다.", 2
    return "나쁨", "내 예상 승률보다 시장 가격이 비쌉니다.", -35


def chase_judgement(reference_price, current_price):
    if reference_price <= 0:
        return "미입력", "처음 봤던 저평가 가격을 입력하지 않았습니다.", 0, 0
    jump = current_price - reference_price
    if jump <= 0:
        return "추격 아님", "처음 봤던 가격보다 아직 비싸지지 않았습니다.", jump, 10
    if jump <= 5:
        return "정상", "처음 봤던 가격보다 조금 올랐습니다.", jump, 5
    if jump <= 15:
        return "주의", "가격이 꽤 올라왔습니다. 진입 금액을 줄이는 게 좋습니다.", jump, -8
    if jump <= 30:
        return "추격 위험", "저평가 구간을 많이 놓쳤습니다. FOMO 가능성을 확인하세요.", jump, -20
    return "FOMO 위험", "30¢ 이상 급등 후 진입은 추격매수 위험이 큽니다.", jump, -35


def bookmaker_judgement(my_prob, book_prob, poly_price):
    my_vs_poly = my_prob - poly_price
    book_vs_poly = book_prob - poly_price if book_prob > 0 else 0
    my_vs_book = my_prob - book_prob if book_prob > 0 else 0

    if book_prob <= 0:
        label = "미입력"
        note = "북메이커 기준 승률을 입력하지 않았습니다."
        score = 0
    elif book_vs_poly >= 10:
        label = "북메이커 대비 강한 저평가"
        note = "스포츠 배당 기준으로도 Polymarket 가격이 싸 보입니다."
        score = 15
    elif book_vs_poly >= 5:
        label = "북메이커 대비 약한 저평가"
        note = "북메이커 기준으로 약간 싸 보입니다."
        score = 8
    elif book_vs_poly > -5:
        label = "비슷함"
        note = "북메이커 기준과 큰 차이가 없습니다."
        score = 0
    elif book_vs_poly > -10:
        label = "약간 비쌈"
        note = "북메이커 기준보다 Polymarket이 약간 비쌉니다."
        score = -8
    else:
        label = "비쌈"
        note = "북메이커 기준으로는 Polymarket 가격이 비싸 보입니다."
        score = -18

    overconfidence_warning = ""
    if book_prob > 0 and my_vs_book >= 10:
        overconfidence_warning = "내 예상 승률이 북메이커보다 10%p 이상 높습니다. 과신 가능성을 재검토하세요."
        score -= 12

    return label, note, my_vs_poly, book_vs_poly, my_vs_book, overconfidence_warning, score


def risk_reward_text(target_profit, stop_loss_result):
    stop_loss_abs = abs(stop_loss_result)
    if stop_loss_abs == 0:
        return "손절 손실이 0으로 계산되어 손익비 해석이 어렵습니다.", 0
    ratio = target_profit / stop_loss_abs
    if target_profit <= 0:
        text = "목표가에 도달해도 수익이 나지 않습니다. 목표가를 다시 설정해야 합니다."
    elif ratio >= 2:
        text = f"목표가까지 얻을 수 있는 금액이 손절 시 잃을 수 있는 금액보다 약 {ratio:.1f}배 큽니다."
    elif ratio >= 1:
        text = f"목표 수익이 손절 손실보다 약 {ratio:.1f}배 큽니다. 나쁘지 않지만 승률 근거가 필요합니다."
    else:
        inverse = stop_loss_abs / target_profit if target_profit > 0 else 0
        text = f"목표가까지 얻을 수 있는 금액보다 손절 시 잃을 수 있는 금액이 약 {inverse:.1f}배 큽니다."
    return text, ratio


def final_decision(score, position_pct, duplicate_pct, fomo_count, stake, recommended_cap, edge):
    if position_pct >= 50:
        return "시스템 실패 — 계좌 생존 리스크", "현재 포지션이 계좌의 50% 이상입니다. 계산상 value가 있어도 진입하면 안 됩니다."
    if stake >= 200:
        return "시스템 실패 — 단일 베팅 과대", "$200 이상 단일 베팅은 감정과 계좌 생존 리스크가 너무 큽니다."
    if position_pct >= 20:
        return "진입 금지", "전체 자산의 20% 이상입니다. 무조건 진입 금지입니다."
    if duplicate_pct >= 20:
        return "진입 금지", "같은 경기/팀/방향 노출이 20% 이상입니다. 중복 노출 때문에 진입 금지입니다."
    if fomo_count >= 3:
        return "신규 진입 금지", "감정 체크가 3개 이상입니다. 지금은 분석이 아니라 감정 배팅일 가능성이 큽니다."
    if edge < 0:
        return "비추천", "Edge가 음수입니다. 내 판단 기준으로는 비싼 가격입니다."
    if stake > recommended_cap * 1.5:
        return "금액 대폭 축소", "추천 상한선보다 훨씬 큽니다. 진입하려면 금액을 크게 줄여야 합니다."
    if stake > recommended_cap:
        return "금액 축소 필요", "추천 상한선을 초과했습니다."
    if score >= 80:
        return "진입 강함", "조건은 좋지만 분할 진입과 매도 기준은 필요합니다."
    if score >= 65:
        return "진입 약함", "소액 진입은 가능하지만 큰 금액은 조심해야 합니다."
    if score >= 50:
        return "관망 우선", "조건이 애매합니다. 더 좋은 가격을 기다리는 편이 좋습니다."
    if score >= 35:
        return "비추천", "리스크 대비 보상이 부족합니다."
    return "강한 비추천", "여러 항목에서 위험 신호가 많습니다."

# =============================
# Header
# =============================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">📊 Memento</div>
        <div class="hero-subtitle">
            Polymarket 배팅 가치 판독기 + 거래 손익 기록장<br>
            자동매매가 아니라, 진입 전 리스크를 숫자로 확인하는 수동 판단 도구입니다.<br>
            핵심 원칙: 수익 가능성보다 <b>계좌 생존, 포지션 크기, 감정 배팅 방지</b>를 우선합니다.
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
# 1. Main Betting Evaluator
# =====================================================
with tab1:
    st.header("🏠 배팅 가치 판독기")
    st.caption("Edge보다 먼저 포트폴리오 크기, 감정 상태, 중복 노출, 고가 정배 리스크를 확인합니다.")

    st.markdown('<div class="card"><div class="card-title">① 시장 / 가격 정보</div><div class="card-text">시장 이름, 현재 가격, 내 예상 승률, 처음 봤던 저평가 가격을 입력하세요.</div></div>', unsafe_allow_html=True)

    market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner", key="main_market_name")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        current_price = st.number_input("현재 Polymarket 가격(센트)", min_value=1.0, max_value=99.0, value=56.0, key="main_current_price")
    with col2:
        my_probability = st.number_input("내가 생각하는 실제 승률(%)", min_value=1.0, max_value=99.0, value=65.0, key="main_my_probability")
    with col3:
        bookmaker_probability = st.number_input("스포츠 북메이커 기준 승률(%)", min_value=0.0, max_value=99.0, value=60.0, key="main_book_prob")
    with col4:
        reference_price = st.number_input("처음 봤던 저평가 가격(센트)", min_value=0.0, max_value=99.0, value=30.0, key="main_reference_price")

    st.markdown('<div class="card"><div class="card-title">② 배팅 목적 / 시장 유형</div><div class="card-text">이 배팅이 만기까지 맞히는 용도인지, 경기 전 가격 상승을 노리는 트레이드인지 구분합니다.</div></div>', unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    with col5:
        confidence = st.selectbox("확신도", ["관찰용", "낮은 확신", "중간 확신", "높은 확신", "초고확신"], index=2, key="main_confidence")
    with col6:
        bet_purpose = st.selectbox(
            "배팅 목적",
            [
                "실제 가치 매수 / 만기까지 보유",
                "경기 시작 전 가격 상승 노림",
                "반반 경기의 강팀 쏠림 이용 / 중간 익절",
                "고가 정배 익절 / 상환 스캘핑",
                "초저가 역배 Bounce Trade",
                "뉴스/이벤트 선반영 트레이드",
            ],
            key="main_bet_purpose"
        )
    with col7:
        market_type = st.selectbox(
            "시장 유형",
            ["Match Moneyline", "Game Winner", "Correct Score", "정치 선거", "뉴스/이벤트", "99¢ 상환 스캘핑", "2~5¢ Bounce Trade"],
            key="main_market_type"
        )

    st.markdown('<div class="card"><div class="card-title">③ 금액 / 계좌 생존 설정</div><div class="card-text">계좌 대비 비중과 감정적으로 감당 가능한 1회 한도를 입력하세요.</div></div>', unsafe_allow_html=True)

    col8, col9, col10 = st.columns(3)
    with col8:
        bankroll = st.number_input("현재 전체 포트폴리오 / 총자산($)", min_value=1.0, value=500.0, key="main_bankroll")
    with col9:
        stake = st.number_input("이번 투자금($)", min_value=1.0, value=50.0, key="main_stake")
    with col10:
        emotional_limit = st.number_input("내 감정 한도 / 1회 감당 가능 금액($)", min_value=1.0, value=50.0, key="main_emotional_limit")

    st.markdown('<div class="card"><div class="card-title">④ 목표가 / 손절가</div><div class="card-text">중간 익절 또는 손절 기준을 입력하면 손익비를 계산합니다.</div></div>', unsafe_allow_html=True)

    col11, col12 = st.columns(2)
    with col11:
        target_sell_price = st.number_input("목표 매도가(센트)", min_value=1.0, max_value=100.0, value=75.0, key="main_target")
    with col12:
        stop_loss_price = st.number_input("손절가(센트)", min_value=0.0, max_value=99.0, value=45.0, key="main_stop")

    st.markdown('<div class="card"><div class="card-title">⑤ 감정 상태 체크</div><div class="card-text">1개 이상이면 추천 금액 50% 감소, 3개 이상이면 신규 진입 금지입니다.</div></div>', unsafe_allow_html=True)

    fomo_options = [
        "방금 큰 수익을 냈다",
        "방금 큰 손실을 냈다",
        "아까 판 게 후회된다",
        "빨리 복구하고 싶다",
        "더 빨리 계좌를 키우고 싶다",
        "놓치면 아깝다고 느낀다",
        "이미 같은 경기에 포지션이 있다",
    ]
    fomo_checked = []
    fcols = st.columns(2)
    for i, option in enumerate(fomo_options):
        with fcols[i % 2]:
            if st.checkbox(option, key=f"fomo_{i}"):
                fomo_checked.append(option)

    st.markdown('<div class="card"><div class="card-title">⑥ 중복 노출 계산</div><div class="card-text">같은 경기나 같은 팀/방향으로 이미 들어간 금액이 있으면 입력하세요.</div></div>', unsafe_allow_html=True)

    col13, col14, col15 = st.columns(3)
    with col13:
        existing_moneyline = st.number_input("기존 같은 경기 Moneyline 노출($)", min_value=0.0, value=0.0, key="existing_moneyline")
    with col14:
        existing_gamewinner = st.number_input("Game Winner 노출($)", min_value=0.0, value=0.0, key="existing_gamewinner")
    with col15:
        existing_same_side = st.number_input("같은 팀/같은 방향 추가 노출($)", min_value=0.0, value=0.0, key="existing_same_side")

    if st.button("🔍 배팅 가치 판독하기", key="main_analyze"):
        price_decimal = current_price / 100
        target_decimal = target_sell_price / 100
        stop_decimal = stop_loss_price / 100

        shares = stake / price_decimal
        current_value = shares * price_decimal
        payout_if_win = shares
        profit_if_win = payout_if_win - stake
        loss_if_lose = stake

        target_sell_amount = shares * target_decimal
        target_profit = target_sell_amount - stake
        stop_loss_amount = shares * stop_decimal
        stop_loss_result = stop_loss_amount - stake
        rr_text, rr_ratio = risk_reward_text(target_profit, stop_loss_result)

        edge = my_probability - current_price
        position_pct = (stake / bankroll) * 100
        same_game_total_exposure = existing_moneyline + existing_gamewinner + existing_same_side + stake
        duplicate_pct = (same_game_total_exposure / bankroll) * 100

        p_label, p_note, p_score = portfolio_judgement(position_pct)
        d_label, d_note, d_score = duplicate_exposure_judgement(duplicate_pct)
        e_label, e_note, e_score = edge_judgement(edge)
        price_note, price_score = high_price_warning(current_price)
        chase_label, chase_note, price_jump, chase_score = chase_judgement(reference_price, current_price)
        book_label, book_note, my_vs_poly, book_vs_poly, my_vs_book, overconfidence_warning, book_score = bookmaker_judgement(my_probability, bookmaker_probability, current_price)

        conf_cap, conf_note = confidence_cap(confidence)
        acc_cap = account_cap(bankroll, confidence)
        market_modifier, market_note = market_type_modifier(market_type)

        base_recommended_cap = min(conf_cap, acc_cap, emotional_limit)
        recommended_cap = base_recommended_cap * market_modifier
        fomo_count = len(fomo_checked)
        fomo_score = 0
        if fomo_count >= 3:
            fomo_score = -60
        elif fomo_count >= 1:
            recommended_cap *= 0.5
            fomo_score = -25

        if stake >= 200:
            stake_warning = "시스템 실패: $200 이상 단일 베팅입니다."
            stake_score = -70
        elif stake >= 100:
            stake_warning = "강한 경고: $100 이상 단일 베팅입니다."
            stake_score = -35
        elif stake > emotional_limit:
            stake_warning = "감정 한도를 초과했습니다."
            stake_score = -20
        else:
            stake_warning = "감정 한도 이내입니다."
            stake_score = 5

        raw_score = 50 + p_score + d_score + e_score + price_score + chase_score + book_score + fomo_score + stake_score
        if stake <= recommended_cap:
            raw_score += 10
        else:
            raw_score -= 20
        final_score = clamp_score(raw_score)

        decision, decision_note = final_decision(final_score, position_pct, duplicate_pct, fomo_count, stake, recommended_cap, edge)

        st.divider()
        st.subheader("📌 최종 판정")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("최종 점수", f"{final_score}/100")
        r2.metric("최종 판단", decision)
        r3.metric("포트폴리오 비중", f"{position_pct:.2f}%")
        r4.metric("추천 상한선", money(recommended_cap))
        st.progress(final_score / 100)

        if "시스템 실패" in decision or decision in ["진입 금지", "신규 진입 금지", "강한 비추천", "비추천"]:
            st.error(f"{decision}: {decision_note}")
        elif decision in ["금액 대폭 축소", "금액 축소 필요", "관망 우선", "진입 약함"]:
            st.warning(f"{decision}: {decision_note}")
        else:
            st.success(f"{decision}: {decision_note}")

        if position_pct >= 50:
            st.markdown('<div class="danger-box"><b>시스템 실패 — 계좌 생존 리스크</b><br>포트폴리오의 50% 이상을 한 포지션에 넣는 구조입니다. 이 앱의 목적상 절대 금지입니다.</div>', unsafe_allow_html=True)
        elif position_pct >= 20:
            st.markdown('<div class="danger-box"><b>진입 금지</b><br>포트폴리오의 20% 이상입니다. 기대값이 좋아 보여도 계좌 생존 기준에서 막아야 합니다.</div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("📊 핵심 계산 결과")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("시장 implied probability", f"{current_price:.2f}%")
        m2.metric("내 예상 승률", f"{my_probability:.2f}%")
        m3.metric("Edge", signed_pct(edge))
        m4.metric("보유 수량", f"{shares:.2f}주")

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("승리 시 총 수령액", money(payout_if_win))
        m6.metric("승리 시 순이익", money(profit_if_win))
        m7.metric("패배 시 손실", f"-{money(loss_if_lose)}")
        m8.metric("목표/손절 손익비", f"{rr_ratio:.2f} : 1")

        st.divider()
        st.subheader("🧠 평가 항목별 판독")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="card"><div class="card-title">1. 포트폴리오 비중</div>
            <div class="card-text">상태: <span class="bad">{p_label}</span><br>투자금: <b>{money(stake)}</b><br>전체 자산: <b>{money(bankroll)}</b><br>비중: <b>{position_pct:.2f}%</b><br>{p_note}</div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">2. 배팅 상한선</div>
            <div class="card-text">확신도: <b>{confidence}</b><br>감정 한도: <b>{money(emotional_limit)}</b><br>계좌 비율 기준 상한: <b>{money(acc_cap)}</b><br>확신도 기준 상한: <b>{money(conf_cap)}</b><br>시장 유형 보정 후 추천 상한: <b>{money(recommended_cap)}</b><br>{conf_note}<br>{market_note}<br>{stake_warning}</div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">3. 진입가격 / 고가 정배 경고</div>
            <div class="card-text">현재 가격: <b>{current_price:.2f}¢</b><br>{price_note}</div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">4. FOMO / 감정 상태</div>
            <div class="card-text">체크 수: <b>{fomo_count}개</b><br>1개 이상이면 추천 금액 50% 감소, 3개 이상이면 신규 진입 금지입니다.<br>체크 항목: {', '.join(fomo_checked) if fomo_checked else '없음'}</div></div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="card"><div class="card-title">5. Edge 평가</div>
            <div class="card-text">상태: <span class="info">{e_label}</span><br>내 예상 승률 - Polymarket 가격: <b>{my_vs_poly:+.2f}%p</b><br>{e_note}</div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">6. 북메이커 비교</div>
            <div class="card-text">상태: <span class="info">{book_label}</span><br>북메이커 기준 - Polymarket: <b>{book_vs_poly:+.2f}%p</b><br>내 예상 - 북메이커 기준: <b>{my_vs_book:+.2f}%p</b><br>{book_note}<br><span class="bad">{overconfidence_warning}</span></div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">7. 추격매수 / FOMO 가격 변화</div>
            <div class="card-text">상태: <span class="warn">{chase_label}</span><br>처음 본 가격: <b>{reference_price:.2f}¢</b><br>현재 가격: <b>{current_price:.2f}¢</b><br>가격 변화: <b>{price_jump:+.2f}¢</b><br>{chase_note}</div></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card"><div class="card-title">8. 중복 노출</div>
            <div class="card-text">상태: <span class="bad">{d_label}</span><br>같은 경기 총 노출: <b>{money(same_game_total_exposure)}</b><br>포트폴리오 대비: <b>{duplicate_pct:.2f}%</b><br>{d_note}</div></div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("🎯 목표가 / 손절가 손익비")
        c1, c2, c3 = st.columns(3)
        c1.metric("목표가 도달 시 예상 수익", money(target_profit))
        c2.metric("손절가 도달 시 예상 손실", money(abs(stop_loss_result)))
        c3.metric("목표/손절 손익비", f"{rr_ratio:.2f} : 1")
        st.info(rr_text)

        st.divider()
        st.subheader("⚠️ 현재가에서 100¢까지 남은 추가수익")
        redeem_total = shares
        additional_profit_to_100 = redeem_total - current_value
        failure_loss_now = current_value
        h1, h2, h3, h4 = st.columns(4)
        h1.metric("현재 평가금", money(current_value))
        h2.metric("100¢ 상환 시 총액", money(redeem_total))
        h3.metric("현재 대비 추가수익", money(additional_profit_to_100))
        h4.metric("실패 시 손실", money(failure_loss_now))
        if current_price >= 80:
            st.warning(f"현재부터 100¢까지 추가로 얻을 수 있는 금액은 {money(additional_profit_to_100)}뿐입니다. 반대로 틀리면 현재 평가금 {money(failure_loss_now)}를 잃을 수 있습니다. 신규 매수보다 익절 구간입니다.")
        else:
            st.caption("고가 정배 구간이 아니어도, 현재 평가금 대비 남은 추가수익을 항상 확인하세요.")

        st.divider()
        st.subheader("📝 기록용 요약")
        summary = (
            f"{market_name}\n"
            f"현재가: {current_price:.0f}¢ / 내 예상 승률: {my_probability:.1f}% / 북메이커: {bookmaker_probability:.1f}% / "
            f"Edge: {edge:+.1f}% / 투자금: ${stake:.2f} / 포트폴리오 비중: {position_pct:.1f}% / "
            f"중복노출: {duplicate_pct:.1f}% / 추천상한: ${recommended_cap:.2f} / "
            f"목적: {bet_purpose} / 시장유형: {market_type} / 최종판정: {decision} / 점수: {final_score}/100"
        )
        st.code(summary)

        if st.button("이 시장을 EDGE / NEWS 보드에 추가", key="add_main_to_board"):
            st.session_state.market_board.append({
                "날짜": str(date.today()),
                "시장 이름": market_name,
                "현재가": f"{current_price:.2f}¢",
                "내 예상 승률": f"{my_probability:.2f}%",
                "북메이커": f"{bookmaker_probability:.2f}%",
                "Edge": edge,
                "포트폴리오 비중": f"{position_pct:.2f}%",
                "중복 노출": f"{duplicate_pct:.2f}%",
                "목적": bet_purpose,
                "시장 유형": market_type,
                "판정": decision,
                "점수": final_score,
                "메모": "메인 판독기에서 추가"
            })
            st.success("EDGE / NEWS 보드에 추가했습니다.")

# =====================================================
# 2. Trade P/L + Partial Sell Tool
# =====================================================
with tab2:
    st.header("💰 거래 손익 계산기")
    st.caption("일반 매도, 부분매도, 원금회수 비율, 복기 질문을 계산합니다.")

    st.subheader("1. 기본 거래 손익 계산기")
    trade_name = st.text_input("거래 이름", "Anyone's Legend vs Bilibili Gaming — Game 1 Winner", key="trade_name")

    col1, col2, col3 = st.columns(3)
    with col1:
        buy_price = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=54.0, key="trade_buy_price")
    with col2:
        sell_price = st.number_input("매도가(센트)", min_value=0.0, max_value=100.0, value=87.0, key="trade_sell_price")
    with col3:
        trade_stake = st.number_input("투자금($)", min_value=1.0, value=77.19, key="trade_stake")

    use_partial_sell = st.checkbox("부분매도 계산하기", key="use_partial_sell")

    if use_partial_sell:
        col4, col5, col6 = st.columns(3)
        with col4:
            partial_sell_price = st.number_input("부분매도 가격(센트)", min_value=0.0, max_value=100.0, value=73.0, key="partial_sell_price")
        with col5:
            partial_sell_shares = st.number_input("부분매도 수량", min_value=0.0, value=24.5, key="partial_sell_shares")
        with col6:
            final_sell_price = st.number_input("남은 포지션 최종 매도가(센트)", min_value=0.0, max_value=100.0, value=100.0, key="final_sell_price")

    if st.button("손익 계산하기", key="calculate_trade"):
        buy_decimal = buy_price / 100
        sell_decimal = sell_price / 100
        total_shares = trade_stake / buy_decimal

        if not use_partial_sell:
            sell_amount = total_shares * sell_decimal
            profit = sell_amount - trade_stake
            roi = (profit / trade_stake) * 100
            a, b, c, d = st.columns(4)
            a.metric("보유 수량", f"{total_shares:.2f}주")
            b.metric("매도금", money(sell_amount))
            c.metric("실현손익", money(profit))
            d.metric("수익률", f"{roi:+.2f}%")
            summary = f"{trade_name}\n매수가: {buy_price:.0f}¢ / 매도가: {sell_price:.0f}¢ / 투자금: ${trade_stake:.2f} / 실현손익: ${profit:+.2f} / 수익률: {roi:+.1f}%"
            st.markdown("### 워드 기록용 한 줄 요약")
            st.code(summary)
            st.session_state.trade_log.append({"날짜": str(date.today()), "거래 이름": trade_name, "매수가": f"{buy_price:.2f}¢", "매도가": f"{sell_price:.2f}¢", "투자금": trade_stake, "손익": profit, "수익률": roi, "형태": "일반매도"})
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
                a, b, c, d = st.columns(4)
                a.metric("전체 수량", f"{total_shares:.2f}주")
                b.metric("총 매도금", money(total_sell_amount))
                c.metric("총손익", money(profit))
                d.metric("수익률", f"{roi:+.2f}%")
                summary = f"{trade_name}\n매수가: {buy_price:.0f}¢ / 부분매도: {partial_sell_price:.0f}¢, {partial_sell_shares:.1f}주, ${partial_sell_amount:.2f} / 남은 포지션: {remaining_shares:.1f}주 상환 ${remaining_sell_amount:.2f} / 투자금: ${trade_stake:.2f} / 총손익: ${profit:+.2f} / 수익률: {roi:+.1f}%"
                st.markdown("### 워드 기록용 한 줄 요약")
                st.code(summary)
                st.session_state.trade_log.append({"날짜": str(date.today()), "거래 이름": trade_name, "매수가": f"{buy_price:.2f}¢", "매도가": f"부분 {partial_sell_price:.2f}¢ / 최종 {final_sell_price:.2f}¢", "투자금": trade_stake, "손익": profit, "수익률": roi, "형태": "부분매도"})

    st.divider()
    st.subheader("2. 부분매도 전략 계산기")
    ps_market_name = st.text_input("시장 이름", "Example: T1 vs HLE", key="ps_market_name")
    colp1, colp2, colp3, colp4 = st.columns(4)
    with colp1:
        ps_buy_price = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=30.0, key="ps_buy_price")
    with colp2:
        ps_current_price = st.number_input("현재가(센트)", min_value=1.0, max_value=100.0, value=70.0, key="ps_current_price")
    with colp3:
        ps_stake = st.number_input("투자금($)", min_value=1.0, value=50.0, key="ps_stake")
    with colp4:
        ps_method = st.selectbox("수량 입력 방식", ["투자금 기준 자동 계산", "보유 수량 직접 입력"], key="ps_method")

    if ps_method == "보유 수량 직접 입력":
        ps_shares = st.number_input("보유 수량", min_value=0.0, value=100.0, key="ps_shares")
    else:
        ps_shares = ps_stake / (ps_buy_price / 100)
        st.caption(f"자동 계산 보유 수량: {ps_shares:.2f}주")

    redeem_to_100 = st.checkbox("100¢ 상환 시나리오 포함", value=True, key="redeem_to_100")

    if st.button("부분매도 표 계산하기", key="calc_partial_table"):
        current_decimal = ps_current_price / 100
        current_value = ps_shares * current_decimal
        ratios = [25, 50, 70, 80, 90, 100]
        rows = []
        for ratio in ratios:
            sell_shares = ps_shares * ratio / 100
            cash_back = sell_shares * current_decimal
            locked_pnl_vs_total = cash_back - ps_stake
            remaining_shares = ps_shares - sell_shares
            remaining_value = remaining_shares * current_decimal
            extra_profit_to_100 = remaining_shares * (1 - current_decimal) if redeem_to_100 else 0
            rows.append({
                "매도 비율": f"{ratio}%",
                "매도 수량": round(sell_shares, 2),
                "회수금": money(cash_back),
                "총 원금 대비 확정손익": money(locked_pnl_vs_total),
                "남은 수량": round(remaining_shares, 2),
                "남은 평가금": money(remaining_value),
                "100¢ 도달 시 남은 추가수익": money(extra_profit_to_100),
            })

        if current_value > 0:
            min_recovery_ratio = (ps_stake / current_value) * 100
        else:
            min_recovery_ratio = 999

        st.markdown(f"### {ps_market_name} 부분매도 표")
        st.dataframe(rows, use_container_width=True)
        if min_recovery_ratio <= 100:
            st.success(f"원금 회수에 필요한 최소 매도 비율: {min_recovery_ratio:.1f}%")
        else:
            st.error(f"현재가에서는 100%를 모두 팔아도 원금 회수가 어렵습니다. 필요한 비율: {min_recovery_ratio:.1f}%")

        st.subheader("현재가에서 100¢까지 남은 추가수익")
        redeem_total = ps_shares
        additional_profit = redeem_total - current_value
        h1, h2, h3, h4 = st.columns(4)
        h1.metric("현재 평가금", money(current_value))
        h2.metric("100¢ 상환 시 총액", money(redeem_total))
        h3.metric("현재 대비 추가수익", money(additional_profit))
        h4.metric("실패 시 손실", money(current_value))
        st.warning(f"현재부터 100¢까지 추가로 얻을 수 있는 금액은 {money(additional_profit)}입니다. 반대로 틀리면 현재 평가금 {money(current_value)}를 잃을 수 있습니다.")

    st.divider()
    st.subheader("3. 거래 복기 질문")
    reflection_questions = [
        "원하는 가격에 진입했는가?",
        "내 예상 승률의 근거는 무엇인가?",
        "북메이커와 왜 다르게 봤는가?",
        "금액은 감당 가능한 크기였는가?",
        "매도 기준을 지켰는가?",
        "감정적으로 들어간 부분이 있었는가?",
        "다음에 반복 가능한 거래인가?",
    ]
    for q in reflection_questions:
        st.write(f"- {q}")

# =====================================================
# 3. Total ROI
# =====================================================
with tab3:
    st.header("📈 총수익률 / 전체 성과")
    col1, col2, col3 = st.columns(3)
    with col1:
        starting_bankroll = st.number_input("시작 자금($)", min_value=0.0, value=500.0, key="starting_bankroll")
    with col2:
        current_bankroll = st.number_input("현재 총자산($)", min_value=0.0, value=650.0, key="current_bankroll")
    with col3:
        net_deposit = st.number_input("추가 입금 / 출금 조정($)", value=0.0, key="net_deposit")

    adjusted_start = starting_bankroll + net_deposit
    total_profit = current_bankroll - adjusted_start
    total_roi = (total_profit / adjusted_start) * 100 if adjusted_start > 0 else 0
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
        trade_roi = (total_trade_profit / total_trade_stake) * 100 if total_trade_stake > 0 else 0
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
    st.caption("현재는 수동 기록 보드입니다. 나중에 Polymarket API, 북메이커, 뉴스 감시를 연결할 수 있습니다.")

    news_market_name = st.text_input("시장 이름", "Example: T1 vs HLE", key="news_market_name")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        news_price = st.number_input("현재 가격(센트)", min_value=1.0, max_value=99.0, value=50.0, key="news_price")
    with col2:
        news_my_probability = st.number_input("내 예상 승률(%)", min_value=1.0, max_value=99.0, value=60.0, key="news_my_probability")
    with col3:
        news_bookmaker = st.number_input("북메이커 기준 승률(%)", min_value=0.0, max_value=99.0, value=55.0, key="news_bookmaker")
    with col4:
        news_importance = st.selectbox("관심도", ["낮음", "보통", "높음", "매우 높음"], key="news_importance")

    news_note = st.text_area("메모 / 뉴스 / 근거", "예: 라인업 변화, 부상, 시장 공포, 과매도, 북메이커와 가격 차이 등", key="news_note")

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
            "북메이커": f"{news_bookmaker:.2f}%",
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
        sorted_board = sorted(st.session_state.market_board, key=lambda x: x["점수"], reverse=True)
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
