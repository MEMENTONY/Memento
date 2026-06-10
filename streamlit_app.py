import streamlit as st
import json
import urllib.parse
import urllib.request
from datetime import date

st.set_page_config(
    page_title="Memento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #ffffff !important; }
.block-container { max-width: 1400px; padding-top: 2rem; padding-bottom: 3rem; }
section[data-testid="stSidebar"] { display: none; }
h1, h2, h3, p, span, label, div { color: #1d1d1f; }
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
textarea {
    background: #f5f5f7 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #1d1d1f !important;
    font-size: 15px !important;
}
div[data-baseweb="select"] > div {
    background: #f5f5f7 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #1d1d1f !important;
}
.stButton > button {
    background: #1d1d1f !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
}
.stButton > button:hover { background: #3d3d3f !important; }
div[data-testid="stMetric"] {
    background: #f5f5f7;
    border-radius: 12px;
    padding: 14px 16px;
    border: none;
}
div[data-testid="stMetricLabel"] p { color: #6e6e73 !important; font-size: 12px !important; }
div[data-testid="stMetricValue"] { color: #1d1d1f !important; font-weight: 600 !important; }
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 1px solid #e8e8ed;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px !important;
    border: 1px solid #e8e8ed !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6e6e73 !important;
    background: white !important;
}
.stTabs [aria-selected="true"] {
    background: #1d1d1f !important;
    color: white !important;
    border-color: #1d1d1f !important;
}
.result-card {
    border-radius: 16px;
    padding: 22px;
    margin: 16px 0;
}
.result-good { background: #f0faf4; border: 1px solid #c3e6cb; }
.result-warn { background: #fffbf0; border: 1px solid #ffe08a; }
.result-bad  { background: #fff0f0; border: 1px solid #ffb3b3; }
.result-title { font-size: 22px; font-weight: 600; color: #1d1d1f; margin-bottom: 4px; }
.result-sub   { font-size: 14px; color: #6e6e73; }
.notice { padding: 12px 16px; border-radius: 10px; font-size: 14px; margin: 6px 0; color: #1d1d1f; }
.notice-good { background: #f0faf4; }
.notice-warn { background: #fffbf0; }
.notice-bad  { background: #fff0f0; }
.bar-wrap { margin: 8px 0 12px 0; }
.bar-label-row { display: flex; justify-content: space-between; font-size: 12px; color: #6e6e73; margin-bottom: 4px; }
.bar-bg { height: 6px; border-radius: 999px; background: #e8e8ed; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; }
.section-title { font-size: 20px; font-weight: 600; color: #1d1d1f; margin: 8px 0 16px 0; }
.muted { color: #6e6e73; font-size: 13px; }
.ai-panel {
    background: #f5f5f7;
    border-radius: 16px;
    padding: 20px;
    height: 100%;
    min-height: 500px;
}
.ai-panel-title {
    font-size: 15px;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 4px;
}
.ai-panel-sub {
    font-size: 12px;
    color: #6e6e73;
    margin-bottom: 16px;
}
.ai-section {
    background: #ffffff;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}
.ai-section-label {
    font-size: 11px;
    font-weight: 600;
    color: #6e6e73;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.ai-section-content {
    font-size: 14px;
    color: #1d1d1f;
    line-height: 1.6;
}
.stExpander { border: 1px solid #e8e8ed !important; border-radius: 12px !important; }
[data-testid="stCheckbox"] label { color: #1d1d1f !important; font-size: 14px !important; }
</style>
""", unsafe_allow_html=True)

# ── 세션 ──────────────────────────────────────────
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []
if "tracked_positions" not in st.session_state:
    st.session_state.tracked_positions = []
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None

# ── 유틸 함수 ─────────────────────────────────────
def clamp(v, lo=0, hi=100): return max(lo, min(hi, v))
def money(v): return f"-${abs(v):,.2f}" if v < 0 else f"${v:,.2f}"
def signed_money(v): return f"+${v:,.2f}" if v >= 0 else f"-${abs(v):,.2f}"
def signed_pct(v): return f"+{v:.1f}%" if v >= 0 else f"{v:.1f}%"
def cents_dec(v): return f"{v*100:.1f}¢" if v is not None else "n/a"
def cents(v): return f"{v:.1f}¢"

def bar(label, value, max_v=100, color="#34c759"):
    w = clamp(value / max_v * 100 if max_v else 0)
    return f"""<div class="bar-wrap">
<div class="bar-label-row"><span>{label}</span><span>{value:.1f}</span></div>
<div class="bar-bg"><div class="bar-fill" style="width:{w:.0f}%;background:{color};"></div></div>
</div>"""

def result_cls(level):
    if level == "good": return "result-good", "✅", "#1a7f37"
    if level == "warn": return "result-warn", "⚠️", "#9a6700"
    return "result-bad", "⛔", "#cf2b2b"

@st.cache_data(ttl=8, show_spinner=False)
def fetch_book(token_id):
    url = f"https://clob.polymarket.com/book?{urllib.parse.urlencode({'token_id': token_id.strip()})}"
    req = urllib.request.Request(url, headers={"User-Agent": "Memento/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

def best_prices(book):
    bids = book.get("bids") or []
    asks = book.get("asks") or []
    bb = max((float(x["price"]) for x in bids if x.get("price")), default=None)
    ba = min((float(x["price"]) for x in asks if x.get("price")), default=None)
    lt = book.get("last_trade_price")
    lt = float(lt) if lt not in [None, ""] else None
    mid = (bb + ba) / 2 if bb and ba else lt
    return bb, ba, lt, mid

def high_price_warn(p_dec):
    if p_dec is None: return None
    p = p_dec * 100
    if p >= 99: return "99¢는 사는 가격이 아니라 파는 가격입니다."
    if p >= 95: return "95~98¢ 고액 매수는 작은 수익을 위해 큰 금액을 위험에 노출합니다."
    if p >= 90: return "90~95¢는 신규 매수 비추천 구간입니다."
    if p >= 85: return "85~90¢는 신규 진입 신중 구간입니다."
    if p >= 80: return "80~85¢는 익절 고려 구간입니다."
    return None

def partial_rows(shares, price_dec, investment):
    rows, min_r = [], None
    if price_dec:
        min_r = investment / (shares * price_dec) * 100 if shares and price_dec else None
    for r in [25, 50, 70, 80, 90, 100]:
        ss = shares * r / 100
        rec = ss * price_dec if price_dec else 0
        rem = shares - ss
        rows.append({
            "매도 비율": f"{r}%",
            "매도 수량": round(ss, 2),
            "회수금": money(rec),
            "원금 대비 손익": signed_money(rec - investment),
            "남은 수량": round(rem, 2),
            "남은 평가금": money(rem * price_dec if price_dec else 0),
            "100¢ 도달 시 추가수익": signed_money(rem * (1 - price_dec) if price_dec else 0),
        })
    return rows, min_r

def call_claude_analysis(team_a, team_b, league, current_price, fair_price, purpose):
    """Claude API로 팀 분석 요청"""
    try:
        try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    try:
        api_key = st.secrets["anthropic"]["api_key"]
    except:
        return "❌ API 키를 찾을 수 없습니다. Secrets 설정을 확인해주세요."
    except Exception:
        return "❌ API 키가 설정되지 않았습니다. Streamlit Secrets에 ANTHROPIC_API_KEY를 등록해주세요."

    prompt = f"""너는 LoL e스포츠 배팅 분석 전문가야.
아래 경기를 배팅 관점에서 분석해줘.

경기: {team_a} vs {team_b}
리그: {league}
현재 배당(¢): {team_a} = {current_price}¢
내가 생각하는 적정가: {fair_price}¢
배팅 목적: {purpose}

아래 항목을 순서대로 분석해줘. 각 항목은 2~3줄로 간결하게.

1. 리그 순위 ({team_a} vs {team_b} 현재 순위)
2. 이번 시즌 전적 (각 팀 승/패)
3. 최근 5경기 폼 (연승/연패 포함)
4. 상대 전적 (두 팀 직접 맞대결)
5. 팀 상태 (로스터, 부진 선수, 이슈)
6. 배팅 관점 ({current_price}¢ 배당이 적절한지, 엣지가 있는지)

마지막에 한 줄 결론: "배팅 추천 / 비추천 / 중립" 중 하나로 끝내줘.
한국어로 답해줘."""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
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
        result = json.loads(r.read().decode())
        return result["content"][0]["text"]

# ── 헤더 ─────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:32px;font-weight:600;color:#1d1d1f;letter-spacing:-0.5px;">Memento</div>
  <div style="font-size:14px;color:#6e6e73;margin-top:2px;">Polymarket 배팅 판단 도구 · LoL e스포츠 특화</div>
</div>
""", unsafe_allow_html=True)

# ── 탭 ───────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ 빠른 판독 + AI 분석",
    "📡 실시간 포지션",
    "💰 손익 계산",
    "🧩 부분매도",
    "📈 거래 기록",
])

# ════════════════════════════════════════════════
# TAB 1 — 빠른 판독 + AI 분석 (좌우 레이아웃)
# ════════════════════════════════════════════════
with tab1:
    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown('<div class="section-title">⚡ 빠른 배팅 판독</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted" style="margin-bottom:16px;">숫자만 넣으면 바로 판단해 드립니다.</div>', unsafe_allow_html=True)

        with st.form("quick_form"):
            q_league  = st.selectbox("리그", ["LCK", "LPL", "LEC", "LCS", "기타"])
            q_team_a  = st.text_input("팀 A (내가 배팅하는 팀)", "T1")
            q_team_b  = st.text_input("팀 B (상대 팀)", "HLE")
            
            c1, c2 = st.columns(2)
            with c1:
                q_current  = st.number_input("현재가 (¢)", 1.0, 99.0, 52.0)
                q_stake    = st.number_input("투자금 ($)", 1.0, value=50.0)
            with c2:
                q_fair     = st.number_input("내 적정가 (¢)", 1.0, 99.0, 65.0)
                q_bankroll = st.number_input("포트폴리오 ($)", 1.0, value=1000.0)

            q_purpose = st.selectbox("배팅 목적", [
                "경기승리 / 만기 보유",
                "경기 시작 전 상승 노림",
                "중간 익절",
                "역배 / Bounce",
                "99¢ 상환 스캘핑",
            ])

            with st.expander("⚙️ 고급 설정 (선택사항)"):
                gc1, gc2 = st.columns(2)
                with gc1:
                    q_target = st.number_input("목표가 (¢)", 1.0, 99.0, 80.0)
                    q_stop   = st.number_input("손절가 (¢)", 1.0, 99.0, 35.0)
                with gc2:
                    st.markdown("**FOMO 체크**")
                    f1 = st.checkbox("방금 큰 수익을 냈다")
                    f2 = st.checkbox("방금 큰 손실을 냈다")
                    f3 = st.checkbox("빨리 복구하고 싶다")
                    f4 = st.checkbox("놓치면 아깝다고 느낀다")
                    f5 = st.checkbox("이미 같은 경기에 포지션이 있다")

            submitted = st.form_submit_button("판독하기 + AI 분석", use_container_width=True)

        if submitted:
            # 판독 계산
            fomo = sum([f1, f2, f3, f4, f5])
            edge = q_fair - q_current
            pos_pct = q_stake / q_bankroll * 100

            score = 50 + edge * 2
            if pos_pct >= 20: score -= 80
            elif pos_pct >= 10: score -= 35
            elif pos_pct >= 5: score -= 15
            if q_current >= 95: score -= 30
            elif q_current >= 90: score -= 20
            elif q_current >= 80: score -= 10
            if fomo >= 3: score -= 50
            elif fomo >= 1: score -= 20
            if "역배" in q_purpose or "99¢" in q_purpose: score -= 10
            score = clamp(score)

            if pos_pct >= 50:   decision, level = "시스템 실패 — 계좌 생존 리스크", "bad"
            elif pos_pct >= 20: decision, level = "진입 금지", "bad"
            elif fomo >= 3:     decision, level = "신규 진입 금지 (감정 불안정)", "bad"
            elif score >= 70:   decision, level = "진입 적절", "good"
            elif score >= 55:   decision, level = "소액 진입 가능", "warn"
            elif score >= 40:   decision, level = "관망 우선", "warn"
            else:               decision, level = "진입 부적절", "bad"

            klass, icon, color = result_cls(level)
            st.markdown(f"""
            <div class="result-card {klass}">
                <div class="result-title">{icon} {decision}</div>
                <div class="result-sub">적절성 점수 {score:.0f}% · 포트폴리오 비중 {pos_pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Edge", f"{edge:+.1f}¢")
            m2.metric("포트폴리오 비중", f"{pos_pct:.1f}%")
            m3.metric("100¢ 상환 수익", f"+${q_stake / q_current * 100 - q_stake:.2f}")

            st.markdown(
                bar("가격 가치", clamp(50 + edge * 2), 100, "#34c759" if edge >= 0 else "#ff3b30") +
                bar("포지션 크기 위험", min(pos_pct, 100), 100,
                    "#ff3b30" if pos_pct >= 20 else "#ff9500" if pos_pct >= 10 else "#34c759"),
                unsafe_allow_html=True
            )

            hw = high_price_warn(q_current / 100)
            if hw:
                st.markdown(f'<div class="notice notice-warn">⚠️ {hw}</div>', unsafe_allow_html=True)
            if fomo >= 1:
                st.markdown(f'<div class="notice notice-warn">🧠 FOMO {fomo}개 체크됨 — 감정 배팅 주의</div>', unsafe_allow_html=True)

            # AI 분석 호출
            with st.spinner("AI 팀 분석 중..."):
                try:
                    analysis = call_claude_analysis(
                        q_team_a, q_team_b, q_league,
                        q_current, q_fair, q_purpose
                    )
                    st.session_state.ai_analysis = analysis
                except Exception as e:
                    st.session_state.ai_analysis = f"분석 실패: {str(e)}"

    # ── 오른쪽: AI 분석 패널 ──────────────────────
    with right_col:
        st.markdown('<div class="section-title">🤖 AI 팀 분석</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted" style="margin-bottom:16px;">판독하기 버튼을 누르면 자동으로 분석됩니다.</div>', unsafe_allow_html=True)

        if st.session_state.ai_analysis:
            # 분석 결과를 섹션별로 표시
            lines = st.session_state.ai_analysis.strip().split("\n")
            
            current_section = []
            current_title = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 번호로 시작하는 섹션 제목 감지 (1. 2. 3. 등)
                if len(line) > 2 and line[0].isdigit() and line[1] == ".":
                    # 이전 섹션 저장
                    if current_title and current_section:
                        content = " ".join(current_section)
                        st.markdown(f"""
                        <div class="ai-section">
                            <div class="ai-section-label">{current_title}</div>
                            <div class="ai-section-content">{content}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    current_title = line
                    current_section = []
                else:
                    current_section.append(line)
            
            # 마지막 섹션
            if current_title and current_section:
                content = " ".join(current_section)
                st.markdown(f"""
                <div class="ai-section">
                    <div class="ai-section-label">{current_title}</div>
                    <div class="ai-section-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            elif current_section:
                # 섹션 구분 없이 전체 텍스트
                st.markdown(f"""
                <div class="ai-section">
                    <div class="ai-section-content">{" ".join(current_section)}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ai-panel">
                <div style="text-align:center;padding-top:80px;">
                    <div style="font-size:40px;margin-bottom:12px;">🤖</div>
                    <div style="font-size:15px;font-weight:500;color:#1d1d1f;margin-bottom:6px;">AI 팀 분석 대기 중</div>
                    <div style="font-size:13px;color:#6e6e73;">왼쪽에서 팀 이름 입력 후<br>판독하기 버튼을 누르면<br>자동으로 분석됩니다.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════
# TAB 2 — 실시간 포지션
# ════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">실시간 포지션 판독</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted" style="margin-bottom:16px;">token_id를 넣으면 Polymarket CLOB에서 실시간 가격을 가져옵니다.</div>', unsafe_allow_html=True)

    with st.form("live_form"):
        c1, c2 = st.columns(2)
        with c1:
            l_name     = st.text_input("거래 이름", "KT Rolster vs Dplus KIA")
            l_outcome  = st.text_input("선택한 팀/결과", "KT Rolster")
            l_token    = st.text_input("token_id", "")
            l_bankroll = st.number_input("포트폴리오 ($)", 1.0, value=814.0)
        with c2:
            l_buy      = st.number_input("평균 매수가 (¢)", 0.1, 99.9, 52.4)
            l_shares   = st.number_input("보유 수량", 0.0, value=1164.12)
            l_invest   = st.number_input("투자금 ($)", 0.0, value=610.0)
            l_target   = st.number_input("목표가 (¢)", 0.1, 100.0, 60.0)
            l_stop     = st.number_input("손절가 (¢)", 0.0, 99.9, 45.0)
        l_fomo = st.checkbox("지금 감정/FOMO 위험이 있다")
        live_submitted = st.form_submit_button("가격 조회 + 판정", use_container_width=True)

    if live_submitted:
        if not l_token.strip():
            st.error("token_id를 입력해 주세요.")
        else:
            try:
                with st.spinner("Polymarket 가격 조회 중..."):
                    book = fetch_book(l_token)
                    bb, ba, lt, mid = best_prices(book)

                sell_p = bb if bb else mid
                disp_p = mid if mid else lt

                if sell_p is None:
                    st.error("가격 정보를 가져오지 못했습니다.")
                else:
                    cur_val   = l_shares * (disp_p or sell_p)
                    sell_amt  = l_shares * sell_p
                    pnl       = sell_amt - l_invest
                    roi       = pnl / l_invest * 100 if l_invest else 0
                    pos_pct   = cur_val / l_bankroll * 100 if l_bankroll else 0

                    if pos_pct >= 20:   decision, level = "즉시 축소 고려 — 생존 리스크", "bad"
                    elif sell_p >= l_target/100: decision, level = "목표가 도달 — 매도 고려", "warn"
                    elif roi >= 30:     decision, level = "원금 회수 또는 부분매도 검토", "warn"
                    elif sell_p <= l_stop/100: decision, level = "손절 고려", "bad"
                    else:               decision, level = "홀딩 가능", "good"

                    if l_fomo and level == "good":
                        decision, level = "홀딩 가능, 단 감정 리스크 확인", "warn"

                    klass, icon, color = result_cls(level)
                    st.markdown(f"""
                    <div class="result-card {klass}">
                        <div class="result-title">{icon} {decision}</div>
                        <div class="result-sub">{l_name} · {l_outcome} · 즉시 매도 기준 {cents_dec(sell_p)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    m1,m2,m3 = st.columns(3)
                    m1.metric("best bid", cents_dec(bb))
                    m2.metric("best ask", cents_dec(ba))
                    m3.metric("last trade", cents_dec(lt))

                    m4,m5,m6,m7 = st.columns(4)
                    m4.metric("현재 평가금", money(cur_val))
                    m5.metric("즉시 매도 회수금", money(sell_amt))
                    m6.metric("실현 가능 손익", signed_money(pnl))
                    m7.metric("수익률", signed_pct(roi))

                    m8,m9,m10 = st.columns(3)
                    m8.metric("100¢ 상환 총액", money(l_shares))
                    m9.metric("실패 시 손실", f"-{money(cur_val)}")
                    m10.metric("포트폴리오 비중", f"{pos_pct:.1f}%")

                    st.markdown(
                        bar("포트폴리오 비중", min(pos_pct, 100), 100,
                            "#ff3b30" if pos_pct >= 20 else "#ff9500" if pos_pct >= 10 else "#34c759") +
                        bar("현재가 위치", (disp_p or 0)*100, 100, "#007aff"),
                        unsafe_allow_html=True
                    )

                    rows, min_r = partial_rows(l_shares, sell_p, l_invest)
                    if rows:
                        st.markdown("##### best bid 기준 부분매도 표")
                        if min_r:
                            if min_r <= 100:
                                st.success(f"원금 회수 최소 매도 비율: {min_r:.1f}%")
                            else:
                                st.warning("현재 가격에서는 100% 팔아도 원금 회수 어렵습니다.")
                        st.dataframe(rows, use_container_width=True)

                    if st.button("이 포지션 저장"):
                        st.session_state.tracked_positions.append({
                            "날짜": str(date.today()),
                            "거래": l_name, "결과": l_outcome,
                            "매수가": f"{l_buy:.1f}¢", "수량": l_shares,
                            "투자금": l_invest, "판정": decision,
                            "best bid": cents_dec(bb),
                        })
                        st.success("저장했습니다.")

            except Exception as e:
                st.error("가격 조회 실패 — token_id가 정확한지 확인해 주세요.")
                st.code(str(e))

    if st.session_state.tracked_positions:
        st.divider()
        st.markdown("##### 저장된 포지션")
        st.dataframe(st.session_state.tracked_positions, use_container_width=True)
        if st.button("포지션 목록 초기화"):
            st.session_state.tracked_positions = []
            st.rerun()


# ════════════════════════════════════════════════
# TAB 3 — 손익 계산
# ════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">거래 손익 계산</div>', unsafe_allow_html=True)

    p_name  = st.text_input("거래 이름", "Anyone's Legend vs Bilibili Gaming")
    c1, c2, c3 = st.columns(3)
    with c1: p_buy    = st.number_input("매수가 (¢)", 1.0, 99.0, 54.0, key="p_buy")
    with c2: p_sell   = st.number_input("매도가 (¢)", 0.0, 100.0, 87.0, key="p_sell")
    with c3: p_invest = st.number_input("투자금 ($)", 1.0, value=77.19, key="p_invest")

    if st.button("손익 계산하기", use_container_width=True):
        shares = p_invest / (p_buy / 100)
        sell_a = shares * (p_sell / 100)
        profit = sell_a - p_invest
        roi    = profit / p_invest * 100

        level = "good" if profit >= 0 else "bad"
        klass, icon, _ = result_cls(level)
        st.markdown(f"""
        <div class="result-card {klass}">
            <div class="result-title">{icon} {signed_money(profit)} ({signed_pct(roi)})</div>
            <div class="result-sub">{p_name}</div>
        </div>
        """, unsafe_allow_html=True)

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("보유 수량", f"{shares:.2f}주")
        m2.metric("매도금", money(sell_a))
        m3.metric("실현 손익", signed_money(profit))
        m4.metric("수익률", signed_pct(roi))

        st.session_state.trade_log.append({
            "날짜": str(date.today()),
            "거래": p_name,
            "매수가": f"{p_buy:.1f}¢",
            "매도가": f"{p_sell:.1f}¢",
            "투자금": p_invest,
            "손익": round(profit, 2),
            "수익률": f"{roi:.1f}%",
        })

    with st.expander("📝 거래 복기 질문"):
        for q in [
            "원하는 가격에 진입했는가?",
            "내 예상 승률의 근거는 무엇인가?",
            "북메이커와 왜 다르게 봤는가?",
            "금액은 감당 가능한 크기였는가?",
            "매도 기준을 지켰는가?",
            "감정적으로 들어간 부분이 있었는가?",
            "다음에 반복 가능한 거래인가?",
        ]:
            st.write(f"— {q}")


# ════════════════════════════════════════════════
# TAB 4 — 부분매도
# ════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">부분매도 계산기</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: s_buy    = st.number_input("매수가 (¢)", 1.0, 99.0, 52.4, key="s_buy")
    with c2: s_cur    = st.number_input("현재가 / 매도 기준가 (¢)", 1.0, 100.0, 58.0, key="s_cur")
    with c3: s_invest = st.number_input("투자금 ($)", 0.0, value=610.0, key="s_invest")

    manual = st.checkbox("보유 수량 직접 입력", value=True)
    if manual:
        s_shares = st.number_input("보유 수량", 0.0, value=1164.12, key="s_shares")
    else:
        s_shares = s_invest / (s_buy / 100)

    if st.button("부분매도 표 계산", use_container_width=True):
        rows, min_r = partial_rows(s_shares, s_cur / 100, s_invest)
        if min_r:
            if min_r <= 100:
                st.success(f"원금 회수 최소 매도 비율: {min_r:.1f}%")
            else:
                st.warning("현재 가격에서는 100% 팔아도 원금 회수 어렵습니다.")
        st.dataframe(rows, use_container_width=True)
        cur_v = s_shares * (s_cur / 100)
        st.info(f"현재 평가금 {money(cur_v)} · 100¢ 상환 총액 {money(s_shares)} · 실패 시 손실 -{money(cur_v)}")


# ════════════════════════════════════════════════
# TAB 5 — 거래 기록
# ════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">거래 기록 / 총수익률</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: r_start   = st.number_input("시작 자금 ($)", 0.0, value=500.0)
    with c2: r_current = st.number_input("현재 총자산 ($)", 0.0, value=650.0)
    with c3: r_deposit = st.number_input("추가 입금/출금 조정 ($)", value=0.0)

    adj = r_start + r_deposit
    total_p = r_current - adj
    total_r = total_p / adj * 100 if adj else 0

    level = "good" if total_p >= 0 else "bad"
    klass, icon, _ = result_cls(level)
    st.markdown(f"""
    <div class="result-card {klass}">
        <div class="result-title">{icon} 총손익 {signed_money(total_p)} ({signed_pct(total_r)})</div>
        <div class="result-sub">현재 총자산 {money(r_current)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.session_state.trade_log:
        st.dataframe(st.session_state.trade_log, use_container_width=True)
        if st.button("거래 기록 초기화"):
            st.session_state.trade_log = []
            st.rerun()
    else:
        st.markdown('<div class="muted">아직 기록된 거래가 없습니다. 손익 계산 탭에서 계산하면 여기에 쌓입니다.</div>', unsafe_allow_html=True)