import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

import pandas as pd
import streamlit as st

# =====================================================
# Memento — Apple-grade light UI
# =====================================================
st.set_page_config(
    page_title="Memento",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');

:root {
  --ink: #1d1d1f;
  --ink2: #424245;
  --gray: #86868b;
  --gray2: #aeaeb2;
  --hairline: #e8e8ed;
  --fill: #f5f5f7;
  --paper: #ffffff;
  --blue: #0071e3;
  --green: #1d7d4f;
  --green-soft: #e9f6ef;
  --red: #d0312d;
  --red-soft: #fdf0ef;
  --amber: #b25e09;
  --amber-soft: #fdf5e9;
}

html, body, .stApp {
  background: #ffffff !important;
  color: var(--ink) !important;
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
}
* { font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important; }

.block-container { max-width: 1120px; padding-top: 2.6rem; padding-bottom: 5rem; }
section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { background: rgba(255,255,255,.85) !important; backdrop-filter: blur(14px); }

h1,h2,h3,h4,p,span,div,label { color: var(--ink); }

/* ---------- inputs: iOS gray-fill fields ---------- */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
  background: var(--fill) !important;
  border: 1px solid transparent !important;
  border-radius: 12px !important;
  color: var(--ink) !important;
  font-size: 15px !important;
  font-weight: 450 !important;
  min-height: 44px;
  box-shadow: none !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
textarea:focus {
  background: #ffffff !important;
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 4px rgba(0,113,227,.12) !important;
}
div[data-baseweb="select"] > div {
  background: var(--fill) !important;
  border: 1px solid transparent !important;
  border-radius: 12px !important;
  color: var(--ink) !important;
  min-height: 44px;
}
div[data-testid="stNumberInput"] button {
  background: transparent !important;
  border: none !important;
  color: var(--gray) !important;
}
div[data-testid="stWidgetLabel"] p {
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--ink2) !important;
  letter-spacing: -.01em;
}

/* ---------- buttons: Apple pill ---------- */
.stButton > button, .stFormSubmitButton > button {
  background: var(--blue) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 980px !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  letter-spacing: -.01em !important;
  min-height: 46px;
  box-shadow: none !important;
  transition: background .18s ease !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: #0077ed !important;
  color: #ffffff !important;
}
.stButton > button:active { background: #006edb !important; }
div[data-testid="stDownloadButton"] > button {
  background: var(--fill) !important;
  color: var(--ink) !important;
  border: none !important;
  border-radius: 980px !important;
  font-weight: 500 !important;
}

/* ---------- tabs: iOS segmented control ---------- */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--fill);
  border-radius: 12px;
  padding: 3px;
  gap: 2px;
  border: none;
  display: inline-flex;
  width: auto;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  border-radius: 9px !important;
  padding: 7px 18px !important;
  background: transparent !important;
  border: none !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] p {
  font-size: 13.5px !important;
  font-weight: 500 !important;
  color: var(--gray) !important;
  letter-spacing: -.01em;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  background: #ffffff !important;
  box-shadow: 0 1px 4px rgba(0,0,0,.10) !important;
}
div[data-testid="stTabs"] [aria-selected="true"] p { color: var(--ink) !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

/* ---------- expander ---------- */
.stExpander {
  border: 1px solid var(--hairline) !important;
  border-radius: 14px !important;
  background: #ffffff !important;
  box-shadow: none !important;
}
.stExpander summary p { font-size: 14px !important; font-weight: 500 !important; }

/* ---------- dataframe ---------- */
div[data-testid="stDataFrame"] {
  border: 1px solid var(--hairline);
  border-radius: 14px;
  overflow: hidden;
}

/* ---------- progress (native bars) ---------- */
div[data-testid="stProgress"] > div > div {
  background: var(--hairline) !important;
  border-radius: 980px;
  height: 4px !important;
}
div[data-testid="stProgress"] > div > div > div {
  background: var(--ink) !important;
  border-radius: 980px;
}

code, pre {
  background: var(--fill) !important;
  border: none !important;
  border-radius: 12px !important;
  color: var(--ink2) !important;
  font-size: 12.5px !important;
  white-space: pre-wrap !important;
}

hr { border: none; border-top: 1px solid var(--hairline); margin: 28px 0; }

/* =====================================================
   Custom components
===================================================== */

/* masthead */
.masthead { padding: 6px 0 34px 0; }
.masthead .name {
  font-size: 21px;
  font-weight: 600;
  letter-spacing: -.022em;
  color: var(--ink);
}
.masthead .tag {
  font-size: 13px;
  color: var(--gray);
  margin-top: 2px;
  letter-spacing: -.01em;
}

/* headline (page section opener) */
.headline {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -.025em;
  line-height: 1.12;
  color: var(--ink);
  margin: 6px 0 4px 0;
}
.subline {
  font-size: 15px;
  color: var(--gray);
  letter-spacing: -.012em;
  line-height: 1.55;
  margin-bottom: 26px;
}

/* eyebrow caption */
.eyebrow {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray);
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

/* verdict block — typography-first */
.verdict { padding: 28px 0 22px 0; border-top: 1px solid var(--hairline); }
.verdict .v-title {
  font-size: 44px;
  font-weight: 600;
  letter-spacing: -.03em;
  line-height: 1.06;
  color: var(--ink);
}
.verdict .v-sub {
  margin-top: 10px;
  font-size: 15px;
  color: var(--gray);
  letter-spacing: -.012em;
  line-height: 1.6;
}
.dot { display:inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 10px; vertical-align: 4px; }
.dot.g { background: var(--green); }
.dot.w { background: var(--amber); }
.dot.b { background: var(--red); }
.dot.i { background: var(--gray2); }

/* open stat row (no boxes) */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline); margin: 4px 0 26px 0; }
.stat { padding: 18px 18px 18px 0; border-right: 1px solid var(--hairline); }
.stat:last-child { border-right: none; }
.stat + .stat { padding-left: 18px; }
.stat .s-label { font-size: 12px; font-weight: 500; color: var(--gray); letter-spacing: -.005em; }
.stat .s-value { margin-top: 6px; font-size: 26px; font-weight: 600; letter-spacing: -.025em; color: var(--ink); font-variant-numeric: tabular-nums; }
.stat .s-value.pos { color: var(--green); }
.stat .s-value.neg { color: var(--red); }
.stat .s-note { margin-top: 4px; font-size: 12px; color: var(--gray2); letter-spacing: -.005em; }

/* spec table (Apple tech-specs style) */
.spec { border-top: 1px solid var(--hairline); }
.spec-row { display: grid; grid-template-columns: 200px 1fr auto; gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--hairline); align-items: start; }
.spec-key { font-size: 13.5px; font-weight: 500; color: var(--gray); letter-spacing: -.008em; padding-top: 1px; }
.spec-val { font-size: 14.5px; color: var(--ink2); letter-spacing: -.01em; line-height: 1.6; }
.spec-val b { color: var(--ink); font-weight: 600; }
.state { font-size: 12.5px; font-weight: 500; white-space: nowrap; padding: 4px 11px; border-radius: 980px; letter-spacing: -.005em; }
.state.g { background: var(--green-soft); color: var(--green); }
.state.w { background: var(--amber-soft); color: var(--amber); }
.state.b { background: var(--red-soft); color: var(--red); }
.state.i { background: var(--fill); color: var(--gray); }

