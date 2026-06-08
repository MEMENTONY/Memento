
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 디자인
# =====================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #07111f;
        --panel: #0f1b2d;
        --panel2: #111f35;
        --border: rgba(148, 163, 184, .22);
        --text: #e5eefb;
        --muted: #94a3b8;
        --green: #16c784;
        --red: #ea3943;
        --yellow: #f0b90b;
        --blue: #3b82f6;
        --cyan: #2dd4bf;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(22,199,132,.13), transparent 32%),
            radial-gradient(circle at top right, rgba(59,130,246,.16), transparent 30%),
            linear-gradient(180deg, #07111f 0%, #0b1220 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    div[data-testid="stTabs"] button {
        background: rgba(15, 27, 45, .72);
        border-radius: 999px;
        padding: 10px 18px;
        margin-right: 8px;
        border: 1px solid rgba(148, 163, 184, .18);
    }

    .hero {
        padding: 26px 28px;
        border-radius: 28px;
        border: 1px solid rgba(148, 163, 184, .22);
        background:
            linear-gradient(135deg, rgba(22,199,132,.18), rgba(59,130,246,.10) 45%, rgba(15,23,42,.88));
        box-shadow: 0 18px 50px rgba(0,0,0,.25);
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1px;
        margin: 0;
    }

    .hero-sub {
        color: #b6c5d8;
        font-size: 16px;
        margin-top: 6px;
        line-height: 1.6;
    }

    .pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, .22);
        background: rgba(15, 27, 45, .85);
        color: #dbeafe;
        font-size: 13px;
        margin-right: 6px;
        margin-top: 10px;
    }

    .result-card {
        padding: 24px;
        border-radius: 26px;
        margin: 14px 0 20px 0;
        box-shadow: 0 18px 50px rgba(0,0,0,.28);
        border: 1px solid rgba(255,255,255,.10);
    }

    .result-good {
        background:
            linear-gradient(135deg, rgba(22,199,132,.24), rgba(15,27,45,.96) 45%, rgba(15,23,42,.98));
        border-color: rgba(22,199,132,.40);
    }

    .result-mid {
        background:
            linear-gradient(135deg, rgba(240,185,11,.24), rgba(15,27,45,.96) 45%, rgba(15,23,42,.98));
        border-color: rgba(240,185,11,.42);
    }

    .result-bad {
        background:
            linear-gradient(135deg, rgba(234,57,67,.24), rgba(15,27,45,.96) 45%, rgba(15,23,42,.98));
        border-color: rgba(234,57,67,.42);
    }

    .result-title {
        font-size: 34px;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    .result-sub {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.6;
    }

    .mini-card {
        padding: 18px;
        border-radius: 22px;
        background: rgba(15, 27, 45, .82);
        border: 1px solid rgba(148, 163, 184, .20);
        margin-bottom: 14px;
    }

    .mini-title {
        font-weight: 800;
        color: #e5eefb;
        font-size: 15px;
        margin-bottom: 6px;
    }

    .mini-value {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    .muted {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.55;
    }

    .green { color: #16c784; }
    .red { color: #ea3943; }
    .yellow { color: #f0b90b; }
    .blue { color: #60a5fa; }
    .cyan { color: #2dd4bf; }

    .section {
        padding: 20px;
        border-radius: 24px;
        background: rgba(15, 27, 45, .70);
        border: 1px solid rgba(148, 163, 184, .18);
        margin: 12px 0 18px 0;
    }

    .section-title {
        font-size: 19px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .bar-wrap {
        margin: 10px 0 14px 0;
    }

    .bar-label {
        display:flex;
        justify-content:space-between;
        color:#cbd5e1;
        font-size:13px;
        margin-bottom:6px;
    }

    .bar-bg {
        width:100%;
        height:12px;
        border-radius:999px;
        background:rgba(148,163,184,.18);
        overflow:hidden;
        border: 1px solid rgba(148,163,184,.10);
    }

    .bar-fill {
        height:100%;
        border-radius:999px;
    }

    .notice {
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(148, 163, 184, .10);
        border: 1px solid rgba(148, 163, 184, .18);
        margin: 8px 0;
        color: #dbeafe;
        font-size: 14px;
        line-height: 1.55;
    }

    .danger-notice {
        background: rgba(234, 57, 67, .12);
        border-color: rgba(234, 57, 67, .35);
    }

    .good-notice {
        background: rgba(22, 199, 132, .12);
        border-color: rgba(22, 199, 132, .35);
    }

    .warn-notice {
        background: rgba(240, 185, 11, .12);
        border-color: rgba(240, 185, 11, .35);
    }

    code {
        white-space: pre-wrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 세션 저장소
# =====================================================
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

if "market_board" not in st.session_state:
    st.session_state.market_board = []

if "last_main_result" not in st.session_state:
    st.session_state.last_main_result = None


# =====================================================
# 유틸 함수
# =====================================================
def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def cents(value):
    return f"{value:.1f}¢"


def signed_pct(value):
    return f"{value:+.1f}%"


def bar_html(label, value, max_value=100, color="#16c784"):
    safe_value = clamp(value, 0, max_value)
    width = 0 if max_value == 0 else (safe_value / max_value) * 100
    return f"""
    <div class="bar-wrap">
        <div class="bar-label"><span>{label}</span><b>{value:.1f}</b></div>
        <div class="bar-bg"><div class="bar-fill" style="width:{width:.1f}%; background:{color};"></div></div>
    </div>
    """


def score_color(score):
    if score >= 70:
        return "#16c784"
    if score >= 50:
        return "#f0b90b"
    return "#ea3943"


def price_warning(price):
    if price >= 99:
        return "99¢는 사는 가격이 아니라 파는 가격에 가깝습니다.", "red", -28
    if price >= 95:
        return "95~98¢는 거의 상환 스캘핑입니다. 고액 신규 매수 금지에 가깝습니다.", "red", -22
    if price >= 90:
        return "90~95¢는 신규 매수 비추천 구간입니다.", "red", -15
    if price >= 85:
        return "85~90¢는 신규 진입을 매우 신중하게 봐야 합니다.", "yellow", -8
    if price >= 80:
        return "80~85¢는 신규 매수보다 익절 고려 구간입니다.", "yellow", -5
    if 2 <= price <= 5:
        return "2~5¢ Bounce Trade는 소액 전용입니다.", "yellow", -8
    if price < 2:
        return "2¢ 미만은 거의 복권형 가격입니다.", "red", -15
    return "가격 구간 자체는 과도한 위험 신호가 크지 않습니다.", "green", 0


def purpose_rule(purpose):
    rules = {
        "경기승리 / 만기 보유": (1.00, 0, "기본적인 승리 베팅입니다. 실제 승률 추정이 가장 중요합니다."),
        "경기 시작 전 가격 상승 노림": (0.70, -6, "실제 승리보다 시장 심리와 타이밍이 중요합니다. 빨리 익절 기준을 정해야 합니다."),
        "반반 경기 강팀 쏠림 이용 / 중간 익절": (0.60, -8, "경기력이 아니라 시장 쏠림을 노리는 거래입니다. 오래 들고 가면 위험합니다."),
        "역배 / Bounce Trade": (0.35, -12, "역배와 bounce는 소액 전용입니다. 맞으면 크지만 실패가 기본값일 수 있습니다."),
        "99¢ 상환 스캘핑": (0.20, -22, "작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."),
        "뉴스/이벤트 선반영": (0.50, -10, "조건문과 해결 기준 확인이 중요합니다. 뉴스 해석 실수 위험이 큽니다."),
    }
    return rules.get(purpose, (1.00, 0, ""))


def market_type_rule(market_type):
    rules = {
        "Match Moneyline": (1.00, 0, "가장 기본적인 시장입니다."),
        "Game Winner": (0.50, -10, "Game Winner는 변동성이 커서 추천 금액을 50% 줄입니다."),
        "Correct Score": (0.25, -25, "Correct Score는 맞히기 어렵습니다. 강한 경고 대상입니다."),
        "정치 선거": (0.50, -12, "정치 선거는 결과 기준과 이의제기 가능성을 확인해야 합니다."),
        "뉴스/이벤트": (0.50, -12, "뉴스/이벤트는 조건문과 resolution 기준 확인이 필수입니다."),
        "99¢ 상환 스캘핑": (0.20, -25, "고가 상환 스캘핑은 고액 금지입니다."),
        "2~5¢ Bounce Trade": (0.20, -18, "초저가 bounce는 소액 전용입니다."),
    }
    return rules.get(market_type, (1.00, 0, ""))


def size_label(position_pct):
    if position_pct >= 50:
        return "시스템 실패 — 계좌 생존 리스크", "red", -100
    if position_pct >= 20:
        return "진입 금지", "red", -80
    if position_pct >= 10:
        return "매우 위험", "red", -35
    if position_pct >= 5:
        return "위험", "yellow", -20
    if position_pct >= 3:
        return "주의", "yellow", -8
    return "정상", "green", 5


def exposure_label(exposure_pct):
    if exposure_pct >= 20:
        return "중복 노출 진입 금지", "red", -55
    if exposure_pct >= 10:
        return "중복 노출 위험", "red", -30
    if exposure_pct >= 5:
        return "중복 노출 주의", "yellow", -12
    return "정상", "green", 0


def confidence_cap(confidence):
    caps = {
        "관찰용": 15,
        "낮은 확신": 25,
        "중간 확신": 50,
        "높은 확신": 70,
        "초고확신": 70,
    }
    return caps.get(confidence, 50)


def portfolio_cap(bankroll, confidence):
    # 생존 우선: 확신별 계좌 비율 상한
    pct_map = {
        "관찰용": 0.01,
        "낮은 확신": 0.02,
        "중간 확신": 0.04,
        "높은 확신": 0.06,
        "초고확신": 0.08,
    }
    return bankroll * pct_map.get(confidence, 0.04)


def calculate_result(
    market_name,
    current_price,
    fair_price,
    stake,
    purpose,
    bankroll,
    emotional_limit,
    market_type,
    confidence,
    target_price,
    stop_price,
    bookmaker_prob,
    previous_good_price,
    duplicate_ml,
    duplicate_game,
    duplicate_same_side,
    fomo_count,
):
    edge = fair_price - current_price
    position_pct = (stake / bankroll) * 100 if bankroll > 0 else 0

    purpose_multiplier, purpose_penalty, purpose_note = purpose_rule(purpose)
    type_multiplier, type_penalty, type_note = market_type_rule(market_type)

    fixed_cap = confidence_cap(confidence)
    port_cap = portfolio_cap(bankroll, confidence)
    base_cap = min(fixed_cap, port_cap, emotional_limit)
    recommended_cap = base_cap * purpose_multiplier * type_multiplier

    # 감정 상태가 있으면 추천금액 50% 감소, 3개 이상이면 신규 진입 금지급
    if fomo_count >= 1:
        recommended_cap *= 0.5

    # 가치 점수: 배팅 규모를 제외한 순수 가격/가치 판단
    value_score = 50 + edge * 2.2
    price_note, price_color, price_penalty = price_warning(current_price)
    value_score += price_penalty + purpose_penalty + type_penalty

    if previous_good_price > 0:
        chase_gap = current_price - previous_good_price
        if chase_gap >= 30:
            chase_penalty = -25
            chase_note = "처음 봤던 저평가 가격보다 30¢ 이상 높습니다. FOMO 추격 위험이 큽니다."
        elif chase_gap >= 15:
            chase_penalty = -13
            chase_note = "처음 봤던 가격보다 많이 올랐습니다. 진입가 매력이 줄었습니다."
        elif chase_gap >= 5:
            chase_penalty = -5
            chase_note = "처음 봤던 가격보다 조금 올랐습니다."
        else:
            chase_penalty = 5
            chase_note = "처음 봤던 가격 대비 아직 추격 위험은 크지 않습니다."
        value_score += chase_penalty
    else:
        chase_gap = 0
        chase_note = "처음 봤던 저평가 가격을 입력하지 않았습니다."

    # 북메이커 비교
    my_vs_poly = edge
    book_vs_poly = bookmaker_prob - current_price if bookmaker_prob > 0 else 0
    my_vs_book = fair_price - bookmaker_prob if bookmaker_prob > 0 else 0
    book_note = "북메이커 기준 승률을 입력하지 않았습니다."
    if bookmaker_prob > 0:
        if my_vs_book >= 10:
            book_note = "내 적정가가 북메이커보다 10%p 이상 높습니다. 과신 가능성을 재검토하세요."
            value_score -= 12
        elif book_vs_poly >= 5:
            book_note = "북메이커 기준으로도 Polymarket 가격이 약간 싸 보입니다."
            value_score += 5
        elif book_vs_poly <= -5:
            book_note = "북메이커 기준으로는 Polymarket 가격이 비싼 편입니다."
            value_score -= 8
        else:
            book_note = "북메이커와 Polymarket 가격 차이가 크지 않습니다."

    value_score = clamp(value_score)

    # 규모/감정/중복 노출 포함 적절성
    size_status, size_color, size_penalty = size_label(position_pct)

    duplicate_total = duplicate_ml + duplicate_game + duplicate_same_side + stake
    duplicate_pct = (duplicate_total / bankroll) * 100 if bankroll > 0 else 0
    exposure_status, exposure_color, exposure_penalty = exposure_label(duplicate_pct)

    fomo_penalty = 0
    if fomo_count >= 3:
        fomo_penalty = -70
    elif fomo_count >= 1:
        fomo_penalty = -20

    cap_penalty = 0
    cap_status = "상한선 이내"
    if stake >= 200:
        cap_penalty = -80
        cap_status = "$200 이상 — 시스템 실패"
    elif stake >= 100:
        cap_penalty = -45
        cap_status = "$100 이상 — 강한 경고"
    elif stake > recommended_cap * 1.2:
        cap_penalty = -30
        cap_status = "추천 상한선 초과"
    elif stake > recommended_cap:
        cap_penalty = -12
        cap_status = "추천 상한선 근처/초과"
    else:
        cap_status = "추천 상한선 이내"

    final_score = clamp(value_score + size_penalty + exposure_penalty + fomo_penalty + cap_penalty)

    hard_stop_reason = None
    if position_pct >= 50:
        hard_stop_reason = "시스템 실패 — 계좌 생존 리스크"
    elif stake >= 200:
        hard_stop_reason = "$200 이상 — 시스템 실패"
    elif position_pct >= 20:
        hard_stop_reason = "진입 금지 — 포트폴리오 20% 이상"
    elif duplicate_pct >= 20:
        hard_stop_reason = "진입 금지 — 같은 경기/같은 방향 노출 20% 이상"
    elif fomo_count >= 3:
        hard_stop_reason = "진입 금지 — 감정 배팅 위험 3개 이상"

    if hard_stop_reason:
        decision = hard_stop_reason
        decision_type = "bad"
    else:
        if final_score >= 75:
            decision = "진입 적절"
            decision_type = "good"
        elif final_score >= 60:
            decision = "소액 진입 가능"
            decision_type = "mid"
        elif final_score >= 45:
            decision = "관망 우선"
            decision_type = "mid"
        else:
            decision = "진입 부적절"
            decision_type = "bad"

    # 목표/손절
    shares = stake / (current_price / 100)
    target_amount = shares * (target_price / 100)
    stop_amount = shares * (stop_price / 100)
    target_profit = target_amount - stake
    stop_loss = stake - stop_amount
    rr = target_profit / stop_loss if stop_loss > 0 else 0

    if target_profit > 0 and stop_loss > 0:
        if stop_loss > target_profit:
            rr_text = f"목표가까지 얻을 수 있는 금액보다 손절 시 잃을 수 있는 금액이 약 {stop_loss / target_profit:.1f}배 큽니다."
        else:
            rr_text = f"목표가 수익이 손절 손실보다 약 {target_profit / stop_loss:.1f}배 큽니다."
    else:
        rr_text = "목표가 또는 손절가 설정을 다시 확인하세요."

    current_value = shares * (current_price / 100)
    redeem_value = shares
    additional_to_100 = redeem_value - current_value
    fail_loss = current_value

    high_price_warning = ""
    if current_price >= 90:
        high_price_warning = (
            f"현재부터 100¢까지 추가로 얻을 수 있는 금액은 {money(additional_to_100)}입니다. "
            f"반대로 틀리면 현재 평가금 {money(fail_loss)}를 잃을 수 있습니다. 신규 매수보다 익절 구간에 가깝습니다."
        )
    if current_price >= 97:
        high_price_warning += " 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."

    reasons = []
    if edge >= 10:
        reasons.append(f"가격 메리트 좋음: 내 적정가가 현재가보다 {edge:.1f}¢ 높음")
    elif edge >= 5:
        reasons.append(f"가격 메리트 약간 있음: edge {edge:.1f}¢")
    elif edge < 0:
        reasons.append(f"가격 메리트 없음: 내 적정가보다 현재가가 {abs(edge):.1f}¢ 비쌈")
    else:
        reasons.append(f"가격 메리트 작음: edge {edge:.1f}¢")

    reasons.append(f"포지션 크기: 총자산의 {position_pct:.1f}% — {size_status}")
    reasons.append(f"추천 상한선: {money(recommended_cap)} / 현재 투자금 {money(stake)} — {cap_status}")

    warnings = []
    if position_pct >= 10:
        warnings.append("포트폴리오 비중이 큽니다. 수익보다 계좌 생존을 먼저 봐야 합니다.")
    if fomo_count >= 1:
        warnings.append(f"감정 체크 {fomo_count}개 선택됨. 추천 금액을 줄여야 합니다.")
    if duplicate_pct >= 5:
        warnings.append(f"같은 경기/방향 총 노출 {duplicate_pct:.1f}%입니다.")
    if current_price >= 80:
        warnings.append(price_note)
    if bookmaker_prob > 0 and my_vs_book >= 10:
        warnings.append(book_note)
    if purpose_note:
        warnings.append(purpose_note)
    if type_note:
        warnings.append(type_note)

    if not warnings:
        warnings.append("큰 위험 신호는 없지만, 손절과 익절 기준은 반드시 정해야 합니다.")

    return {
        "market_name": market_name,
        "current_price": current_price,
        "fair_price": fair_price,
        "stake": stake,
        "purpose": purpose,
        "market_type": market_type,
        "confidence": confidence,
        "bankroll": bankroll,
        "edge": edge,
        "position_pct": position_pct,
        "value_score": round(value_score, 1),
        "final_score": round(final_score, 1),
        "decision": decision,
        "decision_type": decision_type,
        "reasons": reasons,
        "warnings": warnings[:5],
        "shares": shares,
        "recommended_cap": recommended_cap,
        "cap_status": cap_status,
        "size_status": size_status,
        "duplicate_total": duplicate_total,
        "duplicate_pct": duplicate_pct,
        "exposure_status": exposure_status,
        "fomo_count": fomo_count,
        "target_profit": target_profit,
        "stop_loss": stop_loss,
        "rr": rr,
        "rr_text": rr_text,
        "current_value": current_value,
        "redeem_value": redeem_value,
        "additional_to_100": additional_to_100,
        "fail_loss": fail_loss,
        "high_price_warning": high_price_warning,
        "price_note": price_note,
        "chase_note": chase_note,
        "book_note": book_note,
        "my_vs_poly": my_vs_poly,
        "book_vs_poly": book_vs_poly,
        "my_vs_book": my_vs_book,
    }


def render_result(result):
    if not result:
        st.markdown(
            """
            <div class="section">
                <div class="section-title">🔎 아직 판독 결과가 없습니다</div>
                <div class="muted">아래 빠른 입력값을 넣고 <b>판독하기</b>를 누르면 이 자리에 바로 결과보고 창이 뜹니다.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    score = result["final_score"]
    value_score = result["value_score"]
    decision_type = result["decision_type"]

    if decision_type == "good":
        klass = "result-good"
        icon = "✅"
        score_text = f"적절성 {score:.1f}%"
        score_class = "green"
    elif decision_type == "mid":
        klass = "result-mid"
        icon = "⚠️"
        score_text = f"조건부 적절성 {score:.1f}%"
        score_class = "yellow"
    else:
        klass = "result-bad"
        icon = "⛔"
        score_text = f"부적절도 {100 - score:.1f}%"
        score_class = "red"

    st.markdown(
        f"""
        <div class="result-card {klass}">
            <div class="result-title">{icon} {result['decision']}</div>
            <div class="result-sub">
                <b>{result['market_name']}</b><br>
                리스크 포함 판정: <span class="{score_class}"><b>{score_text}</b></span>
                &nbsp; | &nbsp;
                배팅 규모 제외 순수 가치: <span class="blue"><b>{value_score:.1f}%</b></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("현재가", cents(result["current_price"]))
    c2.metric("내 적정가", cents(result["fair_price"]))
    c3.metric("Edge", f"{result['edge']:+.1f}¢")
    c4.metric("포트폴리오 비중", f"{result['position_pct']:.1f}%")

    st.markdown(
        bar_html("리스크 포함 최종 적절성", result["final_score"], 100, score_color(result["final_score"]))
        + bar_html("배팅 규모 제외 순수 가치", result["value_score"], 100, "#60a5fa")
        + bar_html("포트폴리오 사용 비중", min(result["position_pct"], 100), 100, "#f0b90b" if result["position_pct"] < 20 else "#ea3943"),
        unsafe_allow_html=True
    )

    st.markdown("#### 핵심 이유")
    for reason in result["reasons"]:
        st.markdown(f"<div class='notice'>{reason}</div>", unsafe_allow_html=True)

    st.markdown("#### 핵심 경고")
    for warning in result["warnings"]:
        style = "danger-notice" if ("금지" in warning or "위험" in warning or "고액" in warning) else "warn-notice"
        st.markdown(f"<div class='notice {style}'>{warning}</div>", unsafe_allow_html=True)

    st.markdown("#### 한눈에 보는 비교")
    st.markdown(
        bar_html("현재 Polymarket 가격", result["current_price"], 100, "#94a3b8")
        + bar_html("내가 보는 적정 가격", result["fair_price"], 100, "#16c784")
        + bar_html("추천 상한선 대비 현재 투자금", min(result["stake"] / result["recommended_cap"] * 100 if result["recommended_cap"] > 0 else 100, 150), 150, "#f0b90b"),
        unsafe_allow_html=True
    )

    with st.expander("상세 판독 결과 보기", expanded=False):
        a, b, c = st.columns(3)
        a.metric("추천 상한선", money(result["recommended_cap"]))
        b.metric("같은 경기 총 노출", f"{result['duplicate_pct']:.1f}%")
        c.metric("감정 체크 수", f"{result['fomo_count']}개")

        st.write(f"**목표가 도달 시 예상 수익:** {money(result['target_profit'])}")
        st.write(f"**손절가 도달 시 예상 손실:** {money(result['stop_loss'])}")
        st.write(f"**목표/손절 손익비:** {result['rr']:.2f} : 1")
        st.info(result["rr_text"])

        if result["high_price_warning"]:
            st.error(result["high_price_warning"])

        st.write("**북메이커/내 판단 비교**")
        st.write(f"- 내 적정가 - Polymarket 현재가: {result['my_vs_poly']:+.1f}%p")
        st.write(f"- 북메이커 기준 - Polymarket 현재가: {result['book_vs_poly']:+.1f}%p")
        st.write(f"- 내 적정가 - 북메이커 기준: {result['my_vs_book']:+.1f}%p")
        st.caption(result["book_note"])

        summary = (
            f"{result['market_name']}\n"
            f"현재가: {result['current_price']:.1f}¢ / 내 적정가: {result['fair_price']:.1f}¢ / "
            f"Edge: {result['edge']:+.1f}¢ / 투자금: ${result['stake']:.2f} / "
            f"포트폴리오 비중: {result['position_pct']:.1f}% / "
            f"배팅목적: {result['purpose']} / 판정: {result['decision']} / "
            f"리스크포함점수: {result['final_score']:.1f}% / 규모제외가치: {result['value_score']:.1f}%"
        )
        st.code(summary)


# =====================================================
# 상단
# =====================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Memento</div>
        <div class="hero-sub">
            Polymarket 배팅 가치 판독기 + 거래 손익 기록장<br>
            빠르게 입력하고, 먼저 결론을 보고, 필요한 상세 리스크만 펼쳐보는 수동 판단 도구.
        </div>
        <span class="pill">Quick decision</span>
        <span class="pill">Risk first</span>
        <span class="pill">No auto-trading</span>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 메인 판독기",
    "💰 거래 손익",
    "🧩 부분매도",
    "📈 총수익률",
    "📰 EDGE / NEWS"
])


# =====================================================
# 1. 메인 판독기
# =====================================================
with tab1:
    st.subheader("🏠 빠른 배팅 적절성 판독")

    result_area = st.container()
    with result_area:
        render_result(st.session_state.last_main_result)

    st.markdown("<div class='section'><div class='section-title'>빠른 입력</div><div class='muted'>기본 입력은 최소화했습니다. 더 자세한 기준은 아래 고급설정에 숨겨져 있습니다.</div></div>", unsafe_allow_html=True)

    with st.form("main_evaluator_form"):
        market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner")

        c1, c2, c3 = st.columns(3)
        with c1:
            current_price = st.number_input("현재가 / 진입가격(센트)", min_value=1.0, max_value=99.0, value=52.0)
        with c2:
            fair_price = st.number_input("내가 생각하는 적정 가격(센트)", min_value=1.0, max_value=99.0, value=63.0)
        with c3:
            stake = st.number_input("진입 크기 / 투자금($)", min_value=1.0, value=50.0)

        c4, c5 = st.columns(2)
        with c4:
            purpose = st.selectbox(
                "배팅 목적",
                [
                    "경기승리 / 만기 보유",
                    "경기 시작 전 가격 상승 노림",
                    "반반 경기 강팀 쏠림 이용 / 중간 익절",
                    "역배 / Bounce Trade",
                    "99¢ 상환 스캘핑",
                    "뉴스/이벤트 선반영",
                ],
            )
        with c5:
            market_type = st.selectbox(
                "시장 유형",
                [
                    "Match Moneyline",
                    "Game Winner",
                    "Correct Score",
                    "정치 선거",
                    "뉴스/이벤트",
                    "99¢ 상환 스캘핑",
                    "2~5¢ Bounce Trade",
                ],
            )

        with st.expander("고급설정 펼치기", expanded=False):
            st.caption("빠른 판단에 꼭 필요하지 않은 값들은 여기에 숨겼습니다.")

            a1, a2, a3 = st.columns(3)
            with a1:
                bankroll = st.number_input("현재 전체 포트폴리오 / 총자산($)", min_value=1.0, value=814.0)
            with a2:
                emotional_limit = st.number_input("감정적으로 감당 가능한 1회 금액($)", min_value=1.0, value=50.0)
            with a3:
                confidence = st.selectbox("확신 수준", ["관찰용", "낮은 확신", "중간 확신", "높은 확신", "초고확신"], index=2)

            b1, b2, b3 = st.columns(3)
            with b1:
                target_price = st.number_input("목표가(센트)", min_value=1.0, max_value=100.0, value=75.0)
            with b2:
                stop_price = st.number_input("손절가(센트)", min_value=0.0, max_value=99.0, value=42.0)
            with b3:
                bookmaker_prob = st.number_input("북메이커 기준 승률(%)", min_value=0.0, max_value=99.0, value=0.0)

            previous_good_price = st.number_input("처음 봤던 저평가 가격(선택)", min_value=0.0, max_value=99.0, value=0.0)

            st.markdown("##### 같은 경기 / 같은 팀 중복 노출")
            e1, e2, e3 = st.columns(3)
            with e1:
                duplicate_ml = st.number_input("기존 같은 경기 Moneyline 노출($)", min_value=0.0, value=0.0)
            with e2:
                duplicate_game = st.number_input("Game Winner 노출($)", min_value=0.0, value=0.0)
            with e3:
                duplicate_same_side = st.number_input("같은 팀/같은 방향 추가 노출($)", min_value=0.0, value=0.0)

            st.markdown("##### FOMO / 감정 상태 체크")
            fomo_options = [
                "방금 큰 수익을 냈다",
                "방금 큰 손실을 냈다",
                "아까 판 게 후회된다",
                "빨리 복구하고 싶다",
                "더 빨리 계좌를 키우고 싶다",
                "놓치면 아깝다고 느낀다",
                "이미 같은 경기에 포지션이 있다",
            ]

            fomo_count = 0
            fc1, fc2 = st.columns(2)
            for idx, option in enumerate(fomo_options):
                with fc1 if idx % 2 == 0 else fc2:
                    if st.checkbox(option, key=f"fomo_{idx}"):
                        fomo_count += 1

        submitted = st.form_submit_button("🔍 판독하기", use_container_width=True)

    if submitted:
        result = calculate_result(
            market_name=market_name,
            current_price=current_price,
            fair_price=fair_price,
            stake=stake,
            purpose=purpose,
            bankroll=bankroll,
            emotional_limit=emotional_limit,
            market_type=market_type,
            confidence=confidence,
            target_price=target_price,
            stop_price=stop_price,
            bookmaker_prob=bookmaker_prob,
            previous_good_price=previous_good_price,
            duplicate_ml=duplicate_ml,
            duplicate_game=duplicate_game,
            duplicate_same_side=duplicate_same_side,
            fomo_count=fomo_count,
        )
        st.session_state.last_main_result = result
        st.toast("판독 결과가 위쪽 결과보고 창에 생성되었습니다.", icon="📊")
        st.rerun()


# =====================================================
# 2. 거래 손익 계산기
# =====================================================
with tab2:
    st.subheader("💰 거래 손익 계산기")
    st.caption("거래 결과를 계산하고 Word에 붙여넣기 좋은 요약을 만듭니다.")

    trade_name = st.text_input("거래 이름", "Anyone's Legend vs Bilibili Gaming — Game 1 Winner", key="trade_name")
    a, b, c = st.columns(3)
    with a:
        buy_price = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=54.0, key="trade_buy")
    with b:
        sell_price = st.number_input("매도가(센트)", min_value=0.0, max_value=100.0, value=87.0, key="trade_sell")
    with c:
        trade_stake = st.number_input("투자금($)", min_value=1.0, value=77.19, key="trade_stake")

    if st.button("손익 계산하기", use_container_width=True):
        shares = trade_stake / (buy_price / 100)
        sell_amount = shares * (sell_price / 100)
        profit = sell_amount - trade_stake
        roi = profit / trade_stake * 100

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("보유 수량", f"{shares:.2f}주")
        c2.metric("매도금", money(sell_amount))
        c3.metric("실현손익", money(profit))
        c4.metric("수익률", f"{roi:+.1f}%")

        summary = (
            f"{trade_name}\n"
            f"매수가: {buy_price:.0f}¢ / 매도가: {sell_price:.0f}¢ / "
            f"투자금: ${trade_stake:.2f} / 실현손익: ${profit:+.2f} / 수익률: {roi:+.1f}%"
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
# 3. 부분매도 계산기
# =====================================================
with tab3:
    st.subheader("🧩 부분매도 전략 계산기")
    st.caption("현재가에서 몇 %를 팔면 원금 회수/리스크 축소가 되는지 계산합니다.")

    pm_name = st.text_input("시장 이름", "Anyone's Legend vs Team WE — LPL Playoffs BO5", key="pm_name")
    a, b, c = st.columns(3)
    with a:
        pm_buy = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=16.0, key="pm_buy")
    with b:
        pm_current = st.number_input("현재가(센트)", min_value=1.0, max_value=100.0, value=73.0, key="pm_current")
    with c:
        pm_stake = st.number_input("투자금($)", min_value=1.0, value=16.08, key="pm_stake")

    use_manual_shares = st.checkbox("보유 수량 직접 입력", key="pm_manual")
    if use_manual_shares:
        pm_shares = st.number_input("보유 수량", min_value=0.0, value=100.0, key="pm_shares")
    else:
        pm_shares = pm_stake / (pm_buy / 100)

    redeem_100 = st.checkbox("남은 포지션 100¢ 상환 가정", value=True, key="pm_redeem")

    if st.button("부분매도 표 만들기", use_container_width=True):
        st.metric("총 보유 수량", f"{pm_shares:.2f}주")

        needed_ratio = pm_stake / (pm_shares * (pm_current / 100)) if pm_shares > 0 and pm_current > 0 else 0
        needed_ratio_pct = min(needed_ratio * 100, 100)
        st.success(f"원금 회수에 필요한 최소 매도 비율: {needed_ratio_pct:.1f}%")

        rows = []
        for ratio in [25, 50, 70, 80, 90, 100]:
            sell_shares = pm_shares * ratio / 100
            recovered = sell_shares * (pm_current / 100)
            locked_profit = recovered - pm_stake
            remaining_shares = pm_shares - sell_shares
            remaining_value = remaining_shares * (pm_current / 100)
            add_profit_100 = remaining_shares * (1 - pm_current / 100) if redeem_100 else 0

            rows.append({
                "매도 비율": f"{ratio}%",
                "매도 수량": round(sell_shares, 2),
                "회수금": money(recovered),
                "총 원금 대비 확정손익": money(locked_profit),
                "남은 수량": round(remaining_shares, 2),
                "남은 평가금": money(remaining_value),
                "100¢ 도달 시 추가수익": money(add_profit_100),
            })

        st.dataframe(rows, use_container_width=True)

        current_value = pm_shares * (pm_current / 100)
        redeem_value = pm_shares
        add_to_100 = redeem_value - current_value
        fail_loss = current_value

        st.warning(
            f"현재 평가금은 {money(current_value)}입니다. "
            f"100¢ 상환 시 총액은 {money(redeem_value)}이고, 현재 대비 추가수익은 {money(add_to_100)}입니다. "
            f"반대로 실패하면 현재 평가금 {money(fail_loss)}를 잃을 수 있습니다."
        )


# =====================================================
# 4. 총수익률
# =====================================================
with tab4:
    st.subheader("📈 총수익률 / 전체 성과")

    a, b, c = st.columns(3)
    with a:
        start_bankroll = st.number_input("시작 자금($)", min_value=0.0, value=500.0, key="roi_start")
    with b:
        current_bankroll = st.number_input("현재 총자산($)", min_value=0.0, value=650.0, key="roi_current")
    with c:
        net_deposit = st.number_input("추가 입금 / 출금 조정($)", value=0.0, key="roi_deposit")

    adjusted = start_bankroll + net_deposit
    profit = current_bankroll - adjusted
    roi = profit / adjusted * 100 if adjusted > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("총손익", money(profit))
    c2.metric("총수익률", f"{roi:+.1f}%")
    c3.metric("현재 총자산", money(current_bankroll))

    st.divider()
    st.subheader("거래일지")
    if st.session_state.trade_log:
        st.dataframe(st.session_state.trade_log, use_container_width=True)
    else:
        st.info("아직 기록된 거래가 없습니다.")

    if st.button("거래일지 초기화"):
        st.session_state.trade_log = []
        st.rerun()


# =====================================================
# 5. EDGE / NEWS
# =====================================================
with tab5:
    st.subheader("📰 EDGE / NEWS 보드")
    st.caption("현재는 수동 기록용입니다. 나중에 Polymarket API, 북메이커, 뉴스 감시 기능을 연결할 수 있습니다.")

    with st.form("news_form"):
        n1, n2, n3, n4 = st.columns(4)
        with n1:
            news_name = st.text_input("시장 이름", "Example: T1 vs HLE")
        with n2:
            news_price = st.number_input("현재가(센트)", min_value=1.0, max_value=99.0, value=50.0)
        with n3:
            news_fair = st.number_input("내 적정가(센트)", min_value=1.0, max_value=99.0, value=60.0)
        with n4:
            news_importance = st.selectbox("관심도", ["낮음", "보통", "높음", "매우 높음"])
        news_note = st.text_area("메모 / 뉴스 / 근거", "라인업, 부상, 시장 공포, 북메이커 괴리 등")
        add_news = st.form_submit_button("보드에 추가")

    if add_news:
        news_edge = news_fair - news_price
        if news_edge >= 10:
            judge = "저평가 후보"
            score = 80
        elif news_edge >= 5:
            judge = "관찰 후보"
            score = 65
        elif news_edge >= 0:
            judge = "관망"
            score = 50
        else:
            judge = "비추천"
            score = 30

        st.session_state.market_board.append({
            "날짜": str(date.today()),
            "시장": news_name,
            "현재가": f"{news_price:.1f}¢",
            "내 적정가": f"{news_fair:.1f}¢",
            "Edge": news_edge,
            "관심도": news_importance,
            "판정": judge,
            "점수": score,
            "메모": news_note,
        })
        st.success("보드에 추가했습니다.")

    if st.session_state.market_board:
        sorted_board = sorted(st.session_state.market_board, key=lambda x: x["점수"], reverse=True)
        st.dataframe(sorted_board, use_container_width=True)
    else:
        st.info("아직 보드에 추가한 시장이 없습니다.")

    if st.button("보드 초기화"):
        st.session_state.market_board = []
        st.rerun()
