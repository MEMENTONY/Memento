import streamlit as st
import json
import urllib.parse
import urllib.request
import urllib.error
from datetime import date
import pandas as pd

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════
# DESIGN SYSTEM — Trading-grade UI
# Dark accents, clean white canvas, precision typography
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; box-sizing: border-box; }
.stApp { background: #f2f2f7 !important; }
.block-container { max-width: 1440px; padding-top: 1.4rem; padding-bottom: 3rem; }
section[data-testid="stSidebar"] { display: none; }
h1,h2,h3,h4,p,span,div,label { color: #1c1c1e; }

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
    background: #ffffff !important;
    border: 1.5px solid #d1d1d6 !important;
    border-radius: 10px !important;
    color: #1c1c1e !important;
    font-size: 14px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #1c1c1e !important;
    box-shadow: 0 0 0 3px rgba(28,28,30,0.08) !important;
}
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #d1d1d6 !important;
    border-radius: 10px !important;
    color: #1c1c1e !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #1c1c1e !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: -0.1px !important;
    transition: opacity 0.15s ease !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Metrics ── */
div[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px 16px;
    border: 1px solid #e5e5ea;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
div[data-testid="stMetricLabel"] p { color: #8e8e93 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
div[data-testid="stMetricValue"] { color: #1c1c1e !important; font-weight: 700 !important; font-size: 22px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; border-bottom: 1.5px solid #e5e5ea; padding-bottom: 6px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px !important; border: 1px solid transparent !important; padding: 6px 14px !important; font-size: 13px !important; font-weight: 500 !important; color: #8e8e93 !important; background: transparent !important; }
.stTabs [aria-selected="true"] { background: #1c1c1e !important; color: #ffffff !important; }

/* ── Cards ── */
.card { background: #ffffff; border-radius: 18px; padding: 20px; border: 1px solid #e5e5ea; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 14px; }
.card-soft { background: #f2f2f7; border-radius: 14px; padding: 16px 18px; border: 1px solid #e5e5ea; margin-bottom: 12px; }

/* ── Result Cards ── */
.rc { border-radius: 20px; padding: 22px 24px; margin: 14px 0; border: 1.5px solid transparent; }
.rc-good { background: linear-gradient(135deg, #edfbf3 0%, #ffffff 60%); border-color: #86efac; }
.rc-warn { background: linear-gradient(135deg, #fffbeb 0%, #ffffff 60%); border-color: #fcd34d; }
.rc-bad  { background: linear-gradient(135deg, #fef2f2 0%, #ffffff 60%); border-color: #fca5a5; }
.rc-title { font-size: 24px; font-weight: 700; color: #1c1c1e; margin-bottom: 4px; letter-spacing: -0.4px; }
.rc-sub   { font-size: 13px; color: #8e8e93; line-height: 1.55; }

/* ── Score Bars ── */
.bar-wrap { margin: 8px 0 12px 0; }
.bar-row { display:flex; justify-content:space-between; font-size:12px; font-weight:600; color:#6b7280; margin-bottom:4px; }
.bar-bg { height: 7px; border-radius:999px; background:#e5e5ea; overflow:hidden; }
.bar-fill { height:100%; border-radius:999px; }

/* ── Notices ── */
.nbox { padding:12px 15px; border-radius:12px; font-size:13.5px; margin:5px 0; line-height:1.55; }
.ng { background:#edfbf3; color:#166534; }
.nw { background:#fffbeb; color:#92400e; }
.nb { background:#fef2f2; color:#991b1b; }
.ni { background:#eff6ff; color:#1e40af; }

/* ── Report Cards ── */
.rpc { background:#ffffff; border:1px solid #e5e5ea; border-radius:16px; padding:16px 18px; margin-bottom:12px; }
.rpc-label { font-size:11px; font-weight:600; color:#8e8e93; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:3px; }
.rpc-value { font-size:15px; font-weight:600; color:#1c1c1e; margin-bottom:6px; }
.rpc-body  { font-size:13px; color:#6b7280; line-height:1.55; }
.badge { display:inline-block; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; margin-bottom:7px; }
.bg-good { background:#dcfce7; color:#166534; }
.bg-warn { background:#fef9c3; color:#854d0e; }
.bg-bad  { background:#fee2e2; color:#991b1b; }
.bg-blue { background:#dbeafe; color:#1e40af; }

/* ── AI Panel ── */
.ai-panel { background: #f2f2f7; border-radius: 18px; padding: 20px; min-height: 480px; }
.ai-section { background:#ffffff; border-radius:12px; padding:14px 16px; margin-bottom:10px; border:1px solid #e5e5ea; }
.ai-section-label { font-size:10px; font-weight:700; color:#8e8e93; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:5px; }
.ai-section-body { font-size:14px; color:#1c1c1e; line-height:1.65; }

/* ── Hero ── */
.hero { background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 50%, #f0faf4 100%); border:1px solid #e5e5ea; border-radius:20px; padding:24px 28px; margin-bottom:18px; box-shadow:0 4px 20px rgba(0,0,0,0.05); }
.hero-title { font-size:34px; font-weight:700; color:#1c1c1e; letter-spacing:-1px; line-height:1; margin-bottom:6px; }
.hero-sub { font-size:14px; color:#6b7280; line-height:1.6; }
.pill { display:inline-block; padding:4px 11px; border-radius:999px; border:1px solid #e5e5ea; background:#ffffff; color:#6b7280; font-size:12px; font-weight:500; margin-top:10px; margin-right:5px; }

/* ── Misc ── */
.stExpander { border:1px solid #e5e5ea !important; border-radius:14px !important; background:#ffffff !important; }
[data-testid="stCheckbox"] label { color:#1c1c1e !important; font-size:14px !important; }
hr { border:none; border-top:1px solid #e5e5ea; margin:18px 0; }
code { color:#1c1c1e !important; background:#f2f2f7 !important; border:1px solid #e5e5ea !important; white-space:pre-wrap !important; font-size:12px !important; }
div[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; border:1px solid #e5e5ea; }
.section-title { font-size:18px; font-weight:700; color:#1c1c1e; margin:4px 0 14px 0; letter-spacing:-0.3px; }
.muted { color:#8e8e93; font-size:13px; line-height:1.55; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
for key, default in [
    ("trade_log", []),
    ("tracked_positions", []),
    ("last_entry_result", None),
    ("last_position_result", None),
    ("ai_result", ""),
    ("ai_team_a", ""),
    ("ai_team_b", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ═══════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════
def clamp(v, lo=0, hi=100): return max(lo, min(hi, v))
def money(v): return f"-${abs(v):,.2f}" if v < 0 else f"${v:,.2f}"
def signed_money(v): return f"+${v:,.2f}" if v >= 0 else f"-${abs(v):,.2f}"
def signed_pct(v): return f"+{v:.1f}%" if v >= 0 else f"{v:.1f}%"
def cents_val(v): return f"{v:.1f}¢"
def cents_dec(v): return f"{v*100:.1f}¢" if v is not None else "n/a"

def bar(label, value, max_v=100, color="#34c759"):
    w = clamp((value / max_v * 100) if max_v else 0)
    return f"""<div class="bar-wrap">
<div class="bar-row"><span>{label}</span><span>{value:.1f}</span></div>
<div class="bar-bg"><div class="bar-fill" style="width:{w:.0f}%;background:{color};"></div></div>
</div>"""

def notice(text, kind="i"):
    cls = {"g": "ng", "w": "nw", "b": "nb", "i": "ni"}.get(kind, "ni")
    return f'<div class="nbox {cls}">{text}</div>'

def badge_html(text, kind="i"):
    cls = {"g": "bg-good", "w": "bg-warn", "b": "bg-bad", "i": "bg-blue"}.get(kind, "bg-blue")
    return f'<span class="badge {cls}">{text}</span>'

def rpc(label, value, body, badge_text="", badge_kind="i"):
    b = badge_html(badge_text, badge_kind) if badge_text else ""
    return f"""<div class="rpc">
<div class="rpc-label">{label}</div>
{b}
<div class="rpc-value">{value}</div>
<div class="rpc-body">{body}</div>
</div>"""

def result_cls(level):
    if level == "good": return "rc-good", "✅", "#166534"
    if level == "warn": return "rc-warn", "⚠️", "#92400e"
    return "rc-bad", "⛔", "#991b1b"


# ═══════════════════════════════════════════════════════
# SCORING RULES
# ═══════════════════════════════════════════════════════
def price_zone(price):
    if price >= 99:
        return "99¢ 매수 금지", "b", -30, "99¢는 사는 가격이 아니라 파는 가격입니다."
    if price >= 95:
        return "상환 스캘핑", "b", -24, "95~98¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."
    if price >= 90:
        return "신규매수 비추천", "b", -18, "90~95¢는 신규 매수 비추천 구간입니다."
    if price >= 85:
        return "매우 신중", "w", -10, "85~90¢는 신규 진입을 매우 신중하게 봐야 합니다."
    if price >= 80:
        return "익절 고려", "w", -6, "80~85¢는 신규 매수보다 익절 고려 구간입니다."
    if 2 <= price <= 5:
        return "초저가 bounce", "w", -12, "2~5¢ Bounce Trade는 소액 전용입니다."
    if price < 2:
        return "복권형", "b", -18, "2¢ 미만은 거의 복권형 가격입니다."
    if price <= 20:
        return "고변동", "w", -4, "저가 구간은 변동성이 큽니다. 소액만 적합합니다."
    return "정상 구간", "g", 0, "가격 구간 자체는 과도한 위험 신호가 없습니다."

def purpose_rule(p):
    rules = {
        "경기승리 / 만기 보유":        (1.00, 0,   "실제 승률 추정이 핵심인 기본 승리 베팅입니다."),
        "경기 시작 전 가격 상승 노림":  (0.70, -6,  "시장 심리와 타이밍이 핵심입니다. 익절 기준이 더 중요합니다."),
        "반반 경기 쏠림 이용 / 중간 익절": (0.60, -8, "승리보다 시장 쏠림을 이용하는 구조입니다."),
        "역배 / Bounce Trade":         (0.35, -13, "소액 전용입니다. 손실 제한이 핵심입니다."),
        "99¢ 상환 스캘핑":             (0.20, -25, "작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."),
        "뉴스/이벤트 선반영":          (0.50, -12, "조건문, resolution 기준, 뉴스 해석 오류를 반드시 확인해야 합니다."),
    }
    return rules.get(p, (1.00, 0, "일반 베팅으로 계산합니다."))

def market_type_rule(m):
    rules = {
        "Match Moneyline": (1.00, 0,   "가장 기본적인 시장입니다."),
        "Game Winner":     (0.50, -10, "단판 시장입니다. Moneyline보다 변동성이 큽니다. 추천 금액 50% 감소."),
        "Correct Score":   (0.25, -25, "맞히기 매우 어렵습니다. 강한 경고 대상입니다."),
        "정치 선거":        (0.50, -12, "결과 기준과 이의제기 가능성을 반드시 확인해야 합니다."),
        "뉴스/이벤트":      (0.50, -12, "조건문과 resolution 기준 확인이 필수입니다."),
        "99¢ 상환 스캘핑":  (0.20, -25, "고가 상환 스캘핑은 고액 금지입니다."),
        "2~5¢ Bounce Trade": (0.20, -18, "초저가 bounce는 소액 전용입니다."),
    }
    return rules.get(m, (1.00, 0, "일반 시장으로 계산합니다."))

def position_size_rule(pct):
    if pct >= 50: return "시스템 실패", "b", -100, "계좌 생존 리스크입니다. 절대 금지에 가깝습니다."
    if pct >= 20: return "진입 금지",  "b", -85,  "20% 이상은 진입 금지급 노출입니다."
    if pct >= 10: return "매우 위험",  "b", -38,  "10~20%는 매우 큰 포지션입니다. 일부 축소가 우선입니다."
    if pct >= 5:  return "위험",       "w", -20,  "5~10%는 위험 구간입니다. 확신보다 손실 가능액을 먼저 봐야 합니다."
    if pct >= 3:  return "주의",       "w", -8,   "3~5%는 주의 구간입니다."
    return "정상", "g", 5, "0~3%는 포지션 크기상 정상 범위입니다."

def exposure_rule(pct):
    if pct >= 20: return "중복 노출 금지", "b", -60, "같은 경기/방향 총 노출이 20% 이상입니다."
    if pct >= 10: return "중복 노출 위험", "b", -35, "같은 경기/방향 총 노출이 10~20%입니다."
    if pct >= 5:  return "중복 노출 주의", "w", -12, "같은 경기/방향 총 노출이 5~10%입니다."
    return "정상", "g", 0, "중복 노출은 관리 가능한 범위입니다."

def confidence_cap(c):
    return {"관찰용": 15, "낮은 확신": 25, "중간 확신": 50, "높은 확신": 70, "초고확신": 70}.get(c, 50)

def portfolio_cap(bankroll, c):
    pct = {"관찰용": 0.01, "낮은 확신": 0.02, "중간 확신": 0.04, "높은 확신": 0.06, "초고확신": 0.08}.get(c, 0.04)
    return bankroll * pct


# ═══════════════════════════════════════════════════════
# ENTRY CALCULATION ENGINE
# ═══════════════════════════════════════════════════════
def calculate_entry(
    market_name, current_price, fair_price, stake, purpose, market_type,
    bankroll, emotional_limit, confidence, target_price, stop_price,
    bookmaker_prob, previous_good_price, dup_ml, dup_game, dup_side, fomo_count
):
    edge = fair_price - current_price
    position_pct = (stake / bankroll) * 100 if bankroll > 0 else 0

    zone_label, zone_kind, zone_pen, zone_note = price_zone(current_price)
    p_mult, p_pen, p_note   = purpose_rule(purpose)
    m_mult, m_pen, m_note   = market_type_rule(market_type)
    size_label, size_kind, size_pen, size_note = position_size_rule(position_pct)

    base_cap = min(confidence_cap(confidence), portfolio_cap(bankroll, confidence), emotional_limit)
    rec_cap  = base_cap * p_mult * m_mult
    if fomo_count >= 1: rec_cap *= 0.5

    cap_status, cap_kind, cap_pen = "추천 상한선 이내", "g", 0
    if stake >= 200:       cap_status, cap_kind, cap_pen = "$200 이상 시스템 실패", "b", -90
    elif stake >= 100:     cap_status, cap_kind, cap_pen = "$100 이상 강한 경고", "b", -50
    elif stake > rec_cap * 1.2: cap_status, cap_kind, cap_pen = "추천 상한선 초과", "b", -32
    elif stake > rec_cap:  cap_status, cap_kind, cap_pen = "상한선 소폭 초과", "w", -12

    dup_total = dup_ml + dup_game + dup_side + stake
    dup_pct   = (dup_total / bankroll) * 100 if bankroll > 0 else 0
    exp_label, exp_kind, exp_pen, exp_note = exposure_rule(dup_pct)

    fomo_pen, fomo_status, fomo_kind = 0, "정상", "g"
    fomo_note = "감정 체크가 없습니다."
    if fomo_count >= 3:
        fomo_status, fomo_kind, fomo_pen = "감정 진입 금지", "b", -75
        fomo_note = "감정 체크 3개 이상입니다. 신규 진입 금지로 봐야 합니다."
    elif fomo_count >= 1:
        fomo_status, fomo_kind, fomo_pen = "감정 위험", "w", -20
        fomo_note = "감정 체크가 있습니다. 추천 금액을 50% 줄였습니다."

    chase_gap, chase_label, chase_kind, chase_pen = 0, "미입력", "i", 0
    chase_note = "처음 봤던 저평가 가격을 입력하지 않았습니다."
    if previous_good_price > 0:
        chase_gap = current_price - previous_good_price
        if chase_gap >= 30:   chase_label, chase_kind, chase_pen = "FOMO 추격", "b", -25; chase_note = "처음 봤던 가격보다 30¢ 이상 올랐습니다. 추격매수 위험이 큽니다."
        elif chase_gap >= 15: chase_label, chase_kind, chase_pen = "추격 위험", "w", -13; chase_note = "처음 봤던 가격보다 많이 올라 진입가 매력이 줄었습니다."
        elif chase_gap >= 5:  chase_label, chase_kind, chase_pen = "조금 상승", "w", -5;  chase_note = "처음 봤던 가격보다 조금 올랐습니다."
        else:                 chase_label, chase_kind, chase_pen = "추격 아님", "g", 5;   chase_note = "처음 봤던 가격 대비 추격 위험은 크지 않습니다."

    my_vs_poly  = fair_price - current_price
    book_vs_poly = bookmaker_prob - current_price if bookmaker_prob > 0 else 0
    my_vs_book   = fair_price - bookmaker_prob if bookmaker_prob > 0 else 0
    book_label, book_kind, book_pen = "북메이커 미입력", "i", 0
    book_note = "북메이커 기준 승률을 입력하면 공식 배당과의 괴리를 같이 볼 수 있습니다."
    if bookmaker_prob > 0:
        if my_vs_book >= 10:    book_label, book_kind, book_pen = "과신 재검토", "b", -12; book_note = "내 적정가가 북메이커보다 10%p 이상 높습니다."
        elif book_vs_poly >= 5: book_label, book_kind, book_pen = "외부배당도 저평가", "g", 6; book_note = "북메이커 기준으로도 Polymarket 가격이 싸 보입니다."
        elif book_vs_poly <= -5: book_label, book_kind, book_pen = "외부배당 기준 비쌈", "w", -8; book_note = "북메이커 기준으로는 Polymarket 가격이 비싼 편입니다."
        else: book_label, book_kind, book_pen = "큰 차이 없음", "i", 0; book_note = "북메이커와 Polymarket 가격 차이가 크지 않습니다."

    value_score = clamp(50 + edge*2.2 + zone_pen + p_pen + m_pen + chase_pen + book_pen)
    final_score = clamp(value_score + size_pen + exp_pen + fomo_pen + cap_pen)

    hard_stop = None
    if position_pct >= 50:  hard_stop = "시스템 실패 — 계좌 생존 리스크"
    elif stake >= 200:      hard_stop = "$200 이상 — 시스템 실패"
    elif position_pct >= 20: hard_stop = "진입 금지 — 포트폴리오 20% 이상"
    elif dup_pct >= 20:     hard_stop = "진입 금지 — 중복 노출 20% 이상"
    elif fomo_count >= 3:   hard_stop = "진입 금지 — 감정 배팅 위험"

    if hard_stop:        decision, level = hard_stop, "bad"
    elif final_score >= 75: decision, level = "진입 적절", "good"
    elif final_score >= 60: decision, level = "소액 진입 가능", "warn"
    elif final_score >= 45: decision, level = "관망 우선", "warn"
    else:                decision, level = "진입 부적절", "bad"

    shares = stake / (current_price / 100)
    win_profit = shares - stake
    target_profit = shares * (target_price/100) - stake
    stop_loss_amt = stake - shares * (stop_price/100)
    rr = target_profit / stop_loss_amt if stop_loss_amt > 0 else 0

    if target_profit > 0 and stop_loss_amt > 0:
        if stop_loss_amt > target_profit: rr_text, rr_level = f"손절 손실이 목표 수익보다 {stop_loss_amt/target_profit:.1f}배 큽니다.", "bad"
        elif target_profit >= stop_loss_amt*1.5: rr_text, rr_level = f"목표 수익이 손절 손실보다 {target_profit/stop_loss_amt:.1f}배 큽니다.", "good"
        else: rr_text, rr_level = f"손익비 {rr:.2f}:1 입니다.", "warn"
    else:
        rr_text, rr_level = "목표가 또는 손절가를 확인하세요.", "warn"

    current_value = shares * (current_price/100)
    additional_to_100 = shares - current_value
    high_warn = ""
    if current_price >= 90:
        high_warn = (f"현재부터 100¢까지 추가수익은 {money(additional_to_100)}뿐입니다. "
                     f"반대로 틀리면 현재 평가금 {money(current_value)}를 잃을 수 있습니다.")
    if current_price >= 97:
        high_warn += " 97~99¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출하는 구조입니다."

    reasons = []
    if edge >= 10:    reasons.append(("g", f"가격 메리트 좋음: 내 적정가가 현재가보다 {edge:.1f}¢ 높습니다."))
    elif edge >= 5:   reasons.append(("w", f"가격 메리트 약간 있음: edge {edge:.1f}¢ 입니다."))
    elif edge < 0:    reasons.append(("b", f"가격 메리트 없음: 현재가가 내 적정가보다 {abs(edge):.1f}¢ 비쌉니다."))
    else:             reasons.append(("w", f"가격 메리트 작음: edge {edge:.1f}¢ 입니다."))
    reasons.append((size_kind, f"포지션 크기: 총자산의 {position_pct:.1f}% — {size_label}"))
    reasons.append((cap_kind, f"추천 상한선: {money(rec_cap)} / 현재 투자금 {money(stake)} — {cap_status}"))
    reasons.append((zone_kind, f"가격 구간: {zone_label} — {zone_note}"))

    return dict(
        market_name=market_name, current_price=current_price, fair_price=fair_price,
        stake=stake, purpose=purpose, market_type=market_type, bankroll=bankroll,
        confidence=confidence, edge=edge, position_pct=position_pct, rec_cap=rec_cap,
        value_score=round(value_score,1), final_score=round(final_score,1),
        decision=decision, level=level, shares=shares, win_profit=win_profit,
        target_profit=target_profit, stop_loss_amt=stop_loss_amt, rr=rr,
        rr_text=rr_text, rr_level=rr_level, current_value=current_value,
        additional_to_100=additional_to_100, high_warn=high_warn,
        bookmaker_prob=bookmaker_prob, my_vs_poly=my_vs_poly,
        book_vs_poly=book_vs_poly, my_vs_book=my_vs_book,
        book_label=book_label, book_kind=book_kind, book_note=book_note,
        zone_label=zone_label, zone_kind=zone_kind, zone_note=zone_note,
        size_label=size_label, size_kind=size_kind, size_note=size_note,
        cap_status=cap_status, cap_kind=cap_kind, p_note=p_note, m_note=m_note,
        dup_total=dup_total, dup_pct=dup_pct,
        exp_label=exp_label, exp_kind=exp_kind, exp_note=exp_note,
        fomo_count=fomo_count, fomo_status=fomo_status, fomo_kind=fomo_kind, fomo_note=fomo_note,
        chase_gap=chase_gap, chase_label=chase_label, chase_kind=chase_kind, chase_note=chase_note,
        reasons=reasons,
    )


# ═══════════════════════════════════════════════════════
# CLAUDE AI ANALYSIS
# ═══════════════════════════════════════════════════════
def get_api_key():
    """Robustly fetch API key from Streamlit secrets"""
    for attempt in [
        lambda: st.secrets["ANTHROPIC_API_KEY"],
        lambda: st.secrets["anthropic"]["api_key"],
        lambda: st.secrets["anthropic"]["ANTHROPIC_API_KEY"],
    ]:
        try:
            key = attempt()
            if key and str(key).strip().startswith("sk-"):
                return str(key).strip()
        except Exception:
            continue
    return None


def call_claude_ai(team_a, team_b, league, current_price, fair_price, purpose):
    api_key = get_api_key()
    if not api_key:
        return None, "❌ API 키를 찾을 수 없습니다.\nStreamlit Secrets에 아래 형식으로 저장해주세요:\n\nANTHROPIC_API_KEY = \"sk-ant-...\""

    prompt = f"""당신은 LoL e스포츠 배팅 분석 전문가입니다.
배팅 관점에서 아래 경기를 분석해주세요.

경기 정보:
- 경기: {team_a} vs {team_b}
- 리그: {league}
- {team_a} 현재 Polymarket 배당: {current_price}¢
- 사용자의 적정가 추정: {fair_price}¢
- 배팅 목적: {purpose}

아래 6개 항목을 순서대로 분석해주세요.
각 항목 앞에 반드시 "1." "2." 형식의 번호를 붙여주세요.
각 항목은 2~3문장으로 간결하게 작성해주세요.

1. 리그 순위 ({league} 기준 {team_a}와 {team_b}의 현재 순위 및 포인트)
2. 이번 시즌 전적 (각 팀의 승/패 기록과 승률)
3. 최근 5경기 폼 (각 팀의 최근 흐름, 연승/연패 여부 포함)
4. 직접 상대 전적 (두 팀의 역대 및 최근 맞대결 기록)
5. 팀 상태 (로스터 이슈, 부진 선수, 눈에 띄는 특이사항)
6. 배팅 관점 ({current_price}¢ 배당이 실제 승률 대비 적절한지, 엣지가 있는지 직접 판단)

마지막 줄에 반드시 아래 형식으로 결론을 작성해주세요:
결론: [배팅 추천 / 비추천 / 중립]

반드시 한국어로 답변해주세요."""

    try:
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": prompt}]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["content"][0]["text"], None

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        if e.code == 401:
            return None, f"❌ API 키 인증 실패 (401)\n\nStreamlit Secrets에서 ANTHROPIC_API_KEY 값을 확인해주세요.\n현재 키가 올바른지 console.anthropic.com에서 확인하세요."
        return None, f"❌ API 오류 {e.code}: {body[:200]}"
    except Exception as e:
        return None, f"❌ 분석 실패: {str(e)}"


def render_ai_result(text):
    """Parse and render Claude's analysis as structured cards"""
    if not text:
        return

    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    sections = []
    cur_title, cur_body = "", []

    for line in lines:
        if len(line) > 2 and line[0].isdigit() and line[1] == ".":
            if cur_title:
                sections.append((cur_title, "\n".join(cur_body)))
            cur_title = line
            cur_body = []
        elif line.startswith("결론:"):
            if cur_title:
                sections.append((cur_title, "\n".join(cur_body)))
                cur_title, cur_body = "", []
            # Render conclusion prominently
            verdict = line
            kind = "rc-good" if "추천" in line and "비추천" not in line else "rc-bad" if "비추천" in line else "rc-warn"
            icon = "✅" if kind == "rc-good" else "⛔" if kind == "rc-bad" else "⚠️"
            st.markdown(f"""<div class="rc {kind}">
<div class="rc-title">{icon} {verdict}</div>
</div>""", unsafe_allow_html=True)
        else:
            cur_body.append(line)

    if cur_title and cur_body:
        sections.append((cur_title, "\n".join(cur_body)))

    for title, body in sections:
        st.markdown(f"""<div class="ai-section">
<div class="ai-section-label">{title}</div>
<div class="ai-section-body">{body}</div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# POLYMARKET API
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=8, show_spinner=False)
def fetch_clob(token_id):
    url = f"https://clob.polymarket.com/book?{urllib.parse.urlencode({'token_id': token_id.strip()})}"
    req = urllib.request.Request(url, headers={"User-Agent": "Memento/2.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

def parse_book(book):
    bids = book.get("bids") or []
    asks = book.get("asks") or []
    bb = max((float(x["price"]) for x in bids if x.get("price")), default=None)
    ba = min((float(x["price"]) for x in asks if x.get("price")), default=None)
    lt = book.get("last_trade_price")
    lt = float(lt) if lt not in [None, ""] else None
    mid = (bb + ba) / 2 if bb and ba else lt
    return bb, ba, lt, mid

@st.cache_data(ttl=60, show_spinner=False)
def fetch_gamma_event(slug):
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Memento/2.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode())

def extract_markets(payload):
    events = payload if isinstance(payload, list) else payload.get("events", [])
    rows = []
    for event in events:
        for m in event.get("markets", []):
            question = m.get("question") or m.get("title") or "Unknown"
            def parse_list(v):
                if isinstance(v, list): return v
                if isinstance(v, str):
                    try: return json.loads(v)
                    except: return []
                return []
            outcomes = parse_list(m.get("outcomes"))
            prices   = parse_list(m.get("outcomePrices"))
            tokens   = parse_list(m.get("clobTokenIds"))
            for i, outcome in enumerate(outcomes):
                rows.append({
                    "시장": question,
                    "선택지": outcome,
                    "현재가 (¢)": round(float(prices[i])*100, 1) if i < len(prices) else None,
                    "token_id": tokens[i] if i < len(tokens) else "",
                })
    return rows


# ═══════════════════════════════════════════════════════
# PARTIAL SELL CALCULATOR
# ═══════════════════════════════════════════════════════
def partial_sell_table(shares, price_dec, investment):
    rows, min_r = [], None
    if shares and price_dec and price_dec > 0:
        min_r = investment / (shares * price_dec) * 100
    for r in [25, 50, 70, 80, 90, 100]:
        ss  = shares * r / 100
        rec = ss * price_dec if price_dec else 0
        rem = shares - ss
        rows.append({
            "매도 비율": f"{r}%",
            "매도 수량": round(ss, 2),
            "회수금": money(rec),
            "원금 대비 손익": signed_money(rec - investment),
            "남은 수량": round(rem, 2),
            "남은 평가금": money(rem * price_dec if price_dec else 0),
            "100¢ 도달 추가수익": signed_money(rem * (1 - price_dec) if price_dec else 0),
        })
    return rows, min_r


# ═══════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-title">Memento</div>
  <div class="hero-sub">
    Polymarket 배팅 판단 도구 · 계좌를 지키는 수동 리스크 관리 앱<br>
    <b>좋은 팀이 아니라 좋은 가격을 산다. Edge가 좋아도 금액이 과하면 나쁜 거래다.</b>
  </div>
  <span class="pill">⚡ 진입 판독</span>
  <span class="pill">🤖 AI 팀 분석</span>
  <span class="pill">📍 포지션 관리</span>
  <span class="pill">🧩 부분매도</span>
  <span class="pill">🔎 URL 도우미</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ 진입 판독 + AI 분석",
    "📍 포지션 관리",
    "🧩 부분매도",
    "📈 거래일지",
    "🔎 URL 도우미",
])


# ════════════════════════════════════════════════════════
# TAB 1 — ENTRY EVALUATOR + AI ANALYSIS
# ════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([1, 1], gap="large")

    # ── LEFT: Entry Form + Results ──────────────────
    with left:
        st.markdown('<div class="section-title">⚡ 배팅 진입 판독</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted" style="margin-bottom:14px;">진입 전 숫자로 멈춰 세워주는 도구입니다.</div>', unsafe_allow_html=True)

        # Show previous result at top
        if st.session_state.last_entry_result:
            r = st.session_state.last_entry_result
            klass, icon, _ = result_cls(r["level"])
            score_text = f"적절성 {r['final_score']:.0f}%" if r["level"] != "bad" else f"부적절도 {100-r['final_score']:.0f}%"
            st.markdown(f"""<div class="rc {klass}">
<div class="rc-title">{icon} {r['decision']}</div>
<div class="rc-sub">
  <b>{r['market_name']}</b> &nbsp;|&nbsp;
  리스크 포함: <b>{score_text}</b> &nbsp;|&nbsp;
  순수 가치: <b>{r['value_score']:.0f}%</b>
</div>
</div>""", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            edge_c = "normal" if r["edge"] >= 5 else "inverse"
            c1.metric("Edge", f"{r['edge']:+.1f}¢", delta_color=edge_c)
            c2.metric("포트폴리오 비중", f"{r['position_pct']:.1f}%")
            c3.metric("추천 상한선", money(r["rec_cap"]))
            c4.metric("100¢ 추가수익", money(r["additional_to_100"]))

            st.markdown(
                bar("리스크 포함 최종 적절성", r["final_score"], 100,
                    "#34c759" if r["final_score"]>=70 else "#ff9500" if r["final_score"]>=50 else "#ff3b30") +
                bar("순수 가격 가치", r["value_score"], 100, "#007aff") +
                bar("포지션 크기 위험", min(r["position_pct"],100), 100,
                    "#ff3b30" if r["position_pct"]>=20 else "#ff9500" if r["position_pct"]>=5 else "#34c759"),
                unsafe_allow_html=True
            )

            # Key notices
            for kind, text in r["reasons"]:
                st.markdown(notice(text, kind), unsafe_allow_html=True)
            if r["high_warn"]:
                st.markdown(notice(r["high_warn"], "b"), unsafe_allow_html=True)

            # Detailed report (collapsed)
            with st.expander("📋 상세 판독 리포트 보기"):
                row1, row2 = st.columns(2)
                with row1:
                    st.markdown(rpc("진입가격 구간", r["zone_label"], r["zone_note"], badge_text=r["zone_label"], badge_kind=r["zone_kind"]), unsafe_allow_html=True)
                    st.markdown(rpc("배팅금액 / 계좌 생존", r["size_label"],
                        f"투자금 <b>{money(r['stake'])}</b> / 총자산 <b>{money(r['bankroll'])}</b><br>비중 {r['position_pct']:.1f}% — {r['size_note']}",
                        badge_text=r["size_label"], badge_kind=r["size_kind"]), unsafe_allow_html=True)
                    st.markdown(rpc("추천 상한선", r["cap_status"],
                        f"추천 {money(r['rec_cap'])} / 현재 {money(r['stake'])} / 확신: {r['confidence']}",
                        badge_text=r["cap_status"], badge_kind=r["cap_kind"]), unsafe_allow_html=True)
                    st.markdown(rpc("북메이커 비교", r["book_label"],
                        f"내 적정가-현재가: <b>{r['my_vs_poly']:+.1f}%p</b> / 북메이커-현재가: <b>{r['book_vs_poly']:+.1f}%p</b><br>{r['book_note']}",
                        badge_text=r["book_label"], badge_kind=r["book_kind"]), unsafe_allow_html=True)
                with row2:
                    st.markdown(rpc("손익비 / 목표가·손절가", f"손익비 {r['rr']:.2f}:1",
                        f"목표가 도달 시: <b>{money(r['target_profit'])}</b><br>손절 시 손실: <b>{money(r['stop_loss_amt'])}</b><br>{r['rr_text']}",
                        badge_text="손익비 분석", badge_kind=r["rr_level"]), unsafe_allow_html=True)
                    st.markdown(rpc("감정 / FOMO", r["fomo_status"],
                        f"체크 {r['fomo_count']}개 — {r['fomo_note']}",
                        badge_text=r["fomo_status"], badge_kind=r["fomo_kind"]), unsafe_allow_html=True)
                    st.markdown(rpc("중복 노출", r["exp_label"],
                        f"같은 경기 총 노출: <b>{money(r['dup_total'])}</b> / 비중 <b>{r['dup_pct']:.1f}%</b><br>{r['exp_note']}",
                        badge_text=r["exp_label"], badge_kind=r["exp_kind"]), unsafe_allow_html=True)
                    st.markdown(rpc("배팅 목적 / 시장 유형", "구조 리스크",
                        f"목적: <b>{r['purpose']}</b><br>{r['p_note']}<br>유형: <b>{r['market_type']}</b><br>{r['m_note']}",
                        badge_text="구조 분석", badge_kind="i"), unsafe_allow_html=True)

                # Scenario
                st.markdown("##### 수익/손실 시나리오")
                sc1, sc2, sc3, sc4 = st.columns(4)
                sc1.metric("보유 수량", f"{r['shares']:.2f}주")
                sc2.metric("승리 시 순이익", money(r["win_profit"]))
                sc3.metric("패배 시 손실", money(-r["stake"]))
                sc4.metric("100¢까지 추가수익", money(r["additional_to_100"]))

                summary = (f"{r['market_name']} | 현재가:{r['current_price']:.0f}¢ 적정가:{r['fair_price']:.0f}¢ "
                           f"Edge:{r['edge']:+.0f}¢ | 투자금:{money(r['stake'])} 비중:{r['position_pct']:.1f}% | "
                           f"판정:{r['decision']} | 적절성:{r['final_score']:.0f}% 가치:{r['value_score']:.0f}%")
                st.markdown("##### 기록용 한 줄 요약")
                st.code(summary)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="muted" style="margin-bottom:10px;">▼ 새 판독 입력</div>', unsafe_allow_html=True)

        with st.form("entry_form"):
            q_league = st.selectbox("리그", ["LCK", "LPL", "LEC", "LCS", "MSI/Worlds", "기타"])
            c1, c2 = st.columns(2)
            with c1: q_team_a = st.text_input("내가 배팅하는 팀", "T1")
            with c2: q_team_b = st.text_input("상대 팀", "HLE")

            market_name = st.text_input("시장 이름", "T1 vs HLE — Match Winner")

            c3, c4 = st.columns(2)
            with c3:
                current_price = st.number_input("현재가 (¢)", 1.0, 99.0, 52.0)
                stake = st.number_input("투자금 ($)", 1.0, value=50.0)
            with c4:
                fair_price = st.number_input("내 적정가 (¢)", 1.0, 99.0, 65.0)
                bankroll = st.number_input("포트폴리오 총액 ($)", 1.0, value=814.0)

            c5, c6 = st.columns(2)
            with c5:
                purpose = st.selectbox("배팅 목적", [
                    "경기승리 / 만기 보유", "경기 시작 전 가격 상승 노림",
                    "반반 경기 쏠림 이용 / 중간 익절", "역배 / Bounce Trade",
                    "99¢ 상환 스캘핑", "뉴스/이벤트 선반영",
                ])
            with c6:
                market_type = st.selectbox("시장 유형", [
                    "Match Moneyline", "Game Winner", "Correct Score",
                    "정치 선거", "뉴스/이벤트", "99¢ 상환 스캘핑", "2~5¢ Bounce Trade",
                ])

            with st.expander("⚙️ 고급 설정 (목표가·손절가·FOMO·중복)"):
                g1, g2, g3 = st.columns(3)
                with g1:
                    emotional_limit = st.number_input("감정 한도 ($)", 1.0, value=50.0)
                    confidence = st.selectbox("확신 수준", ["관찰용","낮은 확신","중간 확신","높은 확신","초고확신"], index=2)
                with g2:
                    target_price = st.number_input("목표가 (¢)", 1.0, 100.0, 75.0)
                    stop_price   = st.number_input("손절가 (¢)", 0.0, 99.0,  40.0)
                with g3:
                    bookmaker_prob     = st.number_input("북메이커 승률 (%)", 0.0, 99.0, 0.0)
                    previous_good_price = st.number_input("처음 봤던 저평가 가격 (¢)", 0.0, 99.0, 0.0)

                st.markdown("**중복 노출 ($)**")
                d1, d2, d3 = st.columns(3)
                with d1: dup_ml   = st.number_input("같은 경기 ML", 0.0, value=0.0)
                with d2: dup_game = st.number_input("Game Winner", 0.0, value=0.0, key="dup_game")
                with d3: dup_side = st.number_input("같은 방향 추가", 0.0, value=0.0)

                st.markdown("**FOMO / 감정 체크**")
                fomo_opts = [
                    "방금 큰 수익을 냈다", "방금 큰 손실을 냈다",
                    "아까 판 게 후회된다", "빨리 복구하고 싶다",
                    "더 빨리 계좌를 키우고 싶다", "놓치면 아깝다고 느낀다",
                    "이미 같은 경기에 포지션이 있다",
                ]
                fomo_count = 0
                fa, fb = st.columns(2)
                for i, opt in enumerate(fomo_opts):
                    with fa if i % 2 == 0 else fb:
                        if st.checkbox(opt, key=f"fe_{i}"): fomo_count += 1

            do_submit = st.form_submit_button("⚡ 판독하기 + AI 분석 요청", use_container_width=True)

        if do_submit:
            st.session_state.last_entry_result = calculate_entry(
                market_name, current_price, fair_price, stake, purpose, market_type,
                bankroll, emotional_limit, confidence, target_price, stop_price,
                bookmaker_prob, previous_good_price, dup_ml, dup_game, dup_side, fomo_count
            )
            st.session_state.ai_team_a = q_team_a
            st.session_state.ai_team_b = q_team_b
            with st.spinner("🤖 AI 팀 분석 중... (5~15초 소요)"):
                text, err = call_claude_ai(q_team_a, q_team_b, q_league, current_price, fair_price, purpose)
                st.session_state.ai_result = text if text else err
            st.rerun()

    # ── RIGHT: AI Analysis Panel ─────────────────────
    with right:
        st.markdown('<div class="section-title">🤖 AI 팀 분석</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted" style="margin-bottom:14px;">판독하기 버튼을 누르면 자동으로 분석됩니다.</div>', unsafe_allow_html=True)

        if st.session_state.ai_result:
            a_text = st.session_state.ai_result
            ta = st.session_state.get("ai_team_a", "")
            tb = st.session_state.get("ai_team_b", "")
            if ta and tb:
                st.markdown(f'<div class="card-soft" style="margin-bottom:14px;"><b>{ta} vs {tb}</b> — Claude AI 분석 결과</div>', unsafe_allow_html=True)

            if a_text.startswith("❌"):
                st.error(a_text)
                st.info("💡 **해결 방법:**\n1. share.streamlit.io → 앱 설정 → Secrets 탭\n2. `ANTHROPIC_API_KEY = \"sk-ant-...\"` 형식으로 저장\n3. 앱 Reboot")
            else:
                render_ai_result(a_text)

            if st.button("🔄 AI 분석 다시 요청", use_container_width=True):
                ta = st.session_state.get("ai_team_a", "")
                tb = st.session_state.get("ai_team_b", "")
                if ta and tb and st.session_state.last_entry_result:
                    r = st.session_state.last_entry_result
                    with st.spinner("🤖 재분석 중..."):
                        text, err = call_claude_ai(ta, tb, "LCK", r["current_price"], r["fair_price"], r["purpose"])
                        st.session_state.ai_result = text if text else err
                    st.rerun()
        else:
            st.markdown("""<div class="ai-panel">
<div style="text-align:center;padding:80px 20px;">
  <div style="font-size:52px;margin-bottom:14px;">🤖</div>
  <div style="font-size:16px;font-weight:600;color:#1c1c1e;margin-bottom:8px;">AI 분석 대기 중</div>
  <div style="font-size:13px;color:#8e8e93;line-height:1.7;">
    왼쪽에서 팀 이름을 입력하고<br>
    <b>판독하기 + AI 분석 요청</b>을<br>
    누르면 자동으로 분석됩니다.<br><br>
    <span style="font-size:12px;color:#aeaeb2;">LoL 팀의 리그 순위, 전적,<br>최근 폼, 상대 전적, 배팅 관점을<br>Claude AI가 분석해드립니다.</span>
  </div>
</div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 2 — POSITION MANAGEMENT
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📍 포지션 관리</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted" style="margin-bottom:16px;">이미 진입한 포지션의 현재가를 입력해서 매도/홀딩 타이밍을 판단합니다.</div>', unsafe_allow_html=True)

    # Show previous result
    if st.session_state.last_position_result:
        r = st.session_state.last_position_result
        klass, icon, _ = result_cls(r["level"])
        st.markdown(f"""<div class="rc {klass}">
<div class="rc-title">{icon} {r['decision']}</div>
<div class="rc-sub">{r.get('name','포지션')} · 현재가 기준 매도/홀딩 판단</div>
</div>""", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("현재 평가금", money(r["current_value"]))
        m2.metric("즉시 매도 손익", signed_money(r["pnl"]))
        m3.metric("현재 수익률", signed_pct(r["roi"]))
        m4.metric("포트폴리오 비중", f"{r['position_pct']:.1f}%")

        m5, m6, m7 = st.columns(3)
        m5.metric("100¢ 상환 총액", money(r["shares"]))
        m6.metric("100¢까지 추가수익", signed_money(r["additional"]))
        m7.metric("실패 시 손실", f"-{money(r['current_value'])}")

        st.markdown(
            bar("현재 수익률", max(r["roi"], 0), 100, "#34c759" if r["roi"] >= 0 else "#ff3b30") +
            bar("포트폴리오 비중", min(r["position_pct"], 100), 100,
                "#ff3b30" if r["position_pct"]>=20 else "#ff9500" if r["position_pct"]>=10 else "#34c759") +
            bar("현재가 위치 (¢)", r["current_price"], 100, "#007aff"),
            unsafe_allow_html=True
        )
        col_r, col_w = st.columns(2)
        with col_r:
            st.markdown("**이유**")
            for x in r["reasons"]:
                st.markdown(notice(x, "g"), unsafe_allow_html=True)
        with col_w:
            st.markdown("**경고**")
            for x in r["warnings"]:
                st.markdown(notice(x, "b" if "금지" in x or "손절" in x else "w"), unsafe_allow_html=True)

        # Partial sell table
        rows, min_r = partial_sell_table(r["shares"], r["current_price"]/100, r["investment"])
        if rows:
            st.markdown("##### 부분매도 시나리오")
            if min_r:
                if min_r <= 100: st.success(f"원금 회수 최소 매도 비율: {min_r:.1f}%")
                else: st.warning("현재 가격에서는 100% 팔아도 원금 회수 어렵습니다.")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        if st.button("이 포지션 목록에 저장", key="save_pos"):
            st.session_state.tracked_positions.append({
                "날짜": str(date.today()), "거래": r.get("name",""), "판정": r["decision"],
                "현재가": cents_val(r["current_price"]), "수익률": signed_pct(r["roi"]),
                "투자금": money(r["investment"]),
            })
            st.success("저장됐습니다.")

    st.markdown("<hr>", unsafe_allow_html=True)
    with st.form("position_form"):
        p_name = st.text_input("거래 이름", "KT Rolster vs Dplus KIA — Match Winner")
        p1, p2, p3 = st.columns(3)
        with p1:
            p_avg_buy    = st.number_input("평균 매수가 (¢)", 1.0, 99.0, 52.4)
        with p2:
            p_current    = st.number_input("현재가 / best bid (¢)", 1.0, 100.0, 58.0)
        with p3:
            p_shares     = st.number_input("보유 수량", 0.01, value=1164.12)

        p4, p5, p6 = st.columns(3)
        with p4: p_invest = st.number_input("투자금 ($)", 1.0, value=610.0)
        with p5: p_target = st.number_input("목표가 (¢)", 1.0, 100.0, 60.0)
        with p6: p_stop   = st.number_input("손절가 (¢)", 0.0, 99.0, 45.0)

        p7, p8 = st.columns(2)
        with p7: p_bankroll = st.number_input("포트폴리오 ($)", 1.0, value=814.0, key="p_bankroll")
        with p8: p_fomo     = st.slider("현재 감정 위험 체크 수", 0, 7, 0)

        pos_submit = st.form_submit_button("📍 포지션 판독하기", use_container_width=True)

    if pos_submit:
        cur_val = p_shares * (p_current / 100)
        pnl = cur_val - p_invest
        roi = pnl / p_invest * 100 if p_invest else 0
        pos_pct = cur_val / p_bankroll * 100 if p_bankroll else 0

        reasons, warnings = [], []
        if p_current >= p_target:
            decision, level = "목표가 도달 — 매도/부분매도 고려", "warn"
            reasons.append("목표가에 도달했습니다. 최소 일부 익절을 검토할 구간입니다.")
        elif p_current <= p_stop and cur_val >= p_invest * 0.3:
            decision, level = "손절 고려", "bad"
            reasons.append("손절가 이하이고 회수 가능한 금액이 아직 남아 있습니다.")
        elif cur_val <= p_invest * 0.1:
            decision, level = "손절 효용 낮음 — 추가매수 금지", "warn"
            reasons.append(f"현재 평가금이 원금의 {cur_val/p_invest*100:.0f}%입니다. 옵션처럼 보유 가능하지만 추가매수는 금지입니다.")
        else:
            decision, level = "홀딩 가능", "good"
            reasons.append("목표가와 손절가 사이에 있으며 홀딩 기본 조건 충족입니다.")

        if roi >= 30: warnings.append("수익률 +30% 이상 — 원금 회수 또는 부분매도 검토 권장.")
        if pos_pct >= 20: warnings.append("포트폴리오 비중 20% 이상 — 즉시 축소 고려."); decision, level = "진입 금지급 노출 — 즉시 축소", "bad"
        elif pos_pct >= 10: warnings.append("포트폴리오 비중 10% 이상 — 일부 축소 권장.")
        if p_fomo >= 3: warnings.append("감정 체크 3개 이상 — 신규/추가매수 금지."); decision, level = "감정 리스크 — 추가매수 금지", "bad"
        elif p_fomo >= 1: warnings.append("감정 체크 있음 — 섣부른 추가매수 주의.")
        if p_current >= 90: warnings.append(f"90¢ 이상 — 현재부터 100¢까지 추가수익은 {money(p_shares * (1 - p_current/100))}뿐입니다.")
        if not warnings: warnings.append("현재 큰 위험 신호는 없지만 목표가/손절가 기준은 유지해야 합니다.")

        st.session_state.last_position_result = dict(
            name=p_name, decision=decision, level=level,
            current_price=p_current, avg_buy=p_avg_buy, shares=p_shares,
            investment=p_invest, current_value=cur_val, pnl=pnl, roi=roi,
            position_pct=pos_pct, additional=p_shares - cur_val,
            reasons=reasons, warnings=warnings,
        )
        st.rerun()

    if st.session_state.tracked_positions:
        st.divider()
        st.markdown("##### 저장된 포지션")
        st.dataframe(pd.DataFrame(st.session_state.tracked_positions), use_container_width=True, hide_index=True)
        if st.button("포지션 목록 초기화"):
            st.session_state.tracked_positions = []
            st.rerun()


# ════════════════════════════════════════════════════════
# TAB 3 — PARTIAL SELL CALCULATOR
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🧩 부분매도 계산기</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted" style="margin-bottom:16px;">몇 %를 팔면 원금 회수가 되는지, 남은 포지션의 가치는 얼마인지 계산합니다.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: ps_buy    = st.number_input("매수가 (¢)", 1.0, 99.0, 52.4, key="ps_buy")
    with c2: ps_cur    = st.number_input("현재가 (¢)", 1.0, 100.0, 73.0, key="ps_cur")
    with c3: ps_invest = st.number_input("투자금 ($)", 0.0, value=100.0, key="ps_invest")

    use_manual = st.checkbox("보유 수량 직접 입력", value=True)
    if use_manual:
        ps_shares = st.number_input("보유 수량", 0.0, value=190.0, key="ps_shares")
    else:
        ps_shares = ps_invest / (ps_buy / 100) if ps_buy > 0 else 0

    if st.button("부분매도 표 계산하기", use_container_width=True):
        rows, min_r = partial_sell_table(ps_shares, ps_cur/100, ps_invest)
        cur_v = ps_shares * (ps_cur/100)
        additional = ps_shares - cur_v

        cc1, cc2, cc3, cc4 = st.columns(4)
        cc1.metric("보유 수량", f"{ps_shares:.2f}주")
        cc2.metric("현재 평가금", money(cur_v))
        cc3.metric("100¢까지 추가수익", money(additional))
        cc4.metric("실패 시 손실", f"-{money(cur_v)}")

        if min_r:
            if min_r <= 100: st.success(f"원금 회수 최소 매도 비율: {min_r:.1f}%")
            else: st.warning(f"현재 가격에서는 100% 팔아도 원금 회수가 어렵습니다. (필요 비율: {min_r:.1f}%)")

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown(notice(
            f"현재 평가금 <b>{money(cur_v)}</b>에서 100¢까지 추가로 얻을 수 있는 금액은 <b>{money(additional)}</b>입니다. "
            f"반대로 실패하면 현재 평가금 <b>{money(cur_v)}</b>를 잃을 수 있습니다.", "w"
        ), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 4 — TRADE LOG
# ════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">📈 거래일지 / 총수익률</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: r_start   = st.number_input("시작 자금 ($)", 0.0, value=500.0)
    with c2: r_current = st.number_input("현재 총자산 ($)", 0.0, value=650.0)
    with c3: r_deposit = st.number_input("추가 입금/출금 조정 ($)", value=0.0)

    adj = r_start + r_deposit
    total_p = r_current - adj
    total_r = total_p / adj * 100 if adj else 0
    klass, icon, _ = result_cls("good" if total_p >= 0 else "bad")
    st.markdown(f"""<div class="rc {klass}">
<div class="rc-title">{icon} 총손익 {signed_money(total_p)} ({signed_pct(total_r)})</div>
<div class="rc-sub">현재 총자산 {money(r_current)} · 시작 자금 {money(r_start)}</div>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("##### 거래 등록")
    with st.form("trade_form"):
        t1, t2, t3 = st.columns(3)
        with t1:
            log_name  = st.text_input("거래 이름", "T1 vs HLE — Match Winner")
            log_buy   = st.number_input("매수가 (¢)", 1.0, 99.0, 52.0, key="log_buy")
        with t2:
            log_sell  = st.number_input("매도가 (¢)", 0.0, 100.0, 78.0, key="log_sell")
            log_stake = st.number_input("투자금 ($)", 1.0, value=50.0, key="log_stake")
        with t3:
            log_note  = st.text_area("메모 (진입 이유 / 감정 상태)", height=100)
        add_trade = st.form_submit_button("거래 기록 추가", use_container_width=True)

    if add_trade:
        log_shares = log_stake / (log_buy / 100)
        log_sell_amt = log_shares * (log_sell / 100)
        log_profit = log_sell_amt - log_stake
        log_roi = log_profit / log_stake * 100
        st.session_state.trade_log.append({
            "날짜": str(date.today()), "거래": log_name,
            "매수가": f"{log_buy:.1f}¢", "매도가": f"{log_sell:.1f}¢",
            "투자금": money(log_stake), "손익": signed_money(log_profit),
            "수익률": signed_pct(log_roi), "메모": log_note,
        })
        st.success(f"기록 추가: {signed_money(log_profit)} ({signed_pct(log_roi)})")

    if st.session_state.trade_log:
        df_log = pd.DataFrame(st.session_state.trade_log)
        st.dataframe(df_log, use_container_width=True, hide_index=True)
        csv = df_log.to_csv(index=False).encode("utf-8-sig")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.download_button("📥 CSV 다운로드", data=csv, file_name="memento_trades.csv", mime="text/csv")
        with cc2:
            if st.button("거래일지 초기화"):
                st.session_state.trade_log = []
                st.rerun()
    else:
        st.markdown('<div class="muted">아직 기록된 거래가 없습니다. 위에서 거래를 등록해주세요.</div>', unsafe_allow_html=True)

    with st.expander("📝 거래 복기 질문"):
        for q in [
            "원하는 가격에 진입했는가?",
            "내 예상 승률의 근거는 무엇인가?",
            "북메이커와 왜 다르게 봤는가?",
            "금액은 감당 가능한 크기였는가?",
            "매도 기준을 지켰는가?",
            "감정적으로 들어간 부분이 있었는가?",
            "다음에 반복 가능한 거래인가?",
            "놓친 수익을 손실로 착각하고 있지는 않은가?",
            "같은 실수를 반복하지 않기 위해 다음 규칙은 무엇인가?",
        ]:
            st.markdown(f'<div class="nbox ni">— {q}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 5 — POLYMARKET URL HELPER
# ════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🔎 Polymarket URL → token_id 도우미</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted" style="margin-bottom:16px;">URL을 붙여넣으면 시장/선택지/token_id 목록을 보여드립니다. token_id를 복사해서 포지션 관리에 활용하세요.</div>', unsafe_allow_html=True)

    poly_url = st.text_input(
        "Polymarket 시장 URL",
        "https://polymarket.com/event/lck-2025-summer-winner",
        help="polymarket.com/event/... 형식의 URL을 붙여넣으세요"
    )

    if st.button("시장 정보 불러오기", use_container_width=True):
        # Extract slug from URL
        from urllib.parse import urlparse
        parsed = urlparse(poly_url.strip())
        path_parts = [p for p in parsed.path.strip("/").split("/") if p]
        slug = path_parts[-1] if path_parts else ""

        if not slug:
            st.error("URL에서 slug를 찾지 못했습니다. polymarket.com/event/slug-here 형식인지 확인해주세요.")
        else:
            st.markdown(f'<div class="nbox ni">찾은 slug: <code>{slug}</code></div>', unsafe_allow_html=True)
            try:
                with st.spinner("Polymarket Gamma API 조회 중..."):
                    payload = fetch_gamma_event(slug)
                rows = extract_markets(payload)
                if not rows:
                    st.warning("시장 후보를 찾지 못했습니다. URL이 올바른지, 아직 활성화된 시장인지 확인해주세요.")
                    st.info("💡 Tip: /event/ 경로의 URL만 지원됩니다. /ko/ 언어 경로는 /event/로 바꿔보세요.")
                else:
                    df_markets = pd.DataFrame(rows)
                    st.dataframe(df_markets, use_container_width=True, hide_index=True)
                    st.markdown(notice("위 표에서 원하는 선택지의 <b>token_id</b>를 복사해서 포지션 관리 탭에 붙여넣으세요.", "g"), unsafe_allow_html=True)
                    st.markdown(notice("token_id를 이용해 실시간 가격 조회 기능은 다음 버전에서 추가될 예정입니다. 지금은 참고용으로 활용하세요.", "i"), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"불러오기 실패: {str(e)}")
                st.markdown(notice("Gamma API가 일시적으로 응답하지 않을 수 있습니다. 잠시 후 다시 시도해주세요.", "w"), unsafe_allow_html=True)
