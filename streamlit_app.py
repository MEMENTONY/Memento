import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

# =====================================================
# Memento v5 — onboarding · personal risk profile
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
  --ink: #1d1d1f; --ink2: #424245; --gray: #86868b; --gray2: #aeaeb2;
  --hairline: #e8e8ed; --fill: #f5f5f7; --blue: #0071e3;
  --green: #1d7d4f; --green-soft: #e9f6ef;
  --red: #d0312d; --red-soft: #fdf0ef;
  --amber: #b25e09; --amber-soft: #fdf5e9;
}

html, body, .stApp { background: #ffffff !important; color: var(--ink) !important; }

*:not([data-testid="stIconMaterial"]):not(.material-icons):not([class*="material-symbols"]) {
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
}
span[data-testid="stIconMaterial"] {
  font-family: 'Material Symbols Rounded' !important;
  font-size: 19px !important;
  color: var(--gray) !important;
}

.block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 5rem; }
section[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { background: rgba(255,255,255,.85) !important; backdrop-filter: blur(14px); }
h1,h2,h3,h4,p,span,div,label { color: var(--ink); }

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
  background: var(--fill) !important; border: 1px solid transparent !important;
  border-radius: 12px !important; color: var(--ink) !important;
  font-size: 15px !important; font-weight: 450 !important; min-height: 44px;
  box-shadow: none !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
textarea:focus {
  background: #ffffff !important; border-color: var(--blue) !important;
  box-shadow: 0 0 0 4px rgba(0,113,227,.12) !important;
}
div[data-baseweb="select"] > div {
  background: var(--fill) !important; border: 1px solid transparent !important;
  border-radius: 12px !important; color: var(--ink) !important; min-height: 44px;
}
div[data-testid="stNumberInput"] button { background: transparent !important; border: none !important; color: var(--gray) !important; }
div[data-testid="stWidgetLabel"] p { font-size: 13px !important; font-weight: 500 !important; color: var(--ink2) !important; }

.stButton > button, .stFormSubmitButton > button {
  background: var(--blue) !important; color: #ffffff !important;
  border: none !important; border-radius: 980px !important;
  font-size: 15px !important; font-weight: 500 !important;
  min-height: 46px; box-shadow: none !important;
  transition: background .18s ease !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { background: #0077ed !important; color:#fff !important; }
div[data-testid="stDownloadButton"] > button {
  background: var(--fill) !important; color: var(--ink) !important;
  border: none !important; border-radius: 980px !important; font-weight: 500 !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--fill); border-radius: 12px; padding: 3px; gap: 2px;
  border: none; display: inline-flex; width: auto; flex-wrap: wrap;
}
div[data-testid="stTabs"] [data-baseweb="tab"] { border-radius: 9px !important; padding: 7px 16px !important; background: transparent !important; border: none !important; }
div[data-testid="stTabs"] [data-baseweb="tab"] p { font-size: 13.5px !important; font-weight: 500 !important; color: var(--gray) !important; }
div[data-testid="stTabs"] [aria-selected="true"] { background: #ffffff !important; box-shadow: 0 1px 4px rgba(0,0,0,.10) !important; }
div[data-testid="stTabs"] [aria-selected="true"] p { color: var(--ink) !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

div[data-testid="stRadio"] > div { gap: 4px; }
div[data-testid="stRadio"] label p { font-size: 13.5px !important; color: var(--ink2) !important; }

.stExpander { border: 1px solid var(--hairline) !important; border-radius: 14px !important; background: #ffffff !important; box-shadow: none !important; }
.stExpander summary { padding: 13px 16px !important; align-items: center !important; }
.stExpander summary p { font-size: 14px !important; font-weight: 500 !important; }

div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] { border: 1px solid var(--hairline); border-radius: 14px; overflow: hidden; }

code, pre { background: var(--fill) !important; border: none !important; border-radius: 12px !important; color: var(--ink2) !important; font-size: 12.5px !important; white-space: pre-wrap !important; }
hr { border: none; border-top: 1px solid var(--hairline); margin: 26px 0; }

.masthead { padding: 4px 0 8px 0; }
.masthead .name { font-size: 21px; font-weight: 600; letter-spacing: -.022em; }
.masthead .tag { font-size: 13px; color: var(--gray); margin-top: 2px; }

.headline { font-size: 30px; font-weight: 600; letter-spacing: -.025em; line-height: 1.12; margin: 6px 0 4px 0; }
.subline { font-size: 15px; color: var(--gray); line-height: 1.55; margin-bottom: 24px; }
.eyebrow { font-size: 12px; font-weight: 600; color: var(--gray); letter-spacing: .06em; text-transform: uppercase; margin-bottom: 8px; }

.verdict { padding: 26px 0 20px 0; border-top: 1px solid var(--hairline); }
.verdict .v-title { font-size: 42px; font-weight: 600; letter-spacing: -.03em; line-height: 1.08; }
.verdict .v-sub { margin-top: 10px; font-size: 15px; color: var(--gray); line-height: 1.6; }
.dot { display:inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 10px; vertical-align: 4px; }
.dot.g { background: var(--green); } .dot.w { background: var(--amber); }
.dot.b { background: var(--red); } .dot.i { background: var(--gray2); }

.stats { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline); margin: 4px 0 24px 0; }
.stats.three { grid-template-columns: repeat(3, 1fr); }
.stat { padding: 18px 18px 18px 0; border-right: 1px solid var(--hairline); }
.stat:last-child { border-right: none; }
.stat + .stat { padding-left: 18px; }
.stat .s-label { font-size: 12px; font-weight: 500; color: var(--gray); }
.stat .s-value { margin-top: 6px; font-size: 25px; font-weight: 600; letter-spacing: -.025em; font-variant-numeric: tabular-nums; }
.stat .s-value.pos { color: var(--green); } .stat .s-value.neg { color: var(--red); }
.stat .s-note { margin-top: 4px; font-size: 12px; color: var(--gray2); }

.spec { border-top: 1px solid var(--hairline); }
.spec-row { display: grid; grid-template-columns: 190px 1fr auto; gap: 20px; padding: 16px 0; border-bottom: 1px solid var(--hairline); align-items: start; }
.spec-key { font-size: 13.5px; font-weight: 500; color: var(--gray); padding-top: 1px; }
.spec-val { font-size: 14.5px; color: var(--ink2); line-height: 1.6; }
.spec-val b { color: var(--ink); font-weight: 600; }
.state { font-size: 12.5px; font-weight: 500; white-space: nowrap; padding: 4px 11px; border-radius: 980px; }
.state.g { background: var(--green-soft); color: var(--green); }
.state.w { background: var(--amber-soft); color: var(--amber); }
.state.b { background: var(--red-soft); color: var(--red); }
.state.i { background: var(--fill); color: var(--gray); }

.line { display: flex; gap: 12px; padding: 11px 0; border-bottom: 1px solid var(--hairline); font-size: 14px; color: var(--ink2); line-height: 1.6; align-items: baseline; }
.line:last-child { border-bottom: none; }

/* meter with verdict pill */
.meter { margin: 16px 0; }
.meter .m-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.meter .m-label { font-size: 13.5px; color: var(--ink2); font-weight: 600; }
.meter .m-right { display: flex; gap: 10px; align-items: baseline; }
.meter .m-num { font-size: 16px; font-weight: 600; font-variant-numeric: tabular-nums; }
.meter .m-num.g { color: var(--green); } .meter .m-num.w { color: var(--amber); }
.meter .m-num.b { color: var(--red); } .meter .m-num.i { color: var(--ink); }
.meter .m-track { height: 5px; border-radius: 980px; background: var(--hairline); overflow: hidden; }
.meter .m-fill { height: 100%; border-radius: 980px; }
.meter .state { font-size: 12.5px; padding: 4px 12px; font-weight: 600; }

.quiet { border: 1px dashed var(--hairline); border-radius: 16px; padding: 58px 24px; text-align: center; }
.quiet .q-title { font-size: 16px; font-weight: 600; }
.quiet .q-body { margin-top: 8px; font-size: 13.5px; color: var(--gray); line-height: 1.65; }

.ai-block { border-top: 1px solid var(--hairline); padding: 15px 0; }
.ai-block .a-key { font-size: 12px; font-weight: 600; color: var(--gray); letter-spacing: .05em; text-transform: uppercase; }
.ai-block .a-body { margin-top: 7px; font-size: 14.5px; color: var(--ink2); line-height: 1.7; }

.footnote { font-size: 12px; color: var(--gray2); line-height: 1.6; margin-top: 10px; }

.ob-step { font-size: 12px; font-weight: 600; color: var(--blue); letter-spacing: .06em; text-transform: uppercase; margin-bottom: 6px; }

@media (max-width: 880px) {
  .stats { grid-template-columns: repeat(2, 1fr); }
  .spec-row { grid-template-columns: 1fr; gap: 6px; }
  .verdict .v-title { font-size: 30px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# State
# =====================================================
DEFAULTS = {
    "lang": "ko",
    "profile": None,           # set by onboarding
    "last_entry": None,
    "last_position": None,
    "trade_log": [],
    "portfolio": [],
    "cash": 0.0,
    "adj_month": 0.0,          # pre-app P&L adjustments
    "adj_year": 0.0,
    "url_rows": [],
    "ai_text": "", "ai_error": "", "ai_prompt": "", "ai_pair": "",
    "wallet_raw": [],
    "reviews": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def t(ko, en):
    return ko if st.session_state.lang == "ko" else en


def profile():
    p = st.session_state.profile
    if p:
        return p
    return {"assets": 1000.0, "start_capital": 1000.0, "start_when": "",
            "freq": "", "cats": [], "emotional_limit": 50.0,
            "max_pct": 3.0, "block_pct": 12.0, "loss_reaction": ""}


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

def meter(label, value, kind, verdict, max_v=100, unit=""):
    """Meter with explicit colored verdict pill so good/bad is obvious."""
    color = {"g": "var(--green)", "w": "var(--amber)", "b": "var(--red)", "i": "var(--ink)"}.get(kind, "var(--ink)")
    width = clamp(value / max_v * 100 if max_v else 0)
    return f"""<div class="meter">
<div class="m-row">
  <span class="m-label">{label}</span>
  <span class="m-right"><span class="m-num {kind}">{value:.1f}{unit}</span><span class="state {kind}">{verdict}</span></span>
</div>
<div class="m-track"><div class="m-fill" style="width:{width:.1f}%;background:{color};"></div></div>
</div>"""

def line(text, kind="i"):
    return f'<div class="line"><span class="dot {kind}"></span><span>{text}</span></div>'

def verdict_dot(level):
    return {"good": "g", "warn": "w", "bad": "b"}.get(level, "i")

def grade_word(kind):
    return {"g": t("좋음", "Good"), "w": t("주의", "Caution"), "b": t("위험", "Risk"), "i": t("보통", "Neutral")}[kind]


# =====================================================
# Rules — thresholds come from the user's profile
# =====================================================
def price_zone(price):
    if price >= 99: return t("99¢ 매수 금지", "Do not buy at 99¢"), "b", -32, t("99¢는 사는 가격이 아니라 파는 가격입니다.", "99¢ is a selling price, not a buying price.")
    if price >= 95: return t("상환 스캘핑", "Redemption scalping"), "b", -24, t("95~98¢는 거의 상환 스캘핑입니다. 고액 신규 매수 금지에 가깝습니다.", "95–98¢ is near-redemption scalping. Avoid large new buys.")
    if price >= 90: return t("신규매수 비추천", "New buys discouraged"), "b", -18, t("90~95¢는 신규 매수 비추천 구간입니다.", "90–95¢ is a discouraged range for new buys.")
    if price >= 85: return t("매우 신중", "Be very cautious"), "w", -10, t("85~90¢는 신규 진입을 매우 신중하게 봐야 합니다.", "85–90¢ requires extra caution.")
    if price >= 80: return t("익절 고려", "Take-profit zone"), "w", -6, t("80~85¢는 신규 매수보다 익절 고려 구간입니다.", "80–85¢ favors taking profit over new buys.")
    if 2 <= price <= 5: return t("초저가 Bounce", "Deep-value bounce"), "w", -12, t("2~5¢ Bounce Trade는 소액 전용입니다.", "2–5¢ bounce trades are small-size only.")
    if price < 2: return t("복권형", "Lottery ticket"), "b", -20, t("2¢ 미만은 거의 복권형 가격입니다.", "Below 2¢ is essentially a lottery ticket.")
    if price <= 20: return t("고변동", "High volatility"), "w", -4, t("저가 구간은 변동성이 큽니다. 소액만 적합합니다.", "Low prices are volatile. Small size only.")
    return t("정상 구간", "Normal range"), "g", 0, t("가격 구간 자체는 과도한 위험 신호가 크지 않습니다.", "No major risk signal from price alone.")

def purpose_options():
    return [t("경기승리 / 만기 보유", "Win bet / hold to expiry"),
            t("경기 시작 전 가격 상승 노림", "Pre-game price rise"),
            t("반반 경기 쏠림 이용 / 중간 익절", "Crowd-tilt / mid take-profit"),
            t("역배 / Bounce Trade", "Underdog / bounce trade"),
            t("99¢ 상환 스캘핑", "99¢ redemption scalp"),
            t("뉴스/이벤트 선반영", "News/event front-run")]

def purpose_rule(p):
    table = [
        (1.00, 0,  t("실제 승률 추정이 핵심인 기본 승리 베팅입니다.", "Standard win bet; true win-rate matters most.")),
        (0.70, -6, t("시장 심리와 타이밍이 중요합니다. 익절 기준을 먼저 정해야 합니다.", "Sentiment & timing; set a take-profit rule first.")),
        (0.60, -8, t("경기력이 아니라 시장 쏠림을 노리는 거래입니다.", "Targets crowd tilt, not team strength.")),
        (0.35, -13, t("역배와 bounce는 소액 전용입니다. 손실 제한이 핵심입니다.", "Underdog/bounce is small-size only.")),
        (0.20, -25, t("작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다.", "Risks a lot for very little.")),
        (0.50, -12, t("조건문과 resolution 기준 확인이 중요합니다.", "Check resolution criteria carefully.")),
    ]
    opts = purpose_options()
    try: return table[opts.index(p)]
    except ValueError: return (1.0, 0, t("일반 베팅으로 계산합니다.", "Calculated as a standard bet."))

def market_type_options():
    return ["Match Moneyline", "Game Winner", "Correct Score",
            t("정치 선거", "Political election"), t("뉴스/이벤트", "News / event"),
            t("99¢ 상환 스캘핑", "99¢ redemption scalp"), "2~5¢ Bounce Trade"]

def market_type_rule(m):
    table = [
        (1.00, 0,  t("가장 기본적인 시장입니다.", "The most standard market.")),
        (0.50, -10, t("단판 시장은 변동성이 커서 추천 금액을 50% 줄입니다.", "Single-game markets cut suggested size by 50%.")),
        (0.25, -25, t("Correct Score는 맞히기 어렵습니다.", "Correct Score is hard to hit.")),
        (0.50, -12, t("결과 기준과 이의제기 가능성을 확인해야 합니다.", "Verify result criteria & dispute risk.")),
        (0.50, -12, t("조건문과 resolution 기준 확인이 필수입니다.", "Resolution wording check is mandatory.")),
        (0.20, -25, t("고가 상환 스캘핑은 고액 금지입니다.", "No large size for redemption scalps.")),
        (0.20, -18, t("초저가 bounce는 소액 전용입니다.", "Deep-value bounce is small-size only.")),
    ]
    opts = market_type_options()
    try: return table[opts.index(m)]
    except ValueError: return (1.0, 0, t("일반 시장으로 계산합니다.", "Standard market."))

def size_thresholds():
    p = profile()
    g = max(p["max_pct"], 0.5)
    return g, g * 1.5, g * 2.5, max(p["block_pct"], g * 1.6)

def size_rule(pct):
    g, c1, c2, blk = size_thresholds()
    if pct >= 50: return t("시스템 실패", "System failure"), "b", -100, t("계좌 생존 리스크입니다. 50% 이상 노출은 절대 금지입니다.", "Account-survival risk. Never expose 50%+.")
    if pct >= blk: return t("진입 금지", "Entry blocked"), "b", -85, t(f"내 기준 진입 금지선({blk:.0f}%)을 넘었습니다.", f"Above your no-entry line ({blk:.0f}%).")
    if pct >= c2: return t("매우 위험", "Very risky"), "b", -38, t(f"내 적정 비율({g:.0f}%)의 2.5배가 넘는 포지션입니다.", f"Over 2.5× your comfort ratio ({g:.0f}%).")
    if pct >= c1: return t("위험", "Risky"), "w", -20, t(f"내 적정 비율({g:.0f}%)을 크게 넘었습니다.", f"Well above your comfort ratio ({g:.0f}%).")
    if pct > g: return t("주의", "Caution"), "w", -8, t(f"내 적정 비율({g:.0f}%)을 약간 넘었습니다.", f"Slightly above your comfort ratio ({g:.0f}%).")
    return t("정상", "Normal"), "g", 5, t(f"내 적정 비율({g:.0f}%) 이내입니다.", f"Within your comfort ratio ({g:.0f}%).")

def exposure_rule(pct):
    g, c1, c2, blk = size_thresholds()
    if pct >= blk: return t("중복 노출 금지", "Stacked exposure blocked"), "b", -60, t(f"같은 경기·방향 총 노출이 진입 금지선({blk:.0f}%)을 넘었습니다.", f"Same-game/side exposure above your no-entry line ({blk:.0f}%).")
    if pct >= c2: return t("중복 노출 위험", "Stacked exposure risky"), "b", -35, t("같은 경기·방향 총 노출이 큽니다.", "Stacked exposure is large.")
    if pct >= c1: return t("중복 노출 주의", "Stacked exposure caution"), "w", -12, t("같은 경기·방향 노출이 쌓이고 있습니다.", "Exposure is stacking up.")
    return t("정상", "Normal"), "g", 0, t("중복 노출은 관리 가능한 범위입니다.", "Stacked exposure is manageable.")

def confidence_options():
    return [t("관찰용", "Watching"), t("낮은 확신", "Low conviction"), t("중간 확신", "Medium"),
            t("높은 확신", "High conviction"), t("초고확신", "Very high")]

def confidence_caps():
    el = profile()["emotional_limit"]
    return [el * .3, el * .5, el * 1.0, el * 1.4, el * 1.4]

def portfolio_caps(bankroll):
    g = profile()["max_pct"] / 100
    return [bankroll * g * .3, bankroll * g * .5, bankroll * g * 1.0, bankroll * g * 1.3, bankroll * g * 1.5]


def effective_bankroll():
    pos_value = sum((p.get("shares", 0) or 0) * ((p.get("cur", 0) or 0) / 100) for p in st.session_state.portfolio)
    total = st.session_state.cash + pos_value
    return total if total > 0 else profile()["assets"]


# =====================================================
# Entry engine
# =====================================================
def calculate_entry(d):
    prof = profile()
    current_price, fair_price = d["current_price"], d["fair_price"]
    stake, bankroll = d["stake"], d["bankroll"]
    edge = fair_price - current_price
    position_pct = stake / bankroll * 100 if bankroll else 0

    zone_label, zone_kind, zone_pen, zone_note = price_zone(current_price)
    p_mult, p_pen, p_note = purpose_rule(d["purpose"])
    m_mult, m_pen, m_note = market_type_rule(d["market_type"])
    size_label, size_kind, size_pen, size_note = size_rule(position_pct)

    el = prof["emotional_limit"]
    try:
        ci = confidence_options().index(d["confidence"])
    except ValueError:
        ci = 2
    base_cap = min(confidence_caps()[ci], portfolio_caps(bankroll)[ci], el)
    rec_cap = base_cap * p_mult * m_mult
    if d["fomo_count"] >= 1:
        rec_cap *= 0.5

    sys_amt, warn_amt = el * 4, el * 2
    if stake >= sys_amt: cap_label, cap_kind, cap_pen = t(f"감정 한도 4배 초과 — 시스템 실패", "4× emotional cap — system failure"), "b", -90
    elif stake >= warn_amt: cap_label, cap_kind, cap_pen = t(f"감정 한도 2배 초과 — 강한 경고", "2× emotional cap — strong warning"), "b", -50
    elif stake > rec_cap * 1.2: cap_label, cap_kind, cap_pen = t("추천 상한선 초과", "Above suggested cap"), "b", -32
    elif stake > rec_cap: cap_label, cap_kind, cap_pen = t("상한선 소폭 초과", "Slightly above cap"), "w", -12
    else: cap_label, cap_kind, cap_pen = t("상한선 이내", "Within cap"), "g", 0

    dup_total = d["duplicate_ml"] + d["duplicate_game"] + d["duplicate_side"] + stake
    dup_pct = dup_total / bankroll * 100 if bankroll else 0
    exp_label, exp_kind, exp_pen, exp_note = exposure_rule(dup_pct)

    if d["fomo_count"] >= 3:
        fomo_label, fomo_kind, fomo_pen = t("감정 진입 금지", "Emotional — blocked"), "b", -75
        fomo_note = t("감정 체크 3개 이상입니다. 신규 진입 금지로 봐야 합니다.", "3+ emotion checks. Treat as no-entry.")
    elif d["fomo_count"] >= 1:
        fomo_label, fomo_kind, fomo_pen = t("감정 위험", "Emotional risk"), "w", -20
        fomo_note = t("감정 체크가 있습니다. 추천 금액을 50% 줄였습니다.", "Emotion checks present. Size halved.")
    else:
        fomo_label, fomo_kind, fomo_pen = t("정상", "Normal"), "g", 0
        fomo_note = t("감정 체크가 없습니다.", "No emotion checks.")

    if d["previous_good_price"] > 0:
        gap = current_price - d["previous_good_price"]
        if gap >= 30: chase = (t("FOMO 추격", "FOMO chase"), "b", -25, t("처음 봤던 가격보다 30¢ 이상 올랐습니다.", "Up 30¢+ since first sighting."))
        elif gap >= 15: chase = (t("추격 위험", "Chase risk"), "w", -13, t("처음 봤던 가격보다 많이 올랐습니다.", "Up a lot since first sighting."))
        elif gap >= 5: chase = (t("조금 상승", "Slightly up"), "w", -5, t("처음 봤던 가격보다 조금 올랐습니다.", "Slightly up since first sighting."))
        else: chase = (t("추격 아님", "Not a chase"), "g", 5, t("추격 위험은 크지 않습니다.", "Chase risk is small."))
    else:
        chase = (t("미입력", "Not entered"), "i", 0, t("처음 봤던 저평가 가격을 입력하지 않았습니다.", "First-seen price not provided."))
    chase_label, chase_kind, chase_pen, chase_note = chase

    bk = d["bookmaker_prob"]
    my_vs_poly = fair_price - current_price
    book_vs_poly = bk - current_price if bk > 0 else 0
    my_vs_book = fair_price - bk if bk > 0 else 0
    if bk <= 0: book = (t("북메이커 미입력", "No bookmaker input"), "i", 0, t("북메이커 승률을 입력하면 공식 배당과의 괴리를 볼 수 있습니다.", "Enter a bookmaker probability to compare."))
    elif my_vs_book >= 10: book = (t("과신 재검토", "Re-check overconfidence"), "b", -12, t("내 적정가가 북메이커보다 10%p 이상 높습니다.", "Your fair price is 10pp+ above the book."))
    elif book_vs_poly >= 5: book = (t("외부배당도 저평가", "Cheap vs books too"), "g", 6, t("북메이커 기준으로도 가격이 싸 보입니다.", "Cheap even vs bookmakers."))
    elif book_vs_poly <= -5: book = (t("외부배당 기준 비쌈", "Expensive vs books"), "w", -8, t("북메이커 기준으로는 비싼 편입니다.", "Expensive vs bookmakers."))
    else: book = (t("큰 차이 없음", "No big gap"), "i", 0, t("북메이커와 큰 차이가 없습니다.", "No large gap vs books."))
    book_label, book_kind, book_pen, book_note = book

    value_score = clamp(50 + edge * 2.2 + zone_pen + p_pen + m_pen + chase_pen + book_pen)
    final_score = clamp(value_score + size_pen + exp_pen + fomo_pen + cap_pen)

    g, c1, c2, blk = size_thresholds()
    hard_stop = None
    if position_pct >= 50: hard_stop = t("시스템 실패 — 계좌 생존 리스크", "System failure — survival risk")
    elif stake >= sys_amt: hard_stop = t("시스템 실패 — 감정 한도 4배", "System failure — 4× emotional cap")
    elif position_pct >= blk: hard_stop = t(f"진입 금지 — 내 한도 {blk:.0f}% 초과", f"Entry blocked — over your {blk:.0f}% line")
    elif dup_pct >= blk: hard_stop = t(f"진입 금지 — 중복 노출 {blk:.0f}% 초과", f"Entry blocked — stacked over {blk:.0f}%")
    elif d["fomo_count"] >= 3: hard_stop = t("진입 금지 — 감정 배팅 위험", "Entry blocked — emotional betting")

    if hard_stop: decision, level = hard_stop, "bad"
    elif final_score >= 75: decision, level = t("진입 적절", "Good entry"), "good"
    elif final_score >= 60: decision, level = t("소액 진입 가능", "Small entry OK"), "warn"
    elif final_score >= 45: decision, level = t("관망 우선", "Wait and watch"), "warn"
    else: decision, level = t("진입 부적절", "Poor entry"), "bad"

    shares = stake / (current_price / 100)
    win_profit = shares - stake
    target_profit = shares * (d["target_price"] / 100) - stake
    stop_loss_amt = stake - shares * (d["stop_price"] / 100)
    rr = target_profit / stop_loss_amt if stop_loss_amt > 0 else 0

    if target_profit > 0 and stop_loss_amt > 0:
        if stop_loss_amt > target_profit: rr_text, rr_kind = t(f"손절 손실이 목표 수익보다 약 {stop_loss_amt/target_profit:.1f}배 큽니다.", f"Stop-loss ≈ {stop_loss_amt/target_profit:.1f}× the target."), "b"
        elif target_profit >= stop_loss_amt * 1.5: rr_text, rr_kind = t(f"목표 수익이 손절 손실보다 약 {target_profit/stop_loss_amt:.1f}배 큽니다.", f"Target ≈ {target_profit/stop_loss_amt:.1f}× the stop."), "g"
        else: rr_text, rr_kind = t(f"손익비 {rr:.2f}:1 — 큰 우위는 아닙니다.", f"R:R {rr:.2f}:1 — not a big edge."), "w"
    else:
        rr_text, rr_kind = t("목표가 또는 손절가를 다시 확인하세요.", "Re-check target or stop."), "w"

    current_value = shares * (current_price / 100)
    additional_to_100 = shares - current_value
    high_warn = ""
    if current_price >= 90:
        high_warn = t(f"현재부터 100¢까지 추가수익은 {money(additional_to_100)}뿐입니다. 틀리면 {money(current_value)}를 잃을 수 있습니다.",
                      f"Only {money(additional_to_100)} left to 100¢, but a miss costs {money(current_value)}.")
    if current_price >= 97:
        high_warn += t(" 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출합니다.", " Large buys at 97–99¢ risk a lot for little.")

    if edge >= 10: edge_reason = ("g", t(f"가격 메리트 좋음 — 적정가가 현재가보다 {edge:.1f}¢ 높습니다.", f"Good value — fair price {edge:.1f}¢ above market."))
    elif edge >= 5: edge_reason = ("w", t(f"가격 메리트 약간 — edge {edge:.1f}¢.", f"Some value — edge {edge:.1f}¢."))
    elif edge < 0: edge_reason = ("b", t(f"가격 메리트 없음 — 현재가가 {abs(edge):.1f}¢ 더 비쌉니다.", f"No value — market {abs(edge):.1f}¢ above fair."))
    else: edge_reason = ("w", t(f"가격 메리트 작음 — edge {edge:.1f}¢.", f"Thin value — edge {edge:.1f}¢."))

    reasons = [edge_reason,
               (size_kind, t(f"포지션 크기 — 총자산의 {position_pct:.1f}% · {size_label}", f"Size — {position_pct:.1f}% of portfolio · {size_label}")),
               (cap_kind, t(f"추천 상한선 {money(rec_cap)} · 투자금 {money(stake)} — {cap_label}", f"Cap {money(rec_cap)} · stake {money(stake)} — {cap_label}")),
               (zone_kind, t(f"가격 구간 — {zone_label}. {zone_note}", f"Price zone — {zone_label}. {zone_note}"))]

    return {**d, "edge": edge, "position_pct": position_pct,
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
            "reasons": reasons}


# =====================================================
# Position engine
# =====================================================
def evaluate_position(d):
    cp, shares, inv, bankroll = d["current_price"], d["shares"], d["investment"], d["bankroll"]
    current_value = shares * (cp / 100)
    pnl = current_value - inv
    roi = pnl / inv * 100 if inv else 0
    position_pct = current_value / bankroll * 100 if bankroll else 0
    g, c1, c2, blk = size_thresholds()

    reasons, warnings = [], []
    if cp >= d["target_price"]:
        decision, level = t("목표가 도달 — 매도·부분매도 고려", "Target hit — consider selling"), "warn"
        reasons.append(t("목표가에 도달했습니다. 일부 익절을 검토할 구간입니다.", "Target reached. Consider partial profit."))
    elif cp <= d["stop_price"] and current_value >= inv * 0.3:
        decision, level = t("손절 고려", "Consider stop-loss"), "bad"
        reasons.append(t("손절가 이하이고 회수 가능한 금액이 남아 있습니다.", "Below stop; meaningful value recoverable."))
    elif current_value <= inv * 0.1:
        decision, level = t("손절 효용 낮음 — 추가매수 금지", "Stop has little value — no adding"), "warn"
        reasons.append(t("평가금이 원금의 10% 이하입니다. 옵션처럼 보유, 추가매수 금지.", "Under 10% of cost. Hold like an option; never add."))
    else:
        decision, level = t("홀딩 가능", "Holding is fine"), "good"
        reasons.append(t("목표가와 손절가 사이로 홀딩 조건을 충족합니다.", "Between target and stop; hold conditions met."))

    if roi >= 30:
        warnings.append(t("수익률 +30% 이상 — 원금 회수 또는 부분매도 검토.", "ROI +30%+ — consider recovering principal."))
        if level == "good":
            decision, level = t("홀딩 가능, 단 부분매도 검토", "Hold, but consider partial sell"), "warn"
    if position_pct >= blk:
        warnings.append(t(f"포트폴리오 비중이 내 진입 금지선({blk:.0f}%)을 넘었습니다 — 즉시 축소 고려.", f"Over your no-entry line ({blk:.0f}%) — reduce now."))
        decision, level = t("과대 노출 — 즉시 축소 고려", "Excessive exposure — reduce now"), "bad"
    elif position_pct >= c1:
        warnings.append(t(f"포트폴리오 비중이 적정선({g:.0f}%)을 크게 넘었습니다 — 일부 축소 권장.", f"Well above your comfort ratio ({g:.0f}%) — partial reduction advised."))
        if level != "bad":
            decision, level = t("홀딩 가능, 단 포지션 크기 과대", "Hold, but size too large"), "warn"
    if d["fomo_count"] >= 3:
        warnings.append(t("감정 체크 3개 이상 — 추가매수 금지, 축소 우선.", "3+ emotion checks — no adding; reduce first."))
        decision, level = t("감정 리스크 — 추가매수 금지", "Emotional risk — no adding"), "bad"
    elif d["fomo_count"] >= 1:
        warnings.append(t("감정 체크 있음 — 섣부른 추가매수 주의.", "Emotion present — avoid impulsive adds."))

    zl, zk, _, zn = price_zone(cp)
    if cp >= 80:
        warnings.append(zn)
    if not warnings:
        warnings.append(t("큰 위험 신호는 없지만 목표가·손절가 기준은 유지하세요.", "No major risk, but keep target/stop rules."))

    return {**d, "decision": decision, "level": level, "current_value": current_value,
            "pnl": pnl, "roi": roi, "position_pct": position_pct,
            "additional": shares - current_value, "reasons": reasons, "warnings": warnings}


def partial_rows(shares, price_cent, investment):
    pdec = price_cent / 100
    rows, need = [], None
    if shares > 0 and pdec > 0:
        need = investment / (shares * pdec) * 100
    for ratio in [25, 50, 70, 80, 90, 100]:
        ss = shares * ratio / 100
        rec = ss * pdec
        rem = shares - ss
        rows.append({
            t("매도 비율", "Sell %"): f"{ratio}%",
            t("매도 수량", "Shares sold"): round(ss, 2),
            t("회수금", "Recovered"): money(rec),
            t("원금 대비 확정손익", "Locked P&L"): signed_money(rec - investment),
            t("남은 수량", "Shares left"): round(rem, 2),
            t("남은 평가금", "Remaining value"): money(rem * pdec),
            t("100¢ 추가수익", "Extra at 100¢"): signed_money(rem * (1 - pdec)),
        })
    return rows, need


# =====================================================
# Claude AI
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
    lang_line = "한국어로 답변해주세요." if st.session_state.lang == "ko" else "Answer in English."
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
{lang_line}"""

def call_claude(prompt):
    key = get_api_key()
    if not key:
        return None, "no_key"
    try:
        payload = json.dumps({"model": "claude-sonnet-4-20250514", "max_tokens": 1200,
                              "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
                                     headers={"Content-Type": "application/json", "x-api-key": key,
                                              "anthropic-version": "2023-06-01"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["content"][0]["text"], None
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except Exception as e:
        return None, str(e)

def render_ai(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    title, body, blocks, verdict = "", [], [], ""
    for l in lines:
        if len(l) > 2 and l[0].isdigit() and l[1] == ".":
            if title: blocks.append((title, " ".join(body)))
            title, body = l, []
        elif l.startswith("결론") or l.lower().startswith(("conclusion", "verdict")):
            if title:
                blocks.append((title, " ".join(body)))
                title, body = "", []
            verdict = l
        else:
            body.append(l)
    if title and body: blocks.append((title, " ".join(body)))

    if verdict:
        low = verdict.lower()
        is_no = "비추천" in verdict or "not recommend" in low or "avoid" in low
        is_yes = not is_no and ("추천" in verdict or "recommend" in low)
        kind = "g" if is_yes else "b" if is_no else "w"
        clean = verdict.split(":", 1)[-1].strip()
        st.markdown(f"""<div class="verdict" style="border-top:none;padding-top:6px;">
<div class="v-title" style="font-size:28px;"><span class="dot {kind}"></span>{clean}</div>
<div class="v-sub">{t("Claude 분석 결론", "Claude's conclusion")}</div></div>""", unsafe_allow_html=True)
    for tt, b in blocks:
        st.markdown(f'<div class="ai-block"><div class="a-key">{tt}</div><div class="a-body">{b}</div></div>', unsafe_allow_html=True)


# =====================================================
# Polymarket APIs
# =====================================================
def extract_slug(url):
    path = urllib.parse.urlparse(url.strip()).path.strip("/")
    return path.split("/")[-1] if path else ""

@st.cache_data(ttl=60, show_spinner=False)
def fetch_gamma(slug):
    api = f"https://gamma-api.polymarket.com/events?slug={urllib.parse.quote(slug)}"
    req = urllib.request.Request(api, headers={"User-Agent": "Memento/5.0", "Accept": "application/json"})
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
                rows.append({t("시장", "Market"): q, t("선택지", "Outcome"): o,
                             t("현재가 (¢)", "Price (¢)"): price,
                             "token_id": tokens[i] if i < len(tokens) else ""})
    return rows

@st.cache_data(ttl=30, show_spinner=False)
def fetch_wallet_positions(addr):
    """Public Polymarket data API — read-only, no login required."""
    api = f"https://data-api.polymarket.com/positions?user={urllib.parse.quote(addr)}&sizeThreshold=0.5&limit=100"
    req = urllib.request.Request(api, headers={"User-Agent": "Memento/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


MIN_SHARES = 1.0   # 이 미만 수량은 dust로 간주
MIN_VALUE = 1.0    # 평가금 $1 미만은 숨김

def is_open_position(it):
    """현재 실제 보유 중인 포지션인지 판단"""
    try:
        size = float(it.get("size", 0))
        cur = float(it.get("curPrice", 0))
        val = float(it.get("currentValue", size * cur))
    except Exception:
        return False
    if it.get("redeemable") is True:
        return False
    if size < MIN_SHARES or val < MIN_VALUE:
        return False
    if cur <= 0.001 or cur >= 0.999:
        return False
    return True


# =====================================================
# Period P&L
# =====================================================
def period_pnl():
    now = datetime.now()
    week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    w = m = y = 0.0
    for tr in st.session_state.trade_log:
        try:
            dt = datetime.fromisoformat(tr["d"])
        except Exception:
            continue
        p = tr.get("profit", 0.0)
        if dt >= week_start: w += p
        if dt.year == now.year and dt.month == now.month: m += p
        if dt.year == now.year: y += p
    return w, m + st.session_state.adj_month, y + st.session_state.adj_year


# =====================================================
# Onboarding gate
# =====================================================
mh_l, mh_r = st.columns([4, 1])
with mh_l:
    st.markdown(
        f"""<div class="masthead">
<div class="name">Memento</div>
<div class="tag">{t("Polymarket 배팅 판단 · 계좌를 지키는 수동 리스크 관리", "Polymarket decisions · manual risk control")}</div>
</div>""", unsafe_allow_html=True)
with mh_r:
    lang_choice = st.radio("lang", ["한국어", "English"],
                           index=0 if st.session_state.lang == "ko" else 1,
                           horizontal=True, label_visibility="collapsed")
    new_lang = "ko" if lang_choice == "한국어" else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

if st.session_state.profile is None:
    # ---------------- ONBOARDING ----------------
    st.markdown(f'<div class="ob-step">{t("시작하기", "Get started")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="headline">{t("먼저 당신의 배팅 스타일을 알려주세요", "First, tell us about your betting style")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subline">{t("이 답변으로 당신만의 리스크 한도가 만들어지고, 모든 판독에 자동으로 적용됩니다. 나중에 설정에서 언제든 바꿀 수 있어요.", "Your answers build a personal risk profile that powers every evaluation. You can change it anytime in Settings.")}</div>', unsafe_allow_html=True)

    with st.form("onboarding"):
        st.markdown(f'<div class="eyebrow">{t("1 · 계좌", "1 · Account")}</div>', unsafe_allow_html=True)
        o1, o2 = st.columns(2)
        with o1:
            ob_assets = st.number_input(t("현재 포트폴리오 총자산 ($)", "Current total assets ($)"), 1.0, value=1000.0)
        with o2:
            ob_start_cap = st.number_input(t("폴리마켓 시작 자금 ($)", "Starting capital ($)"), 1.0, value=1000.0)
        ob_when = st.selectbox(t("폴리마켓을 시작한 지 얼마나 됐나요?", "How long have you been on Polymarket?"),
                               [t("1개월 미만", "Under 1 month"), t("1~6개월", "1–6 months"),
                                t("6개월~1년", "6–12 months"), t("1년 이상", "Over a year")])

        st.markdown(f'<div class="eyebrow" style="margin-top:18px;">{t("2 · 배팅 습관", "2 · Habits")}</div>', unsafe_allow_html=True)
        ob_freq = st.selectbox(t("얼마나 자주 배팅하나요?", "How often do you bet?"),
                               [t("거의 매일", "Almost daily"), t("주 2~3회", "2–3× a week"),
                                t("주 1회 이하", "Weekly or less"), t("가끔, 큰 경기만", "Occasionally, big matches only")])
        ob_cats = st.multiselect(t("주로 배팅하는 항목", "What do you usually bet on?"),
                                 [t("LoL e스포츠", "LoL esports"), t("기타 e스포츠", "Other esports"),
                                  t("스포츠", "Sports"), t("정치·뉴스", "Politics / news"), t("기타", "Other")],
                                 default=[t("LoL e스포츠", "LoL esports")])

        st.markdown(f'<div class="eyebrow" style="margin-top:18px;">{t("3 · 리스크 성향", "3 · Risk tolerance")}</div>', unsafe_allow_html=True)
        ob_emotional = st.number_input(
            t("한 번의 배팅에서 전부 잃어도 감정이 흔들리지 않는 최대 금액은? ($)",
              "Largest single-bet loss you can take without it shaking you? ($)"),
            1.0, value=50.0)
        ob_max_pct = st.slider(
            t("전체 자산 대비, 한 번에 최대 몇 %까지 배팅해도 편안한가요?",
              "What % of your portfolio can you bet at once and still sleep well?"),
            1, 30, 3)
        ob_reaction = st.radio(
            t("$200 포지션이 $100이 됐을 때, 당신은?", "Your $200 position drops to $100. You…"),
            [t("계획대로 손절하거나 홀딩을 냉정하게 판단한다", "Calmly follow my plan — stop or hold"),
             t("흔들리지만 규칙은 지키는 편이다", "Get shaken, but usually stick to my rules"),
             t("복구 배팅 충동이 생기고 판단이 흐려진다", "Feel the urge to chase losses; judgment blurs")],
            index=1)

        ob_submit = st.form_submit_button(t("프로필 만들고 시작하기", "Create profile and start"), use_container_width=True)

    if ob_submit:
        reactions = [t("계획대로 손절하거나 홀딩을 냉정하게 판단한다", "Calmly follow my plan — stop or hold"),
                     t("흔들리지만 규칙은 지키는 편이다", "Get shaken, but usually stick to my rules"),
                     t("복구 배팅 충동이 생기고 판단이 흐려진다", "Feel the urge to chase losses; judgment blurs")]
        mult = [4.0, 3.0, 2.0][reactions.index(ob_reaction)]
        block = min(max(ob_max_pct * mult, 8.0), 30.0)
        st.session_state.profile = {
            "assets": ob_assets, "start_capital": ob_start_cap, "start_when": ob_when,
            "freq": ob_freq, "cats": ob_cats,
            "emotional_limit": ob_emotional,
            "max_pct": float(ob_max_pct), "block_pct": round(block, 1),
            "loss_reaction": ob_reaction,
        }
        st.rerun()

    st.markdown(f'<div class="footnote">{t("진입 금지선은 [편안한 비율 × 손실 반응 계수]로 계산됩니다. 냉정할수록 더 넓은 한도를 드려요.", "Your no-entry line = comfort ratio × loss-reaction factor. The calmer you are, the wider your limit.")}</div>', unsafe_allow_html=True)
    st.stop()

# profile summary chip under masthead
prof = profile()
g_, c1_, c2_, blk_ = size_thresholds()
eb_ = effective_bankroll()
exp_limit_ = min(blk_ * 2, 50)
st.markdown(
    f'<div class="footnote" style="margin:-2px 0 14px 0;">'
    f'{t("내 리스크 기준", "My limits")} · '
    f'{t("적정", "comfort")} {g_:.0f}% ({money(eb_*g_/100)}) · '
    f'{t("최대", "max")} {c1_:.0f}% ({money(eb_*c1_/100)}) · '
    f'{t("진입 금지", "block")} {blk_:.0f}% ({money(eb_*blk_/100)}) · '
    f'{t("전체 노출 한도", "total exposure")} {exp_limit_:.0f}% ({money(eb_*exp_limit_/100)}) · '
    f'{t("감정 한도", "cap")} {money(prof["emotional_limit"])}</div>',
    unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab_pf, tab_set = st.tabs([
    t("진입 판독", "Entry check"),
    t("포지션 관리", "Positions"),
    t("부분매도", "Partial sell"),
    t("거래일지", "Journal"),
    t("포트폴리오", "Portfolio"),
    t("설정 · 도구", "Settings · tools"),
])


# =====================================================
# Render: entry result
# =====================================================
def render_entry_result(r):
    if not r:
        st.markdown(
            f"""<div class="quiet">
<div class="q-title">{t("판독 결과가 여기에 표시됩니다", "Your verdict appears here")}</div>
<div class="q-body">{t("오른쪽에서 시장 정보와 투자금을 입력하고<br>판독하기를 누르세요.", "Enter the market details on the right<br>and press Evaluate.")}</div>
</div>""", unsafe_allow_html=True)
        return

    k = verdict_dot(r["level"])
    score_word = t("적절성", "Suitability") if r["level"] != "bad" else t("부적절도", "Unsuitability")
    score_val = r["final_score"] if r["level"] != "bad" else 100 - r["final_score"]

    st.markdown(
        f"""<div class="verdict">
<div class="eyebrow">{t("판정", "Verdict")}</div>
<div class="v-title"><span class="dot {k}"></span>{r["decision"]}</div>
<div class="v-sub">{r["market_name"]} · {score_word} {score_val:.0f}% · {t("규모 제외 순수 가치", "Pure value")} {r["value_score"]:.0f}%</div>
</div>""", unsafe_allow_html=True)

    edge_tone = "pos" if r["edge"] >= 5 else "neg" if r["edge"] < 0 else ""
    pos_tone = "neg" if r["size_kind"] == "b" else ""
    st.markdown(
        '<div class="stats">'
        + stat(t("현재가", "Price"), cents(r["current_price"]), t("시장 implied probability", "Implied probability"))
        + stat("Edge", f"{r['edge']:+.1f}¢", t("내 적정가 대비", "vs fair price"), edge_tone)
        + stat(t("포트폴리오 비중", "Portfolio %"), f"{r['position_pct']:.1f}%", r["size_label"], pos_tone)
        + stat(t("추천 상한선", "Suggested cap"), money(r["rec_cap"]), t(f"투자금 {money(r['stake'])}", f"Stake {money(r['stake'])}"))
        + "</div>",
        unsafe_allow_html=True)

    # ---- meters with explicit verdicts ----
    fs = r["final_score"]
    fs_kind = "g" if fs >= 70 else "w" if fs >= 50 else "b"
    vs = r["value_score"]
    vs_kind = "g" if vs >= 70 else "w" if vs >= 50 else "b"
    pp = min(r["position_pct"], 100)
    pp_kind = r["size_kind"]
    pz_kind = r["zone_kind"]

    st.markdown(
        meter(t("리스크 포함 최종 적절성", "Final suitability incl. risk"), fs, fs_kind, grade_word(fs_kind), unit="%")
        + meter(t("배팅 규모 제외 순수 가치", "Pure value ex-size"), vs, vs_kind, grade_word(vs_kind), unit="%")
        + meter(t("포트폴리오 사용 비중", "Portfolio usage"), pp, pp_kind, r["size_label"], unit="%")
        + meter(t("현재가 위치", "Price position"), r["current_price"], pz_kind, r["zone_label"], unit="¢"),
        unsafe_allow_html=True)

    st.markdown(f'<div class="eyebrow" style="margin-top:22px;">{t("핵심 판단 근거", "Key reasoning")}</div>', unsafe_allow_html=True)
    notes = "".join(line(txt, kk) for kk, txt in r["reasons"])
    if r["fomo_count"] > 0: notes += line(r["fomo_note"], r["fomo_kind"])
    if r["duplicate_pct"] >= size_thresholds()[1]: notes += line(r["exp_note"], r["exp_kind"])
    if r["high_warn"]: notes += line(r["high_warn"], "b")
    st.markdown(notes, unsafe_allow_html=True)

    with st.expander(t("상세 리포트", "Detailed report")):
        st.markdown(
            '<div class="spec">'
            + spec_row(t("진입가격 구간", "Price zone"), f"{t('현재가','Price')} <b>{cents(r['current_price'])}</b> — {r['zone_note']}", r["zone_label"], r["zone_kind"])
            + spec_row(t("배팅금액 · 계좌 생존", "Stake · survival"), f"{t('투자금','Stake')} <b>{money(r['stake'])}</b> / {t('총자산','Portfolio')} <b>{money(r['bankroll'])}</b> · <b>{r['position_pct']:.1f}%</b><br>{r['size_note']}", r["size_label"], r["size_kind"])
            + spec_row(t("북메이커 비교", "Bookmaker check"), f"{t('내 적정가−현재가','Fair−mkt')} <b>{r['my_vs_poly']:+.1f}%p</b> · {t('북메이커−현재가','Book−mkt')} <b>{r['book_vs_poly']:+.1f}%p</b><br>{r['book_note']}", r["book_label"], r["book_kind"])
            + spec_row(t("추천 상한선", "Suggested cap"), f"<b>{money(r['rec_cap'])}</b> · {t('투자금','Stake')} <b>{money(r['stake'])}</b> · {r['confidence']}", r["cap_label"], r["cap_kind"])
            + spec_row(t("손익비", "Risk : reward"), f"{t('목표 도달','At target')} <b>{money(r['target_profit'])}</b> · {t('손절','At stop')} <b>{money(r['stop_loss_amt'])}</b><br>{r['rr_text']}", f"{r['rr']:.2f} : 1", r["rr_kind"])
            + spec_row(t("감정 · FOMO", "Emotion · FOMO"), f"{t('체크','Checks')} <b>{r['fomo_count']}</b> — {r['fomo_note']}", r["fomo_label"], r["fomo_kind"])
            + spec_row(t("중복 노출", "Stacked exposure"), f"<b>{money(r['duplicate_total'])}</b> · <b>{r['duplicate_pct']:.1f}%</b><br>{r['exp_note']}", r["exp_label"], r["exp_kind"])
            + spec_row(t("추격매수 점검", "Chase check"), r["chase_note"], r["chase_label"], r["chase_kind"])
            + spec_row(t("목적 · 시장 유형", "Purpose · type"), f"<b>{r['purpose']}</b> — {r['purpose_note']}<br><b>{r['market_type']}</b> — {r['market_type_note']}", t("구조", "Structure"), "i")
            + "</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="eyebrow" style="margin-top:24px;">{t("수익 · 손실 시나리오", "P&L scenarios")}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="stats">'
            + stat(t("보유 수량", "Shares"), f"{r['shares']:.2f}", t("투자금 ÷ 현재가", "Stake ÷ price"))
            + stat(t("승리 시 순이익", "Profit if win"), money(r["win_profit"]), t("100¢ 상환 기준", "At 100¢"), "pos")
            + stat(t("패배 시 손실", "Loss if lose"), money(-r["stake"]), t("전액 손실 가정", "Total loss"), "neg")
            + stat(t("100¢까지 추가수익", "Left to 100¢"), money(r["additional_to_100"]), t("남은 업사이드", "Upside left"))
            + "</div>", unsafe_allow_html=True)

        summary = (f"{r['market_name']} | {cents(r['current_price'])} → fair {cents(r['fair_price'])} · edge {r['edge']:+.0f}¢ | "
                   f"{money(r['stake'])} · {r['position_pct']:.1f}% | {r['decision']} | {r['final_score']:.0f}% / {r['value_score']:.0f}%")
        st.markdown(f'<div class="eyebrow" style="margin-top:20px;">{t("기록용 한 줄 요약", "One-line summary")}</div>', unsafe_allow_html=True)
        st.code(summary)


def render_position_result(r):
    if not r:
        st.markdown(
            f"""<div class="quiet">
<div class="q-title">{t("포지션 결과가 여기에 표시됩니다", "Position verdict appears here")}</div>
<div class="q-body">{t("오른쪽에서 현재가와 보유 수량을 입력하세요.", "Enter price and shares on the right.")}</div>
</div>""", unsafe_allow_html=True)
        return

    k = verdict_dot(r["level"])
    st.markdown(
        f"""<div class="verdict">
<div class="eyebrow">{t("포지션 판정", "Position verdict")}</div>
<div class="v-title"><span class="dot {k}"></span>{r["decision"]}</div>
<div class="v-sub">{r["name"]} · {t("현재가", "Price")} {cents(r["current_price"])}</div>
</div>""", unsafe_allow_html=True)

    pnl_tone = "pos" if r["pnl"] >= 0 else "neg"
    st.markdown(
        '<div class="stats">'
        + stat(t("현재 평가금", "Current value"), money(r["current_value"]), t("현재가 × 수량", "Price × shares"))
        + stat(t("즉시 매도 손익", "P&L if sold"), signed_money(r["pnl"]), f"{t('수익률','ROI')} {signed_pct(r['roi'])}", pnl_tone)
        + stat(t("100¢ 상환 총액", "Value at 100¢"), money(r["shares"]), t("승리 시", "If it wins"))
        + stat(t("실패 시 손실", "Loss if fails"), money(-r["current_value"]), t("평가금 전액", "Full value"), "neg")
        + "</div>", unsafe_allow_html=True)

    roi_kind = "g" if r["roi"] >= 0 else "b"
    g_, c1_, c2_, blk_ = size_thresholds()
    pp_kind = "b" if r["position_pct"] >= blk_ else "w" if r["position_pct"] >= c1_ else "g"
    zl, zk, _, _ = price_zone(r["current_price"])
    st.markdown(
        meter(t("현재 수익률", "Current ROI"), max(r["roi"], -100), roi_kind, signed_pct(r["roi"]), max_v=100, unit="%")
        + meter(t("포트폴리오 비중", "Portfolio share"), min(r["position_pct"], 100), pp_kind,
                grade_word(pp_kind), unit="%")
        + meter(t("현재가 위치", "Price position"), r["current_price"], zk, zl, unit="¢"),
        unsafe_allow_html=True)

    st.markdown(f'<div class="eyebrow" style="margin-top:20px;">{t("판단 근거", "Reasoning")}</div>', unsafe_allow_html=True)
    notes = "".join(line(x, "g") for x in r["reasons"])
    for w in r["warnings"]:
        kind = "b" if (("금지" in w or "손절" in w or "축소" in w) or any(s in w.lower() for s in ["block", "reduce now"])) else "w"
        notes += line(w, kind)
    st.markdown(notes, unsafe_allow_html=True)

    rows, need = partial_rows(r["shares"], r["current_price"], r["investment"])
    st.markdown(f'<div class="eyebrow" style="margin-top:22px;">{t("부분매도 시나리오", "Partial-sell scenarios")}</div>', unsafe_allow_html=True)
    if need is not None:
        if need <= 100:
            st.markdown(line(t(f"원금 회수 최소 매도 비율: <b>{need:.1f}%</b>", f"Min sell ratio to recover cost: <b>{need:.1f}%</b>"), "g"), unsafe_allow_html=True)
        else:
            st.markdown(line(t(f"100% 팔아도 원금 회수가 어렵습니다 (필요 {need:.1f}%).", f"Even 100% can't recover cost (needs {need:.1f}%)."), "w"), unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# =====================================================
# Tab 1 — Entry
# =====================================================
with tab1:
    left, right = st.columns([1.05, 0.95], gap="large")

    with right:
        st.markdown(f'<div class="eyebrow" style="margin-top:8px;">{t("입력", "Input")}</div>', unsafe_allow_html=True)
        eb = effective_bankroll()
        with st.form("entry_form"):
            market_name = st.text_input(t("시장 이름", "Market name"), "T1 vs HLE — Match Winner")
            c0a, c0b = st.columns(2)
            with c0a: team_a = st.text_input(t("내가 보는 팀", "My team"), "T1")
            with c0b: team_b = st.text_input(t("상대 팀", "Opponent"), "HLE")
            league = st.selectbox(t("리그", "League"), ["LCK", "LPL", "LEC", "LCS", "MSI/Worlds", t("기타", "Other")])

            c1, c2 = st.columns(2)
            with c1:
                current_price = st.number_input(t("현재가 (¢)", "Price (¢)"), 1.0, 99.0, 52.0)
                stake = st.number_input(t("투자금 ($)", "Stake ($)"), 1.0, value=50.0)
            with c2:
                fair_price = st.number_input(t("내 적정가 (¢)", "My fair price (¢)"), 1.0, 99.0, 65.0)
                confidence = st.selectbox(t("확신 수준", "Conviction"), confidence_options(), index=2)

            c3, c4 = st.columns(2)
            with c3: purpose = st.selectbox(t("배팅 목적", "Purpose"), purpose_options())
            with c4: market_type = st.selectbox(t("시장 유형", "Market type"), market_type_options())

            st.markdown(f'<div class="footnote" style="margin-top:4px;">{t(f"총자산 {money(eb)} · 감정 한도 {money(prof['emotional_limit'])} — 프로필 기준 자동 적용", f"Portfolio {money(eb)} · emotional cap {money(prof['emotional_limit'])} — applied from your profile")}</div>', unsafe_allow_html=True)

            with st.expander(t("선택 입력 (목표가·손절가·중복·FOMO)", "Optional (target · stop · stacking · FOMO)")):
                a, b = st.columns(2)
                with a:
                    target_price = st.number_input(t("목표가 (¢)", "Target (¢)"), 1.0, 100.0, 75.0)
                    bookmaker_prob = st.number_input(t("북메이커 승률 (%)", "Bookmaker prob (%)"), 0.0, 99.0, 0.0)
                with b:
                    stop_price = st.number_input(t("손절가 (¢)", "Stop (¢)"), 0.0, 99.0, 40.0)
                    previous_good_price = st.number_input(t("처음 봤던 가격 (¢)", "First-seen price (¢)"), 0.0, 99.0, 0.0)

                st.markdown(f'<div class="eyebrow" style="margin-top:14px;">{t("중복 노출 ($)", "Stacked exposure ($)")}</div>', unsafe_allow_html=True)
                d1, d2, d3 = st.columns(3)
                with d1: duplicate_ml = st.number_input(t("같은 경기 ML", "Same-game ML"), 0.0, value=0.0)
                with d2: duplicate_game = st.number_input("Game Winner", 0.0, value=0.0)
                with d3: duplicate_side = st.number_input(t("같은 방향 추가", "Same side extra"), 0.0, value=0.0)

                st.markdown(f'<div class="eyebrow" style="margin-top:14px;">{t("감정 · FOMO 체크", "Emotion · FOMO checks")}</div>', unsafe_allow_html=True)
                fomo_options = [
                    t("방금 큰 수익을 냈다", "Just made a big profit"),
                    t("방금 큰 손실을 냈다", "Just took a big loss"),
                    t("아까 판 게 후회된다", "Regret selling earlier"),
                    t("빨리 복구하고 싶다", "Want to recover fast"),
                    t("더 빨리 계좌를 키우고 싶다", "Want to grow faster"),
                    t("놓치면 아깝다고 느낀다", "Afraid of missing out"),
                    t("이미 같은 경기에 포지션이 있다", "Already in this game"),
                ]
                fomo_count = 0
                f1c, f2c = st.columns(2)
                for i, opt in enumerate(fomo_options):
                    with f1c if i % 2 == 0 else f2c:
                        if st.checkbox(opt, key=f"fomo_{i}"):
                            fomo_count += 1

            submitted = st.form_submit_button(t("판독하기", "Evaluate"), use_container_width=True)

        if submitted:
            data = dict(market_name=market_name, team_a=team_a, team_b=team_b, league=league,
                        current_price=current_price, fair_price=fair_price, stake=stake,
                        purpose=purpose, market_type=market_type, bankroll=eb,
                        confidence=confidence, target_price=target_price, stop_price=stop_price,
                        bookmaker_prob=bookmaker_prob, previous_good_price=previous_good_price,
                        duplicate_ml=duplicate_ml, duplicate_game=duplicate_game,
                        duplicate_side=duplicate_side, fomo_count=fomo_count)
            st.session_state.last_entry = calculate_entry(data)
            prompt = build_prompt(team_a, team_b, league, current_price, fair_price, purpose)
            st.session_state.ai_prompt = prompt
            st.session_state.ai_pair = f"{team_a} vs {team_b}"
            with st.spinner(t("Claude가 팀을 분석하고 있습니다", "Claude is analyzing")):
                text, err = call_claude(prompt)
            st.session_state.ai_text = text or ""
            st.session_state.ai_error = err or ""
            st.rerun()

        st.markdown(f'<div class="eyebrow" style="margin-top:26px;">{t("Claude 팀 분석", "Claude team analysis")}</div>', unsafe_allow_html=True)
        if st.session_state.ai_text:
            st.markdown(f'<div class="footnote" style="margin-bottom:4px;">{st.session_state.ai_pair}</div>', unsafe_allow_html=True)
            render_ai(st.session_state.ai_text)
        elif st.session_state.ai_error:
            if st.session_state.ai_error == "no_key":
                st.markdown(line(t("API 키가 없어 분석 프롬프트를 생성했습니다. Claude나 ChatGPT에 붙여넣으세요.", "No API key — paste this prompt into Claude or ChatGPT."), "w"), unsafe_allow_html=True)
            elif st.session_state.ai_error.startswith("http_401"):
                st.markdown(line(t("API 키 인증 실패 (401). Secrets의 ANTHROPIC_API_KEY 확인 후 Reboot 해주세요.", "Auth failed (401). Check ANTHROPIC_API_KEY and reboot."), "b"), unsafe_allow_html=True)
            else:
                st.markdown(line(t(f"분석 실패 ({st.session_state.ai_error}). 아래 프롬프트를 사용하세요.", f"Failed ({st.session_state.ai_error}). Use the prompt below."), "w"), unsafe_allow_html=True)
            if st.session_state.ai_prompt:
                st.code(st.session_state.ai_prompt)
        else:
            st.markdown(
                f"""<div class="quiet" style="padding:40px 20px;">
<div class="q-title">{t("판독하면 자동으로 분석합니다", "Runs when you evaluate")}</div>
<div class="q-body">{t("리그 순위, 전적, 최근 폼, 상대 전적,<br>가격 적정성까지 Claude가 정리합니다.", "Standings, record, form, head-to-head<br>and price check — by Claude.")}</div>
</div>""", unsafe_allow_html=True)

    with left:
        render_entry_result(st.session_state.last_entry)


# =====================================================
# Tab 2 — Position
# =====================================================
with tab2:
    left, right = st.columns([1.05, 0.95], gap="large")

    with right:
        st.markdown(f'<div class="eyebrow" style="margin-top:8px;">{t("입력", "Input")}</div>', unsafe_allow_html=True)
        with st.form("position_form"):
            name = st.text_input(t("거래 이름", "Trade name"), "KT Rolster vs Dplus KIA — Match Winner")
            p1, p2 = st.columns(2)
            with p1:
                avg_buy = st.number_input(t("평균 매수가 (¢)", "Avg buy (¢)"), 1.0, 99.0, 52.4)
                shares_in = st.number_input(t("보유 수량", "Shares"), 0.01, value=1164.12)
                target_price = st.number_input(t("목표가 (¢)", "Target (¢)"), 1.0, 100.0, 60.0)
            with p2:
                current_price_p = st.number_input(t("현재가 (¢)", "Price (¢)"), 1.0, 100.0, 58.0)
                investment = st.number_input(t("투자금 ($)", "Cost ($)"), 1.0, value=610.0)
                stop_price_p = st.number_input(t("손절가 (¢)", "Stop (¢)"), 0.0, 99.0, 45.0)
            fomo_p = st.slider(t("감정 위험 체크 수", "Emotion checks"), 0, 7, 0)
            pos_submit = st.form_submit_button(t("포지션 판독하기", "Evaluate position"), use_container_width=True)

        if pos_submit:
            st.session_state.last_position = evaluate_position(dict(
                name=name, avg_buy=avg_buy, current_price=current_price_p,
                shares=shares_in, investment=investment,
                target_price=target_price, stop_price=stop_price_p,
                bankroll=effective_bankroll(), fomo_count=fomo_p))
            st.rerun()

        if st.session_state.last_position:
            if st.button(t("이 포지션을 포트폴리오에 추가", "Add to Portfolio"), use_container_width=True):
                r = st.session_state.last_position
                st.session_state.portfolio.append(dict(
                    name=r["name"], outcome="", buy=r["avg_buy"],
                    shares=round(r["shares"], 2), inv=round(r["investment"], 2),
                    cur=r["current_price"]))
                st.toast(t("포트폴리오에 추가했습니다", "Added"))

    with left:
        render_position_result(st.session_state.last_position)


# =====================================================
# Tab 3 — Partial sell
# =====================================================
with tab3:
    st.markdown(f'<div class="headline">{t("부분매도 계산기", "Partial-sell calculator")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subline">{t("원금 회수 최소 비율과 비율별 회수금·확정손익을 계산합니다.", "Min sell ratio to recover cost, plus per-ratio recovery and locked P&L.")}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: buy_price = st.number_input(t("매수가 (¢)", "Buy (¢)"), 1.0, 99.0, 16.0, key="pb")
    with c2: cur_price = st.number_input(t("현재가 (¢)", "Price (¢)"), 1.0, 100.0, 73.0, key="pc")
    with c3: inv = st.number_input(t("투자금 ($)", "Cost ($)"), 0.0, value=16.08, key="pi")

    manual = st.checkbox(t("보유 수량 직접 입력", "Enter shares manually"))
    shares_ps = st.number_input(t("보유 수량", "Shares"), 0.0, value=100.0, key="psh") if manual else (inv / (buy_price / 100) if buy_price > 0 else 0)

    if st.button(t("계산하기", "Calculate"), use_container_width=True):
        rows, need = partial_rows(shares_ps, cur_price, inv)
        cur_val = shares_ps * (cur_price / 100)
        add = shares_ps - cur_val
        st.markdown(
            '<div class="stats" style="margin-top:22px;">'
            + stat(t("보유 수량", "Shares"), f"{shares_ps:.2f}", "")
            + stat(t("현재 평가금", "Current value"), money(cur_val), "")
            + stat(t("100¢까지 추가수익", "Left to 100¢"), money(add), "", "pos")
            + stat(t("실패 시 손실", "Loss if fails"), money(-cur_val), "", "neg")
            + "</div>", unsafe_allow_html=True)
        if need is not None:
            if need <= 100:
                st.markdown(line(t(f"원금 회수 최소 매도 비율: <b>{need:.1f}%</b>", f"Min sell ratio: <b>{need:.1f}%</b>"), "g"), unsafe_allow_html=True)
            else:
                st.markdown(line(t(f"100% 팔아도 원금 회수 불가 (필요 {need:.1f}%).", f"Even 100% can't recover cost ({need:.1f}% needed)."), "w"), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# =====================================================
# Tab 4 — Journal
# =====================================================
with tab4:
    st.markdown(f'<div class="headline">{t("거래일지", "Journal")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subline">{t("기록한 거래는 포트폴리오의 주·월·연 실현손익에 자동 반영됩니다.", "Trades feed the weekly / monthly / yearly P&L in Portfolio.")}</div>', unsafe_allow_html=True)

    with st.form("trade_form"):
        t1c, t2c, t3c = st.columns(3)
        with t1c:
            tname = st.text_input(t("거래 이름", "Trade name"), "T1 vs HLE — Match Winner")
            tbuy = st.number_input(t("매수가 (¢)", "Buy (¢)"), 1.0, 99.0, 52.0, key="jb")
        with t2c:
            tsell = st.number_input(t("매도가 (¢)", "Sell (¢)"), 0.0, 100.0, 78.0, key="js")
            tstake = st.number_input(t("투자금 ($)", "Stake ($)"), 1.0, value=50.0, key="jst")
        with t3c:
            tdate = st.date_input(t("거래일", "Date"), value=date.today())
            tmemo = st.text_input(t("메모", "Memo"), "")
        add = st.form_submit_button(t("기록 추가", "Add"), use_container_width=True)

    if add:
        tsh = tstake / (tbuy / 100)
        tp = tsh * (tsell / 100) - tstake
        tr_ = tp / tstake * 100
        st.session_state.trade_log.append({
            "d": datetime.combine(tdate, datetime.min.time()).isoformat(),
            "name": tname, "buy": tbuy, "sell": tsell, "stake": tstake,
            "profit": round(tp, 2), "roi": round(tr_, 1), "memo": tmemo})
        st.toast(f"{signed_money(tp)} ({signed_pct(tr_)})")
        st.rerun()

    if st.session_state.trade_log:
        view = pd.DataFrame([{
            t("날짜", "Date"): tr["d"][:10], t("거래", "Trade"): tr["name"],
            t("매수가", "Buy"): cents(tr["buy"]), t("매도가", "Sell"): cents(tr["sell"]),
            t("투자금", "Stake"): money(tr["stake"]), t("손익", "P&L"): signed_money(tr["profit"]),
            t("수익률", "ROI"): signed_pct(tr["roi"]), t("메모", "Memo"): tr["memo"],
        } for tr in st.session_state.trade_log])
        st.dataframe(view, use_container_width=True, hide_index=True)

        total_realized = sum(tr["profit"] for tr in st.session_state.trade_log)
        k = "g" if total_realized >= 0 else "b"
        st.markdown(line(t(f"거래 {len(st.session_state.trade_log)}건 · 총 실현손익 <b>{signed_money(total_realized)}</b>",
                           f"{len(st.session_state.trade_log)} trades · total <b>{signed_money(total_realized)}</b>"), k), unsafe_allow_html=True)

        csv = view.to_csv(index=False).encode("utf-8-sig")
        cdl, crs = st.columns(2)
        with cdl:
            st.download_button(t("CSV 내려받기", "Download CSV"), data=csv, file_name="memento_trades.csv",
                               mime="text/csv", use_container_width=True)
        with crs:
            if st.button(t("거래일지 비우기", "Clear journal"), use_container_width=True):
                st.session_state.trade_log = []
                st.rerun()
    else:
        st.markdown(f'<div class="footnote">{t("아직 기록된 거래가 없습니다.", "No trades yet.")}</div>', unsafe_allow_html=True)

    with st.expander(t("거래 복기", "Trade review")):
        with st.form("review_form"):
            rv_name = st.text_input(t("어떤 거래?", "Which trade?"),
                st.session_state.trade_log[-1]["name"] if st.session_state.trade_log else "")
            r1, r2 = st.columns(2)
            with r1:
                rv_plan = st.radio(t("계획대로 진입했는가?", "Entered as planned?"), ["Yes", "No"], horizontal=True)
                rv_stop = st.radio(t("손절 기준을 지켰는가?", "Followed stop rule?"), ["Yes", "No"], horizontal=True)
            with r2:
                rv_emo = st.radio(t("감정적으로 진입했는가?", "Entered emotionally?"), ["No", "Yes"], horizontal=True)
                rv_tp = st.radio(t("익절 기준을 지켰는가?", "Followed TP rule?"), ["Yes", "No"], horizontal=True)
            rv_reason = st.text_area(t("진입 이유", "Why did you enter?"), height=70)
            rv_one = st.text_input(t("결과 한 줄 복기", "One-line review"))
            rv_fix = st.text_input(t("다음 거래에서 고칠 점", "Fix for next trade"))
            rv_save = st.form_submit_button(t("복기 저장", "Save review"), use_container_width=True)

        if rv_save:
            st.session_state.reviews.append({
                t("날짜", "Date"): date.today().isoformat(),
                t("거래", "Trade"): rv_name,
                t("계획 진입", "Planned"): rv_plan,
                t("감정 진입", "Emotional"): rv_emo,
                t("손절 준수", "Stop kept"): rv_stop,
                t("익절 준수", "TP kept"): rv_tp,
                t("진입 이유", "Reason"): rv_reason,
                t("복기", "Review"): rv_one,
                t("개선점", "Fix"): rv_fix})
            st.toast(t("저장했습니다", "Saved"))

        if st.session_state.reviews:
            st.dataframe(pd.DataFrame(st.session_state.reviews), use_container_width=True, hide_index=True)


# =====================================================
# Tab 5 — Portfolio (now last among data tabs)
# =====================================================
with tab_pf:
    st.markdown(f'<div class="headline">{t("포트폴리오", "Portfolio")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subline">{t("보유 포지션·현금·성과를 한눈에. 시작 자금 대비 얼마나 성장했는지도 보여드립니다.", "Positions, cash and performance — including growth vs your starting capital.")}</div>', unsafe_allow_html=True)

    # wallet import
    with st.expander(t("폴리마켓 지갑으로 포지션 불러오기", "Import positions from a Polymarket wallet")):
        st.markdown(f'<div class="footnote" style="margin:0 0 10px 0;">{t("폴리마켓 프로필 주소(0x로 시작)를 붙여넣으면 공개 데이터 API로 보유 포지션을 읽어옵니다. 로그인·서명 없이 조회만 합니다.", "Paste your Polymarket profile address (starts with 0x). We read your open positions via the public data API — read-only, no login or signing.")}</div>', unsafe_allow_html=True)
        addr = st.text_input(t("지갑 주소", "Wallet address"), "", placeholder="0x...")
        if st.button(t("불러오기", "Import"), use_container_width=True):
            a = addr.strip()
            if not (a.startswith("0x") and len(a) == 42):
                st.markdown(line(t("주소 형식 오류 — 0x로 시작하는 42자 주소인지 확인하세요.", "Bad address — must be 42 chars starting with 0x."), "b"), unsafe_allow_html=True)
            else:
                try:
                    with st.spinner(t("폴리마켓에서 불러오는 중", "Fetching")):
                        items = fetch_wallet_positions(a)
                    st.session_state.wallet_raw = items
                    open_items = [it for it in items if is_open_position(it)] if isinstance(items, list) else []
                    st.session_state.portfolio = [dict(
                        name=it.get("title") or "Polymarket position",
                        outcome=it.get("outcome", ""),
                        buy=round(float(it.get("avgPrice", 0)) * 100, 1),
                        shares=round(float(it.get("size", 0)), 2),
                        inv=round(float(it.get("initialValue", 0)), 2),
                        cur=round(float(it.get("curPrice", 0)) * 100, 1),
                    ) for it in open_items]
                    st.toast(t(f"보유 포지션 {len(open_items)}개", f"{len(open_items)} open positions"))
                    st.rerun()
                except urllib.error.HTTPError as e:
                    st.markdown(line(t(f"연결 실패 (HTTP {e.code}) — 주소 확인 필요", f"Failed (HTTP {e.code}) — check address"), "b"), unsafe_allow_html=True)
                except urllib.error.URLError:
                    st.markdown(line(t("응답 없음 — 잠시 후 다시 시도하세요.", "No response — try again later."), "b"), unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(line(t(f"불러오기 실패 — {e}", f"Import failed — {e}"), "b"), unsafe_allow_html=True)

    with st.expander(t("디버그 — raw API 응답 보기", "Debug — raw API response")):
        st.json(st.session_state.wallet_raw)

    cash = st.number_input(t("현금 잔고 (USDC, $)", "Cash balance (USDC, $)"), 0.0, value=float(st.session_state.cash), key="cash_input")
    st.session_state.cash = cash

    st.markdown(f'<div class="eyebrow" style="margin-top:18px;">{t("보유 포지션", "Open positions")}</div>', unsafe_allow_html=True)
    if st.session_state.portfolio:
        df = pd.DataFrame(st.session_state.portfolio)
        col_cfg = {
            "name": st.column_config.TextColumn(t("거래", "Trade")),
            "outcome": st.column_config.TextColumn(t("선택", "Side")),
            "buy": st.column_config.NumberColumn(t("매수가 (¢)", "Buy (¢)"), format="%.1f"),
            "shares": st.column_config.NumberColumn(t("수량", "Shares"), format="%.2f"),
            "inv": st.column_config.NumberColumn(t("투자금 ($)", "Cost ($)"), format="%.2f"),
            "cur": st.column_config.NumberColumn(t("현재가 (¢)", "Now (¢)"), format="%.1f"),
        }
        edited = st.data_editor(df, column_config=col_cfg, use_container_width=True,
                                hide_index=True, num_rows="dynamic", key="pf_editor")
        st.session_state.portfolio = edited.to_dict("records")
        st.markdown(f'<div class="footnote">{t("현재가 칸을 수정하면 손익이 다시 계산됩니다.", "Edit the Now (¢) column to recalculate.")}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f"""<div class="quiet" style="padding:36px 20px;">
<div class="q-title">{t("등록된 포지션이 없습니다", "No positions yet")}</div>
<div class="q-body">{t("아래에서 직접 추가하거나, 위에서 지갑으로 불러오세요.", "Add manually below, or import via wallet above.")}</div>
</div>""", unsafe_allow_html=True)

    with st.form("add_pos"):
        a1, a2, a3 = st.columns(3)
        with a1:
            np_name = st.text_input(t("거래 이름", "Trade name"), "")
            np_out = st.text_input(t("선택한 팀·결과", "Side"), "")
        with a2:
            np_buy = st.number_input(t("평균 매수가 (¢)", "Avg buy (¢)"), 0.1, 99.9, 50.0)
            np_cur = st.number_input(t("현재가 (¢)", "Now (¢)"), 0.1, 100.0, 50.0)
        with a3:
            np_shares = st.number_input(t("보유 수량", "Shares"), 0.0, value=0.0)
            np_inv = st.number_input(t("투자금 ($)", "Cost ($)"), 0.0, value=0.0)
        add_pos = st.form_submit_button(t("포지션 추가", "Add position"), use_container_width=True)

    if add_pos:
        if not np_name.strip():
            st.markdown(line(t("거래 이름을 입력해주세요.", "Please enter a name."), "w"), unsafe_allow_html=True)
        else:
            shares_v = np_shares if np_shares > 0 else (np_inv / (np_buy / 100) if np_buy > 0 else 0)
            inv_v = np_inv if np_inv > 0 else shares_v * (np_buy / 100)
            st.session_state.portfolio.append(dict(name=np_name, outcome=np_out, buy=np_buy,
                                                   shares=round(shares_v, 2), inv=round(inv_v, 2), cur=np_cur))
            st.rerun()

    # ---- assets ----
    pos_value = sum((p.get("shares", 0) or 0) * ((p.get("cur", 0) or 0) / 100) for p in st.session_state.portfolio)
    pos_cost = sum((p.get("inv", 0) or 0) for p in st.session_state.portfolio)
    unrealized = pos_value - pos_cost
    total_assets = cash + pos_value
    sc = prof["start_capital"]
    growth = (total_assets - sc) / sc * 100 if sc else 0
    g_tone = "pos" if growth >= 0 else "neg"
    u_tone = "pos" if unrealized >= 0 else "neg"

    realized_total = sum(tr["profit"] for tr in st.session_state.trade_log) + st.session_state.adj_year
    total_pnl = unrealized + realized_total
    total_roi = total_pnl / sc * 100 if sc else 0

    st.markdown(f'<div class="eyebrow" style="margin-top:22px;">{t("자산 현황", "Assets")}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stats">'
        + stat(t("현재 총자산", "Total assets"), money(total_assets), t("현금 + 평가금", "Cash + value"))
        + stat(t("총 투자금", "Total invested"), money(pos_cost), "")
        + stat(t("현재 평가금액", "Current value"), money(pos_value), "")
        + stat(t("보유 포지션", "Open positions"), f"{len(st.session_state.portfolio)}", "")
        + "</div>"
        + '<div class="stats">'
        + stat(t("실현손익", "Realized"), signed_money(realized_total), "", "pos" if realized_total >= 0 else "neg")
        + stat(t("미실현손익", "Unrealized"), signed_money(unrealized), "", "pos" if unrealized >= 0 else "neg")
        + stat(t("총 손익", "Total P&L"), signed_money(total_pnl), "", "pos" if total_pnl >= 0 else "neg")
        + stat(t("총 수익률", "Total ROI"), signed_pct(total_roi), t(f"시작 {money(sc)}", f"Start {money(sc)}"), "pos" if total_roi >= 0 else "neg")
        + "</div>", unsafe_allow_html=True)

    def pos_status(pct):
        if pct >= 2: return t("이익", "Profit"), "g"
        if pct <= -2: return t("손실", "Loss"), "b"
        return t("본전 근처", "Break-even"), "w"

    pos_rows = []
    for p in st.session_state.portfolio:
        sh = p.get("shares", 0) or 0
        pb = p.get("buy", 0) or 0
        pc = p.get("cur", 0) or 0
        pi = p.get("inv", 0) or 0
        val = sh * pc / 100
        up = val - pi
        upct = up / pi * 100 if pi else 0
        status, kind = pos_status(upct)
        color = {"g": "#1d7d4f", "b": "#d0312d", "w": "#b25e09"}[kind]
        pos_rows.append(
            f'<div class="spec-row"><div class="spec-key">{p.get("name", "")} · {p.get("outcome", "")}</div>'
            f'<div class="spec-val">{sh:.1f} · {pb:.1f}¢ → {pc:.1f}¢ · {money(val)} · '
            f'<b style="color:{color}">{signed_money(up)} ({signed_pct(upct)})</b></div>'
            f'<div><span class="state {kind}">{status}</span></div></div>')
    if pos_rows:
        st.markdown(f'<div class="eyebrow">{t("포지션별 손익", "Per-position P&L")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="spec">' + "".join(pos_rows) + '</div>', unsafe_allow_html=True)

    # ---- realized P&L by period with adjustments ----
    st.markdown(f'<div class="eyebrow">{t("실현손익", "Realized P&L")}</div>', unsafe_allow_html=True)
    with st.expander(t("앱 사용 전 손익 보정 (이미 번 돈 반영)", "Pre-app P&L adjustment (count earlier gains)")):
        st.markdown(f'<div class="footnote" style="margin:0 0 10px 0;">{t("앱을 쓰기 전에 이미 번(잃은) 금액을 더해 이번 달·올해 손익에 반영합니다.", "Add gains/losses made before using this app, so monthly/yearly totals are accurate.")}</div>', unsafe_allow_html=True)
        j1, j2 = st.columns(2)
        with j1:
            st.session_state.adj_month = st.number_input(t("이번 달 보정 ($)", "This-month adjustment ($)"), value=float(st.session_state.adj_month))
        with j2:
            st.session_state.adj_year = st.number_input(t("올해 보정 ($)", "This-year adjustment ($)"), value=float(st.session_state.adj_year))

    w, m, y = period_pnl()
    def pct_of_start(v):
        return signed_pct(v / sc * 100) if sc else "—"
    st.markdown(
        '<div class="stats three">'
        + stat(t("이번 주", "This week"), signed_money(w), pct_of_start(w), "pos" if w >= 0 else "neg")
        + stat(t("이번 달", "This month"), signed_money(m), pct_of_start(m), "pos" if m >= 0 else "neg")
        + stat(t("올해", "This year"), signed_money(y), pct_of_start(y), "pos" if y >= 0 else "neg")
        + "</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="footnote">{t("퍼센트는 시작 자금 기준입니다. 거래일지 기록 + 위 보정값으로 계산됩니다.", "Percentages are vs starting capital. Computed from journal entries + adjustments above.")}</div>', unsafe_allow_html=True)


# =====================================================
# Tab — Settings · tools
# =====================================================
with tab_set:
    st.markdown(f'<div class="headline">{t("설정 · 도구", "Settings · tools")}</div>', unsafe_allow_html=True)

    # ---- risk profile ----
    st.markdown(f'<div class="eyebrow">{t("내 리스크 프로필", "My risk profile")}</div>', unsafe_allow_html=True)
    with st.form("profile_form"):
        s1, s2 = st.columns(2)
        with s1:
            pf_assets = st.number_input(t("총자산 ($) — 포트폴리오 미사용 시 기준값", "Total assets ($) — fallback when portfolio empty"), 1.0, value=float(prof["assets"]))
            pf_start = st.number_input(t("시작 자금 ($)", "Starting capital ($)"), 1.0, value=float(prof["start_capital"]))
            pf_emotional = st.number_input(t("감정 한도 ($)", "Emotional cap ($)"), 1.0, value=float(prof["emotional_limit"]))
        with s2:
            pf_max = st.slider(t("적정 배팅 비율 (%)", "Comfort bet ratio (%)"), 1, 30, int(prof["max_pct"]))
            pf_block = st.slider(t("진입 금지선 (%)", "No-entry line (%)"), 5, 40, int(prof["block_pct"]))
        save_prof = st.form_submit_button(t("저장", "Save"), use_container_width=True)

    if save_prof:
        p = dict(prof)
        p.update(assets=pf_assets, start_capital=pf_start, emotional_limit=pf_emotional,
                 max_pct=float(pf_max), block_pct=float(max(pf_block, pf_max + 2)))
        st.session_state.profile = p
        st.toast(t("저장했습니다", "Saved"))
        st.rerun()

    if st.button(t("설문 다시 하기", "Redo questionnaire"), use_container_width=True):
        st.session_state.profile = None
        st.rerun()

    st.markdown(
        f'<div class="footnote">{t(f"현재 적용 — 적정 {g_:.0f}% · 주의 {c1_:.0f}% · 위험 {c2_:.0f}% · 진입 금지 {blk_:.0f}% · 시스템 실패 50% / 감정 한도 {money(prof['emotional_limit'])} · 강한 경고 {money(prof['emotional_limit']*2)} · 시스템 실패 {money(prof['emotional_limit']*4)}", f"Active — comfort {g_:.0f}% · caution {c1_:.0f}% · risk {c2_:.0f}% · block {blk_:.0f}% · failure 50% / cap {money(prof['emotional_limit'])} · strong warning {money(prof['emotional_limit']*2)} · failure {money(prof['emotional_limit']*4)}")}</div>',
        unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- URL helper ----
    st.markdown(f'<div class="eyebrow">{t("Polymarket URL 도우미", "Polymarket URL helper")}</div>', unsafe_allow_html=True)
    url = st.text_input("Polymarket URL", "https://polymarket.com/event/")
    if st.button(t("시장 정보 불러오기", "Fetch market info"), use_container_width=True):
        slug = extract_slug(url)
        if not slug:
            st.markdown(line(t("URL에서 slug를 찾지 못했습니다.", "Couldn't find a slug."), "b"), unsafe_allow_html=True)
        else:
            try:
                with st.spinner(t("불러오는 중", "Fetching")):
                    payload = fetch_gamma(slug)
                rows = extract_markets(payload)
                st.session_state.url_rows = rows
                if not rows:
                    st.markdown(line(t("시장을 찾지 못했습니다. /event/ URL인지 확인해주세요.", "No markets found. Check it's an /event/ URL."), "w"), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(line(t(f"불러오기 실패 — {e}", f"Fetch failed — {e}"), "b"), unsafe_allow_html=True)
    if st.session_state.url_rows:
        st.dataframe(pd.DataFrame(st.session_state.url_rows), use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- backup ----
    st.markdown(f'<div class="eyebrow">{t("백업 · 복원", "Backup · restore")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="footnote" style="margin:0 0 10px 0;">{t("새로고침하면 데이터가 사라집니다. 백업을 내려받아 두세요. 프로필도 함께 저장됩니다.", "Data is lost on refresh. Download a backup — your profile is included.")}</div>', unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        backup = {"profile": st.session_state.profile, "cash": st.session_state.cash,
                  "portfolio": st.session_state.portfolio, "trade_log": st.session_state.trade_log,
                  "adj_month": st.session_state.adj_month, "adj_year": st.session_state.adj_year,
                  "reviews": st.session_state.reviews}
        st.download_button(t("백업 내려받기 (JSON)", "Download backup (JSON)"),
                           data=json.dumps(backup, ensure_ascii=False, indent=2).encode("utf-8"),
                           file_name="memento_backup.json", mime="application/json", use_container_width=True)
    with bc2:
        up = st.file_uploader(t("백업 불러오기", "Restore backup"), type=["json"], label_visibility="collapsed")
        if up is not None:
            try:
                data = json.loads(up.read().decode("utf-8"))
                st.session_state.profile = data.get("profile") or st.session_state.profile
                st.session_state.cash = float(data.get("cash", 0))
                st.session_state.portfolio = data.get("portfolio", [])
                st.session_state.trade_log = data.get("trade_log", [])
                st.session_state.adj_month = float(data.get("adj_month", 0))
                st.session_state.adj_year = float(data.get("adj_year", 0))
                st.session_state.reviews = data.get("reviews", [])
                st.toast(t("복원했습니다", "Restored"))
                st.rerun()
            except Exception:
                st.markdown(line(t("백업 파일을 읽지 못했습니다.", "Could not read backup."), "b"), unsafe_allow_html=True)
