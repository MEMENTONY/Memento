
import streamlit as st
import json
import urllib.parse
import urllib.request
from datetime import date, datetime

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================
# LIGHT THEME CSS
# =====================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #ffffff;
        --soft-bg: #f7f9fc;
        --card: #ffffff;
        --border: #e5e7eb;
        --text: #111827;
        --muted: #6b7280;
        --green: #00a660;
        --red: #d93025;
        --orange: #f59e0b;
        --blue: #2563eb;
        --purple: #7c3aed;
    }

    .stApp {
        background: #ffffff !important;
        color: var(--text) !important;
    }

    .block-container {
        padding-top: 1.2rem;
        max-width: 1240px;
    }

    html, body, [class*="css"] {
        color: var(--text) !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border);
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.92) !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    textarea,
    input {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-color: #d1d5db !important;
        border-radius: 12px !important;
    }

    button[kind="primary"], .stButton > button {
        border-radius: 14px !important;
        border: 1px solid #111827 !important;
        background: #111827 !important;
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #f5f8ff 52%, #eefcf6 100%);
        border: 1px solid var(--border);
        border-radius: 26px;
        padding: 24px 26px;
        margin-bottom: 18px;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 950;
        letter-spacing: -1.2px;
        color: #111827;
        margin-bottom: 4px;
    }

    .hero-sub {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.6;
    }

    .pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #ffffff;
        border: 1px solid var(--border);
        color: #374151;
        font-size: 13px;
        font-weight: 700;
        margin-top: 12px;
        margin-right: 6px;
    }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
        margin-bottom: 14px;
    }

    .soft-card {
        background: var(--soft-bg);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 12px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 6px;
    }

    .muted {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.55;
    }

    .result {
        border-radius: 26px;
        padding: 24px;
        margin: 12px 0 18px 0;
        border: 1px solid var(--border);
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.10);
    }

    .result-good {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 70%);
        border-color: #86efac;
    }

    .result-warn {
        background: linear-gradient(135deg, #fffbeb 0%, #ffffff 70%);
        border-color: #fcd34d;
    }

    .result-bad {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 70%);
        border-color: #fca5a5;
    }

    .result-title {
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -0.7px;
        color: #111827;
        margin-bottom: 8px;
    }

    .big-score {
        font-size: 22px;
        font-weight: 950;
    }

    .green { color: var(--green) !important; }
    .red { color: var(--red) !important; }
    .orange { color: var(--orange) !important; }
    .blue { color: var(--blue) !important; }

    .notice {
        padding: 13px 15px;
        border-radius: 16px;
        border: 1px solid var(--border);
        background: #ffffff;
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.55;
    }

    .notice-good {
        background: #ecfdf5;
        border-color: #86efac;
    }

    .notice-warn {
        background: #fffbeb;
        border-color: #fcd34d;
    }

    .notice-bad {
        background: #fef2f2;
        border-color: #fca5a5;
    }

    .bar-wrap {
        margin: 10px 0 14px 0;
    }

    .bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: #374151;
        margin-bottom: 5px;
        font-weight: 700;
    }

    .bar-bg {
        width: 100%;
        height: 13px;
        border-radius: 999px;
        background: #e5e7eb;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 5px 14px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] p {
        color: #6b7280 !important;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 900 !important;
    }

    div[data-testid="stTabs"] button {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 999px;
        margin-right: 8px;
        padding: 8px 14px;
        color: #111827 !important;
        font-weight: 800;
    }

    code {
        white-space: pre-wrap !important;
        color: #111827 !important;
        background: #f3f4f6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# SESSION
# =====================================================
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

if "tracked_positions" not in st.session_state:
    st.session_state.tracked_positions = []

if "market_board" not in st.session_state:
    st.session_state.market_board = []


# =====================================================
# HELPERS
# =====================================================
def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def cents_from_decimal(value):
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}¢"


def cents(value):
    return f"{value:.1f}¢"


def signed_money(value):
    if value >= 0:
        return f"+${value:,.2f}"
    return f"-${abs(value):,.2f}"


def signed_pct(value):
    if value >= 0:
        return f"+{value:.1f}%"
    return f"{value:.1f}%"


