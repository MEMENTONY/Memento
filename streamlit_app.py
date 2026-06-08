import streamlit as st

st.set_page_config(page_title="Memento", page_icon="📊")

st.title("📊 Memento")
st.write("Polymarket 배팅 가치 판독기 + 거래일지 앱입니다.")

st.header("1. 배팅 가치 판독기")

market_name = st.text_input("시장 이름", "DK vs BRION BO5")

current_price = st.number_input(
    "현재 가격(센트)",
    min_value=1.0,
    max_value=99.0,
    value=50.0
)

my_probability = st.number_input(
    "내가 생각하는 실제 승률(%)",
    min_value=1.0,
    max_value=99.0,
    value=60.0
)

stake = st.number_input(
    "투자금($)",
    min_value=1.0,
    value=50.0
)

if st.button("분석하기"):
    price_decimal = current_price / 100
    shares = stake / price_decimal

    payout_if_win = shares * 1
    profit_if_win = payout_if_win - stake
    loss_if_lose = stake
    edge = my_probability - current_price

    st.subheader("분석 결과")

    st.write(f"시장 이름: {market_name}")
    st.write(f"시장 implied probability: {current_price:.2f}%")
    st.write(f"내 예상 승률: {my_probability:.2f}%")
    st.write(f"Edge: {edge:.2f}%")
    st.write(f"보유 수량: {shares:.2f}주")
    st.write(f"승리 시 총 수령액: ${payout_if_win:.2f}")
    st.write(f"승리 시 순이익: ${profit_if_win:.2f}")
    st.write(f"패배 시 손실: -${loss_if_lose:.2f}")

    if edge >= 10:
        st.success("판정: 좋은 value 가능성이 있습니다.")
    elif edge >= 5:
        st.info("판정: 소액 진입은 검토 가능합니다.")
    elif edge >= 0:
        st.warning("판정: edge가 작습니다. 신중해야 합니다.")
    else:
        st.error("판정: 현재 가격은 비싸 보입니다.")

    if current_price >= 90:
        st.error("주의: 90¢ 이상은 신규 매수보다 익절 구간에 가깝습니다.")
    elif current_price >= 80:
        st.warning("주의: 80¢ 이상은 손익비가 나빠질 수 있습니다.")
    elif current_price <= 10:
        st.info("주의: 초저가 역배 구간입니다. 소액 bounce trade만 적절합니다.")


st.header("2. 거래 손익 계산기")

trade_name = st.text_input("거래 이름", "Anyone's Legend vs BLG Game 1")

buy_price = st.number_input(
    "매수가(센트)",
    min_value=1.0,
    max_value=99.0,
    value=50.0
)

sell_price = st.number_input(
    "매도가(센트)",
    min_value=0.0,
    max_value=100.0,
    value=70.0
)

trade_stake = st.number_input(
    "투자금($)",
    min_value=1.0,
    value=50.0,
    key="trade_stake"
)

if st.button("손익 계산하기"):
    buy_decimal = buy_price / 100
    sell_decimal = sell_price / 100

    shares = trade_stake / buy_decimal
    sell_amount = shares * sell_decimal
    profit = sell_amount - trade_stake
    roi = (profit / trade_stake) * 100

    st.subheader("거래 요약")

    st.write(f"거래 이름: {trade_name}")
    st.write(f"매수가: {buy_price:.2f}¢")
    st.write(f"매도가: {sell_price:.2f}¢")
    st.write(f"투자금: ${trade_stake:.2f}")
    st.write(f"보유 수량: {shares:.2f}주")
    st.write(f"매도금: ${sell_amount:.2f}")
    st.write(f"실현손익: ${profit:.2f}")
    st.write(f"수익률: {roi:.2f}%")

    st.markdown("### 워드 기록용 한 줄 요약")

    summary = (
        f"{trade_name} / "
        f"매수가: {buy_price:.2f}¢ / "
        f"매도가: {sell_price:.2f}¢ / "
        f"투자금: ${trade_stake:.2f} / "
        f"실현손익: ${profit:+.2f} / "
        f"수익률: {roi:+.2f}%"
    )

    st.write(summary)