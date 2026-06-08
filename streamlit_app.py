import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# 기본 저장 공간 만들기
# -----------------------------
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


# -----------------------------
# 작은 계산 함수들
# -----------------------------
def money(value):
    return f"${value:,.2f}"

def percent(value):
    return f"{value:+.2f}%"

def cents(value):
    return f"{value:.2f}¢"


# -----------------------------
# 앱 제목
# -----------------------------
st.title("📊 Memento")
st.write("Polymarket 배팅 가치 판독기 + 거래일지 앱입니다.")
st.caption("현재 버전은 자동매매가 아니라, 수동 입력형 분석 도구입니다.")

st.divider()


# -----------------------------
# 메뉴 탭
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 배팅 가치 판독기",
    "💰 거래 손익 계산기",
    "📈 총수익률",
    "📰 EDGE / NEWS"
])


# =====================================================
# 1. 배팅 가치 판독기
# =====================================================
with tab1:
    st.header("🏠 배팅 가치 판독기")
    st.write("현재 가격이 내가 생각하는 실제 승률보다 싼지 비싼지 판단합니다.")

    market_name = st.text_input(
        "시장 이름",
        "T1 vs HLE — Match Winner",
        key="value_market_name"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        current_price = st.number_input(
            "현재 가격(센트)",
            min_value=1.0,
            max_value=99.0,
            value=56.0,
            key="value_current_price"
        )

    with col2:
        my_probability = st.number_input(
            "내가 생각하는 실제 승률(%)",
            min_value=1.0,
            max_value=99.0,
            value=65.0,
            key="value_my_probability"
        )

    with col3:
        stake = st.number_input(
            "투자금($)",
            min_value=1.0,
            value=50.0,
            key="value_stake"
        )

    col4, col5 = st.columns(2)

    with col4:
        target_sell_price = st.number_input(
            "목표 매도가(센트)",
            min_value=1.0,
            max_value=100.0,
            value=75.0,
            key="value_target_sell"
        )

    with col5:
        stop_loss_price = st.number_input(
            "손절가(센트)",
            min_value=0.0,
            max_value=99.0,
            value=45.0,
            key="value_stop_loss"
        )

    if st.button("배팅 가치 분석하기", key="analyze_value"):
        price_decimal = current_price / 100
        target_decimal = target_sell_price / 100
        stop_decimal = stop_loss_price / 100

        shares = stake / price_decimal

        payout_if_win = shares * 1
        profit_if_win = payout_if_win - stake
        loss_if_lose = stake

        edge = my_probability - current_price

        target_sell_amount = shares * target_decimal
        target_profit = target_sell_amount - stake

        stop_loss_amount = shares * stop_decimal
        stop_loss_result = stop_loss_amount - stake

        risk_amount = stake - stop_loss_amount
        reward_amount = target_profit

        if risk_amount > 0:
            risk_reward_ratio = reward_amount / risk_amount
        else:
            risk_reward_ratio = 0

        st.subheader("분석 결과")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("시장 가격", f"{current_price:.2f}%")
        m2.metric("내 예상 승률", f"{my_probability:.2f}%")
        m3.metric("Edge", percent(edge))
        m4.metric("보유 수량", f"{shares:.2f}주")

        st.write(f"승리 시 총 수령액: **{money(payout_if_win)}**")
        st.write(f"승리 시 순이익: **{money(profit_if_win)}**")
        st.write(f"패배 시 손실: **-{money(loss_if_lose)}**")

        st.write(f"목표 매도가 도달 시 예상 수익: **{money(target_profit)}**")
        st.write(f"손절가 도달 시 예상 손익: **{money(stop_loss_result)}**")
        st.write(f"대략적인 손익비: **{risk_reward_ratio:.2f} : 1**")

        st.subheader("판정")

        if edge >= 10:
            st.success("좋은 value 가능성이 있습니다. 단, 경기 변수와 유동성은 반드시 확인해야 합니다.")
        elif edge >= 5:
            st.info("소액 진입은 검토 가능합니다. 큰 금액은 아직 조심해야 합니다.")
        elif edge >= 0:
            st.warning("Edge가 작습니다. 신중하게 봐야 합니다.")
        else:
            st.error("현재 가격은 비싸 보입니다. 신규 진입은 비추천입니다.")

        if current_price >= 90:
            st.error("90¢ 이상입니다. 신규 매수보다 익절 구간에 가깝습니다.")
        elif current_price >= 80:
            st.warning("80¢ 이상입니다. 손익비가 나빠질 수 있습니다.")
        elif 2 <= current_price <= 10:
            st.info("2~10¢ 초저가 역배 구간입니다. bounce trade 소액 전용으로 보는 게 좋습니다.")

        st.markdown("### 기록용 요약")

        value_summary = (
            f"{market_name} / "
            f"현재가: {current_price:.2f}¢ / "
            f"내 예상 승률: {my_probability:.2f}% / "
            f"Edge: {edge:+.2f}% / "
            f"투자금: ${stake:.2f} / "
            f"목표가: {target_sell_price:.2f}¢ / "
            f"손절가: {stop_loss_price:.2f}¢"
        )

        st.code(value_summary)


# =====================================================
# 2. 거래 손익 계산기
# =====================================================
with tab2:
    st.header("💰 거래 손익 계산기")
    st.write("매수가, 매도가, 투자금을 입력하면 손익과 수익률을 계산합니다.")

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
        st.info("부분매도 버전입니다. 일부는 중간에 팔고, 남은 수량은 최종 가격으로 계산합니다.")

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

            st.write(f"거래 이름: **{trade_name}**")
            st.write(f"매수가: **{cents(buy_price)}**")
            st.write(f"매도가: **{cents(sell_price)}**")
            st.write(f"투자금: **{money(trade_stake)}**")
            st.write(f"보유 수량: **{total_shares:.2f}주**")
            st.write(f"매도금: **{money(sell_amount)}**")
            st.write(f"실현손익: **{money(profit)}**")
            st.write(f"수익률: **{roi:+.2f}%**")

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
                st.error("부분매도 수량이 전체 보유 수량보다 큽니다. 수량을 다시 확인하세요.")
            else:
                remaining_sell_amount = remaining_shares * final_decimal
                total_sell_amount = partial_sell_amount + remaining_sell_amount

                profit = total_sell_amount - trade_stake
                roi = (profit / trade_stake) * 100

                st.subheader("부분매도 거래 요약")

                st.write(f"거래 이름: **{trade_name}**")
                st.write(f"매수가: **{cents(buy_price)}**")
                st.write(f"전체 보유 수량: **{total_shares:.2f}주**")
                st.write(f"부분매도: **{cents(partial_sell_price)}, {partial_sell_shares:.2f}주, {money(partial_sell_amount)}**")
                st.write(f"남은 포지션: **{remaining_shares:.2f}주, 최종 매도가 {cents(final_sell_price)}, 상환 {money(remaining_sell_amount)}**")
                st.write(f"투자금: **{money(trade_stake)}**")
                st.write(f"총 매도금: **{money(total_sell_amount)}**")
                st.write(f"총손익: **{money(profit)}**")
                st.write(f"수익률: **{roi:+.2f}%**")

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
    st.write("전체 자금 기준 수익률과 거래일지 기준 누적 손익을 확인합니다.")

    st.subheader("1. 계좌 전체 기준")

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

    m1, m2, m3 = st.columns(3)

    m1.metric("총손익", money(total_profit))
    m2.metric("총수익률", f"{total_roi:+.2f}%")
    m3.metric("현재 총자산", money(current_bankroll))

    st.divider()

    st.subheader("2. 거래일지 기준")

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
        st.success("거래일지를 초기화했습니다. 새로고침하면 반영됩니다.")


# =====================================================
# 4. EDGE / NEWS
# =====================================================
with tab4:
    st.header("📰 EDGE 높은 시장 / NEWS")
    st.write("나중에 Polymarket API, 뉴스, 배당률 데이터를 연결할 공간입니다.")
    st.warning("현재는 자동 뉴스 기능이 아니라, 수동으로 관심 시장을 기록하는 윤곽 버전입니다.")

    st.subheader("관심 시장 수동 추가")

    news_market_name = st.text_input(
        "시장 이름",
        "Example: T1 vs HLE",
        key="news_market_name"
    )

    col1, col2, col3 = st.columns(3)

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

    if st.button("관심 시장 추가", key="add_watchlist"):
        news_edge = news_my_probability - news_price

        st.session_state.watchlist.append({
            "시장 이름": news_market_name,
            "현재 가격": f"{news_price:.2f}¢",
            "내 예상 승률": f"{news_my_probability:.2f}%",
            "Edge": news_edge,
            "관심도": news_importance,
            "메모": news_note
        })

        st.success("관심 시장에 추가했습니다.")

    st.subheader("EDGE 높은 시장 목록")

    if len(st.session_state.watchlist) == 0:
        st.info("아직 추가한 관심 시장이 없습니다.")
    else:
        sorted_watchlist = sorted(
            st.session_state.watchlist,
            key=lambda x: x["Edge"],
            reverse=True
        )

        st.dataframe(sorted_watchlist, use_container_width=True)

    if st.button("관심 시장 목록 초기화", key="clear_watchlist"):
        st.session_state.watchlist = []
        st.success("관심 시장 목록을 초기화했습니다. 새로고침하면 반영됩니다.")

    st.divider()

    st.subheader("나중에 확장할 기능")
    st.write("- Polymarket API 자동 연결")
    st.write("- 시장 가격 자동 불러오기")
    st.write("- 북메이커 배당률과 비교")
    st.write("- 뉴스/부상/라인업 자동 감시")
    st.write("- Edge 높은 시장 자동 정렬")
    st.write("- 텔레그램/디스코드 알림")
    st.write("- 반자동 주문 보조")