def html_bar(label, value, max_value=100, color="#00a660"):
    display_value = value
    value = clamp(value, 0, max_value)
    width = (value / max_value) * 100 if max_value > 0 else 0
    return f"""
    <div class="bar-wrap">
        <div class="bar-label"><span>{label}</span><span>{display_value:.1f}</span></div>
        <div class="bar-bg"><div class="bar-fill" style="width:{width:.1f}%; background:{color};"></div></div>
    </div>
    """


def orderbook_best_prices(book):
    bids = book.get("bids", []) or []
    asks = book.get("asks", []) or []

    best_bid = None
    best_ask = None

    if bids:
        best_bid = max(float(item["price"]) for item in bids if item.get("price") is not None)

    if asks:
        best_ask = min(float(item["price"]) for item in asks if item.get("price") is not None)

    last = book.get("last_trade_price")
    last_trade = float(last) if last not in [None, ""] else None

    if best_bid is not None and best_ask is not None:
        mid = (best_bid + best_ask) / 2
    else:
        mid = last_trade

    return best_bid, best_ask, last_trade, mid


@st.cache_data(ttl=8, show_spinner=False)
def fetch_polymarket_orderbook(token_id: str):
    token_id = token_id.strip()
    if not token_id:
        raise ValueError("token_id가 비어 있습니다.")

    base = "https://clob.polymarket.com/book"
    query = urllib.parse.urlencode({"token_id": token_id})
    url = f"{base}?{query}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Memento-Streamlit-App/1.0",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        raw = response.read().decode("utf-8")
        data = json.loads(raw)

    return data


def high_price_warning(price_decimal):
    if price_decimal is None:
        return None

    price = price_decimal * 100

    if price >= 99:
        return "99¢는 사는 가격이 아니라 파는 가격에 가깝습니다."
    if price >= 95:
        return "95~98¢는 거의 상환 스캘핑입니다. 고액 금지 구간입니다. 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."
    if price >= 90:
        return "90~95¢는 신규 매수 비추천 구간입니다."
    if price >= 85:
        return "85~90¢는 신규 진입 신중 구간입니다."
    if price >= 80:
        return "80~85¢는 익절 고려 구간입니다."
    return None


