
import json
from datetime import date
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #ffffff;
        --soft-bg: #f6f8fb;
        --card: #ffffff;
        --border: #e5e7eb;
        --text: #111827;
        --muted: #6b7280;
        --green: #00a660;
        --green-bg: #e9f9f1;
        --red: #e23b3b;
        --red-bg: #fff0f0;
        --yellow: #f59e0b;
        --yellow-bg: #fff7e6;
        --blue: #2563eb;
        --blue-bg: #eff6ff;
    }
    html, body, .stApp {
        background: var(--bg) !important;
        color: var(--text) !important;
    }
    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--text);
    }
    div[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border);
    }
    input, textarea, select {
        background-color: #ffffff !important;
        color: #111827 !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
    }
    div[data-testid="stTabs"] button {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 10px 18px;
        margin-right: 8px;
        color: #111827;
        font-weight: 650;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        border-color: #111827;
        background: #111827;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #ffffff !important;
    }
    .stButton button {
        border-radius: 14px !important;
        border: 1px solid #111827 !important;
        background: #111827 !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        padding: 0.7rem 1rem !important;
    }
    .hero {
        background:
            radial-gradient(circle at 18% 20%, rgba(0,166,96,.16), transparent 26%),
            radial-gradient(circle at 95% 10%, rgba(37,99,235,.14), transparent 28%),
            linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 26px 28px;
        box-shadow: 0 16px 44px rgba(15, 23, 42, .07);
        margin-bottom: 18px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 950;
        letter-spacing: -1.4px;
        color: #0f172a;
        margin: 0;
        line-height: 1.05;
    }
    .hero-subtitle {
        margin-top: 8px;
        font-size: 16px;
        color: #475569;
        line-height: 1.6;
    }
    .pill {
        display: inline-block;
        margin-top: 14px;
        margin-right: 7px;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: #ffffff;
        color: #334155;
        font-size: 13px;
        font-weight: 750;
    }
    .panel {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 30px rgba(15, 23, 42, .045);
        margin: 12px 0 18px 0;
    }
    .panel-soft {
        background: var(--soft-bg);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 20px;
        margin: 12px 0 18px 0;
    }
    .section-title {
        font-size: 18px;
        font-weight: 900;
        color: #111827;
        letter-spacing: -.2px;
        margin-bottom: 4px;
    }
    .muted {
        color: var(--muted);
        font-size: 13.5px;
        line-height: 1.55;
    }
    .result-card {
        border-radius: 28px;
        padding: 24px;
        border: 1px solid var(--border);
        box-shadow: 0 18px 50px rgba(15, 23, 42, .08);
        margin-bottom: 18px;
    }
    .result-good {
        background: linear-gradient(135deg, #e9f9f1 0%, #ffffff 54%, #f8fafc 100%);
        border-color: rgba(0,166,96,.30);
    }
    .result-mid {
        background: linear-gradient(135deg, #fff7e6 0%, #ffffff 54%, #f8fafc 100%);
        border-color: rgba(245,158,11,.35);
    }
    .result-bad {
        background: linear-gradient(135deg, #fff0f0 0%, #ffffff 54%, #f8fafc 100%);
        border-color: rgba(226,59,59,.35);
    }
    .result-title {
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -.8px;
        line-height: 1.15;
        color: #111827;
        margin-bottom: 8px;
    }
    .result-sub {
        color: #475569;
        font-size: 15px;
        line-height: 1.65;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 17px 18px;
        box-shadow: 0 7px 24px rgba(15, 23, 42, .045);
        margin-bottom: 12px;
        min-height: 108px;
    }
    .metric-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .35px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 950;
        color: #0f172a;
        line-height: 1.1;
    }
    .metric-note {
        color: #64748b;
        font-size: 12.5px;
        margin-top: 6px;
        line-height: 1.4;
    }
    .good { color: var(--green) !important; }
    .bad { color: var(--red) !important; }
    .warn { color: var(--yellow) !important; }
    .blue { color: var(--blue) !important; }
    .report-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 28px rgba(15, 23, 42, .04);
        margin-bottom: 14px;
        min-height: 170px;
    }
    .report-title {
        font-size: 16px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 6px;
    }
    .report-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 850;
        margin-bottom: 10px;
    }
    .badge-good { background: var(--green-bg); color: var(--green); }
    .badge-bad { background: var(--red-bg); color: var(--red); }
    .badge-warn { background: var(--yellow-bg); color: #b45309; }
    .badge-blue { background: var(--blue-bg); color: var(--blue); }
    .report-text {
        color: #475569;
        font-size: 13.5px;
        line-height: 1.62;
    }
    .bar-wrap {
        margin: 10px 0 14px 0;
    }
    .bar-line {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        color: #334155;
        font-size: 13px;
        font-weight: 760;
        margin-bottom: 6px;
    }
    .bar-bg {
        width: 100%;
        height: 13px;
        border-radius: 999px;
        background: #eef2f7;
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 999px;
    }
    .notice {
        padding: 13px 15px;
        border-radius: 16px;
        border: 1px solid var(--border);
        background: #f8fafc;
        color: #334155;
        font-size: 13.7px;
        line-height: 1.55;
        margin: 7px 0;
    }
    .notice-good {
        background: var(--green-bg);
        border-color: rgba(0,166,96,.25);
        color: #065f46;
    }
    .notice-warn {
        background: var(--yellow-bg);
        border-color: rgba(245,158,11,.28);
        color: #7c4a03;
    }
    .notice-bad {
        background: var(--red-bg);
        border-color: rgba(226,59,59,.28);
        color: #991b1b;
    }
    code {
        color: #111827 !important;
        background: #f8fafc !important;
        border: 1px solid #e5e7eb !important;
        white-space: pre-wrap !important;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "trade_log" not in st.session_state:
    st.session_state.trade_log = []
if "market_board" not in st.session_state:
    st.session_state.market_board = []
if "last_entry_result" not in st.session_state:
    st.session_state.last_entry_result = None
if "last_position_result" not in st.session_state:
    st.session_state.last_position_result = None


def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def cents(value):
    return f"{value:.1f}¢"


def score_color(score):
    if score >= 72:
        return "#00a660"
    if score >= 50:
        return "#f59e0b"
    return "#e23b3b"


def badge_class(level):
    if level == "good":
        return "badge-good"
    if level == "bad":
        return "badge-bad"
    if level == "warn":
        return "badge-warn"
    return "badge-blue"


def bar_html(label, value, max_value=100, color="#00a660", suffix=""):
    safe = clamp(value, 0, max_value)
    width = 0 if max_value <= 0 else (safe / max_value) * 100
    return f"""
    <div class="bar-wrap">
        <div class="bar-line"><span>{label}</span><span>{value:.1f}{suffix}</span></div>
        <div class="bar-bg"><div class="bar-fill" style="width:{width:.1f}%; background:{color};"></div></div>
    </div>
    """


def metric_card(label, value, note="", cls=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {cls}">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """


def report_card(title, badge, badge_level, body):
    return f"""
    <div class="report-card">
        <div class="report-title">{title}</div>
        <span class="report-badge {badge_class(badge_level)}">{badge}</span>
        <div class="report-text">{body}</div>
    </div>
    """


def price_zone(price):
    if price >= 99:
        return ("99¢ 매수 금지", "bad", -30, "99¢는 사는 가격이 아니라 파는 가격에 가깝습니다.")
    if price >= 95:
        return ("상환 스캘핑", "bad", -24, "95~98¢는 거의 상환 스캘핑입니다. 고액 신규 매수 금지에 가깝습니다.")
    if price >= 90:
        return ("신규매수 비추천", "bad", -18, "90~95¢는 신규 매수 비추천 구간입니다.")
    if price >= 85:
        return ("매우 신중", "warn", -10, "85~90¢는 신규 진입을 매우 신중하게 봐야 합니다.")
    if price >= 80:
        return ("익절 고려", "warn", -6, "80~85¢는 신규 매수보다 익절 고려 구간입니다.")
    if 2 <= price <= 5:
        return ("초저가 bounce", "warn", -12, "2~5¢ Bounce Trade는 소액 전용입니다.")
    if price < 2:
        return ("복권형", "bad", -18, "2¢ 미만은 거의 복권형 가격입니다.")
    if price <= 20:
        return ("고변동", "warn", -4, "저가 구간은 변동성이 큽니다. 소액만 적합합니다.")
    return ("정상 구간", "good", 0, "가격 구간 자체는 과도한 위험 신호가 크지 않습니다.")


def purpose_rule(purpose):
    rules = {
        "경기승리 / 만기 보유": (1.00, 0, "실제 승률 추정이 핵심인 기본 승리 베팅입니다."),
        "경기 시작 전 가격 상승 노림": (0.70, -6, "시장 심리와 타이밍을 노리는 거래입니다. 익절 기준이 더 중요합니다."),
        "반반 경기 강팀 쏠림 이용 / 중간 익절": (0.60, -8, "승리보다 시장 쏠림을 이용하는 구조입니다. 오래 들고 가면 위험합니다."),
        "역배 / Bounce Trade": (0.35, -13, "역배/bounce는 소액 전용입니다. 맞히는 것보다 손실 제한이 핵심입니다."),
        "99¢ 상환 스캘핑": (0.20, -25, "작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."),
        "뉴스/이벤트 선반영": (0.50, -12, "조건문, resolution 기준, 뉴스 해석 오류를 반드시 확인해야 합니다."),
    }
    return rules.get(purpose, (1.00, 0, "일반 베팅으로 계산합니다."))


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
    return rules.get(market_type, (1.00, 0, "일반 시장으로 계산합니다."))


def position_size_rule(position_pct):
    if position_pct >= 50:
        return ("시스템 실패", "bad", -100, "계좌 생존 리스크입니다. 50% 이상 노출은 절대 금지에 가깝습니다.")
    if position_pct >= 20:
        return ("진입 금지", "bad", -85, "20% 이상은 진입 금지급 노출입니다.")
    if position_pct >= 10:
        return ("매우 위험", "bad", -38, "10~20%는 매우 큰 포지션입니다. 일부 축소가 우선입니다.")
    if position_pct >= 5:
        return ("위험", "warn", -20, "5~10%는 위험 구간입니다. 확신보다 손실 가능액을 먼저 봐야 합니다.")
    if position_pct >= 3:
        return ("주의", "warn", -8, "3~5%는 주의 구간입니다.")
    return ("정상", "good", 5, "0~3%는 포지션 크기상 정상 범위입니다.")


def exposure_rule(exposure_pct):
    if exposure_pct >= 20:
        return ("중복 노출 금지", "bad", -60, "같은 경기/방향 총 노출이 20% 이상입니다.")
    if exposure_pct >= 10:
        return ("중복 노출 위험", "bad", -35, "같은 경기/방향 총 노출이 10~20%입니다.")
    if exposure_pct >= 5:
        return ("중복 노출 주의", "warn", -12, "같은 경기/방향 총 노출이 5~10%입니다.")
    return ("정상", "good", 0, "중복 노출은 관리 가능한 범위입니다.")


def confidence_cap(confidence):
    return {
        "관찰용": 15,
        "낮은 확신": 25,
        "중간 확신": 50,
        "높은 확신": 70,
        "초고확신": 70,
    }.get(confidence, 50)


def portfolio_cap(bankroll, confidence):
    pct_map = {
        "관찰용": 0.01,
        "낮은 확신": 0.02,
        "중간 확신": 0.04,
        "높은 확신": 0.06,
        "초고확신": 0.08,
    }
    return bankroll * pct_map.get(confidence, 0.04)


def calculate_entry_result(
    market_name,
    current_price,
    fair_price,
    stake,
    purpose,
    market_type,
    bankroll,
    emotional_limit,
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

    zone_label, zone_level, zone_penalty, zone_note = price_zone(current_price)
    purpose_mult, purpose_penalty, purpose_note = purpose_rule(purpose)
    type_mult, type_penalty, type_note = market_type_rule(market_type)
    size_label, size_level, size_penalty, size_note = position_size_rule(position_pct)

    base_cap = min(confidence_cap(confidence), portfolio_cap(bankroll, confidence), emotional_limit)
    recommended_cap = base_cap * purpose_mult * type_mult
    if fomo_count >= 1:
        recommended_cap *= 0.5

    cap_status = "추천 상한선 이내"
    cap_level = "good"
    cap_penalty = 0
    if stake >= 200:
        cap_status, cap_level, cap_penalty = "$200 이상 시스템 실패", "bad", -90
    elif stake >= 100:
        cap_status, cap_level, cap_penalty = "$100 이상 강한 경고", "bad", -50
    elif stake > recommended_cap * 1.2:
        cap_status, cap_level, cap_penalty = "추천 상한선 초과", "bad", -32
    elif stake > recommended_cap:
        cap_status, cap_level, cap_penalty = "상한선 근처/소폭 초과", "warn", -12

    duplicate_total = duplicate_ml + duplicate_game + duplicate_same_side + stake
    duplicate_pct = (duplicate_total / bankroll) * 100 if bankroll > 0 else 0
    exposure_label, exposure_level, exposure_penalty, exposure_note = exposure_rule(duplicate_pct)

    fomo_penalty = 0
    fomo_status = "정상"
    fomo_level = "good"
    fomo_note = "감정 체크가 없습니다."
    if fomo_count >= 3:
        fomo_status, fomo_level, fomo_penalty = "감정 진입 금지", "bad", -75
        fomo_note = "감정 체크 3개 이상입니다. 신규 진입 금지로 봐야 합니다."
    elif fomo_count >= 1:
        fomo_status, fomo_level, fomo_penalty = "감정 위험", "warn", -20
        fomo_note = "감정 체크가 있습니다. 추천 금액을 50% 줄였습니다."

    chase_gap = 0
    chase_label = "미입력"
    chase_level = "blue"
    chase_note = "처음 봤던 저평가 가격을 입력하지 않았습니다."
    chase_penalty = 0
    if previous_good_price > 0:
        chase_gap = current_price - previous_good_price
        if chase_gap >= 30:
            chase_label, chase_level, chase_penalty = "FOMO 추격", "bad", -25
            chase_note = "처음 봤던 가격보다 30¢ 이상 올랐습니다. 추격매수 위험이 큽니다."
        elif chase_gap >= 15:
            chase_label, chase_level, chase_penalty = "추격 위험", "warn", -13
            chase_note = "처음 봤던 가격보다 많이 올라 진입가 매력이 줄었습니다."
        elif chase_gap >= 5:
            chase_label, chase_level, chase_penalty = "조금 상승", "warn", -5
            chase_note = "처음 봤던 가격보다 조금 올랐습니다."
        else:
            chase_label, chase_level, chase_penalty = "추격 아님", "good", 5
            chase_note = "처음 봤던 가격 대비 추격 위험은 크지 않습니다."

    my_vs_poly = fair_price - current_price
    book_vs_poly = bookmaker_prob - current_price if bookmaker_prob > 0 else 0
    my_vs_book = fair_price - bookmaker_prob if bookmaker_prob > 0 else 0
    book_label, book_level, book_penalty = "북메이커 미입력", "blue", 0
    book_note = "북메이커 기준 승률을 입력하면 공식 배당/외부 시장과의 괴리를 같이 볼 수 있습니다."
    if bookmaker_prob > 0:
        if my_vs_book >= 10:
            book_label, book_level, book_penalty = "과신 재검토", "bad", -12
            book_note = "내 적정가가 북메이커보다 10%p 이상 높습니다. 과신 가능성을 재검토하세요."
        elif book_vs_poly >= 5:
            book_label, book_level, book_penalty = "외부배당도 저평가", "good", 6
            book_note = "북메이커 기준으로도 Polymarket 가격이 싸 보입니다."
        elif book_vs_poly <= -5:
            book_label, book_level, book_penalty = "외부배당 기준 비쌈", "warn", -8
            book_note = "북메이커 기준으로는 Polymarket 가격이 비싼 편입니다."
        else:
            book_label, book_level, book_penalty = "큰 차이 없음", "blue", 0
            book_note = "북메이커와 Polymarket 가격 차이가 크지 않습니다."

    value_score = clamp(50 + edge * 2.2 + zone_penalty + purpose_penalty + type_penalty + chase_penalty + book_penalty)
    final_score = clamp(value_score + size_penalty + exposure_penalty + fomo_penalty + cap_penalty)

    hard_stop = None
    if position_pct >= 50:
        hard_stop = "시스템 실패 — 계좌 생존 리스크"
    elif stake >= 200:
        hard_stop = "$200 이상 — 시스템 실패"
    elif position_pct >= 20:
        hard_stop = "진입 금지 — 포트폴리오 20% 이상"
    elif duplicate_pct >= 20:
        hard_stop = "진입 금지 — 중복 노출 20% 이상"
    elif fomo_count >= 3:
        hard_stop = "진입 금지 — 감정 배팅 위험"

    if hard_stop:
        decision, decision_level = hard_stop, "bad"
    elif final_score >= 75:
        decision, decision_level = "진입 적절", "good"
    elif final_score >= 60:
        decision, decision_level = "소액 진입 가능", "warn"
    elif final_score >= 45:
        decision, decision_level = "관망 우선", "warn"
    else:
        decision, decision_level = "진입 부적절", "bad"

    shares = stake / (current_price / 100)
    win_payout = shares
    win_profit = win_payout - stake
    lose_loss = stake

    target_amount = shares * (target_price / 100)
    target_profit = target_amount - stake
    stop_amount = shares * (stop_price / 100)
    stop_loss = stake - stop_amount
    rr = target_profit / stop_loss if stop_loss > 0 else 0

    if target_profit > 0 and stop_loss > 0:
        if stop_loss > target_profit:
            rr_text = f"목표가까지 얻을 수 있는 금액보다 손절 시 잃을 수 있는 금액이 약 {stop_loss / target_profit:.1f}배 큽니다."
            rr_level = "bad"
        elif target_profit >= stop_loss * 1.5:
            rr_text = f"목표가 수익이 손절 손실보다 약 {target_profit / stop_loss:.1f}배 큽니다."
            rr_level = "good"
        else:
            rr_text = f"목표 수익과 손절 손실의 차이가 크지 않습니다. 손익비 {rr:.2f}:1 입니다."
            rr_level = "warn"
    else:
        rr_text = "목표가 또는 손절가 설정을 다시 확인하세요."
        rr_level = "warn"

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
        reasons.append(("good", f"가격 메리트 좋음: 내 적정가가 현재가보다 {edge:.1f}¢ 높습니다."))
    elif edge >= 5:
        reasons.append(("warn", f"가격 메리트 약간 있음: edge {edge:.1f}¢입니다."))
    elif edge < 0:
        reasons.append(("bad", f"가격 메리트 없음: 현재가가 내 적정가보다 {abs(edge):.1f}¢ 비쌉니다."))
    else:
        reasons.append(("warn", f"가격 메리트 작음: edge {edge:.1f}¢입니다."))

    reasons.append((size_level, f"포지션 크기: 총자산의 {position_pct:.1f}% — {size_label}"))
    reasons.append((cap_level, f"추천 상한선: {money(recommended_cap)} / 현재 투자금 {money(stake)} — {cap_status}"))
    reasons.append((zone_level, f"진입가격 구간: {zone_label} — {zone_note}"))

    warnings = []
    for level, text in reasons:
        if level in ["bad", "warn"]:
            warnings.append((level, text))
    if bookmaker_prob > 0 and my_vs_book >= 10:
        warnings.append(("bad", book_note))
    if fomo_count > 0:
        warnings.append((fomo_level, fomo_note))
    if duplicate_pct >= 5:
        warnings.append((exposure_level, exposure_note))
    if high_price_warning:
        warnings.append(("bad", high_price_warning))
    if not warnings:
        warnings.append(("good", "큰 위험 신호는 없지만, 손절/익절 기준은 반드시 정해야 합니다."))

    return {
        "market_name": market_name,
        "current_price": current_price,
        "fair_price": fair_price,
        "stake": stake,
        "purpose": purpose,
        "market_type": market_type,
        "bankroll": bankroll,
        "confidence": confidence,
        "edge": edge,
        "position_pct": position_pct,
        "recommended_cap": recommended_cap,
        "value_score": round(value_score, 1),
        "final_score": round(final_score, 1),
        "decision": decision,
        "decision_level": decision_level,
        "shares": shares,
        "win_payout": win_payout,
        "win_profit": win_profit,
        "lose_loss": lose_loss,
        "target_price": target_price,
        "stop_price": stop_price,
        "target_profit": target_profit,
        "stop_loss": stop_loss,
        "rr": rr,
        "rr_text": rr_text,
        "rr_level": rr_level,
        "current_value": current_value,
        "redeem_value": redeem_value,
        "additional_to_100": additional_to_100,
        "fail_loss": fail_loss,
        "high_price_warning": high_price_warning,
        "bookmaker_prob": bookmaker_prob,
        "my_vs_poly": my_vs_poly,
        "book_vs_poly": book_vs_poly,
        "my_vs_book": my_vs_book,
        "book_label": book_label,
        "book_level": book_level,
        "book_note": book_note,
        "zone_label": zone_label,
        "zone_level": zone_level,
        "zone_note": zone_note,
        "size_label": size_label,
        "size_level": size_level,
        "size_note": size_note,
        "cap_status": cap_status,
        "cap_level": cap_level,
        "purpose_note": purpose_note,
        "type_note": type_note,
        "duplicate_total": duplicate_total,
        "duplicate_pct": duplicate_pct,
        "exposure_label": exposure_label,
        "exposure_level": exposure_level,
        "exposure_note": exposure_note,
        "fomo_count": fomo_count,
        "fomo_status": fomo_status,
        "fomo_level": fomo_level,
        "fomo_note": fomo_note,
        "chase_gap": chase_gap,
        "chase_label": chase_label,
        "chase_level": chase_level,
        "chase_note": chase_note,
        "reasons": reasons,
        "warnings": warnings[:6],
    }


def render_entry_result(result):
    if result is None:
        st.markdown(
            """
            <div class="panel-soft">
                <div class="section-title">🔎 아직 판독 결과가 없습니다</div>
                <div class="muted">
                    아래 빠른 입력값을 넣고 <b>판독하기</b>를 누르면 이 자리에 결론 + 상세 리포트가 함께 표시됩니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    level = result["decision_level"]
    klass = "result-good" if level == "good" else "result-mid" if level == "warn" else "result-bad"
    icon = "✅" if level == "good" else "⚠️" if level == "warn" else "⛔"
    score = result["final_score"]
    value_score = result["value_score"]
    score_text = f"적절성 {score:.1f}%" if level != "bad" else f"부적절도 {100 - score:.1f}%"

    st.markdown(
        f"""
        <div class="result-card {klass}">
            <div class="result-title">{icon} {result['decision']}</div>
            <div class="result-sub">
                <b>{result['market_name']}</b><br>
                리스크 포함 최종 판정: <b>{score_text}</b>
                &nbsp; | &nbsp;
                배팅 규모 제외 순수 가치: <b>{value_score:.1f}%</b>
                &nbsp; | &nbsp;
                목적: <b>{result['purpose']}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("현재가 / implied", cents(result["current_price"]), "시장 가격 = implied probability"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("내 적정가", cents(result["fair_price"]), "내가 보는 실제 적정 확률"), unsafe_allow_html=True)
    with c3:
        edge_cls = "good" if result["edge"] >= 5 else "bad" if result["edge"] < 0 else "warn"
        st.markdown(metric_card("Edge", f"{result['edge']:+.1f}¢", "내 적정가 - 현재가", edge_cls), unsafe_allow_html=True)
    with c4:
        pos_cls = "bad" if result["position_pct"] >= 10 else "warn" if result["position_pct"] >= 3 else "good"
        st.markdown(metric_card("포트폴리오 비중", f"{result['position_pct']:.1f}%", result["size_label"], pos_cls), unsafe_allow_html=True)

    st.markdown(
        "<div class='panel'><div class='section-title'>한눈에 보는 점수</div>"
        + bar_html("리스크 포함 최종 적절성", result["final_score"], 100, score_color(result["final_score"]), "%")
        + bar_html("배팅 규모 제외 순수 가치", result["value_score"], 100, "#2563eb", "%")
        + bar_html("포트폴리오 사용 비중", min(result["position_pct"], 100), 100, "#f59e0b" if result["position_pct"] < 20 else "#e23b3b", "%")
        + bar_html("현재가 vs 100¢ 위치", result["current_price"], 100, "#64748b", "¢")
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown("<div class='section-title'>핵심 이유</div>", unsafe_allow_html=True)
        for level, text in result["reasons"]:
            cls = "notice-good" if level == "good" else "notice-bad" if level == "bad" else "notice-warn"
            st.markdown(f"<div class='notice {cls}'>{text}</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>핵심 경고</div>", unsafe_allow_html=True)
        for level, text in result["warnings"]:
            cls = "notice-good" if level == "good" else "notice-bad" if level == "bad" else "notice-warn"
            st.markdown(f"<div class='notice {cls}'>{text}</div>", unsafe_allow_html=True)

    st.markdown("### 상세 판독 리포트")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(report_card("1. 진입가격 평가", result["zone_label"], result["zone_level"], f"현재가 <b>{cents(result['current_price'])}</b><br>{result['zone_note']}"), unsafe_allow_html=True)
        st.markdown(report_card("2. 배팅금액 / 계좌 생존", result["size_label"], result["size_level"], f"투자금 <b>{money(result['stake'])}</b> / 총자산 <b>{money(result['bankroll'])}</b><br>포트폴리오 비중 <b>{result['position_pct']:.1f}%</b><br>{result['size_note']}"), unsafe_allow_html=True)
        st.markdown(report_card("3. 북메이커 / 공식 배당 비교", result["book_label"], result["book_level"], f"내 적정가 - 현재가: <b>{result['my_vs_poly']:+.1f}%p</b><br>북메이커 - 현재가: <b>{result['book_vs_poly']:+.1f}%p</b><br>내 적정가 - 북메이커: <b>{result['my_vs_book']:+.1f}%p</b><br>{result['book_note']}"), unsafe_allow_html=True)
        st.markdown(report_card("4. 감정 / FOMO 평가", result["fomo_status"], result["fomo_level"], f"선택된 감정 체크: <b>{result['fomo_count']}개</b><br>{result['fomo_note']}"), unsafe_allow_html=True)
    with r2:
        st.markdown(report_card("5. 추천 상한선 평가", result["cap_status"], result["cap_level"], f"추천 상한선: <b>{money(result['recommended_cap'])}</b><br>현재 투자금: <b>{money(result['stake'])}</b><br>확신 수준: <b>{result['confidence']}</b>"), unsafe_allow_html=True)
        st.markdown(report_card("6. 손익비 / 목표가·손절가", f"손익비 {result['rr']:.2f}:1", result["rr_level"], f"목표가 {cents(result['target_price'])} 도달 시 예상 수익: <b>{money(result['target_profit'])}</b><br>손절가 {cents(result['stop_price'])} 도달 시 예상 손실: <b>{money(result['stop_loss'])}</b><br>{result['rr_text']}"), unsafe_allow_html=True)
        st.markdown(report_card("7. 중복 노출 평가", result["exposure_label"], result["exposure_level"], f"같은 경기/같은 방향 총 노출: <b>{money(result['duplicate_total'])}</b><br>총자산 대비: <b>{result['duplicate_pct']:.1f}%</b><br>{result['exposure_note']}"), unsafe_allow_html=True)
        st.markdown(report_card("8. 배팅 목적 / 시장 유형", "구조 리스크", "blue", f"배팅 목적: <b>{result['purpose']}</b><br>{result['purpose_note']}<br><br>시장 유형: <b>{result['market_type']}</b><br>{result['type_note']}"), unsafe_allow_html=True)

    st.markdown("### 수익/손실 시나리오")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(metric_card("보유 수량", f"{result['shares']:.2f}주", "투자금 / 현재가"), unsafe_allow_html=True)
    with s2:
        st.markdown(metric_card("승리 시 순이익", money(result["win_profit"]), "100¢ 상환 기준", "good"), unsafe_allow_html=True)
    with s3:
        st.markdown(metric_card("패배 시 손실", money(-result["lose_loss"]), "전액 손실 가정", "bad"), unsafe_allow_html=True)
    with s4:
        st.markdown(metric_card("100¢까지 추가수익", money(result["additional_to_100"]), "현재가 기준 남은 업사이드", "blue"), unsafe_allow_html=True)

    if result["high_price_warning"]:
        st.markdown(f"<div class='notice notice-bad'>{result['high_price_warning']}</div>", unsafe_allow_html=True)

    summary = (
        f"{result['market_name']}\n"
        f"현재가: {result['current_price']:.1f}¢ / 내 적정가: {result['fair_price']:.1f}¢ / "
        f"Edge: {result['edge']:+.1f}¢ / 투자금: ${result['stake']:.2f} / "
        f"포트폴리오 비중: {result['position_pct']:.1f}% / "
        f"북메이커: {result['bookmaker_prob']:.1f}% / "
        f"판정: {result['decision']} / "
        f"리스크 포함: {result['final_score']:.1f}% / 규모 제외 가치: {result['value_score']:.1f}%"
    )
    st.markdown("### 기록용 요약")
    st.code(summary)


def evaluate_position(current_price, avg_buy, shares, investment, target_price, stop_price, bankroll, fomo_count):
    current_value = shares * (current_price / 100)
    pnl = current_value - investment
    roi = (pnl / investment) * 100 if investment > 0 else 0
    redeem_total = shares
    additional_profit = redeem_total - current_value
    fail_loss = current_value
    position_pct = (current_value / bankroll) * 100 if bankroll > 0 else 0

    reasons = []
    warnings = []

    if current_price >= target_price:
        decision = "목표가 도달 — 매도/부분매도 고려"
        level = "warn"
        reasons.append("목표가에 도달했습니다. 최소 일부 익절을 검토할 구간입니다.")
    elif current_price <= stop_price and current_value >= investment * 0.3:
        decision = "손절 고려"
        level = "bad"
        reasons.append("손절가 이하이고 회수 가능한 금액이 아직 남아 있습니다.")
    elif current_value <= investment * 0.1:
        decision = "손절 효용 낮음 — 추가매수 금지"
        level = "bad"
        reasons.append("현재 평가금이 원금의 10% 이하입니다. 옵션처럼 보유는 가능하지만 추가매수는 금지입니다.")
    else:
        decision = "홀딩 가능"
        level = "good"
        reasons.append("목표가와 손절가 사이에 있으며 기본 조건상 홀딩은 가능합니다.")

    if roi >= 30:
        warnings.append("현재 수익률이 +30% 이상입니다. 원금 회수 또는 부분매도 검토가 필요합니다.")
        if level == "good":
            decision, level = "홀딩 가능, 단 부분매도 검토", "warn"
    if position_pct >= 20:
        warnings.append("포트폴리오 비중 20% 이상입니다. 진입 금지급 노출 — 즉시 축소 고려.")
        decision, level = "진입 금지급 노출 — 즉시 축소 고려", "bad"
    elif position_pct >= 10:
        warnings.append("포트폴리오 비중 10% 이상입니다. 포지션 크기 과대 — 일부 축소 권장.")
        if level != "bad":
            decision, level = "홀딩 가능, 단 포지션 크기 과대", "warn"
    if fomo_count >= 3:
        warnings.append("감정 체크 3개 이상입니다. 신규 추가매수 금지, 축소 우선.")
        decision, level = "감정 리스크 과대 — 추가매수 금지", "bad"
    elif fomo_count >= 1:
        warnings.append("감정 체크가 있습니다. 판단이 흔들릴 수 있으므로 부분매도 우선 검토.")

    zone_label, zone_level, _, zone_note = price_zone(current_price)
    if current_price >= 80:
        warnings.append(zone_note)
    if current_price >= 97:
        warnings.append("97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다.")
    if not warnings:
        warnings.append("현재 큰 위험 신호는 없지만 목표가/손절가 기준은 유지해야 합니다.")

    return {
        "decision": decision,
        "level": level,
        "current_value": current_value,
        "pnl": pnl,
        "roi": roi,
        "redeem_total": redeem_total,
        "additional_profit": additional_profit,
        "fail_loss": fail_loss,
        "position_pct": position_pct,
        "reasons": reasons,
        "warnings": warnings[:5],
        "zone_label": zone_label,
        "zone_level": zone_level,
        "zone_note": zone_note,
    }


def render_position_result(result, name):
    if result is None:
        st.info("현재가와 포지션 정보를 입력하고 판독 버튼을 누르면 결과가 표시됩니다.")
        return

    level = result["level"]
    klass = "result-good" if level == "good" else "result-mid" if level == "warn" else "result-bad"
    icon = "✅" if level == "good" else "⚠️" if level == "warn" else "⛔"

    st.markdown(
        f"""
        <div class="result-card {klass}">
            <div class="result-title">{icon} {result['decision']}</div>
            <div class="result-sub"><b>{name}</b><br>현재 포지션 기준 매도/홀딩 판단 결과입니다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    metrics = [
        ("현재 평가금", money(result["current_value"]), "현재가 × 보유수량", ""),
        ("즉시 매도 손익", money(result["pnl"]), f"ROI {result['roi']:+.1f}%", "good" if result["pnl"] >= 0 else "bad"),
        ("100¢ 상환 총액", money(result["redeem_total"]), "승리 시 총액", "blue"),
        ("실패 시 손실", money(-result["fail_loss"]), "현재 평가금 손실", "bad"),
    ]
    for col, (label, value, note, cls) in zip(cols, metrics):
        with col:
            st.markdown(metric_card(label, value, note, cls), unsafe_allow_html=True)

    st.markdown(
        "<div class='panel'><div class='section-title'>포지션 위험 시각화</div>"
        + bar_html("현재 수익률", max(result["roi"], 0), 100, "#00a660" if result["roi"] >= 0 else "#e23b3b", "%")
        + bar_html("포트폴리오 비중", min(result["position_pct"], 100), 100, "#f59e0b" if result["position_pct"] < 20 else "#e23b3b", "%")
        + bar_html("100¢까지 남은 추가수익", min(result["additional_profit"] / max(result["redeem_total"], 1) * 100, 100), 100, "#2563eb", "%")
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### 이유")
        for x in result["reasons"]:
            st.markdown(f"<div class='notice notice-good'>{x}</div>", unsafe_allow_html=True)
    with right:
        st.markdown("#### 경고")
        for x in result["warnings"]:
            cls = "notice-bad" if ("금지" in x or "위험" in x or "고액" in x) else "notice-warn"
            st.markdown(f"<div class='notice {cls}'>{x}</div>", unsafe_allow_html=True)

    rows = []
    shares_est = result["redeem_total"]
    current_price_est = (result["current_value"] / shares_est * 100) if shares_est > 0 else 0
    for ratio in [25, 50, 70, 80, 90, 100]:
        sell_shares = shares_est * ratio / 100
        recovered = sell_shares * (current_price_est / 100)
        remaining_shares = shares_est - sell_shares
        remaining_value = remaining_shares * (current_price_est / 100)
        additional = remaining_shares * (1 - current_price_est / 100)
        rows.append({
            "매도 비율": f"{ratio}%",
            "매도 수량": round(sell_shares, 2),
            "회수금": money(recovered),
            "남은 수량": round(remaining_shares, 2),
            "남은 평가금": money(remaining_value),
            "100¢ 추가수익": money(additional),
        })
    st.markdown("#### 부분매도 시나리오")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def extract_slug(url):
    parsed = urlparse(url.strip())
    path = parsed.path.strip("/")
    if not path:
        return ""
    return path.split("/")[-1]


def parse_jsonish_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []
    return []


@st.cache_data(ttl=60)
def fetch_polymarket_event(slug):
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    response = requests.get(url, timeout=12)
    response.raise_for_status()
    return response.json()


def flatten_event_markets(payload):
    events = payload if isinstance(payload, list) else payload.get("events", [])
    rows = []
    for event in events:
        markets = event.get("markets", [])
        for m in markets:
            question = m.get("question") or m.get("title") or m.get("slug", "Unknown market")
            outcomes = parse_jsonish_list(m.get("outcomes"))
            prices = parse_jsonish_list(m.get("outcomePrices"))
            tokens = parse_jsonish_list(m.get("clobTokenIds"))
            for idx, outcome in enumerate(outcomes):
                rows.append({
                    "market": question,
                    "outcome": outcome,
                    "price": float(prices[idx]) if idx < len(prices) else None,
                    "token_id": tokens[idx] if idx < len(tokens) else "",
                })
    return rows


st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Memento</div>
        <div class="hero-subtitle">
            Polymarket 배팅 가치 판독기 + 거래 손익 기록장<br>
            <b>입력은 빠르게, 결과는 리포트처럼 자세하게.</b> 자동매매가 아니라 계좌 생존을 위한 수동 판단 도구입니다.
        </div>
        <span class="pill">Entry Evaluator</span>
        <span class="pill">Position Monitor</span>
        <span class="pill">Risk-first</span>
        <span class="pill">Manual Trading</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_entry, tab_position, tab_partial, tab_log, tab_url = st.tabs(
    ["🏠 진입 판독", "📍 포지션 관리", "🧩 부분매도", "📈 거래일지/성과", "🔎 URL 도우미"]
)

with tab_entry:
    st.subheader("🏠 빠른 진입 판독")
    st.caption("기본 입력은 최소화하고, 결과는 결론 + 리스크 + 공식배당 + 손익비까지 상세 리포트로 보여줍니다.")

    render_entry_result(st.session_state.last_entry_result)

    st.markdown(
        """
        <div class="panel-soft">
            <div class="section-title">빠른 입력</div>
            <div class="muted">시장명, 현재가, 내 적정가, 투자금, 배팅 목적만 빠르게 입력하세요. 나머지는 고급설정에 숨겨져 있습니다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("entry_form"):
        market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner")
        a, b, c = st.columns(3)
        with a:
            current_price = st.number_input("현재가 / 진입가격(센트)", min_value=1.0, max_value=99.0, value=52.0)
        with b:
            fair_price = st.number_input("내가 생각하는 적정 가격(센트)", min_value=1.0, max_value=99.0, value=63.0)
        with c:
            stake = st.number_input("진입 크기 / 투자금($)", min_value=1.0, value=50.0)

        d, e = st.columns(2)
        with d:
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
        with e:
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
            st.caption("상세 리스크 계산에 쓰이는 값입니다. 비워도 기본값으로 계산됩니다.")

            g1, g2, g3 = st.columns(3)
            with g1:
                bankroll = st.number_input("전체 포트폴리오 / 총자산($)", min_value=1.0, value=814.0)
            with g2:
                emotional_limit = st.number_input("감정적으로 감당 가능한 1회 금액($)", min_value=1.0, value=50.0)
            with g3:
                confidence = st.selectbox("확신 수준", ["관찰용", "낮은 확신", "중간 확신", "높은 확신", "초고확신"], index=2)

            g4, g5, g6 = st.columns(3)
            with g4:
                target_price = st.number_input("목표가(센트)", min_value=1.0, max_value=100.0, value=75.0)
            with g5:
                stop_price = st.number_input("손절가(센트)", min_value=0.0, max_value=99.0, value=42.0)
            with g6:
                bookmaker_prob = st.number_input("북메이커/공식배당 기준 승률(%)", min_value=0.0, max_value=99.0, value=0.0)

            previous_good_price = st.number_input("처음 봤던 저평가 가격(선택)", min_value=0.0, max_value=99.0, value=0.0)

            st.markdown("##### 중복 노출")
            x1, x2, x3 = st.columns(3)
            with x1:
                duplicate_ml = st.number_input("기존 같은 경기 Moneyline 노출($)", min_value=0.0, value=0.0)
            with x2:
                duplicate_game = st.number_input("Game Winner 노출($)", min_value=0.0, value=0.0)
            with x3:
                duplicate_same_side = st.number_input("같은 팀/같은 방향 추가 노출($)", min_value=0.0, value=0.0)

            st.markdown("##### FOMO / 감정 상태")
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
                    if st.checkbox(option, key=f"entry_fomo_{idx}"):
                        fomo_count += 1

        submit_entry = st.form_submit_button("🔍 판독하기", use_container_width=True)

    if submit_entry:
        st.session_state.last_entry_result = calculate_entry_result(
            market_name=market_name,
            current_price=current_price,
            fair_price=fair_price,
            stake=stake,
            purpose=purpose,
            market_type=market_type,
            bankroll=bankroll,
            emotional_limit=emotional_limit,
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
        st.toast("판독 리포트가 상단에 생성되었습니다.", icon="📊")
        st.rerun()

with tab_position:
    st.subheader("📍 포지션 관리")
    st.caption("이미 들어간 포지션의 현재가를 수동 입력해서 매도/홀딩/부분매도 타이밍을 판단합니다.")

    render_position_result(st.session_state.last_position_result, "현재 포지션")

    with st.form("position_form"):
        p_name = st.text_input("거래 이름", "KT Rolster vs Dplus KIA — Match Winner")
        p1, p2, p3 = st.columns(3)
        with p1:
            avg_buy = st.number_input("평균 매수가(센트)", min_value=1.0, max_value=99.0, value=52.4)
        with p2:
            current_live = st.number_input("현재가 / best bid 기준(센트)", min_value=1.0, max_value=100.0, value=58.0)
        with p3:
            shares = st.number_input("보유 수량", min_value=0.01, value=1164.12)

        p4, p5, p6 = st.columns(3)
        with p4:
            investment = st.number_input("투자금($)", min_value=1.0, value=610.0)
        with p5:
            target = st.number_input("목표 매도가(센트)", min_value=1.0, max_value=100.0, value=60.0)
        with p6:
            stop = st.number_input("손절가(센트)", min_value=0.0, max_value=99.0, value=45.0)

        p7, p8 = st.columns(2)
        with p7:
            bankroll_p = st.number_input("전체 포트폴리오 금액($)", min_value=1.0, value=1200.0, key="pos_bankroll")
        with p8:
            fomo_p = st.slider("현재 감정 위험 체크 수", min_value=0, max_value=7, value=0)

        submit_pos = st.form_submit_button("📍 현재 포지션 판독하기", use_container_width=True)

    if submit_pos:
        st.session_state.last_position_result = evaluate_position(
            current_price=current_live,
            avg_buy=avg_buy,
            shares=shares,
            investment=investment,
            target_price=target,
            stop_price=stop,
            bankroll=bankroll_p,
            fomo_count=fomo_p,
        )
        st.toast("포지션 판독 결과가 상단에 생성되었습니다.", icon="📍")
        st.rerun()

with tab_partial:
    st.subheader("🧩 부분매도 계산기")
    st.caption("현재가에서 몇 %를 팔면 원금 회수/리스크 축소가 되는지 계산합니다.")

    pm_name = st.text_input("시장 이름", "Anyone's Legend vs Team WE — LPL Playoffs BO5", key="pm_name")
    a, b, c = st.columns(3)
    with a:
        pm_buy = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=16.0, key="pm_buy")
    with b:
        pm_current = st.number_input("현재가(센트)", min_value=1.0, max_value=100.0, value=73.0, key="pm_current")
    with c:
        pm_stake = st.number_input("투자금($)", min_value=1.0, value=16.08, key="pm_stake")

    manual = st.checkbox("보유 수량 직접 입력", key="pm_manual")
    if manual:
        pm_shares = st.number_input("보유 수량", min_value=0.0, value=100.0, key="pm_shares")
    else:
        pm_shares = pm_stake / (pm_buy / 100)

    if st.button("부분매도 표 만들기", use_container_width=True):
        needed_ratio = pm_stake / (pm_shares * (pm_current / 100)) if pm_shares > 0 and pm_current > 0 else 0
        needed_ratio_pct = min(needed_ratio * 100, 100)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(metric_card("보유 수량", f"{pm_shares:.2f}주", "자동 계산 또는 직접 입력"), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("현재 평가금", money(pm_shares * (pm_current / 100)), "현재가 기준"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("원금회수 최소비율", f"{needed_ratio_pct:.1f}%", "이 이상 팔면 원금 회수", "good"), unsafe_allow_html=True)

        rows = []
        for ratio in [25, 50, 70, 80, 90, 100]:
            sell_shares = pm_shares * ratio / 100
            recovered = sell_shares * (pm_current / 100)
            locked_profit = recovered - pm_stake
            remain = pm_shares - sell_shares
            remain_value = remain * (pm_current / 100)
            additional_100 = remain * (1 - pm_current / 100)
            rows.append({
                "매도 비율": f"{ratio}%",
                "매도 수량": round(sell_shares, 2),
                "회수금": money(recovered),
                "원금 대비 확정손익": money(locked_profit),
                "남은 수량": round(remain, 2),
                "남은 평가금": money(remain_value),
                "100¢ 추가수익": money(additional_100),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        current_value = pm_shares * (pm_current / 100)
        redeem_total = pm_shares
        additional = redeem_total - current_value
        st.warning(
            f"현재 평가금 {money(current_value)}에서 100¢까지 추가수익은 {money(additional)}입니다. "
            f"반대로 실패하면 현재 평가금 {money(current_value)}를 잃을 수 있습니다."
        )

with tab_log:
    st.subheader("📈 거래일지 / 전체 성과")

    a, b, c = st.columns(3)
    with a:
        start_bankroll = st.number_input("시작 자금($)", min_value=0.0, value=500.0, key="log_start")
    with b:
        current_bankroll = st.number_input("현재 총자산($)", min_value=0.0, value=650.0, key="log_current")
    with c:
        net_deposit = st.number_input("추가 입금 / 출금 조정($)", value=0.0, key="log_deposit")

    adjusted = start_bankroll + net_deposit
    total_profit = current_bankroll - adjusted
    total_roi = total_profit / adjusted * 100 if adjusted > 0 else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(metric_card("총손익", money(total_profit), "현재 총자산 - 조정 시작자금", "good" if total_profit >= 0 else "bad"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("총수익률", f"{total_roi:+.1f}%", "계좌 기준 ROI", "good" if total_roi >= 0 else "bad"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("현재 총자산", money(current_bankroll), "수동 입력 기준"), unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 거래 등록")
    with st.form("trade_log_form"):
        t1, t2, t3 = st.columns(3)
        with t1:
            log_name = st.text_input("거래 이름", "Example trade")
            log_buy = st.number_input("매수가(센트)", min_value=1.0, max_value=99.0, value=50.0)
        with t2:
            log_sell = st.number_input("매도가(센트)", min_value=0.0, max_value=100.0, value=70.0)
            log_stake = st.number_input("투자금($)", min_value=1.0, value=50.0)
        with t3:
            log_note = st.text_area("메모", "진입 이유 / 매도 이유 / 감정 상태")
        add_trade = st.form_submit_button("거래 기록 추가", use_container_width=True)

    if add_trade:
        shares_log = log_stake / (log_buy / 100)
        sell_amount = shares_log * (log_sell / 100)
        profit = sell_amount - log_stake
        roi = profit / log_stake * 100
        st.session_state.trade_log.append({
            "날짜": str(date.today()),
            "거래 이름": log_name,
            "매수가": f"{log_buy:.1f}¢",
            "매도가": f"{log_sell:.1f}¢",
            "투자금": log_stake,
            "실현손익": profit,
            "수익률": roi,
            "메모": log_note,
        })
        st.success("거래를 기록했습니다.")

    if st.session_state.trade_log:
        df = pd.DataFrame(st.session_state.trade_log)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV 다운로드", data=csv, file_name="memento_trade_log.csv", mime="text/csv")
    else:
        st.info("아직 기록된 거래가 없습니다.")

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

    if st.button("거래일지 초기화"):
        st.session_state.trade_log = []
        st.rerun()

with tab_url:
    st.subheader("🔎 Polymarket URL 도우미")
    st.caption("token_id를 직접 찾기 어려우니, URL을 넣으면 시장/선택지/token_id 후보를 표로 보여주는 보조 기능입니다. 아직 거래 자동화는 아닙니다.")

    poly_url = st.text_input("Polymarket 시장 URL", "https://polymarket.com/ko/esports/league-of-legends/emea-masters/lol-fn-vdn-2026-06-08")

    if st.button("URL에서 시장 후보 불러오기", use_container_width=True):
        slug = extract_slug(poly_url)
        if not slug:
            st.error("URL에서 slug를 찾지 못했습니다.")
        else:
            st.write(f"찾은 slug: `{slug}`")
            try:
                payload = fetch_polymarket_event(slug)
                rows = flatten_event_markets(payload)
                if not rows:
                    st.warning("시장 후보를 찾지 못했습니다. URL이 event/market 구조와 다를 수 있습니다.")
                else:
                    df = pd.DataFrame(rows)
                    if "price" in df.columns:
                        df["price_cent"] = (df["price"] * 100).round(2)
                    st.dataframe(df[["market", "outcome", "price_cent", "token_id"]], use_container_width=True, hide_index=True)
                    st.info("지금 단계에서는 token_id를 복사해서 쓰기보다, 어떤 시장/선택지가 어떤 ID인지 확인하는 용도로만 쓰는 걸 추천합니다.")
            except Exception as e:
                st.error(f"불러오기 실패: {e}")
