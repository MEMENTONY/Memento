
import json
import urllib.parse
import urllib.request
from datetime import date

import pandas as pd
import streamlit as st


# =====================================================
# Memento Grandmaster
# =====================================================
st.set_page_config(
    page_title="Memento Grandmaster",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================
# Premium light UI
# =====================================================
st.markdown(
    """
<style>
:root {
  --bg: #f5f7fb;
  --paper: #ffffff;
  --paper2: #f8fafc;
  --ink: #0f172a;
  --muted: #64748b;
  --line: #e2e8f0;
  --line2: #cbd5e1;
  --green: #00a76f;
  --green-bg: #e8fff5;
  --red: #ef4444;
  --red-bg: #fff1f2;
  --amber: #f59e0b;
  --amber-bg: #fffbeb;
  --blue: #2563eb;
  --blue-bg: #eff6ff;
  --violet: #7c3aed;
  --violet-bg: #f5f3ff;
  --black: #101828;
}

html, body, .stApp {
  background:
    radial-gradient(circle at 5% 0%, rgba(0,167,111,.10), transparent 26%),
    radial-gradient(circle at 100% 10%, rgba(37,99,235,.10), transparent 22%),
    linear-gradient(180deg, #ffffff 0%, #f5f7fb 45%, #f7f8fb 100%) !important;
  color: var(--ink) !important;
}

.block-container {
  max-width: 1360px;
  padding-top: 1.1rem;
  padding-bottom: 4rem;
}

h1,h2,h3,h4,h5,h6,p,span,div,label {
  color: var(--ink);
}

section[data-testid="stSidebar"] {
  background: #ffffff !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
  background: #ffffff !important;
  color: var(--ink) !important;
  border: 1px solid var(--line2) !important;
  border-radius: 14px !important;
  min-height: 42px;
  box-shadow: 0 1px 2px rgba(15,23,42,.04);
}

div[data-baseweb="select"] > div {
  background: #ffffff !important;
  color: var(--ink) !important;
  border: 1px solid var(--line2) !important;
  border-radius: 14px !important;
  min-height: 42px;
}

.stButton > button,
button[kind="primary"] {
  background: linear-gradient(135deg, #111827 0%, #020617 100%) !important;
  color: #ffffff !important;
  border: 0 !important;
  border-radius: 14px !important;
  font-weight: 800 !important;
  min-height: 44px;
  box-shadow: 0 10px 22px rgba(2,6,23,.18);
}

.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(2,6,23,.22);
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 8px;
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 6px;
  box-shadow: 0 10px 28px rgba(15,23,42,.06);
}

div[data-testid="stTabs"] [data-baseweb="tab"] {
  border-radius: 999px !important;
  color: var(--muted) !important;
  font-weight: 800 !important;
  padding: 7px 16px !important;
}

div[data-testid="stTabs"] [aria-selected="true"] {
  background: #0f172a !important;
  color: #ffffff !important;
}

div[data-testid="stTabs"] [aria-selected="true"] p {
  color: #ffffff !important;
}

div[data-testid="stMetric"] {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 8px 24px rgba(15,23,42,.055);
}

div[data-testid="stMetricLabel"] p {
  color: var(--muted) !important;
  font-size: 11px !important;
  font-weight: 900 !important;
  letter-spacing: .05em;
  text-transform: uppercase;
}

div[data-testid="stMetricValue"] {
  color: var(--ink) !important;
  font-weight: 950 !important;
}

.hero {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 10% 15%, rgba(0,167,111,.16), transparent 26%),
    radial-gradient(circle at 90% 10%, rgba(37,99,235,.16), transparent 25%),
    linear-gradient(135deg, #ffffff 0%, #f8fafc 48%, #eef6ff 100%);
  border: 1px solid var(--line);
  border-radius: 34px;
  padding: 30px;
  box-shadow: 0 24px 70px rgba(15,23,42,.09);
  margin-bottom: 18px;
}

.hero:after {
  content: "";
  position: absolute;
  right: -80px;
  top: -80px;
  width: 240px;
  height: 240px;
  border-radius: 999px;
  background: rgba(0,167,111,.09);
  border: 1px solid rgba(0,167,111,.14);
}

.brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.brand-title {
  font-size: 46px;
  line-height: .95;
  letter-spacing: -1.8px;
  font-weight: 1000;
  color: #020617;
}

.brand-sub {
  margin-top: 10px;
  color: #475569;
  line-height: 1.65;
  font-size: 15px;
}

.status-chip {
  display:inline-block;
  border-radius: 999px;
  padding: 7px 12px;
  background: #ffffff;
  border: 1px solid var(--line);
  color: #334155;
  font-size: 12px;
  font-weight: 850;
  margin-right: 6px;
  margin-top: 14px;
  box-shadow: 0 4px 14px rgba(15,23,42,.04);
}

.command-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 16px 0 20px 0;
}

.command-card {
  background: rgba(255,255,255,.82);
  backdrop-filter: blur(8px);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 16px;
  box-shadow: 0 12px 34px rgba(15,23,42,.055);
}

.command-label {
  color: var(--muted);
  font-size: 11px;
  text-transform: uppercase;
  font-weight: 900;
  letter-spacing: .06em;
}

.command-value {
  margin-top: 5px;
  color: #020617;
  font-size: 22px;
  font-weight: 1000;
  letter-spacing: -.5px;
}

.command-note {
  margin-top: 5px;
  color: #64748b;
  font-size: 12px;
  line-height: 1.4;
}

.card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 14px 42px rgba(15,23,42,.06);
  margin-bottom: 16px;
}

.card-soft {
  background: #f8fafc;
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 18px;
  margin-bottom: 14px;
}

.section-title {
  font-size: 19px;
  font-weight: 950;
  letter-spacing: -.25px;
  color: #0f172a;
  margin-bottom: 5px;
}

.muted {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.58;
}

.result {
  border-radius: 30px;
  padding: 24px;
  border: 1px solid var(--line);
  box-shadow: 0 22px 56px rgba(15,23,42,.08);
  margin: 10px 0 18px 0;
}

.result.good {
  background: linear-gradient(135deg, var(--green-bg) 0%, #ffffff 55%, #f8fafc 100%);
  border-color: rgba(0,167,111,.28);
}

.result.warn {
  background: linear-gradient(135deg, var(--amber-bg) 0%, #ffffff 55%, #f8fafc 100%);
  border-color: rgba(245,158,11,.30);
}

.result.bad {
  background: linear-gradient(135deg, var(--red-bg) 0%, #ffffff 55%, #f8fafc 100%);
  border-color: rgba(239,68,68,.30);
}

.result-top {
  display:flex;
  align-items:flex-start;
  justify-content: space-between;
  gap:18px;
}

.result-title {
  font-size: 32px;
  line-height: 1.15;
  letter-spacing: -.9px;
  font-weight: 1000;
  color: #020617;
}

.result-sub {
  margin-top: 7px;
  color: #475569;
  line-height: 1.62;
  font-size: 14px;
}

.score-badge {
  min-width: 130px;
  text-align:center;
  border-radius: 22px;
  background:#ffffff;
  border:1px solid var(--line);
  padding: 14px;
  box-shadow: 0 10px 28px rgba(15,23,42,.06);
}

.score-num {
  font-size: 34px;
  font-weight:1000;
  color:#0f172a;
  line-height:1;
}

.score-label {
  color: var(--muted);
  font-size: 11px;
  text-transform: uppercase;
  font-weight:900;
  letter-spacing:.05em;
  margin-top:5px;
}

.kpi-grid {
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 14px 0;
}

.kpi {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 16px;
  min-height: 105px;
  box-shadow: 0 10px 26px rgba(15,23,42,.045);
}

.kpi-label {
  color: var(--muted);
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: .055em;
}

.kpi-value {
  margin-top: 7px;
  font-size: 27px;
  line-height: 1.08;
  font-weight: 1000;
  letter-spacing: -.6px;
  color: #020617;
}

.kpi-note {
  margin-top: 7px;
  color: #64748b;
  font-size: 12px;
  line-height: 1.36;
}

.good-text { color: var(--green) !important; }
.bad-text { color: var(--red) !important; }
.warn-text { color: var(--amber) !important; }
.blue-text { color: var(--blue) !important; }

.bar-wrap { margin: 10px 0 14px 0; }
.bar-row {
  display:flex; justify-content:space-between; gap:10px;
  font-size: 12px; font-weight: 900; color:#334155; margin-bottom: 5px;
}
.bar-bg {
  width:100%; height: 12px; border-radius:999px;
  background:#e9edf4; border:1px solid #e2e8f0; overflow:hidden;
}
.bar-fill { height:100%; border-radius:999px; }

.report-grid {
  display:grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.report-card {
  background:#ffffff;
  border:1px solid var(--line);
  border-radius:22px;
  padding:18px;
  box-shadow: 0 10px 26px rgba(15,23,42,.045);
  min-height: 168px;
}

.report-head {
  display:flex;
  justify-content:space-between;
  gap:10px;
  align-items:flex-start;
}

.report-title {
  color:#0f172a;
  font-size:16px;
  font-weight:950;
  letter-spacing:-.2px;
}

.badge {
  display:inline-block;
  border-radius:999px;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 950;
  white-space:nowrap;
}

.badge.good { background: var(--green-bg); color:#067647; }
.badge.warn { background: var(--amber-bg); color:#92400e; }
.badge.bad { background: var(--red-bg); color:#991b1b; }
.badge.blue { background: var(--blue-bg); color:#1d4ed8; }
.badge.violet { background: var(--violet-bg); color:#6d28d9; }

.report-body {
  margin-top: 10px;
  color:#475569;
  font-size: 13.4px;
  line-height: 1.62;
}

.notice {
  border-radius: 16px;
  padding: 13px 15px;
  border:1px solid var(--line);
  margin: 7px 0;
  color: #334155;
  font-size:13.4px;
  line-height:1.55;
}

.notice.good { background: var(--green-bg); border-color: rgba(0,167,111,.22); color:#065f46; }
.notice.warn { background: var(--amber-bg); border-color: rgba(245,158,11,.25); color:#78350f; }
.notice.bad { background: var(--red-bg); border-color: rgba(239,68,68,.25); color:#991b1b; }
.notice.blue { background: var(--blue-bg); border-color: rgba(37,99,235,.20); color:#1e3a8a; }

.ai-board {
  background:
    radial-gradient(circle at top right, rgba(124,58,237,.12), transparent 24%),
    linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border:1px solid var(--line);
  border-radius: 28px;
  padding: 20px;
  box-shadow: 0 14px 42px rgba(15,23,42,.06);
}

.ai-empty {
  min-height: 390px;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  background:#f8fafc;
  border:1px dashed #cbd5e1;
  border-radius:22px;
}

.ai-card {
  background:#ffffff;
  border:1px solid var(--line);
  border-radius:18px;
  padding:16px;
  margin-bottom:12px;
}

.ai-label {
  color:#7c3aed;
  font-weight:950;
  font-size:12px;
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom:5px;
}

.ai-body {
  color:#334155;
  line-height:1.62;
  font-size:13.5px;
}

.form-title {
  font-weight:950;
  color:#0f172a;
  font-size:16px;
  margin: 8px 0 8px;
}

hr {
  border:none;
  border-top: 1px solid var(--line);
  margin: 18px 0;
}

code, pre {
  color: #0f172a !important;
  background: #f8fafc !important;
  border: 1px solid var(--line) !important;
  border-radius: 16px !important;
  white-space: pre-wrap !important;
  font-size: 12px !important;
}

div[data-testid="stDataFrame"] {
  border: 1px solid var(--line);
  border-radius: 18px;
  overflow:hidden;
}

.stExpander {
  border: 1px solid var(--line) !important;
  border-radius: 18px !important;
  background:#ffffff !important;
}

@media (max-width: 900px) {
  .command-strip, .kpi-grid, .report-grid { grid-template-columns: 1fr; }
  .result-top { flex-direction: column; }
  .score-badge { width: 100%; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# State
# =====================================================
DEFAULTS = {
    "last_entry": None,
    "last_position": None,
    "trade_log": [],
    "tracked_positions": [],
    "url_rows": [],
    "analysis_prompt": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =====================================================
# Utility
# =====================================================
def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def money(v):
    return f"-${abs(v):,.2f}" if v < 0 else f"${v:,.2f}"


def signed_money(v):
    return f"+${v:,.2f}" if v >= 0 else f"-${abs(v):,.2f}"


def signed_pct(v):
    return f"+{v:.1f}%" if v >= 0 else f"{v:.1f}%"


def cents(v):
    return f"{v:.1f}¢"


def tag(kind):
    return {"g": "good", "w": "warn", "b": "bad", "i": "blue", "v": "violet"}.get(kind, "blue")


def score_color(score):
    if score >= 72:
        return "#00a76f"
    if score >= 50:
        return "#f59e0b"
    return "#ef4444"


def kpi(label, value, note="", cls=""):
    cls_attr = f" {cls}-text" if cls else ""
    return f"""
    <div class="kpi">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value{cls_attr}">{value}</div>
      <div class="kpi-note">{note}</div>
    </div>
    """


def bar(label, value, max_v=100, color="#00a76f", suffix=""):
    width = 0 if max_v <= 0 else clamp(value / max_v * 100, 0, 100)
    return f"""
    <div class="bar-wrap">
      <div class="bar-row"><span>{label}</span><span>{value:.1f}{suffix}</span></div>
      <div class="bar-bg"><div class="bar-fill" style="width:{width:.1f}%; background:{color};"></div></div>
    </div>
    """


def notice(text, kind="i"):
    return f'<div class="notice {tag(kind)}">{text}</div>'


def report_card(title, badge, kind, body):
    return f"""
    <div class="report-card">
      <div class="report-head">
        <div class="report-title">{title}</div>
        <span class="badge {tag(kind)}">{badge}</span>
      </div>
      <div class="report-body">{body}</div>
    </div>
    """


def result_class(level):
    if level == "good":
        return "good", "✅", "적절"
    if level == "warn":
        return "warn", "⚠️", "조건부"
    return "bad", "⛔", "부적절"


# =====================================================
# Rules
# =====================================================
def price_zone(price):
    if price >= 99:
        return "99¢ 매수 금지", "b", -32, "99¢는 사는 가격이 아니라 파는 가격입니다."
    if price >= 95:
        return "상환 스캘핑", "b", -24, "95~98¢는 거의 상환 스캘핑입니다. 고액 신규 매수 금지에 가깝습니다."
    if price >= 90:
        return "신규매수 비추천", "b", -18, "90~95¢는 신규 매수 비추천 구간입니다."
    if price >= 85:
        return "매우 신중", "w", -10, "85~90¢는 신규 진입을 매우 신중하게 봐야 합니다."
    if price >= 80:
        return "익절 고려", "w", -6, "80~85¢는 신규 매수보다 익절 고려 구간입니다."
    if 2 <= price <= 5:
        return "초저가 Bounce", "w", -12, "2~5¢ Bounce Trade는 소액 전용입니다."
    if price < 2:
        return "복권형", "b", -20, "2¢ 미만은 거의 복권형 가격입니다."
    if price <= 20:
        return "고변동", "w", -4, "저가 구간은 변동성이 큽니다. 소액만 적합합니다."
    return "정상 구간", "g", 0, "가격 구간 자체는 과도한 위험 신호가 크지 않습니다."


def purpose_rule(purpose):
    rules = {
        "경기승리 / 만기 보유": (1.00, 0, "실제 승률 추정이 핵심인 기본 승리 베팅입니다."),
        "경기 시작 전 가격 상승 노림": (0.70, -6, "실제 승리보다 시장 심리와 타이밍이 중요합니다. 빨리 익절 기준을 정해야 합니다."),
        "반반 경기 쏠림 이용 / 중간 익절": (0.60, -8, "경기력이 아니라 시장 쏠림을 노리는 거래입니다. 오래 들고 가면 위험합니다."),
        "역배 / Bounce Trade": (0.35, -13, "역배와 bounce는 소액 전용입니다. 맞으면 크지만 실패가 기본값일 수 있습니다."),
        "99¢ 상환 스캘핑": (0.20, -25, "작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."),
        "뉴스/이벤트 선반영": (0.50, -12, "조건문과 해결 기준 확인이 중요합니다. 뉴스 해석 실수 위험이 큽니다."),
    }
    return rules.get(purpose, (1.0, 0, "일반 베팅으로 계산합니다."))


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
    return rules.get(market_type, (1.0, 0, "일반 시장으로 계산합니다."))


def size_rule(position_pct):
    if position_pct >= 50:
        return "시스템 실패", "b", -100, "계좌 생존 리스크입니다. 50% 이상 노출은 절대 금지입니다."
    if position_pct >= 20:
        return "진입 금지", "b", -85, "20% 이상은 진입 금지급 노출입니다."
    if position_pct >= 10:
        return "매우 위험", "b", -38, "10~20%는 매우 큰 포지션입니다. 일부 축소가 우선입니다."
    if position_pct >= 5:
        return "위험", "w", -20, "5~10%는 위험 구간입니다. 확신보다 손실 가능액을 먼저 봐야 합니다."
    if position_pct >= 3:
        return "주의", "w", -8, "3~5%는 주의 구간입니다."
    return "정상", "g", 5, "0~3%는 포지션 크기상 정상 범위입니다."


def exposure_rule(exposure_pct):
    if exposure_pct >= 20:
        return "중복 노출 금지", "b", -60, "같은 경기/방향 총 노출이 20% 이상입니다."
    if exposure_pct >= 10:
        return "중복 노출 위험", "b", -35, "같은 경기/방향 총 노출이 10~20%입니다."
    if exposure_pct >= 5:
        return "중복 노출 주의", "w", -12, "같은 경기/방향 총 노출이 5~10%입니다."
    return "정상", "g", 0, "중복 노출은 관리 가능한 범위입니다."


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


# =====================================================
# Entry engine
# =====================================================
def calculate_entry(data):
    current_price = data["current_price"]
    fair_price = data["fair_price"]
    stake = data["stake"]
    bankroll = data["bankroll"]
    edge = fair_price - current_price
    position_pct = (stake / bankroll) * 100 if bankroll else 0

    zone_label, zone_kind, zone_pen, zone_note = price_zone(current_price)
    purpose_mult, purpose_pen, purpose_note = purpose_rule(data["purpose"])
    type_mult, type_pen, type_note = market_type_rule(data["market_type"])
    size_label, size_kind, size_pen, size_note = size_rule(position_pct)

    base_cap = min(
        confidence_cap(data["confidence"]),
        portfolio_cap(bankroll, data["confidence"]),
        data["emotional_limit"],
    )
    rec_cap = base_cap * purpose_mult * type_mult
    if data["fomo_count"] >= 1:
        rec_cap *= 0.5

    if stake >= 200:
        cap_label, cap_kind, cap_pen = "$200 이상 시스템 실패", "b", -90
    elif stake >= 100:
        cap_label, cap_kind, cap_pen = "$100 이상 강한 경고", "b", -50
    elif stake > rec_cap * 1.2:
        cap_label, cap_kind, cap_pen = "추천 상한선 초과", "b", -32
    elif stake > rec_cap:
        cap_label, cap_kind, cap_pen = "상한선 근처/소폭 초과", "w", -12
    else:
        cap_label, cap_kind, cap_pen = "추천 상한선 이내", "g", 0

    duplicate_total = data["duplicate_ml"] + data["duplicate_game"] + data["duplicate_side"] + stake
    duplicate_pct = (duplicate_total / bankroll) * 100 if bankroll else 0
    exp_label, exp_kind, exp_pen, exp_note = exposure_rule(duplicate_pct)

    if data["fomo_count"] >= 3:
        fomo_label, fomo_kind, fomo_pen, fomo_note = "감정 진입 금지", "b", -75, "감정 체크 3개 이상입니다. 신규 진입 금지로 봐야 합니다."
    elif data["fomo_count"] >= 1:
        fomo_label, fomo_kind, fomo_pen, fomo_note = "감정 위험", "w", -20, "감정 체크가 있습니다. 추천 금액을 50% 줄였습니다."
    else:
        fomo_label, fomo_kind, fomo_pen, fomo_note = "정상", "g", 0, "감정 체크가 없습니다."

    if data["previous_good_price"] > 0:
        chase_gap = current_price - data["previous_good_price"]
        if chase_gap >= 30:
            chase_label, chase_kind, chase_pen, chase_note = "FOMO 추격", "b", -25, "처음 봤던 가격보다 30¢ 이상 올랐습니다. 추격매수 위험이 큽니다."
        elif chase_gap >= 15:
            chase_label, chase_kind, chase_pen, chase_note = "추격 위험", "w", -13, "처음 봤던 가격보다 많이 올라 진입가 매력이 줄었습니다."
        elif chase_gap >= 5:
            chase_label, chase_kind, chase_pen, chase_note = "조금 상승", "w", -5, "처음 봤던 가격보다 조금 올랐습니다."
        else:
            chase_label, chase_kind, chase_pen, chase_note = "추격 아님", "g", 5, "처음 봤던 가격 대비 추격 위험은 크지 않습니다."
    else:
        chase_gap, chase_label, chase_kind, chase_pen, chase_note = 0, "미입력", "i", 0, "처음 봤던 저평가 가격을 입력하지 않았습니다."

    bookmaker_prob = data["bookmaker_prob"]
    my_vs_poly = fair_price - current_price
    book_vs_poly = bookmaker_prob - current_price if bookmaker_prob > 0 else 0
    my_vs_book = fair_price - bookmaker_prob if bookmaker_prob > 0 else 0
    if bookmaker_prob <= 0:
        book_label, book_kind, book_pen, book_note = "북메이커 미입력", "i", 0, "북메이커 기준 승률을 입력하면 공식 배당과의 괴리를 같이 볼 수 있습니다."
    elif my_vs_book >= 10:
        book_label, book_kind, book_pen, book_note = "과신 재검토", "b", -12, "내 적정가가 북메이커보다 10%p 이상 높습니다. 과신 가능성을 재검토하세요."
    elif book_vs_poly >= 5:
        book_label, book_kind, book_pen, book_note = "외부배당도 저평가", "g", 6, "북메이커 기준으로도 Polymarket 가격이 싸 보입니다."
    elif book_vs_poly <= -5:
        book_label, book_kind, book_pen, book_note = "외부배당 기준 비쌈", "w", -8, "북메이커 기준으로는 Polymarket 가격이 비싼 편입니다."
    else:
        book_label, book_kind, book_pen, book_note = "큰 차이 없음", "i", 0, "북메이커와 Polymarket 가격 차이가 크지 않습니다."

    value_score = clamp(50 + edge * 2.2 + zone_pen + purpose_pen + type_pen + chase_pen + book_pen)
    final_score = clamp(value_score + size_pen + exp_pen + fomo_pen + cap_pen)

    hard_stop = None
    if position_pct >= 50:
        hard_stop = "시스템 실패 — 계좌 생존 리스크"
    elif stake >= 200:
        hard_stop = "$200 이상 — 시스템 실패"
    elif position_pct >= 20:
        hard_stop = "진입 금지 — 포트폴리오 20% 이상"
    elif duplicate_pct >= 20:
        hard_stop = "진입 금지 — 중복 노출 20% 이상"
    elif data["fomo_count"] >= 3:
        hard_stop = "진입 금지 — 감정 배팅 위험"

    if hard_stop:
        decision, level = hard_stop, "bad"
    elif final_score >= 75:
        decision, level = "진입 적절", "good"
    elif final_score >= 60:
        decision, level = "소액 진입 가능", "warn"
    elif final_score >= 45:
        decision, level = "관망 우선", "warn"
    else:
        decision, level = "진입 부적절", "bad"

    shares = stake / (current_price / 100)
    win_profit = shares - stake
    target_profit = shares * (data["target_price"] / 100) - stake
    stop_loss_amt = stake - shares * (data["stop_price"] / 100)
    rr = target_profit / stop_loss_amt if stop_loss_amt > 0 else 0

    if target_profit > 0 and stop_loss_amt > 0:
        if stop_loss_amt > target_profit:
            rr_text, rr_kind = f"손절 손실이 목표 수익보다 약 {stop_loss_amt / target_profit:.1f}배 큽니다.", "b"
        elif target_profit >= stop_loss_amt * 1.5:
            rr_text, rr_kind = f"목표 수익이 손절 손실보다 약 {target_profit / stop_loss_amt:.1f}배 큽니다.", "g"
        else:
            rr_text, rr_kind = f"목표 수익과 손절 손실 차이가 크지 않습니다. 손익비 {rr:.2f}:1 입니다.", "w"
    else:
        rr_text, rr_kind = "목표가 또는 손절가 설정을 다시 확인하세요.", "w"

    current_value = shares * (current_price / 100)
    additional_to_100 = shares - current_value
    high_warn = ""
    if current_price >= 90:
        high_warn = f"현재부터 100¢까지 추가수익은 {money(additional_to_100)}뿐입니다. 반대로 틀리면 현재 평가금 {money(current_value)}를 잃을 수 있습니다."
    if current_price >= 97:
        high_warn += " 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."

    if edge >= 10:
        edge_reason = ("g", f"가격 메리트 좋음: 내 적정가가 현재가보다 {edge:.1f}¢ 높습니다.")
    elif edge >= 5:
        edge_reason = ("w", f"가격 메리트 약간 있음: edge {edge:.1f}¢ 입니다.")
    elif edge < 0:
        edge_reason = ("b", f"가격 메리트 없음: 현재가가 내 적정가보다 {abs(edge):.1f}¢ 비쌉니다.")
    else:
        edge_reason = ("w", f"가격 메리트 작음: edge {edge:.1f}¢ 입니다.")

    reasons = [
        edge_reason,
        (size_kind, f"포지션 크기: 총자산의 {position_pct:.1f}% — {size_label}"),
        (cap_kind, f"추천 상한선: {money(rec_cap)} / 현재 투자금 {money(stake)} — {cap_label}"),
        (zone_kind, f"가격 구간: {zone_label} — {zone_note}"),
    ]

    return {
        **data,
        "edge": edge,
        "position_pct": position_pct,
        "duplicate_total": duplicate_total,
        "duplicate_pct": duplicate_pct,
        "rec_cap": rec_cap,
        "value_score": round(value_score, 1),
        "final_score": round(final_score, 1),
        "decision": decision,
        "level": level,
        "shares": shares,
        "win_profit": win_profit,
        "target_profit": target_profit,
        "stop_loss_amt": stop_loss_amt,
        "rr": rr,
        "rr_text": rr_text,
        "rr_kind": rr_kind,
        "current_value": current_value,
        "additional_to_100": additional_to_100,
        "high_warn": high_warn,
        "zone_label": zone_label,
        "zone_kind": zone_kind,
        "zone_note": zone_note,
        "purpose_note": purpose_note,
        "market_type_note": type_note,
        "size_label": size_label,
        "size_kind": size_kind,
        "size_note": size_note,
        "cap_label": cap_label,
        "cap_kind": cap_kind,
        "exp_label": exp_label,
        "exp_kind": exp_kind,
        "exp_note": exp_note,
        "fomo_label": fomo_label,
        "fomo_kind": fomo_kind,
        "fomo_note": fomo_note,
        "chase_gap": chase_gap,
        "chase_label": chase_label,
        "chase_kind": chase_kind,
        "chase_note": chase_note,
        "book_label": book_label,
        "book_kind": book_kind,
        "book_note": book_note,
        "my_vs_poly": my_vs_poly,
        "book_vs_poly": book_vs_poly,
        "my_vs_book": my_vs_book,
        "reasons": reasons,
    }


# =====================================================
# Position engine
# =====================================================
def evaluate_position(data):
    current_price = data["current_price"]
    shares = data["shares"]
    investment = data["investment"]
    bankroll = data["bankroll"]
    current_value = shares * (current_price / 100)
    pnl = current_value - investment
    roi = pnl / investment * 100 if investment else 0
    position_pct = current_value / bankroll * 100 if bankroll else 0
    additional = shares - current_value

    reasons = []
    warnings = []

    if current_price >= data["target_price"]:
        decision, level = "목표가 도달 — 매도/부분매도 고려", "warn"
        reasons.append("목표가에 도달했습니다. 최소 일부 익절을 검토할 구간입니다.")
    elif current_price <= data["stop_price"] and current_value >= investment * 0.3:
        decision, level = "손절 고려", "bad"
        reasons.append("손절가 이하이고 회수 가능한 금액이 아직 남아 있습니다.")
    elif current_value <= investment * 0.1:
        decision, level = "손절 효용 낮음 — 추가매수 금지", "warn"
        reasons.append("현재 평가금이 원금의 10% 이하입니다. 옵션처럼 보유 가능하지만 추가매수는 금지입니다.")
    else:
        decision, level = "홀딩 가능", "good"
        reasons.append("목표가와 손절가 사이에 있으며 홀딩 기본 조건은 충족합니다.")

    if roi >= 30:
        warnings.append("수익률 +30% 이상입니다. 원금 회수 또는 부분매도 검토가 필요합니다.")
        if level == "good":
            decision, level = "홀딩 가능, 단 부분매도 검토", "warn"

    if position_pct >= 20:
        warnings.append("포트폴리오 비중 20% 이상입니다. 진입 금지급 노출 — 즉시 축소 고려.")
        decision, level = "진입 금지급 노출 — 즉시 축소 고려", "bad"
    elif position_pct >= 10:
        warnings.append("포트폴리오 비중 10% 이상입니다. 포지션 크기 과대 — 일부 축소 권장.")
        if level != "bad":
            decision, level = "홀딩 가능, 단 포지션 크기 과대", "warn"

    if data["fomo_count"] >= 3:
        warnings.append("감정 체크 3개 이상입니다. 신규/추가매수 금지, 축소 우선.")
        decision, level = "감정 리스크 과대 — 추가매수 금지", "bad"
    elif data["fomo_count"] >= 1:
        warnings.append("감정 체크가 있습니다. 섣부른 추가매수 주의.")

    zone_label, zone_kind, _, zone_note = price_zone(current_price)
    if current_price >= 80:
        warnings.append(zone_note)

    if not warnings:
        warnings.append("현재 큰 위험 신호는 없지만 목표가/손절가 기준은 유지해야 합니다.")

    return {
        **data,
        "decision": decision,
        "level": level,
        "current_value": current_value,
        "pnl": pnl,
        "roi": roi,
        "position_pct": position_pct,
        "additional": additional,
        "zone_label": zone_label,
        "zone_kind": zone_kind,
        "zone_note": zone_note,
        "reasons": reasons,
        "warnings": warnings,
    }


def partial_rows(shares, price_cent, investment):
    price_dec = price_cent / 100
    rows = []
    need_ratio = None
    if shares > 0 and price_dec > 0:
        need_ratio = investment / (shares * price_dec) * 100

    for ratio in [25, 50, 70, 80, 90, 100]:
        sell_shares = shares * ratio / 100
        recovered = sell_shares * price_dec
        remaining = shares - sell_shares
        remain_value = remaining * price_dec
        additional_100 = remaining * (1 - price_dec)
        rows.append({
            "매도 비율": f"{ratio}%",
            "매도 수량": round(sell_shares, 2),
            "회수금": money(recovered),
            "원금 대비 확정손익": signed_money(recovered - investment),
            "남은 수량": round(remaining, 2),
            "남은 평가금": money(remain_value),
            "100¢ 추가수익": signed_money(additional_100),
        })
    return rows, need_ratio


# =====================================================
# URL helper
# =====================================================
def extract_slug(url):
    path = urllib.parse.urlparse(url.strip()).path.strip("/")
    return path.split("/")[-1] if path else ""


@st.cache_data(ttl=60, show_spinner=False)
def fetch_gamma(slug):
    api = f"https://gamma-api.polymarket.com/events?slug={urllib.parse.quote(slug)}"
    req = urllib.request.Request(api, headers={"User-Agent": "Memento-Grandmaster/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []
    return []


def extract_markets(payload):
    events = payload if isinstance(payload, list) else payload.get("events", [])
    rows = []
    for event in events:
        for market in event.get("markets", []):
            question = market.get("question") or market.get("title") or market.get("slug") or "Unknown market"
            outcomes = parse_list(market.get("outcomes"))
            prices = parse_list(market.get("outcomePrices"))
            tokens = parse_list(market.get("clobTokenIds"))
            for i, outcome in enumerate(outcomes):
                price = None
                if i < len(prices):
                    try:
                        price = round(float(prices[i]) * 100, 2)
                    except Exception:
                        price = None
                rows.append({
                    "시장": question,
                    "선택지": outcome,
                    "현재가(¢)": price,
                    "token_id": tokens[i] if i < len(tokens) else "",
                })
    return rows


def analysis_prompt(team_a, team_b, league, current_price, fair_price, purpose):
    return f"""너는 LoL/e스포츠 배팅 리스크 분석가다.
아래 경기를 배팅 관점에서 분석해줘.

경기: {team_a} vs {team_b}
리그: {league}
내가 보는 팀/선택지: {team_a}
현재 Polymarket 가격: {current_price}¢
내 적정가 추정: {fair_price}¢
배팅 목적: {purpose}

아래 형식으로 한국어로 답변해줘.

1. 리그/순위 관점
2. 최근 경기력/폼
3. 상대전적/스타일 상성
4. 로스터/부상/메타 변수
5. 현재 가격 {current_price}¢가 싼지 비싼지
6. 내가 과신하고 있을 가능성
7. 최종 결론: 배팅 추천 / 소액만 / 관망 / 비추천
"""


# =====================================================
# Render functions
# =====================================================
def render_entry_result(r):
    if not r:
        st.markdown(
            """
            <div class="card-soft">
              <div class="section-title">아직 판독 결과가 없습니다</div>
              <div class="muted">아래 빠른 입력값을 넣고 <b>판독하기</b>를 누르면 결론, 리스크, 공식배당, 손익비가 한 화면에 표시됩니다.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    klass, icon, label = result_class(r["level"])
    badness = 100 - r["final_score"]
    score_text = f"적절성 {r['final_score']:.0f}%" if r["level"] != "bad" else f"부적절도 {badness:.0f}%"

    st.markdown(
        f"""
        <div class="result {klass}">
          <div class="result-top">
            <div>
              <div class="result-title">{icon} {r['decision']}</div>
              <div class="result-sub">
                <b>{r['market_name']}</b><br>
                리스크 포함: <b>{score_text}</b> · 규모 제외 순수 가치: <b>{r['value_score']:.0f}%</b> · 목적: <b>{r['purpose']}</b>
              </div>
            </div>
            <div class="score-badge">
              <div class="score-num">{r['final_score']:.0f}</div>
              <div class="score-label">Risk Score</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kpi-grid">
          {kpi("현재가 / implied", cents(r["current_price"]), "시장 가격 = implied probability")}
          {kpi("내 적정가", cents(r["fair_price"]), "내가 보는 실제 적정 확률")}
          {kpi("Edge", f"{r['edge']:+.1f}¢", "내 적정가 - 현재가", "good" if r["edge"] >= 5 else "bad" if r["edge"] < 0 else "warn")}
          {kpi("포트폴리오 비중", f"{r['position_pct']:.1f}%", r["size_label"], "bad" if r["position_pct"] >= 10 else "warn" if r["position_pct"] >= 3 else "good")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='card'><div class='section-title'>점수 보드</div>"
        + bar("리스크 포함 최종 적절성", r["final_score"], 100, score_color(r["final_score"]), "%")
        + bar("배팅 규모 제외 순수 가치", r["value_score"], 100, "#2563eb", "%")
        + bar("포트폴리오 사용 비중", min(r["position_pct"], 100), 100, "#ef4444" if r["position_pct"] >= 20 else "#f59e0b" if r["position_pct"] >= 5 else "#00a76f", "%")
        + bar("현재가 위치", r["current_price"], 100, "#64748b", "¢")
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### 핵심 이유")
        for kind, text in r["reasons"]:
            st.markdown(notice(text, kind), unsafe_allow_html=True)
    with right:
        st.markdown("#### 핵심 경고")
        warnings = []
        for kind, text in r["reasons"]:
            if kind in ["b", "w"]:
                warnings.append((kind, text))
        if r["book_kind"] == "b":
            warnings.append(("b", r["book_note"]))
        if r["fomo_count"] > 0:
            warnings.append((r["fomo_kind"], r["fomo_note"]))
        if r["duplicate_pct"] >= 5:
            warnings.append((r["exp_kind"], r["exp_note"]))
        if r["high_warn"]:
            warnings.append(("b", r["high_warn"]))
        if not warnings:
            warnings = [("g", "큰 위험 신호는 없지만 손절/익절 기준은 유지해야 합니다.")]
        for kind, text in warnings[:6]:
            st.markdown(notice(text, kind), unsafe_allow_html=True)

    st.markdown("### 판독 리포트")
    st.markdown(
        f"""
        <div class="report-grid">
          {report_card("1. 진입가격 평가", r["zone_label"], r["zone_kind"], f"현재가 <b>{cents(r['current_price'])}</b><br>{r['zone_note']}")}
          {report_card("2. 배팅금액 / 계좌 생존", r["size_label"], r["size_kind"], f"투자금 <b>{money(r['stake'])}</b> / 총자산 <b>{money(r['bankroll'])}</b><br>포트폴리오 비중 <b>{r['position_pct']:.1f}%</b><br>{r['size_note']}")}
          {report_card("3. 북메이커 / 공식배당", r["book_label"], r["book_kind"], f"내 적정가 - 현재가: <b>{r['my_vs_poly']:+.1f}%p</b><br>북메이커 - 현재가: <b>{r['book_vs_poly']:+.1f}%p</b><br>내 적정가 - 북메이커: <b>{r['my_vs_book']:+.1f}%p</b><br>{r['book_note']}")}
          {report_card("4. 추천 상한선", r["cap_label"], r["cap_kind"], f"추천 상한선 <b>{money(r['rec_cap'])}</b><br>현재 투자금 <b>{money(r['stake'])}</b><br>확신 수준: <b>{r['confidence']}</b>")}
          {report_card("5. 손익비 / 목표가·손절가", f"손익비 {r['rr']:.2f}:1", r["rr_kind"], f"목표가 도달 시 예상수익 <b>{money(r['target_profit'])}</b><br>손절가 도달 시 예상손실 <b>{money(r['stop_loss_amt'])}</b><br>{r['rr_text']}")}
          {report_card("6. 감정 / FOMO", r["fomo_label"], r["fomo_kind"], f"감정 체크 <b>{r['fomo_count']}개</b><br>{r['fomo_note']}")}
          {report_card("7. 중복 노출", r["exp_label"], r["exp_kind"], f"같은 경기/방향 총 노출 <b>{money(r['duplicate_total'])}</b><br>총자산 대비 <b>{r['duplicate_pct']:.1f}%</b><br>{r['exp_note']}")}
          {report_card("8. 배팅 목적 / 시장 유형", "구조 분석", "v", f"목적: <b>{r['purpose']}</b><br>{r['purpose_note']}<br><br>시장 유형: <b>{r['market_type']}</b><br>{r['market_type_note']}")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 수익/손실 시나리오")
    st.markdown(
        f"""
        <div class="kpi-grid">
          {kpi("보유 수량", f"{r['shares']:.2f}주", "투자금 / 현재가")}
          {kpi("승리 시 순이익", money(r["win_profit"]), "100¢ 상환 기준", "good")}
          {kpi("패배 시 손실", money(-r["stake"]), "전액 손실 가정", "bad")}
          {kpi("100¢까지 추가수익", money(r["additional_to_100"]), "현재가 기준 남은 업사이드", "blue")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary = (
        f"{r['market_name']}\n"
        f"현재가: {r['current_price']:.1f}¢ / 내 적정가: {r['fair_price']:.1f}¢ / "
        f"Edge: {r['edge']:+.1f}¢ / 투자금: ${r['stake']:.2f} / "
        f"포트폴리오 비중: {r['position_pct']:.1f}% / 북메이커: {r['bookmaker_prob']:.1f}% / "
        f"판정: {r['decision']} / 리스크 포함: {r['final_score']:.0f}% / 규모 제외 가치: {r['value_score']:.0f}%"
    )
    st.markdown("### 기록용 요약")
    st.code(summary)


def render_position_result(r):
    if not r:
        st.markdown(
            """
            <div class="card-soft">
              <div class="section-title">포지션 결과 대기</div>
              <div class="muted">현재가와 보유수량을 입력하면 매도/홀딩/부분매도 타이밍을 리포트로 보여줍니다.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    klass, icon, _ = result_class(r["level"])
    st.markdown(
        f"""
        <div class="result {klass}">
          <div class="result-top">
            <div>
              <div class="result-title">{icon} {r['decision']}</div>
              <div class="result-sub"><b>{r['name']}</b><br>현재 포지션 기준 매도/홀딩 판단입니다.</div>
            </div>
            <div class="score-badge">
              <div class="score-num">{signed_pct(r['roi'])}</div>
              <div class="score-label">Current ROI</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kpi-grid">
          {kpi("현재 평가금", money(r["current_value"]), "현재가 × 보유수량")}
          {kpi("즉시 매도 손익", signed_money(r["pnl"]), f"ROI {signed_pct(r['roi'])}", "good" if r["pnl"] >= 0 else "bad")}
          {kpi("100¢ 상환 총액", money(r["shares"]), "승리 시 총액", "blue")}
          {kpi("실패 시 손실", money(-r["current_value"]), "현재 평가금 손실", "bad")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='card'><div class='section-title'>포지션 위험 시각화</div>"
        + bar("현재 수익률", max(r["roi"], 0), 100, "#00a76f" if r["roi"] >= 0 else "#ef4444", "%")
        + bar("포트폴리오 비중", min(r["position_pct"], 100), 100, "#ef4444" if r["position_pct"] >= 20 else "#f59e0b" if r["position_pct"] >= 10 else "#00a76f", "%")
        + bar("현재가 위치", r["current_price"], 100, "#2563eb", "¢")
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### 이유")
        for text in r["reasons"]:
            st.markdown(notice(text, "g"), unsafe_allow_html=True)
    with right:
        st.markdown("#### 경고")
        for text in r["warnings"]:
            kind = "b" if "금지" in text or "손절" in text or "20%" in text else "w"
            st.markdown(notice(text, kind), unsafe_allow_html=True)

    rows, need = partial_rows(r["shares"], r["current_price"], r["investment"])
    st.markdown("#### 부분매도 시나리오")
    if need is not None:
        if need <= 100:
            st.success(f"원금 회수 최소 매도 비율: {need:.1f}%")
        else:
            st.warning(f"현재 가격에서는 100% 팔아도 원금 회수가 어렵습니다. 필요 비율: {need:.1f}%")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# =====================================================
# Header
# =====================================================
st.markdown(
    """
    <div class="hero">
      <div class="brand-row">
        <div>
          <div class="brand-title">Memento<br>Grandmaster</div>
          <div class="brand-sub">
            Polymarket 배팅 판단 도구 · 계좌를 지키는 수동 리스크 관리 앱<br>
            <b>좋은 팀이 아니라 좋은 가격을 산다. Edge가 좋아도 금액이 과하면 나쁜 거래다.</b>
          </div>
          <span class="status-chip">⚡ Entry Command</span>
          <span class="status-chip">📍 Position Studio</span>
          <span class="status-chip">🧩 Partial Exit</span>
          <span class="status-chip">🔎 URL Helper</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

last = st.session_state.last_entry
st.markdown(
    f"""
    <div class="command-strip">
      <div class="command-card">
        <div class="command-label">Last Decision</div>
        <div class="command-value">{last['decision'] if last else '대기 중'}</div>
        <div class="command-note">최근 진입 판독 결과</div>
      </div>
      <div class="command-card">
        <div class="command-label">Risk Score</div>
        <div class="command-value">{str(last['final_score']) + '%' if last else '-'}</div>
        <div class="command-note">리스크 포함 적절성</div>
      </div>
      <div class="command-card">
        <div class="command-label">Pure Value</div>
        <div class="command-value">{str(last['value_score']) + '%' if last else '-'}</div>
        <div class="command-note">배팅 규모 제외 가치</div>
      </div>
      <div class="command-card">
        <div class="command-label">Trade Logs</div>
        <div class="command-value">{len(st.session_state.trade_log)}개</div>
        <div class="command-note">세션 내 기록된 거래</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Tabs
# =====================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ 진입 판독",
    "📍 포지션 관리",
    "🧩 부분매도",
    "📈 거래일지",
    "🔎 URL 도우미",
])


# =====================================================
# Tab 1: Entry
# =====================================================
with tab1:
    left, right = st.columns([1.02, 0.98], gap="large")

    with left:
        st.markdown('<div class="section-title">⚡ 배팅 진입 판독</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">입력은 간단하게, 결과는 리포트처럼 자세하게 보여줍니다.</div>', unsafe_allow_html=True)
        render_entry_result(st.session_state.last_entry)

    with right:
        st.markdown('<div class="section-title">🎛️ 입력 패널</div>', unsafe_allow_html=True)
        with st.form("entry_form"):
            market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner")
            team_a = st.text_input("내가 보는 팀/선택지", "T1")
            team_b = st.text_input("상대 팀/선택지", "HLE")
            league = st.selectbox("리그", ["LCK", "LPL", "LEC", "LCS", "MSI/Worlds", "기타"])

            c1, c2 = st.columns(2)
            with c1:
                current_price = st.number_input("현재가 / 진입가격(센트)", 1.0, 99.0, 52.0)
                stake = st.number_input("진입 크기 / 투자금($)", 1.0, value=50.0)
                purpose = st.selectbox("배팅 목적", [
                    "경기승리 / 만기 보유",
                    "경기 시작 전 가격 상승 노림",
                    "반반 경기 쏠림 이용 / 중간 익절",
                    "역배 / Bounce Trade",
                    "99¢ 상환 스캘핑",
                    "뉴스/이벤트 선반영",
                ])
            with c2:
                fair_price = st.number_input("내가 생각하는 적정 가격(센트)", 1.0, 99.0, 65.0)
                bankroll = st.number_input("전체 포트폴리오 / 총자산($)", 1.0, value=814.0)
                market_type = st.selectbox("시장 유형", [
                    "Match Moneyline",
                    "Game Winner",
                    "Correct Score",
                    "정치 선거",
                    "뉴스/이벤트",
                    "99¢ 상환 스캘핑",
                    "2~5¢ Bounce Trade",
                ])

            with st.expander("⚙️ 고급 설정"):
                a, b, c = st.columns(3)
                with a:
                    emotional_limit = st.number_input("감정 한도($)", 1.0, value=50.0)
                    confidence = st.selectbox("확신 수준", ["관찰용", "낮은 확신", "중간 확신", "높은 확신", "초고확신"], index=2)
                with b:
                    target_price = st.number_input("목표가(센트)", 1.0, 100.0, 75.0)
                    stop_price = st.number_input("손절가(센트)", 0.0, 99.0, 40.0)
                with c:
                    bookmaker_prob = st.number_input("북메이커/공식배당 기준 승률(%)", 0.0, 99.0, 0.0)
                    previous_good_price = st.number_input("처음 봤던 저평가 가격(센트)", 0.0, 99.0, 0.0)

                st.markdown('<div class="form-title">중복 노출</div>', unsafe_allow_html=True)
                d1, d2, d3 = st.columns(3)
                with d1:
                    duplicate_ml = st.number_input("같은 경기 ML 노출($)", 0.0, value=0.0)
                with d2:
                    duplicate_game = st.number_input("Game Winner 노출($)", 0.0, value=0.0)
                with d3:
                    duplicate_side = st.number_input("같은 방향 추가 노출($)", 0.0, value=0.0)

                st.markdown('<div class="form-title">FOMO / 감정 체크</div>', unsafe_allow_html=True)
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
                f1, f2 = st.columns(2)
                for i, opt in enumerate(fomo_options):
                    with f1 if i % 2 == 0 else f2:
                        if st.checkbox(opt, key=f"fomo_{i}"):
                            fomo_count += 1

            submitted = st.form_submit_button("⚡ 판독하기", use_container_width=True)

        if submitted:
            data = {
                "market_name": market_name,
                "team_a": team_a,
                "team_b": team_b,
                "league": league,
                "current_price": current_price,
                "fair_price": fair_price,
                "stake": stake,
                "purpose": purpose,
                "market_type": market_type,
                "bankroll": bankroll,
                "emotional_limit": emotional_limit,
                "confidence": confidence,
                "target_price": target_price,
                "stop_price": stop_price,
                "bookmaker_prob": bookmaker_prob,
                "previous_good_price": previous_good_price,
                "duplicate_ml": duplicate_ml,
                "duplicate_game": duplicate_game,
                "duplicate_side": duplicate_side,
                "fomo_count": fomo_count,
            }
            st.session_state.last_entry = calculate_entry(data)
            st.session_state.analysis_prompt = analysis_prompt(team_a, team_b, league, current_price, fair_price, purpose)
            st.toast("판독 리포트가 생성되었습니다.", icon="📊")
            st.rerun()

        st.markdown('<div class="ai-board">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 AI 분석 프롬프트</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">API 키 없이도 바로 쓸 수 있게, Claude/ChatGPT에 붙여넣을 분석 프롬프트를 자동 생성합니다.</div>', unsafe_allow_html=True)
        if st.session_state.analysis_prompt:
            st.code(st.session_state.analysis_prompt)
        else:
            st.markdown(
                """
                <div class="ai-empty">
                  <div>
                    <div style="font-size:46px;">🤖</div>
                    <div style="font-weight:950; margin-top:10px;">판독 후 자동 생성</div>
                    <div class="muted" style="margin-top:8px;">팀명, 리그, 가격 정보를 기반으로<br>분석 프롬프트가 만들어집니다.</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# Tab 2: Position
# =====================================================
with tab2:
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown('<div class="section-title">📍 포지션 결과</div>', unsafe_allow_html=True)
        render_position_result(st.session_state.last_position)

    with right:
        st.markdown('<div class="section-title">📍 포지션 입력</div>', unsafe_allow_html=True)
        with st.form("position_form"):
            name = st.text_input("거래 이름", "KT Rolster vs Dplus KIA — Match Winner")
            p1, p2, p3 = st.columns(3)
            with p1:
                avg_buy = st.number_input("평균 매수가(센트)", 1.0, 99.0, 52.4)
            with p2:
                current_price = st.number_input("현재가 / best bid(센트)", 1.0, 100.0, 58.0)
            with p3:
                shares = st.number_input("보유 수량", 0.01, value=1164.12)

            p4, p5, p6 = st.columns(3)
            with p4:
                investment = st.number_input("투자금($)", 1.0, value=610.0)
            with p5:
                target_price = st.number_input("목표 매도가(센트)", 1.0, 100.0, 60.0)
            with p6:
                stop_price = st.number_input("손절가(센트)", 0.0, 99.0, 45.0)

            p7, p8 = st.columns(2)
            with p7:
                bankroll = st.number_input("전체 포트폴리오 금액($)", 1.0, value=1200.0, key="pos_bankroll")
            with p8:
                fomo_count = st.slider("현재 감정 위험 체크 수", 0, 7, 0)

            pos_submit = st.form_submit_button("📍 포지션 판독하기", use_container_width=True)

        if pos_submit:
            st.session_state.last_position = evaluate_position({
                "name": name,
                "avg_buy": avg_buy,
                "current_price": current_price,
                "shares": shares,
                "investment": investment,
                "target_price": target_price,
                "stop_price": stop_price,
                "bankroll": bankroll,
                "fomo_count": fomo_count,
            })
            st.rerun()

        if st.session_state.last_position:
            if st.button("현재 포지션을 목록에 저장", use_container_width=True):
                r = st.session_state.last_position
                st.session_state.tracked_positions.append({
                    "날짜": str(date.today()),
                    "거래": r["name"],
                    "판정": r["decision"],
                    "현재가": cents(r["current_price"]),
                    "수익률": signed_pct(r["roi"]),
                    "평가금": money(r["current_value"]),
                })
                st.success("포지션 목록에 저장했습니다.")

        if st.session_state.tracked_positions:
            st.markdown("#### 저장된 포지션")
            st.dataframe(pd.DataFrame(st.session_state.tracked_positions), use_container_width=True, hide_index=True)


# =====================================================
# Tab 3: Partial
# =====================================================
with tab3:
    st.markdown('<div class="section-title">🧩 부분매도 계산기</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">원금 회수 최소 비율과 25/50/70/80/90/100% 매도 시나리오를 계산합니다.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        buy_price = st.number_input("매수가(센트)", 1.0, 99.0, 16.0, key="partial_buy")
    with c2:
        current_price = st.number_input("현재가(센트)", 1.0, 100.0, 73.0, key="partial_current")
    with c3:
        investment = st.number_input("투자금($)", 0.0, value=16.08, key="partial_investment")

    manual = st.checkbox("보유 수량 직접 입력", value=False)
    if manual:
        shares = st.number_input("보유 수량", 0.0, value=100.0)
    else:
        shares = investment / (buy_price / 100) if buy_price > 0 else 0

    if st.button("부분매도 표 계산하기", use_container_width=True):
        rows, need = partial_rows(shares, current_price, investment)
        current_value = shares * (current_price / 100)
        additional = shares - current_value

        st.markdown(
            f"""
            <div class="kpi-grid">
              {kpi("보유 수량", f"{shares:.2f}주", "투자금 기준 자동 계산")}
              {kpi("현재 평가금", money(current_value), "현재가 기준")}
              {kpi("100¢까지 추가수익", money(additional), "남은 업사이드", "blue")}
              {kpi("실패 시 손실", money(-current_value), "현재 평가금 손실", "bad")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if need is not None:
            if need <= 100:
                st.success(f"원금 회수에 필요한 최소 매도 비율: {need:.1f}%")
            else:
                st.warning(f"현재 가격에서는 100% 팔아도 원금 회수가 어렵습니다. 필요 비율: {need:.1f}%")

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.markdown(
            notice(
                f"현재 평가금 {money(current_value)}에서 100¢까지 추가로 얻을 수 있는 금액은 {money(additional)}입니다. 반대로 실패하면 현재 평가금 {money(current_value)}를 잃을 수 있습니다.",
                "w",
            ),
            unsafe_allow_html=True,
        )


# =====================================================
# Tab 4: Trade log
# =====================================================
with tab4:
    st.markdown('<div class="section-title">📈 거래일지 / 총수익률</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        start_bankroll = st.number_input("시작 자금($)", 0.0, value=500.0)
    with b:
        current_bankroll = st.number_input("현재 총자산($)", 0.0, value=650.0)
    with c:
        net_deposit = st.number_input("추가 입금 / 출금 조정($)", value=0.0)

    adjusted = start_bankroll + net_deposit
    total_profit = current_bankroll - adjusted
    total_roi = total_profit / adjusted * 100 if adjusted > 0 else 0

    level = "good" if total_profit >= 0 else "bad"
    klass, icon, _ = result_class(level)
    st.markdown(
        f"""
        <div class="result {klass}">
          <div class="result-title">{icon} 총손익 {signed_money(total_profit)} ({signed_pct(total_roi)})</div>
          <div class="result-sub">현재 총자산 {money(current_bankroll)} · 시작 자금 {money(start_bankroll)} · 조정 {money(net_deposit)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 거래 등록")
    with st.form("trade_form"):
        t1, t2, t3 = st.columns(3)
        with t1:
            name = st.text_input("거래 이름", "T1 vs HLE — Match Winner")
            buy = st.number_input("매수가(센트)", 1.0, 99.0, 52.0, key="log_buy")
        with t2:
            sell = st.number_input("매도가(센트)", 0.0, 100.0, 78.0, key="log_sell")
            stake = st.number_input("투자금($)", 1.0, value=50.0, key="log_stake")
        with t3:
            memo = st.text_area("메모", "진입 이유 / 매도 이유 / 감정 상태", height=100)
        add = st.form_submit_button("거래 기록 추가", use_container_width=True)

    if add:
        shares = stake / (buy / 100)
        sell_amount = shares * (sell / 100)
        profit = sell_amount - stake
        roi = profit / stake * 100
        st.session_state.trade_log.append({
            "날짜": str(date.today()),
            "거래": name,
            "매수가": cents(buy),
            "매도가": cents(sell),
            "투자금": money(stake),
            "손익": signed_money(profit),
            "수익률": signed_pct(roi),
            "메모": memo,
        })
        st.success(f"기록 추가: {signed_money(profit)} ({signed_pct(roi)})")

    if st.session_state.trade_log:
        df = pd.DataFrame(st.session_state.trade_log)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV 다운로드", data=csv, file_name="memento_trades.csv", mime="text/csv")
    else:
        st.info("아직 기록된 거래가 없습니다.")

    with st.expander("거래 복기 질문", expanded=True):
        for q in [
            "원하는 가격에 진입했는가?",
            "내 예상 승률의 근거는 무엇인가?",
            "북메이커와 왜 다르게 봤는가?",
            "금액은 감당 가능한 크기였는가?",
            "매도 기준을 지켰는가?",
            "감정적으로 들어간 부분이 있었는가?",
            "다음에 반복 가능한 거래인가?",
            "놓친 수익을 손실로 착각하고 있지는 않은가?",
        ]:
            st.markdown(notice("— " + q, "i"), unsafe_allow_html=True)

    if st.button("거래일지 초기화"):
        st.session_state.trade_log = []
        st.rerun()


# =====================================================
# Tab 5: URL Helper
# =====================================================
with tab5:
    st.markdown('<div class="section-title">🔎 Polymarket URL 도우미</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">token_id를 직접 찾기 어려울 때, URL에서 시장/선택지/token_id 후보를 표로 보여줍니다. 자동매매 기능은 아닙니다.</div>', unsafe_allow_html=True)

    url = st.text_input("Polymarket 시장 URL", "https://polymarket.com/ko/esports/league-of-legends/emea-masters/lol-fn-vdn-2026-06-08")

    if st.button("URL에서 시장 후보 불러오기", use_container_width=True):
        slug = extract_slug(url)
        if not slug:
            st.error("URL에서 slug를 찾지 못했습니다.")
        else:
            st.write(f"찾은 slug: `{slug}`")
            try:
                payload = fetch_gamma(slug)
                rows = extract_markets(payload)
                st.session_state.url_rows = rows
                if rows:
                    st.success(f"{len(rows)}개의 선택지 후보를 찾았습니다.")
                else:
                    st.warning("시장 후보를 찾지 못했습니다.")
            except Exception as e:
                st.error(f"불러오기 실패: {e}")

    if st.session_state.url_rows:
        df = pd.DataFrame(st.session_state.url_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown(notice("현재 단계에서는 token_id를 복사해 확인용으로만 사용하세요. 다음 단계에서는 URL → 시장 선택 → 가격 자동 조회까지 연결하면 됩니다.", "i"), unsafe_allow_html=True)