/* inline note lines */
.line { display: flex; gap: 12px; padding: 11px 0; border-bottom: 1px solid var(--hairline); font-size: 14px; color: var(--ink2); letter-spacing: -.01em; line-height: 1.6; align-items: baseline; }
.line:last-child { border-bottom: none; }

/* meter */
.meter { margin: 14px 0; }
.meter .m-row { display: flex; justify-content: space-between; font-size: 13px; color: var(--ink2); letter-spacing: -.008em; margin-bottom: 7px; font-variant-numeric: tabular-nums; }
.meter .m-row .m-val { color: var(--gray); }
.meter .m-track { height: 4px; border-radius: 980px; background: var(--hairline); overflow: hidden; }
.meter .m-fill { height: 100%; border-radius: 980px; }

/* quiet placeholder */
.quiet {
  border: 1px dashed var(--hairline);
  border-radius: 16px;
  padding: 64px 24px;
  text-align: center;
}
.quiet .q-title { font-size: 16px; font-weight: 600; color: var(--ink); letter-spacing: -.015em; }
.quiet .q-body { margin-top: 8px; font-size: 13.5px; color: var(--gray); line-height: 1.65; letter-spacing: -.008em; }

/* AI answer */
.ai-block { border-top: 1px solid var(--hairline); padding: 16px 0; }
.ai-block .a-key { font-size: 12px; font-weight: 600; color: var(--gray); letter-spacing: .05em; text-transform: uppercase; }
.ai-block .a-body { margin-top: 7px; font-size: 14.5px; color: var(--ink2); line-height: 1.7; letter-spacing: -.01em; }

.footnote { font-size: 12px; color: var(--gray2); letter-spacing: -.005em; line-height: 1.6; margin-top: 10px; }