def judge_live_position(best_bid, best_ask, mid, last_trade, avg_buy_price, shares, investment, target_price, stop_loss_price, bankroll, fomo_risk=False):
    sell_price = best_bid if best_bid is not None else mid
    display_price = mid if mid is not None else last_trade

    if sell_price is None:
        return {
            "decision": "가격 조회 불가",
            "level": "bad",
            "reasons": ["best bid/mid/last trade 정보를 가져오지 못했습니다."],
            "warnings": ["token_id가 올바른지, 해당 outcome token의 order book이 활성화되어 있는지 확인하세요."],
        }

    current_value = shares * display_price if display_price is not None else shares * sell_price
    instant_sell_amount = shares * sell_price
    pnl = instant_sell_amount - investment
    roi = (pnl / investment) * 100 if investment > 0 else 0

    redeem_value = shares * 1
    additional_to_100 = redeem_value - current_value
    fail_loss = current_value

    position_pct = (current_value / bankroll) * 100 if bankroll > 0 else 0
    target_decimal = target_price / 100
    stop_decimal = stop_loss_price / 100

    reasons = []
    warnings = []
    decision = "홀딩 가능"
    level = "good"

    if sell_price >= target_decimal:
        decision = "목표가 도달 — 매도 또는 부분매도 고려"
        level = "warn"
        reasons.append(f"현재 즉시 매도 가능 가격 {cents_from_decimal(sell_price)}이 목표가 {target_price:.1f}¢ 이상입니다.")

    if roi >= 30:
        decision = "원금 회수 또는 부분매도 검토"
        level = "warn"
        reasons.append(f"현재 수익률이 {roi:.1f}%입니다. 원금 회수 또는 50~70% 부분매도를 검토할 수 있습니다.")

    if position_pct >= 20:
        decision = "진입 금지급 노출 — 즉시 축소 고려"
        level = "bad"
        warnings.append(f"현재 포지션 평가금이 포트폴리오의 {position_pct:.1f}%입니다. 20% 이상은 생존 리스크입니다.")
    elif position_pct >= 10:
        if level != "bad":
            decision = f"{decision}, 단 포지션 크기 과대"
            level = "warn"
        warnings.append(f"포트폴리오 비중이 {position_pct:.1f}%입니다. 10% 이상은 일부 축소 권장입니다.")

    if sell_price <= stop_decimal:
        remaining_ratio = current_value / investment if investment > 0 else 0
        if remaining_ratio <= 0.10:
            decision = "손절 효용 낮음 — 추가매수 금지, 옵션처럼 보유 가능"
            level = "warn"
            warnings.append("현재 평가금이 원금의 10% 이하입니다. 팔아도 회수금이 작으므로 추가매수 금지가 더 중요합니다.")
        elif remaining_ratio >= 0.30:
            decision = "손절 고려"
            level = "bad"
            warnings.append("현재가가 손절가 이하이고 원금의 30% 이상이 남아 있습니다. 손절 효용이 있습니다.")

    if fomo_risk:
        if level == "good":
            level = "warn"
            decision = "홀딩 가능, 단 감정 리스크 확인"
        warnings.append("감정 체크가 켜져 있습니다. 복구심리/FOMO 상태에서는 즉시 매도·추가매수 결정을 피하세요.")

    price_warning = high_price_warning(display_price)
    if price_warning:
        warnings.append(price_warning)

    if not reasons:
        reasons.append("현재가가 목표가보다 낮고 손절가보다 높습니다.")
    if position_pct < 10 and not fomo_risk:
        reasons.append("포트폴리오 비중과 감정 리스크가 과도하지 않습니다.")

    return {
        "decision": decision,
        "level": level,
        "reasons": reasons,
        "warnings": warnings,
        "sell_price": sell_price,
        "display_price": display_price,
        "current_value": current_value,
        "instant_sell_amount": instant_sell_amount,
        "pnl": pnl,
        "roi": roi,
        "redeem_value": redeem_value,
        "additional_to_100": additional_to_100,
        "fail_loss": fail_loss,
        "position_pct": position_pct,
    }


def result_class(level):
    if level == "good":
        return "result-good", "✅", "green"
    if level == "warn":
        return "result-warn", "⚠️", "orange"
    return "result-bad", "⛔", "red"


def partial_sell_rows(shares, current_price_decimal, investment):
    rows = []
    if current_price_decimal is None:
        return rows, None

    min_ratio = investment / (shares * current_price_decimal) * 100 if shares > 0 and current_price_decimal > 0 else None

    for ratio in [25, 50, 70, 80, 90, 100]:
        sell_shares = shares * ratio / 100
        recovered = sell_shares * current_price_decimal
        locked_pnl_vs_principal = recovered - investment
        remaining_shares = shares - sell_shares
        remaining_value = remaining_shares * current_price_decimal
        additional_if_100 = remaining_shares * (1 - current_price_decimal)

        rows.append({
            "매도 비율": f"{ratio}%",
            "매도 수량": round(sell_shares, 2),
            "회수금": money(recovered),
            "원금 대비 확정손익": signed_money(locked_pnl_vs_principal),
            "남은 수량": round(remaining_shares, 2),
            "남은 평가금": money(remaining_value),
            "100¢ 도달 시 추가수익": signed_money(additional_if_100),
        })

    return rows, min_ratio


# =====================================================
# HERO
# =====================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Memento</div>
        <div class="hero-sub">
            Polymarket 배팅 가치 판독기 + 거래 손익 기록장<br>
            자동매매가 아니라, 내가 등록한 거래의 현재 리스크와 매도/홀딩 타이밍을 확인하는 수동 도구입니다.
        </div>
        <span class="pill">Light theme</span>
        <span class="pill">Manual journal</span>
        <span class="pill">Live CLOB price</span>
        <span class="pill">Risk first</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 실시간 포지션 판독",
    "🏠 빠른 배팅 적절성",
    "💰 거래 손익",
    "🧩 부분매도",
    "📈 총수익률",
])


# =====================================================
# TAB 1: LIVE POSITION MONITOR
# =====================================================
with tab1:
    st.subheader("📡 실시간 포지션 판독")
    st.caption("token_id를 넣으면 Polymarket CLOB order book에서 best bid / best ask / last trade price를 조회합니다.")

    with st.form("live_position_form"):
        st.markdown("<div class='card'><div class='card-title'>거래 등록 + 실시간 가격 조회</div><div class='muted'>처음에는 지갑 로그인 없이 token_id 기반 가격 조회만 합니다. 즉시 매도 기준은 best bid입니다.</div></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            trade_name = st.text_input("거래 이름", "KT Rolster vs Dplus KIA — Match Winner")
            market_name = st.text_input("시장 이름", "LoL: KT Rolster vs Dplus KIA")
        with c2:
            outcome_name = st.text_input("선택한 팀/결과", "KT Rolster")
            token_id = st.text_input("Polymarket token_id", "")
        with c3:
            portfolio_value = st.number_input("전체 포트폴리오 금액($)", min_value=1.0, value=814.0)
            fomo_risk = st.checkbox("지금 감정/FOMO 위험이 있다")

        c4, c5, c6 = st.columns(3)
        with c4:
            avg_buy_price_cent = st.number_input("평균 매수가(센트)", min_value=0.1, max_value=99.9, value=52.4)
        with c5:
            shares = st.number_input("보유 수량", min_value=0.0, value=1164.12)
        with c6:
            investment = st.number_input("투자금($)", min_value=0.0, value=610.0)

        c7, c8 = st.columns(2)
        with c7:
            target_sell_price = st.number_input("목표 매도가(센트)", min_value=0.1, max_value=100.0, value=60.0)
        with c8:
            stop_loss_price = st.number_input("손절가(센트)", min_value=0.0, max_value=99.9, value=45.0)

        submitted = st.form_submit_button("가격 조회 + 매도/홀딩 판정", use_container_width=True)

    if submitted:
        if not token_id.strip():
            st.error("token_id를 입력해야 합니다. Polymarket market/outcome의 token_id를 복사해서 넣어주세요.")
        else:
            try:
                with st.spinner("Polymarket CLOB order book 조회 중..."):
                    book = fetch_polymarket_orderbook(token_id)
                    best_bid, best_ask, last_trade, mid = orderbook_best_prices(book)

                result = judge_live_position(
                    best_bid=best_bid,
                    best_ask=best_ask,
                    mid=mid,
                    last_trade=last_trade,
                    avg_buy_price=avg_buy_price_cent / 100,
                    shares=shares,
                    investment=investment,
                    target_price=target_sell_price,
                    stop_loss_price=stop_loss_price,
                    bankroll=portfolio_value,
                    fomo_risk=fomo_risk,
                )

                klass, icon, color_name = result_class(result["level"])

                st.markdown(
                    f"""
                    <div class="result {klass}">
                        <div class="result-title">{icon} 판정: {result['decision']}</div>
                        <div class="big-score {color_name}">
                            현재 즉시 매도 기준: {cents_from_decimal(result['sell_price'])}
                        </div>
                        <div class="muted">
                            {trade_name} · {outcome_name} · token_id 기반 실시간 조회
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                m1, m2, m3 = st.columns(3)
                m1.metric("현재 best bid", cents_from_decimal(best_bid))
                m2.metric("현재 best ask", cents_from_decimal(best_ask))
                m3.metric("last trade price", cents_from_decimal(last_trade))

                m4, m5, m6 = st.columns(3)
                m4.metric("mid price", cents_from_decimal(mid))
                m5.metric("내 평균 매수가", cents(avg_buy_price_cent))
                m6.metric("보유 수량", f"{shares:,.2f}주")

                st.divider()

                a, b, c, d = st.columns(4)
                a.metric("현재 평가금", money(result["current_value"]))
                b.metric("즉시 팔면 회수금", money(result["instant_sell_amount"]))
                c.metric("실현 가능 손익", signed_money(result["pnl"]))
                d.metric("현재 수익률", signed_pct(result["roi"]))

                e, f, g, h = st.columns(4)
                e.metric("100¢ 상환 시 총액", money(result["redeem_value"]))
                f.metric("100¢까지 남은 추가수익", signed_money(result["additional_to_100"]))
                g.metric("실패 시 현재 평가금 손실", f"-{money(result['fail_loss'])}")
                h.metric("포트폴리오 비중", f"{result['position_pct']:.1f}%")

                st.markdown(
                    html_bar("포트폴리오 비중", min(result["position_pct"], 100), 100, "#d93025" if result["position_pct"] >= 20 else "#f59e0b" if result["position_pct"] >= 10 else "#00a660")
                    + html_bar("현재 수익률", clamp(result["roi"], 0, 100), 100, "#00a660" if result["roi"] >= 0 else "#d93025")
                    + html_bar("현재 가격 위치", (result["display_price"] or 0) * 100, 100, "#2563eb"),
                    unsafe_allow_html=True,
                )

                st.markdown("#### 이유")
                for r in result["reasons"]:
                    st.markdown(f"<div class='notice notice-good'>{r}</div>", unsafe_allow_html=True)

                st.markdown("#### 경고")
                for w in result["warnings"]:
                    st.markdown(f"<div class='notice notice-warn'>{w}</div>", unsafe_allow_html=True)

                if result["position_pct"] >= 10 or result["roi"] >= 30 or result["sell_price"] >= target_sell_price / 100:
                    st.info("부분매도 후보: 현재 상태에서는 50~70% 부분매도로 원금 회수 또는 노출 축소를 검토할 수 있습니다.")

                rows, min_ratio = partial_sell_rows(shares, result["sell_price"], investment)
                if rows:
                    st.markdown("#### best bid 기준 부분매도 표")
                    if min_ratio is not None:
                        if min_ratio <= 100:
                            st.success(f"원금 회수에 필요한 최소 매도 비율: {min_ratio:.1f}%")
                        else:
                            st.warning(f"현재 best bid에서는 100%를 팔아도 원금 회수가 어렵습니다. 필요 비율: {min_ratio:.1f}%")
                    st.dataframe(rows, use_container_width=True)

                summary = (
                    f"{trade_name}\n"
                    f"현재 best bid: {cents_from_decimal(best_bid)} / best ask: {cents_from_decimal(best_ask)} / last: {cents_from_decimal(last_trade)}\n"
                    f"평균 매수가: {avg_buy_price_cent:.1f}¢ / 보유 수량: {shares:.2f}주 / 투자금: ${investment:.2f}\n"
                    f"즉시 매도 회수금: {money(result['instant_sell_amount'])} / "
                    f"실현 가능 손익: {signed_money(result['pnl'])} / 수익률: {signed_pct(result['roi'])}\n"
                    f"100¢ 상환 총액: {money(result['redeem_value'])} / "
                    f"남은 추가수익: {signed_money(result['additional_to_100'])} / "
                    f"실패 시 손실: -{money(result['fail_loss'])}\n"
                    f"판정: {result['decision']}"
                )
                st.markdown("#### 기록용 요약")
                st.code(summary)

                if st.button("이 거래를 포지션 목록에 저장"):
                    st.session_state.tracked_positions.append({
                        "등록일": str(date.today()),
                        "거래 이름": trade_name,
                        "시장 이름": market_name,
                        "선택": outcome_name,
                        "token_id": token_id,
                        "평균 매수가": f"{avg_buy_price_cent:.1f}¢",
                        "수량": shares,
                        "투자금": investment,
                        "목표가": f"{target_sell_price:.1f}¢",
                        "손절가": f"{stop_loss_price:.1f}¢",
                        "최근 판정": result["decision"],
                        "최근 best bid": cents_from_decimal(best_bid),
                        "최근 손익": result["pnl"],
                    })
                    st.success("포지션 목록에 저장했습니다.")

            except Exception as e:
                st.error("가격 조회에 실패했습니다.")
                st.write("확인할 것: token_id가 정확한지, 해당 outcome의 order book이 존재하는지, Polymarket API가 일시적으로 응답하지 않는지 확인하세요.")
                st.code(str(e))

    st.divider()
    st.subheader("저장된 포지션 목록")
    if st.session_state.tracked_positions:
        st.dataframe(st.session_state.tracked_positions, use_container_width=True)
        if st.button("저장된 포지션 목록 초기화"):
            st.session_state.tracked_positions = []
            st.rerun()
    else:
        st.info("아직 저장된 포지션이 없습니다.")


# =====================================================
# TAB 2: QUICK ENTRY EVALUATOR
# =====================================================
with tab2:
    st.subheader("🏠 빠른 배팅 적절성")
    st.caption("진입 전 빠르게 가격 value와 포지션 크기를 확인합니다.")

    with st.form("quick_entry_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            q_market = st.text_input("시장 이름", "T1 vs HLE — Match Winner")
            q_current = st.number_input("현재가 / 진입가격(센트)", min_value=1.0, max_value=99.0, value=52.0)
        with c2:
            q_fair = st.number_input("내가 생각하는 적정 가격(센트)", min_value=1.0, max_value=99.0, value=63.0)
            q_stake = st.number_input("진입 크기 / 투자금($)", min_value=1.0, value=50.0)
        with c3:
            q_bankroll = st.number_input("총자산($)", min_value=1.0, value=814.0)
            q_purpose = st.selectbox("배팅 목적", ["경기승리 / 만기 보유", "경기 시작 전 상승 노림", "중간 익절", "역배 / Bounce", "99¢ 상환 스캘핑"])

        q_submit = st.form_submit_button("빠른 판독", use_container_width=True)

    if q_submit:
        edge = q_fair - q_current
        pos_pct = q_stake / q_bankroll * 100
        score = 50 + edge * 2
        if pos_pct >= 20:
            score -= 80
        elif pos_pct >= 10:
            score -= 35
        elif pos_pct >= 5:
            score -= 15
        if q_current >= 95:
            score -= 30
        elif q_current >= 90:
            score -= 20
        elif q_current >= 80:
            score -= 10
        if "역배" in q_purpose or "99¢" in q_purpose:
            score -= 10

        score = clamp(score)

        if pos_pct >= 50:
            decision = "시스템 실패 — 계좌 생존 리스크"
            level = "bad"
        elif pos_pct >= 20:
            decision = "진입 금지"
            level = "bad"
        elif score >= 70:
            decision = "진입 적절"
            level = "good"
        elif score >= 55:
            decision = "소액 진입 가능"
            level = "warn"
        elif score >= 40:
            decision = "관망 우선"
            level = "warn"
        else:
            decision = "진입 부적절"
            level = "bad"

        klass, icon, color = result_class(level)
        st.markdown(
            f"""
            <div class="result {klass}">
                <div class="result-title">{icon} {decision}</div>
                <div class="big-score {color}">적절성 점수: {score:.1f}%</div>
                <div class="muted">{q_market}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        a, b, c = st.columns(3)
        a.metric("Edge", f"{edge:+.1f}¢")
        b.metric("포트폴리오 비중", f"{pos_pct:.1f}%")
        c.metric("현재 가격", cents(q_current))

        st.markdown(
            html_bar("가격 Value", clamp(50 + edge * 2), 100, "#00a660" if edge >= 0 else "#d93025")
            + html_bar("포지션 크기 위험", min(pos_pct, 100), 100, "#d93025" if pos_pct >= 20 else "#f59e0b" if pos_pct >= 10 else "#00a660"),
            unsafe_allow_html=True,
        )


# =====================================================
# TAB 3: TRADE PNL
# =====================================================
with tab3:
    st.subheader("💰 거래 손익 계산기")

    trade_name = st.text_input("거래 이름", "Anyone's Legend vs Bilibili Gaming — Game 1 Winner", key="pnl_name")
    c1, c2, c3 = st.columns(3)
    with c1:
        buy_price = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=54.0, key="pnl_buy")
    with c2:
        sell_price = st.number_input("매도가(센트)", min_value=0.0, max_value=100.0, value=87.0, key="pnl_sell")
    with c3:
        trade_stake = st.number_input("투자금($)", min_value=1.0, value=77.19, key="pnl_stake")

    if st.button("손익 계산하기", use_container_width=True):
        shares = trade_stake / (buy_price / 100)
        sell_amount = shares * (sell_price / 100)
        profit = sell_amount - trade_stake
        roi = (profit / trade_stake) * 100

        a, b, c, d = st.columns(4)
        a.metric("보유 수량", f"{shares:.2f}주")
        b.metric("매도금", money(sell_amount))
        c.metric("실현손익", signed_money(profit))
        d.metric("수익률", signed_pct(roi))

        summary = (
            f"{trade_name}\n"
            f"매수가: {buy_price:.0f}¢ / 매도가: {sell_price:.0f}¢ / 투자금: ${trade_stake:.2f} / "
            f"실현손익: {signed_money(profit)} / 수익률: {signed_pct(roi)}"
        )
        st.code(summary)

        st.session_state.trade_log.append({
            "날짜": str(date.today()),
            "거래 이름": trade_name,
            "매수가": f"{buy_price:.1f}¢",
            "매도가": f"{sell_price:.1f}¢",
            "투자금": trade_stake,
            "손익": profit,
            "수익률": roi,
        })

    with st.expander("거래 복기 질문", expanded=True):
        questions = [
            "원하는 가격에 진입했는가?",
            "내 예상 승률의 근거는 무엇인가?",
            "북메이커와 왜 다르게 봤는가?",
            "금액은 감당 가능한 크기였는가?",
            "매도 기준을 지켰는가?",
            "감정적으로 들어간 부분이 있었는가?",
            "다음에 반복 가능한 거래인가?",
        ]
        for q in questions:
            st.write(f"- {q}")


# =====================================================
# TAB 4: PARTIAL SELL
# =====================================================
with tab4:
    st.subheader("🧩 부분매도 계산기")

    c1, c2, c3 = st.columns(3)
    with c1:
        ps_buy = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=52.4, key="ps_buy")
    with c2:
        ps_current = st.number_input("현재가 / 매도 기준가(센트)", min_value=1.0, max_value=100.0, value=58.0, key="ps_current")
    with c3:
        ps_investment = st.number_input("투자금($)", min_value=0.0, value=610.0, key="ps_investment")

    use_manual_shares = st.checkbox("보유 수량 직접 입력", value=True)
    if use_manual_shares:
        ps_shares = st.number_input("보유 수량", min_value=0.0, value=1164.12, key="ps_shares")
    else:
        ps_shares = ps_investment / (ps_buy / 100)

    if st.button("부분매도 표 계산", use_container_width=True):
        rows, min_ratio = partial_sell_rows(ps_shares, ps_current / 100, ps_investment)

        if min_ratio is not None:
            if min_ratio <= 100:
                st.success(f"원금 회수에 필요한 최소 매도 비율: {min_ratio:.1f}%")
            else:
                st.warning(f"현재 가격에서는 100% 매도해도 원금 회수가 어렵습니다. 필요 비율: {min_ratio:.1f}%")

        st.dataframe(rows, use_container_width=True)

        current_value = ps_shares * (ps_current / 100)
        redeem = ps_shares
        add_profit = redeem - current_value
        st.warning(
            f"현재 평가금 {money(current_value)} / 100¢ 상환 시 총액 {money(redeem)} / "
            f"현재 대비 추가수익 {signed_money(add_profit)} / 실패 시 손실 -{money(current_value)}"
        )


# =====================================================
# TAB 5: ROI
# =====================================================
with tab5:
    st.subheader("📈 총수익률 / 거래일지")

    c1, c2, c3 = st.columns(3)
    with c1:
        start_bankroll = st.number_input("시작 자금($)", min_value=0.0, value=500.0)
    with c2:
        current_bankroll = st.number_input("현재 총자산($)", min_value=0.0, value=650.0)
    with c3:
        net_deposit = st.number_input("추가 입금 / 출금 조정($)", value=0.0)

    adjusted = start_bankroll + net_deposit
    total_profit = current_bankroll - adjusted
    total_roi = (total_profit / adjusted) * 100 if adjusted > 0 else 0

    a, b, c = st.columns(3)
    a.metric("총손익", signed_money(total_profit))
    b.metric("총수익률", signed_pct(total_roi))
    c.metric("현재 총자산", money(current_bankroll))

    st.divider()

    if st.session_state.trade_log:
        st.dataframe(st.session_state.trade_log, use_container_width=True)
    else:
        st.info("아직 거래 손익 계산기에 기록된 거래가 없습니다.")

    if st.button("거래일지 초기화"):
        st.session_state.trade_log = []
        st.rerun()