@media (max-width: 880px) {
  .stats { grid-template-columns: repeat(2, 1fr); }
  .stat:nth-child(2) { border-right: none; }
  .stat:nth-child(3) { border-top: 1px solid var(--hairline); padding-left: 0; }
  .stat:nth-child(4) { border-top: 1px solid var(--hairline); }
  .spec-row { grid-template-columns: 1fr; gap: 6px; }
  .verdict .v-title { font-size: 32px; }
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
    "ai_text": "",
    "ai_error": "",
    "ai_prompt": "",
    "ai_pair": "",
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

def stat(label, value, note="", tone=""):
    cls = " pos" if tone == "pos" else " neg" if tone == "neg" else ""
    return f"""<div class="stat"><div class="s-label">{label}</div><div class="s-value{cls}">{value}</div><div class="s-note">{note}</div></div>"""

def spec_row(key, val, state_text="", kind="i"):
    s = f'<span class="state {kind}">{state_text}</span>' if state_text else ""
    return f"""<div class="spec-row"><div class="spec-key">{key}</div><div class="spec-val">{val}</div><div>{s}</div></div>"""

def meter(label, value, max_v=100, kind="i"):
    color = {"g": "var(--green)", "w": "var(--amber)", "b": "var(--red)", "i": "var(--ink)"}.get(kind, "var(--ink)")
    width = clamp(value / max_v * 100 if max_v else 0)
    return f"""<div class="meter"><div class="m-row"><span>{label}</span><span class="m-val">{value:.1f}</span></div><div class="m-track"><div class="m-fill" style="width:{width:.1f}%;background:{color};"></div></div></div>"""

def line(text, kind="i"):
    return f'<div class="line"><span class="dot {kind}"></span><span>{text}</span></div>'

def verdict_dot(level):
    return {"good": "g", "warn": "w", "bad": "b"}.get(level, "i")


# =====================================================
# Rules (unchanged engine)
# =====================================================
def price_zone(price):
    if price >= 99: return "99¢ 매수 금지", "b", -32, "99¢는 사는 가격이 아니라 파는 가격입니다."
    if price >= 95: return "상환 스캘핑", "b", -24, "95~98¢는 거의 상환 스캘핑입니다. 고액 신규 매수 금지에 가깝습니다."
    if price >= 90: return "신규매수 비추천", "b", -18, "90~95¢는 신규 매수 비추천 구간입니다."
    if price >= 85: return "매우 신중", "w", -10, "85~90¢는 신규 진입을 매우 신중하게 봐야 합니다."
    if price >= 80: return "익절 고려", "w", -6, "80~85¢는 신규 매수보다 익절 고려 구간입니다."
    if 2 <= price <= 5: return "초저가 Bounce", "w", -12, "2~5¢ Bounce Trade는 소액 전용입니다."
    if price < 2: return "복권형", "b", -20, "2¢ 미만은 거의 복권형 가격입니다."
    if price <= 20: return "고변동", "w", -4, "저가 구간은 변동성이 큽니다. 소액만 적합합니다."
    return "정상 구간", "g", 0, "가격 구간 자체는 과도한 위험 신호가 크지 않습니다."

def purpose_rule(p):
    rules = {
        "경기승리 / 만기 보유": (1.00, 0, "실제 승률 추정이 핵심인 기본 승리 베팅입니다."),
        "경기 시작 전 가격 상승 노림": (0.70, -6, "실제 승리보다 시장 심리와 타이밍이 중요합니다. 익절 기준을 먼저 정해야 합니다."),
        "반반 경기 쏠림 이용 / 중간 익절": (0.60, -8, "경기력이 아니라 시장 쏠림을 노리는 거래입니다. 오래 들고 가면 위험합니다."),
        "역배 / Bounce Trade": (0.35, -13, "역배와 bounce는 소액 전용입니다. 손실 제한이 핵심입니다."),
        "99¢ 상환 스캘핑": (0.20, -25, "작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."),
        "뉴스/이벤트 선반영": (0.50, -12, "조건문과 resolution 기준 확인이 중요합니다."),
    }
    return rules.get(p, (1.0, 0, "일반 베팅으로 계산합니다."))

def market_type_rule(m):
    rules = {
        "Match Moneyline": (1.00, 0, "가장 기본적인 시장입니다."),
        "Game Winner": (0.50, -10, "단판 시장은 변동성이 커서 추천 금액을 50% 줄입니다."),
        "Correct Score": (0.25, -25, "Correct Score는 맞히기 어렵습니다. 강한 경고 대상입니다."),
        "정치 선거": (0.50, -12, "결과 기준과 이의제기 가능성을 확인해야 합니다."),
        "뉴스/이벤트": (0.50, -12, "조건문과 resolution 기준 확인이 필수입니다."),
        "99¢ 상환 스캘핑": (0.20, -25, "고가 상환 스캘핑은 고액 금지입니다."),
        "2~5¢ Bounce Trade": (0.20, -18, "초저가 bounce는 소액 전용입니다."),
    }
    return rules.get(m, (1.0, 0, "일반 시장으로 계산합니다."))

def size_rule(pct):
    if pct >= 50: return "시스템 실패", "b", -100, "계좌 생존 리스크입니다. 50% 이상 노출은 절대 금지입니다."
    if pct >= 20: return "진입 금지", "b", -85, "20% 이상은 진입 금지급 노출입니다."
    if pct >= 10: return "매우 위험", "b", -38, "10~20%는 매우 큰 포지션입니다. 일부 축소가 우선입니다."
    if pct >= 5: return "위험", "w", -20, "5~10%는 위험 구간입니다. 확신보다 손실 가능액을 먼저 봐야 합니다."
    if pct >= 3: return "주의", "w", -8, "3~5%는 주의 구간입니다."
    return "정상", "g", 5, "0~3%는 포지션 크기상 정상 범위입니다."

def exposure_rule(pct):
    if pct >= 20: return "중복 노출 금지", "b", -60, "같은 경기·방향 총 노출이 20% 이상입니다."
    if pct >= 10: return "중복 노출 위험", "b", -35, "같은 경기·방향 총 노출이 10~20%입니다."
    if pct >= 5: return "중복 노출 주의", "w", -12, "같은 경기·방향 총 노출이 5~10%입니다."
    return "정상", "g", 0, "중복 노출은 관리 가능한 범위입니다."

def confidence_cap(c):
    return {"관찰용": 15, "낮은 확신": 25, "중간 확신": 50, "높은 확신": 70, "초고확신": 70}.get(c, 50)

def portfolio_cap(bankroll, c):
    pct = {"관찰용": .01, "낮은 확신": .02, "중간 확신": .04, "높은 확신": .06, "초고확신": .08}.get(c, .04)
    return bankroll * pct


# =====================================================
# Entry engine
# =====================================================
def calculate_entry(d):
    current_price, fair_price = d["current_price"], d["fair_price"]
    stake, bankroll = d["stake"], d["bankroll"]
    edge = fair_price - current_price
    position_pct = stake / bankroll * 100 if bankroll else 0

    zone_label, zone_kind, zone_pen, zone_note = price_zone(current_price)
    p_mult, p_pen, p_note = purpose_rule(d["purpose"])
    m_mult, m_pen, m_note = market_type_rule(d["market_type"])
    size_label, size_kind, size_pen, size_note = size_rule(position_pct)

    base_cap = min(confidence_cap(d["confidence"]), portfolio_cap(bankroll, d["confidence"]), d["emotional_limit"])
    rec_cap = base_cap * p_mult * m_mult
    if d["fomo_count"] >= 1:
        rec_cap *= 0.5

    if stake >= 200: cap_label, cap_kind, cap_pen = "$200 이상 시스템 실패", "b", -90
    elif stake >= 100: cap_label, cap_kind, cap_pen = "$100 이상 강한 경고", "b", -50
    elif stake > rec_cap * 1.2: cap_label, cap_kind, cap_pen = "추천 상한선 초과", "b", -32
    elif stake > rec_cap: cap_label, cap_kind, cap_pen = "상한선 소폭 초과", "w", -12
    else: cap_label, cap_kind, cap_pen = "상한선 이내", "g", 0

    dup_total = d["duplicate_ml"] + d["duplicate_game"] + d["duplicate_side"] + stake
    dup_pct = dup_total / bankroll * 100 if bankroll else 0
    exp_label, exp_kind, exp_pen, exp_note = exposure_rule(dup_pct)

    if d["fomo_count"] >= 3: fomo_label, fomo_kind, fomo_pen, fomo_note = "감정 진입 금지", "b", -75, "감정 체크 3개 이상입니다. 신규 진입 금지로 봐야 합니다."
    elif d["fomo_count"] >= 1: fomo_label, fomo_kind, fomo_pen, fomo_note = "감정 위험", "w", -20, "감정 체크가 있습니다. 추천 금액을 50% 줄였습니다."
    else: fomo_label, fomo_kind, fomo_pen, fomo_note = "정상", "g", 0, "감정 체크가 없습니다."

    if d["previous_good_price"] > 0:
        gap = current_price - d["previous_good_price"]
        if gap >= 30: chase = ("FOMO 추격", "b", -25, "처음 봤던 가격보다 30¢ 이상 올랐습니다. 추격매수 위험이 큽니다.")
        elif gap >= 15: chase = ("추격 위험", "w", -13, "처음 봤던 가격보다 많이 올라 진입가 매력이 줄었습니다.")
        elif gap >= 5: chase = ("조금 상승", "w", -5, "처음 봤던 가격보다 조금 올랐습니다.")
        else: chase = ("추격 아님", "g", 5, "처음 봤던 가격 대비 추격 위험은 크지 않습니다.")
    else:
        gap, chase = 0, ("미입력", "i", 0, "처음 봤던 저평가 가격을 입력하지 않았습니다.")
    chase_label, chase_kind, chase_pen, chase_note = chase

    bk = d["bookmaker_prob"]
    my_vs_poly = fair_price - current_price
    book_vs_poly = bk - current_price if bk > 0 else 0
    my_vs_book = fair_price - bk if bk > 0 else 0
    if bk <= 0: book = ("북메이커 미입력", "i", 0, "북메이커 기준 승률을 입력하면 공식 배당과의 괴리를 같이 볼 수 있습니다.")
    elif my_vs_book >= 10: book = ("과신 재검토", "b", -12, "내 적정가가 북메이커보다 10%p 이상 높습니다. 과신 가능성을 재검토하세요.")
    elif book_vs_poly >= 5: book = ("외부배당도 저평가", "g", 6, "북메이커 기준으로도 Polymarket 가격이 싸 보입니다.")
    elif book_vs_poly <= -5: book = ("외부배당 기준 비쌈", "w", -8, "북메이커 기준으로는 Polymarket 가격이 비싼 편입니다.")
    else: book = ("큰 차이 없음", "i", 0, "북메이커와 Polymarket 가격 차이가 크지 않습니다.")
    book_label, book_kind, book_pen, book_note = book

    value_score = clamp(50 + edge * 2.2 + zone_pen + p_pen + m_pen + chase_pen + book_pen)
    final_score = clamp(value_score + size_pen + exp_pen + fomo_pen + cap_pen)

    hard_stop = None
    if position_pct >= 50: hard_stop = "시스템 실패 — 계좌 생존 리스크"
    elif stake >= 200: hard_stop = "시스템 실패 — $200 이상"
    elif position_pct >= 20: hard_stop = "진입 금지 — 포트폴리오 20% 이상"
    elif dup_pct >= 20: hard_stop = "진입 금지 — 중복 노출 20% 이상"
    elif d["fomo_count"] >= 3: hard_stop = "진입 금지 — 감정 배팅 위험"

    if hard_stop: decision, level = hard_stop, "bad"
    elif final_score >= 75: decision, level = "진입 적절", "good"
    elif final_score >= 60: decision, level = "소액 진입 가능", "warn"
    elif final_score >= 45: decision, level = "관망 우선", "warn"
    else: decision, level = "진입 부적절", "bad"

    shares = stake / (current_price / 100)
    win_profit = shares - stake
    target_profit = shares * (d["target_price"] / 100) - stake
    stop_loss_amt = stake - shares * (d["stop_price"] / 100)
    rr = target_profit / stop_loss_amt if stop_loss_amt > 0 else 0

    if target_profit > 0 and stop_loss_amt > 0:
        if stop_loss_amt > target_profit: rr_text, rr_kind = f"손절 손실이 목표 수익보다 약 {stop_loss_amt/target_profit:.1f}배 큽니다.", "b"
        elif target_profit >= stop_loss_amt * 1.5: rr_text, rr_kind = f"목표 수익이 손절 손실보다 약 {target_profit/stop_loss_amt:.1f}배 큽니다.", "g"
        else: rr_text, rr_kind = f"목표 수익과 손절 손실 차이가 크지 않습니다. 손익비 {rr:.2f}:1 입니다.", "w"
    else:
        rr_text, rr_kind = "목표가 또는 손절가 설정을 다시 확인하세요.", "w"

    current_value = shares * (current_price / 100)
    additional_to_100 = shares - current_value
    high_warn = ""
    if current_price >= 90:
        high_warn = f"현재부터 100¢까지 추가수익은 {money(additional_to_100)}뿐입니다. 반대로 틀리면 현재 평가금 {money(current_value)}를 잃을 수 있습니다."
    if current_price >= 97:
        high_warn += " 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."

    if edge >= 10: edge_reason = ("g", f"가격 메리트 좋음 — 내 적정가가 현재가보다 {edge:.1f}¢ 높습니다.")
    elif edge >= 5: edge_reason = ("w", f"가격 메리트 약간 있음 — edge {edge:.1f}¢ 입니다.")
    elif edge < 0: edge_reason = ("b", f"가격 메리트 없음 — 현재가가 내 적정가보다 {abs(edge):.1f}¢ 비쌉니다.")
    else: edge_reason = ("w", f"가격 메리트 작음 — edge {edge:.1f}¢ 입니다.")

    reasons = [
        edge_reason,
        (size_kind, f"포지션 크기 — 총자산의 {position_pct:.1f}%, {size_label}"),
        (cap_kind, f"추천 상한선 {money(rec_cap)}, 현재 투자금 {money(stake)} — {cap_label}"),
        (zone_kind, f"가격 구간 — {zone_label}. {zone_note}"),
    ]

    return {
        **d, "edge": edge, "position_pct": position_pct,
        "duplicate_total": dup_total, "duplicate_pct": dup_pct, "rec_cap": rec_cap,
        "value_score": round(value_score, 1), "final_score": round(final_score, 1),
        "decision": decision, "level": level, "shares": shares,
        "win_profit": win_profit, "target_profit": target_profit,
        "stop_loss_amt": stop_loss_amt, "rr": rr, "rr_text": rr_text, "rr_kind": rr_kind,
        "current_value": current_value, "additional_to_100": additional_to_100,
        "high_warn": high_warn,
        "zone_label": zone_label, "zone_kind": zone_kind, "zone_note": zone_note,
        "purpose_note": p_note, "market_type_note": m_note,
        "size_label": size_label, "size_kind": size_kind, "size_note": size_note,
        "cap_label": cap_label, "cap_kind": cap_kind,
        "exp_label": exp_label, "exp_kind": exp_kind, "exp_note": exp_note,
        "fomo_label": fomo_label, "fomo_kind": fomo_kind, "fomo_note": fomo_note,
        "chase_label": chase_label, "chase_kind": chase_kind, "chase_note": chase_note,
        "book_label": book_label, "book_kind": book_kind, "book_note": book_note,
        "my_vs_poly": my_vs_poly, "book_vs_poly": book_vs_poly, "my_vs_book": my_vs_book,
        "reasons": reasons,
    }


# =====================================================
# Position engine
# =====================================================
def evaluate_position(d):
    cp, shares, inv, bankroll = d["current_price"], d["shares"], d["investment"], d["bankroll"]
    current_value = shares * (cp / 100)
    pnl = current_value - inv
    roi = pnl / inv * 100 if inv else 0
    position_pct = current_value / bankroll * 100 if bankroll else 0
    additional = shares - current_value

    reasons, warnings = [], []

    if cp >= d["target_price"]:
        decision, level = "목표가 도달 — 매도·부분매도 고려", "warn"
        reasons.append("목표가에 도달했습니다. 최소 일부 익절을 검토할 구간입니다.")
    elif cp <= d["stop_price"] and current_value >= inv * 0.3:
        decision, level = "손절 고려", "bad"
        reasons.append("손절가 이하이고 회수 가능한 금액이 아직 남아 있습니다.")
    elif current_value <= inv * 0.1:
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
        warnings.append("포트폴리오 비중 10% 이상입니다. 일부 축소 권장.")
        if level != "bad":
            decision, level = "홀딩 가능, 단 포지션 크기 과대", "warn"
    if d["fomo_count"] >= 3:
        warnings.append("감정 체크 3개 이상입니다. 신규·추가매수 금지, 축소 우선.")
        decision, level = "감정 리스크 과대 — 추가매수 금지", "bad"
    elif d["fomo_count"] >= 1:
        warnings.append("감정 체크가 있습니다. 섣부른 추가매수에 주의하세요.")

    zl, zk, _, zn = price_zone(cp)
    if cp >= 80:
        warnings.append(zn)
    if not warnings:
        warnings.append("현재 큰 위험 신호는 없지만 목표가·손절가 기준은 유지해야 합니다.")

    return {**d, "decision": decision, "level": level, "current_value": current_value,
            "pnl": pnl, "roi": roi, "position_pct": position_pct, "additional": additional,
            "reasons": reasons, "warnings": warnings}


def partial_rows(shares, price_cent, investment):
    pd_ = price_cent / 100
    rows, need = [], None
    if shares > 0 and pd_ > 0:
        need = investment / (shares * pd_) * 100
    for ratio in [25, 50, 70, 80, 90, 100]:
        ss = shares * ratio / 100
        rec = ss * pd_
        rem = shares - ss
        rows.append({
            "매도 비율": f"{ratio}%",
            "매도 수량": round(ss, 2),
            "회수금": money(rec),
            "원금 대비 확정손익": signed_money(rec - investment),
            "남은 수량": round(rem, 2),
            "남은 평가금": money(rem * pd_),
            "100¢ 추가수익": signed_money(rem * (1 - pd_)),
        })
    return rows, need


# =====================================================
# Claude AI analysis (with prompt fallback)
# =====================================================
def get_api_key():
    for fn in (lambda: st.secrets["ANTHROPIC_API_KEY"],
               lambda: st.secrets["anthropic"]["api_key"],
               lambda: st.secrets["anthropic"]["ANTHROPIC_API_KEY"]):
        try:
            k = str(fn()).strip()
            if k.startswith("sk-"):
                return k
        except Exception:
            continue
    return None


def build_prompt(team_a, team_b, league, current_price, fair_price, purpose):
    return f"""당신은 LoL e스포츠 배팅 분석 전문가입니다. 아래 경기를 배팅 관점에서 분석해주세요.

경기: {team_a} vs {team_b}
리그: {league}
{team_a}의 현재 Polymarket 배당: {current_price}¢
사용자의 적정가 추정: {fair_price}¢
배팅 목적: {purpose}

아래 6개 항목을 순서대로, 각 항목 앞에 "1." 형식 번호를 붙여서, 항목당 2~3문장으로 분석해주세요.

1. 리그 순위 — {league} 기준 두 팀의 현재 순위
2. 시즌 전적 — 각 팀의 승패 기록
3. 최근 폼 — 최근 5경기 흐름, 연승·연패 여부
4. 상대 전적 — 두 팀의 직접 맞대결 기록
5. 팀 변수 — 로스터, 부진 선수, 특이사항
6. 가격 판단 — {current_price}¢ 배당이 실제 승률 대비 싼지 비싼지

마지막 줄은 반드시 이 형식으로: 결론: 배팅 추천 / 비추천 / 중립 중 하나
한국어로 답변해주세요."""


def call_claude(prompt):
    key = get_api_key()
    if not key:
        return None, "no_key"
    try:
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["content"][0]["text"], None
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except Exception as e:
        return None, str(e)


def render_ai(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    title, body = "", []
    blocks = []
    verdict = ""
    for l in lines:
        if len(l) > 2 and l[0].isdigit() and l[1] == ".":
            if title:
                blocks.append((title, " ".join(body)))
            title, body = l, []
        elif l.startswith("결론"):
            if title:
                blocks.append((title, " ".join(body)))
                title, body = "", []
            verdict = l
        else:
            body.append(l)
    if title and body:
        blocks.append((title, " ".join(body)))

    if verdict:
        kind = "g" if ("추천" in verdict and "비추천" not in verdict) else "b" if "비추천" in verdict else "w"
        st.markdown(
            f"""<div class="verdict" style="border-top:none;padding-top:6px;">
<div class="v-title" style="font-size:30px;"><span class="dot {kind}"></span>{verdict.replace("결론:", "").strip()}</div>
<div class="v-sub">Claude 분석 결론</div></div>""",
            unsafe_allow_html=True,
        )
    for t, b in blocks:
        st.markdown(f'<div class="ai-block"><div class="a-key">{t}</div><div class="a-body">{b}</div></div>', unsafe_allow_html=True)


# =====================================================
# URL helper
# =====================================================
def extract_slug(url):
    path = urllib.parse.urlparse(url.strip()).path.strip("/")
    return path.split("/")[-1] if path else ""

@st.cache_data(ttl=60, show_spinner=False)
def fetch_gamma(slug):
    api = f"https://gamma-api.polymarket.com/events?slug={urllib.parse.quote(slug)}"
    req = urllib.request.Request(api, headers={"User-Agent": "Memento/3.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))

def parse_list(v):
    if isinstance(v, list): return v
    if isinstance(v, str):
        try: return json.loads(v)
        except Exception: return []
    return []

def extract_markets(payload):
    events = payload if isinstance(payload, list) else payload.get("events", [])
    rows = []
    for event in events:
        for m in event.get("markets", []):
            q = m.get("question") or m.get("title") or m.get("slug") or "Unknown"
            outs, prices, tokens = parse_list(m.get("outcomes")), parse_list(m.get("outcomePrices")), parse_list(m.get("clobTokenIds"))
            for i, o in enumerate(outs):
                price = None
                if i < len(prices):
                    try: price = round(float(prices[i]) * 100, 2)
                    except Exception: price = None
                rows.append({"시장": q, "선택지": o, "현재가 (¢)": price, "token_id": tokens[i] if i < len(tokens) else ""})
    return rows


# =====================================================
# Render: entry result
# =====================================================
def render_entry_result(r):
    if not r:
        st.markdown(
            """<div class="quiet">
<div class="q-title">판독 결과가 여기에 표시됩니다</div>
<div class="q-body">오른쪽에서 시장 정보와 투자금을 입력하고<br>판독하기를 누르세요.</div>
</div>""",
            unsafe_allow_html=True,
        )
        return

    k = verdict_dot(r["level"])
    score_word = "적절성" if r["level"] != "bad" else "부적절도"
    score_val = r["final_score"] if r["level"] != "bad" else 100 - r["final_score"]

    st.markdown(
        f"""<div class="verdict">
<div class="eyebrow">판정</div>
<div class="v-title"><span class="dot {k}"></span>{r["decision"]}</div>
<div class="v-sub">{r["market_name"]} · {score_word} {score_val:.0f}% · 규모 제외 순수 가치 {r["value_score"]:.0f}% · {r["purpose"]}</div>
</div>""",
        unsafe_allow_html=True,
    )

    edge_tone = "pos" if r["edge"] >= 5 else "neg" if r["edge"] < 0 else ""
    pos_tone = "neg" if r["position_pct"] >= 10 else ""
    st.markdown(
        '<div class="stats">'
        + stat("현재가", cents(r["current_price"]), "시장 implied probability")
        + stat("Edge", f"{r['edge']:+.1f}¢", "내 적정가 대비", edge_tone)
        + stat("포트폴리오 비중", f"{r['position_pct']:.1f}%", r["size_label"], pos_tone)
        + stat("추천 상한선", money(r["rec_cap"]), f"현재 투자금 {money(r['stake'])}")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        meter("리스크 포함 최종 적절성", r["final_score"], 100,
              "g" if r["final_score"] >= 70 else "w" if r["final_score"] >= 50 else "b")
        + meter("배팅 규모 제외 순수 가치", r["value_score"], 100, "i")
        + meter("포트폴리오 사용 비중 (%)", min(r["position_pct"], 100), 100,
                "b" if r["position_pct"] >= 20 else "w" if r["position_pct"] >= 5 else "g")
        + meter("현재가 위치 (¢)", r["current_price"], 100, "i"),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eyebrow" style="margin-top:22px;">핵심 판단 근거</div>', unsafe_allow_html=True)
    notes = "".join(line(t, kk) for kk, t in r["reasons"])
    if r["fomo_count"] > 0:
        notes += line(r["fomo_note"], r["fomo_kind"])
    if r["duplicate_pct"] >= 5:
        notes += line(r["exp_note"], r["exp_kind"])
    if r["high_warn"]:
        notes += line(r["high_warn"], "b")
    st.markdown(notes, unsafe_allow_html=True)

    with st.expander("상세 리포트"):
        st.markdown(
            '<div class="spec">'
            + spec_row("진입가격 구간", f"현재가 <b>{cents(r['current_price'])}</b> — {r['zone_note']}", r["zone_label"], r["zone_kind"])
            + spec_row("배팅금액 · 계좌 생존", f"투자금 <b>{money(r['stake'])}</b> / 총자산 <b>{money(r['bankroll'])}</b> · 비중 <b>{r['position_pct']:.1f}%</b><br>{r['size_note']}", r["size_label"], r["size_kind"])
            + spec_row("북메이커 비교", f"내 적정가−현재가 <b>{r['my_vs_poly']:+.1f}%p</b> · 북메이커−현재가 <b>{r['book_vs_poly']:+.1f}%p</b> · 내 적정가−북메이커 <b>{r['my_vs_book']:+.1f}%p</b><br>{r['book_note']}", r["book_label"], r["book_kind"])
            + spec_row("추천 상한선", f"상한선 <b>{money(r['rec_cap'])}</b> · 현재 투자금 <b>{money(r['stake'])}</b> · 확신 수준 <b>{r['confidence']}</b>", r["cap_label"], r["cap_kind"])
            + spec_row("손익비", f"목표가 도달 시 <b>{money(r['target_profit'])}</b> · 손절 시 <b>{money(r['stop_loss_amt'])}</b><br>{r['rr_text']}", f"{r['rr']:.2f} : 1", r["rr_kind"])
            + spec_row("감정 · FOMO", f"체크 <b>{r['fomo_count']}개</b> — {r['fomo_note']}", r["fomo_label"], r["fomo_kind"])
            + spec_row("중복 노출", f"같은 경기·방향 총 노출 <b>{money(r['duplicate_total'])}</b> · 총자산 대비 <b>{r['duplicate_pct']:.1f}%</b><br>{r['exp_note']}", r["exp_label"], r["exp_kind"])
            + spec_row("추격매수 점검", r["chase_note"], r["chase_label"], r["chase_kind"])
            + spec_row("배팅 목적 · 시장 유형", f"<b>{r['purpose']}</b> — {r['purpose_note']}<br><b>{r['market_type']}</b> — {r['market_type_note']}", "구조 분석", "i")
            + "</div>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="eyebrow" style="margin-top:24px;">수익 · 손실 시나리오</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="stats">'
            + stat("보유 수량", f"{r['shares']:.2f}주", "투자금 ÷ 현재가")
            + stat("승리 시 순이익", money(r["win_profit"]), "100¢ 상환 기준", "pos")
            + stat("패배 시 손실", money(-r["stake"]), "전액 손실 가정", "neg")
            + stat("100¢까지 추가수익", money(r["additional_to_100"]), "남은 업사이드")
            + "</div>",
            unsafe_allow_html=True,
        )

        summary = (
            f"{r['market_name']} | 현재가 {r['current_price']:.0f}¢ · 적정가 {r['fair_price']:.0f}¢ · Edge {r['edge']:+.0f}¢ | "
            f"투자금 {money(r['stake'])} · 비중 {r['position_pct']:.1f}% | 판정: {r['decision']} | "
            f"적절성 {r['final_score']:.0f}% · 순수 가치 {r['value_score']:.0f}%"
        )
        st.markdown('<div class="eyebrow" style="margin-top:20px;">기록용 한 줄 요약</div>', unsafe_allow_html=True)
        st.code(summary)


# =====================================================
# Render: position result
# =====================================================
def render_position_result(r):
    if not r:
        st.markdown(
            """<div class="quiet">
<div class="q-title">포지션 결과가 여기에 표시됩니다</div>
<div class="q-body">오른쪽에서 현재가와 보유 수량을 입력하면<br>매도·홀딩 판단을 보여드립니다.</div>
</div>""",
            unsafe_allow_html=True,
        )
        return

    k = verdict_dot(r["level"])
    st.markdown(
        f"""<div class="verdict">
<div class="eyebrow">포지션 판정</div>
<div class="v-title"><span class="dot {k}"></span>{r["decision"]}</div>
<div class="v-sub">{r["name"]} · 현재가 {cents(r["current_price"])} 기준</div>
</div>""",
        unsafe_allow_html=True,
    )

    pnl_tone = "pos" if r["pnl"] >= 0 else "neg"
    st.markdown(
        '<div class="stats">'
        + stat("현재 평가금", money(r["current_value"]), "현재가 × 보유수량")
        + stat("즉시 매도 손익", signed_money(r["pnl"]), f"수익률 {signed_pct(r['roi'])}", pnl_tone)
        + stat("100¢ 상환 총액", money(r["shares"]), "승리 시 총액")
        + stat("실패 시 손실", money(-r["current_value"]), "현재 평가금 전액", "neg")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        meter("현재 수익률 (%)", max(r["roi"], 0), 100, "g" if r["roi"] >= 0 else "b")
        + meter("포트폴리오 비중 (%)", min(r["position_pct"], 100), 100,
                "b" if r["position_pct"] >= 20 else "w" if r["position_pct"] >= 10 else "g")
        + meter("현재가 위치 (¢)", r["current_price"], 100, "i"),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eyebrow" style="margin-top:20px;">판단 근거</div>', unsafe_allow_html=True)
    notes = "".join(line(t, "g") for t in r["reasons"])
    for w in r["warnings"]:
        kind = "b" if ("금지" in w or "손절" in w or "20%" in w) else "w"
        notes += line(w, kind)
    st.markdown(notes, unsafe_allow_html=True)

    rows, need = partial_rows(r["shares"], r["current_price"], r["investment"])
    st.markdown('<div class="eyebrow" style="margin-top:22px;">부분매도 시나리오</div>', unsafe_allow_html=True)
    if need is not None:
        if need <= 100:
            st.markdown(line(f"원금 회수에 필요한 최소 매도 비율은 <b>{need:.1f}%</b>입니다.", "g"), unsafe_allow_html=True)
        else:
            st.markdown(line(f"현재 가격에서는 100% 팔아도 원금 회수가 어렵습니다. 필요 비율 {need:.1f}%.", "w"), unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# =====================================================
# Masthead
# =====================================================
st.markdown(
    """<div class="masthead">
<div class="name">Memento</div>
<div class="tag">Polymarket 배팅 판단 · 계좌를 지키는 수동 리스크 관리</div>
</div>""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["진입 판독", "포지션 관리", "부분매도", "거래일지", "URL 도우미"])


# =====================================================
# Tab 1 — Entry
# =====================================================
with tab1:
    left, right = st.columns([1.05, 0.95], gap="large")

    with right:
        st.markdown('<div class="eyebrow" style="margin-top:8px;">입력</div>', unsafe_allow_html=True)
        with st.form("entry_form"):
            market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner")
            c0a, c0b = st.columns(2)
            with c0a:
                team_a = st.text_input("내가 보는 팀", "T1")
            with c0b:
                team_b = st.text_input("상대 팀", "HLE")
            league = st.selectbox("리그", ["LCK", "LPL", "LEC", "LCS", "MSI/Worlds", "기타"])

            c1, c2 = st.columns(2)
            with c1:
                current_price = st.number_input("현재가 (¢)", 1.0, 99.0, 52.0)
                stake = st.number_input("투자금 ($)", 1.0, value=50.0)
            with c2:
                fair_price = st.number_input("내 적정가 (¢)", 1.0, 99.0, 65.0)
                bankroll = st.number_input("총자산 ($)", 1.0, value=814.0)

            c3, c4 = st.columns(2)
            with c3:
                purpose = st.selectbox("배팅 목적", [
                    "경기승리 / 만기 보유", "경기 시작 전 가격 상승 노림",
                    "반반 경기 쏠림 이용 / 중간 익절", "역배 / Bounce Trade",
                    "99¢ 상환 스캘핑", "뉴스/이벤트 선반영"])
            with c4:
                market_type = st.selectbox("시장 유형", [
                    "Match Moneyline", "Game Winner", "Correct Score",
                    "정치 선거", "뉴스/이벤트", "99¢ 상환 스캘핑", "2~5¢ Bounce Trade"])

            with st.expander("고급 설정"):
                a, b, c = st.columns(3)
                with a:
                    emotional_limit = st.number_input("감정 한도 ($)", 1.0, value=50.0)
                    confidence = st.selectbox("확신 수준", ["관찰용", "낮은 확신", "중간 확신", "높은 확신", "초고확신"], index=2)
                with b:
                    target_price = st.number_input("목표가 (¢)", 1.0, 100.0, 75.0)
                    stop_price = st.number_input("손절가 (¢)", 0.0, 99.0, 40.0)
                with c:
                    bookmaker_prob = st.number_input("북메이커 승률 (%)", 0.0, 99.0, 0.0)
                    previous_good_price = st.number_input("처음 봤던 가격 (¢)", 0.0, 99.0, 0.0)

                st.markdown('<div class="eyebrow" style="margin-top:14px;">중복 노출 ($)</div>', unsafe_allow_html=True)
                d1, d2, d3 = st.columns(3)
                with d1:
                    duplicate_ml = st.number_input("같은 경기 ML", 0.0, value=0.0)
                with d2:
                    duplicate_game = st.number_input("Game Winner", 0.0, value=0.0)
                with d3:
                    duplicate_side = st.number_input("같은 방향 추가", 0.0, value=0.0)

                st.markdown('<div class="eyebrow" style="margin-top:14px;">감정 · FOMO 체크</div>', unsafe_allow_html=True)
                fomo_options = [
                    "방금 큰 수익을 냈다", "방금 큰 손실을 냈다", "아까 판 게 후회된다",
                    "빨리 복구하고 싶다", "더 빨리 계좌를 키우고 싶다",
                    "놓치면 아깝다고 느낀다", "이미 같은 경기에 포지션이 있다"]
                fomo_count = 0
                f1c, f2c = st.columns(2)
                for i, opt in enumerate(fomo_options):
                    with f1c if i % 2 == 0 else f2c:
                        if st.checkbox(opt, key=f"fomo_{i}"):
                            fomo_count += 1

            submitted = st.form_submit_button("판독하기", use_container_width=True)

        if submitted:
            data = dict(
                market_name=market_name, team_a=team_a, team_b=team_b, league=league,
                current_price=current_price, fair_price=fair_price, stake=stake,
                purpose=purpose, market_type=market_type, bankroll=bankroll,
                emotional_limit=emotional_limit, confidence=confidence,
                target_price=target_price, stop_price=stop_price,
                bookmaker_prob=bookmaker_prob, previous_good_price=previous_good_price,
                duplicate_ml=duplicate_ml, duplicate_game=duplicate_game,
                duplicate_side=duplicate_side, fomo_count=fomo_count,
            )
            st.session_state.last_entry = calculate_entry(data)
            prompt = build_prompt(team_a, team_b, league, current_price, fair_price, purpose)
            st.session_state.ai_prompt = prompt
            st.session_state.ai_pair = f"{team_a} vs {team_b}"
            with st.spinner("Claude가 팀을 분석하고 있습니다"):
                text, err = call_claude(prompt)
            st.session_state.ai_text = text or ""
            st.session_state.ai_error = err or ""
            st.rerun()

        # ----- AI panel -----
        st.markdown('<div class="eyebrow" style="margin-top:26px;">Claude 팀 분석</div>', unsafe_allow_html=True)
        if st.session_state.ai_text:
            st.markdown(f'<div class="footnote" style="margin-bottom:4px;">{st.session_state.ai_pair}</div>', unsafe_allow_html=True)
            render_ai(st.session_state.ai_text)
        elif st.session_state.ai_error:
            if st.session_state.ai_error == "no_key":
                st.markdown(line("API 키가 설정되어 있지 않아 자동 분석 대신 분석 프롬프트를 생성했습니다. 아래 내용을 Claude나 ChatGPT에 붙여넣으세요.", "w"), unsafe_allow_html=True)
            elif st.session_state.ai_error.startswith("http_401"):
                st.markdown(line("API 키 인증에 실패했습니다 (401). Streamlit Secrets의 ANTHROPIC_API_KEY 값을 확인한 뒤 앱을 Reboot 해주세요. 그동안 아래 프롬프트를 복사해 쓸 수 있습니다.", "b"), unsafe_allow_html=True)
            else:
                st.markdown(line(f"자동 분석에 실패했습니다 ({st.session_state.ai_error}). 아래 프롬프트를 복사해 사용하세요.", "w"), unsafe_allow_html=True)
            if st.session_state.ai_prompt:
                st.code(st.session_state.ai_prompt)
        else:
            st.markdown(
                """<div class="quiet" style="padding:40px 20px;">
<div class="q-title">판독하면 자동으로 분석합니다</div>
<div class="q-body">리그 순위, 시즌 전적, 최근 폼, 상대 전적,<br>가격 적정성까지 Claude가 정리해드립니다.</div>
</div>""",
                unsafe_allow_html=True,
            )

    with left:
        render_entry_result(st.session_state.last_entry)


# =====================================================
# Tab 2 — Position
# =====================================================
with tab2:
    left, right = st.columns([1.05, 0.95], gap="large")

    with right:
        st.markdown('<div class="eyebrow" style="margin-top:8px;">입력</div>', unsafe_allow_html=True)
        with st.form("position_form"):
            name = st.text_input("거래 이름", "KT Rolster vs Dplus KIA — Match Winner")
            p1, p2 = st.columns(2)
            with p1:
                avg_buy = st.number_input("평균 매수가 (¢)", 1.0, 99.0, 52.4)
                shares_in = st.number_input("보유 수량", 0.01, value=1164.12)
                target_price = st.number_input("목표가 (¢)", 1.0, 100.0, 60.0)
            with p2:
                current_price_p = st.number_input("현재가 (¢)", 1.0, 100.0, 58.0)
                investment = st.number_input("투자금 ($)", 1.0, value=610.0)
                stop_price_p = st.number_input("손절가 (¢)", 0.0, 99.0, 45.0)

            p3, p4 = st.columns(2)
            with p3:
                bankroll_p = st.number_input("총자산 ($)", 1.0, value=1200.0, key="pos_bankroll")
            with p4:
                fomo_p = st.slider("감정 위험 체크 수", 0, 7, 0)

            pos_submit = st.form_submit_button("포지션 판독하기", use_container_width=True)

        if pos_submit:
            st.session_state.last_position = evaluate_position(dict(
                name=name, avg_buy=avg_buy, current_price=current_price_p,
                shares=shares_in, investment=investment,
                target_price=target_price, stop_price=stop_price_p,
                bankroll=bankroll_p, fomo_count=fomo_p,
            ))
            st.rerun()

        if st.session_state.last_position:
            if st.button("현재 포지션을 목록에 저장", use_container_width=True):
                r = st.session_state.last_position
                st.session_state.tracked_positions.append({
                    "날짜": str(date.today()), "거래": r["name"], "판정": r["decision"],
                    "현재가": cents(r["current_price"]), "수익률": signed_pct(r["roi"]),
                    "평가금": money(r["current_value"]),
                })
                st.toast("저장했습니다")

        if st.session_state.tracked_positions:
            st.markdown('<div class="eyebrow" style="margin-top:24px;">저장된 포지션</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.tracked_positions), use_container_width=True, hide_index=True)

    with left:
        render_position_result(st.session_state.last_position)


# =====================================================
# Tab 3 — Partial sell
# =====================================================
with tab3:
    st.markdown('<div class="headline">부분매도 계산기</div>', unsafe_allow_html=True)
    st.markdown('<div class="subline">원금 회수에 필요한 최소 매도 비율과, 비율별 회수금·확정손익·남은 가치를 계산합니다.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        buy_price = st.number_input("매수가 (¢)", 1.0, 99.0, 16.0, key="partial_buy")
    with c2:
        cur_price = st.number_input("현재가 (¢)", 1.0, 100.0, 73.0, key="partial_current")
    with c3:
        inv = st.number_input("투자금 ($)", 0.0, value=16.08, key="partial_inv")

    manual = st.checkbox("보유 수량 직접 입력")
    if manual:
        shares_ps = st.number_input("보유 수량", 0.0, value=100.0, key="partial_shares")
    else:
        shares_ps = inv / (buy_price / 100) if buy_price > 0 else 0

    if st.button("계산하기", use_container_width=True):
        rows, need = partial_rows(shares_ps, cur_price, inv)
        cur_val = shares_ps * (cur_price / 100)
        add = shares_ps - cur_val

        st.markdown(
            '<div class="stats" style="margin-top:22px;">'
            + stat("보유 수량", f"{shares_ps:.2f}주", "투자금 기준 자동 계산" if not manual else "직접 입력")
            + stat("현재 평가금", money(cur_val), "현재가 기준")
            + stat("100¢까지 추가수익", money(add), "남은 업사이드", "pos")
            + stat("실패 시 손실", money(-cur_val), "현재 평가금 전액", "neg")
            + "</div>",
            unsafe_allow_html=True,
        )

        if need is not None:
            if need <= 100:
                st.markdown(line(f"원금 회수에 필요한 최소 매도 비율은 <b>{need:.1f}%</b>입니다.", "g"), unsafe_allow_html=True)
            else:
                st.markdown(line(f"현재 가격에서는 100% 팔아도 원금 회수가 어렵습니다. 필요 비율 {need:.1f}%.", "w"), unsafe_allow_html=True)

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.markdown(
            f'<div class="footnote">현재 평가금 {money(cur_val)}에서 100¢까지 추가로 얻을 수 있는 금액은 {money(add)}입니다. 반대로 실패하면 현재 평가금 {money(cur_val)}를 잃을 수 있습니다.</div>',
            unsafe_allow_html=True,
        )


# =====================================================
# Tab 4 — Journal
# =====================================================
with tab4:
    st.markdown('<div class="headline">거래일지</div>', unsafe_allow_html=True)
    st.markdown('<div class="subline">계좌 전체 성과와 개별 거래를 기록합니다.</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        start_bk = st.number_input("시작 자금 ($)", 0.0, value=500.0)
    with b:
        cur_bk = st.number_input("현재 총자산 ($)", 0.0, value=650.0)
    with c:
        net_dep = st.number_input("입금·출금 조정 ($)", value=0.0)

    adjusted = start_bk + net_dep
    total_p = cur_bk - adjusted
    total_r = total_p / adjusted * 100 if adjusted > 0 else 0
    k = "g" if total_p >= 0 else "b"

    st.markdown(
        f"""<div class="verdict">
<div class="eyebrow">계좌 성과</div>
<div class="v-title"><span class="dot {k}"></span>{signed_money(total_p)} <span style="font-size:24px;color:var(--gray);font-weight:500;">({signed_pct(total_r)})</span></div>
<div class="v-sub">현재 총자산 {money(cur_bk)} · 시작 자금 {money(start_bk)} · 조정 {money(net_dep)}</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eyebrow" style="margin-top:8px;">거래 등록</div>', unsafe_allow_html=True)
    with st.form("trade_form"):
        t1, t2, t3 = st.columns(3)
        with t1:
            tname = st.text_input("거래 이름", "T1 vs HLE — Match Winner")
            tbuy = st.number_input("매수가 (¢)", 1.0, 99.0, 52.0, key="log_buy")
        with t2:
            tsell = st.number_input("매도가 (¢)", 0.0, 100.0, 78.0, key="log_sell")
            tstake = st.number_input("투자금 ($)", 1.0, value=50.0, key="log_stake")
        with t3:
            tmemo = st.text_area("메모", "진입 이유 · 매도 이유 · 감정 상태", height=108)
        add = st.form_submit_button("기록 추가", use_container_width=True)

    if add:
        tsh = tstake / (tbuy / 100)
        tsa = tsh * (tsell / 100)
        tp = tsa - tstake
        tr = tp / tstake * 100
        st.session_state.trade_log.append({
            "날짜": str(date.today()), "거래": tname,
            "매수가": cents(tbuy), "매도가": cents(tsell),
            "투자금": money(tstake), "손익": signed_money(tp),
            "수익률": signed_pct(tr), "메모": tmemo,
        })
        st.toast(f"기록 추가 — {signed_money(tp)} ({signed_pct(tr)})")

    if st.session_state.trade_log:
        df = pd.DataFrame(st.session_state.trade_log)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        cdl, crs = st.columns(2)
        with cdl:
            st.download_button("CSV 내려받기", data=csv, file_name="memento_trades.csv", mime="text/csv", use_container_width=True)
        with crs:
            if st.button("거래일지 비우기", use_container_width=True):
                st.session_state.trade_log = []
                st.rerun()
    else:
        st.markdown('<div class="footnote">아직 기록된 거래가 없습니다.</div>', unsafe_allow_html=True)

    with st.expander("거래 복기 질문"):
        qs = "".join(line(q, "i") for q in [
            "원하는 가격에 진입했는가?",
            "내 예상 승률의 근거는 무엇인가?",
            "북메이커와 왜 다르게 봤는가?",
            "금액은 감당 가능한 크기였는가?",
            "매도 기준을 지켰는가?",
            "감정적으로 들어간 부분이 있었는가?",
            "다음에 반복 가능한 거래인가?",
            "놓친 수익을 손실로 착각하고 있지는 않은가?",
        ])
        st.markdown(qs, unsafe_allow_html=True)


# =====================================================
# Tab 5 — URL helper
# =====================================================
with tab5:
    st.markdown('<div class="headline">URL 도우미</div>', unsafe_allow_html=True)
    st.markdown('<div class="subline">Polymarket URL을 붙여넣으면 시장·선택지·token_id 목록을 보여드립니다.</div>', unsafe_allow_html=True)

    url = st.text_input("Polymarket 시장 URL", "https://polymarket.com/event/")

    if st.button("시장 정보 불러오기", use_container_width=True):
        slug = extract_slug(url)
        if not slug:
            st.markdown(line("URL에서 slug를 찾지 못했습니다. polymarket.com/event/… 형식인지 확인해주세요.", "b"), unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="footnote">slug: {slug}</div>', unsafe_allow_html=True)
            try:
                with st.spinner("Polymarket에서 불러오는 중"):
                    payload = fetch_gamma(slug)
                rows = extract_markets(payload)
                st.session_state.url_rows = rows
                if rows:
                    st.markdown(line(f"{len(rows)}개의 선택지를 찾았습니다.", "g"), unsafe_allow_html=True)
                else:
                    st.markdown(line("시장 후보를 찾지 못했습니다. /event/ 경로의 URL인지 확인해주세요.", "w"), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(line(f"불러오기 실패 — {e}", "b"), unsafe_allow_html=True)

    if st.session_state.url_rows:
        st.dataframe(pd.DataFrame(st.session_state.url_rows), use_container_width=True, hide_index=True)
        st.markdown('<div class="footnote">token_id는 복사해 확인용으로 사용하세요. 다음 단계에서 URL → 시장 선택 → 가격 자동 조회까지 연결할 수 있습니다.</div>', unsafe_allow_html=True)
