import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Analyzer",
    page_icon="💳",
    layout="centered"
)

# ── Master CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ── Tokens ── */
:root {
    --bg-deep:      #071510;
    --bg-mid:       #0c1e17;
    --glass-bg:     rgba(18, 42, 30, 0.72);
    --glass-border: rgba(180, 210, 170, 0.13);
    --glass-inner:  rgba(255,255,255,0.035);
    --card-dark:    rgba(10, 28, 20, 0.85);

    --gold:         #c9a96e;
    --gold-light:   #e2c891;
    --gold-dim:     rgba(201,169,110,0.18);
    --gold-glow:    rgba(201,169,110,0.28);

    --green-neon:   #3ecf8e;
    --green-mid:    #2a8c5f;
    --green-dim:    rgba(62,207,142,0.14);
    --green-glow:   rgba(62,207,142,0.3);

    --red-soft:     #e06b6b;
    --red-dim:      rgba(224,107,107,0.14);
    --red-glow:     rgba(224,107,107,0.3);

    --text-bright:  #eeeae0;
    --text-mid:     #a0b8a8;
    --text-dim:     #587a68;

    --radius-xl:    28px;
    --radius-lg:    18px;
    --radius-md:    12px;
    --radius-pill:  999px;
    --blur:         blur(22px);
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-deep) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-bright) !important;
    min-height: 100vh;
}

/* Ambient background blobs */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 55% at 15% 20%,  rgba(34, 90, 58, 0.38) 0%, transparent 70%),
        radial-gradient(ellipse 50% 45% at 85% 75%,  rgba(20, 70, 45, 0.32) 0%, transparent 70%),
        radial-gradient(ellipse 35% 30% at 50% 50%,  rgba(62,207,142,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* Dot-grid texture */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.028) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stSidebar"],
footer { display: none !important; }

section[data-testid="stMain"] > div {
    padding: 2.5rem 1rem 3rem !important;
    position: relative;
    z-index: 1;
}

/* Constrain & center everything */
[data-testid="stVerticalBlock"] {
    max-width: 680px !important;
    margin: 0 auto !important;
}

/* ── Glass Card wrapper ── */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: var(--blur);
    -webkit-backdrop-filter: var(--blur);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-xl);
    padding: 2.2rem 2rem;
    box-shadow:
        0 0 0 1px var(--glass-inner) inset,
        0 32px 80px rgba(0,0,0,0.55),
        0 8px 24px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,169,110,0.45), transparent);
}

/* ── Page Title ── */
.hero-title {
    text-align: center;
    margin-bottom: 0.25rem;
}
.hero-title .icon {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 12px var(--gold-glow));
}
.hero-title h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.05rem !important;
    font-weight: 700 !important;
    color: var(--text-bright) !important;
    letter-spacing: -0.01em;
    line-height: 1.15;
}
.hero-title h1 span {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 60%, #a07840 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    text-align: center;
    color: var(--text-dim) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin-bottom: 2rem !important;
    font-weight: 400 !important;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.67rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--gold) !important;
    margin-bottom: 0.8rem !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--glass-border), transparent);
}

/* ── Widget labels ── */
label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
    margin-bottom: 0.2rem !important;
}

/* ── Number input ── */
[data-testid="stNumberInput"] input {
    background: var(--card-dark) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-bright) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.25) !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim), inset 0 2px 6px rgba(0,0,0,0.25) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(201,169,110,0.1) !important;
    border: 1px solid var(--glass-border) !important;
    color: var(--gold) !important;
    border-radius: 8px !important;
    transition: background 0.15s, box-shadow 0.15s;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--gold-dim) !important;
    box-shadow: 0 0 8px var(--gold-dim) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--card-dark) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-bright) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.25) !important;
}
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}
[data-testid="stSelectbox"] svg { fill: var(--gold) !important; }
[data-baseweb="popover"] [data-baseweb="menu"] {
    background: #0e2018 !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: transparent !important;
    color: var(--text-mid) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    transition: background 0.12s, color 0.12s;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: var(--gold-dim) !important;
    color: var(--gold-light) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--gold) !important;
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 5px var(--gold-dim), 0 2px 10px rgba(0,0,0,0.5) !important;
    width: 18px !important;
    height: 18px !important;
    transition: box-shadow 0.2s;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover {
    box-shadow: 0 0 0 8px var(--gold-dim), 0 0 18px var(--gold-glow) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="Track"] {
    background: rgba(255,255,255,0.07) !important;
    height: 4px !important;
    border-radius: 99px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="Track"]:nth-child(1) {
    background: linear-gradient(90deg, var(--green-mid), var(--green-neon)) !important;
    box-shadow: 0 0 8px var(--green-glow);
}
[data-testid="stSlider"] p {
    color: var(--text-dim) !important;
    font-size: 0.72rem !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--glass-border) !important;
    margin: 1.6rem 0 !important;
}

/* ── Predict Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, rgba(201,169,110,0.12), rgba(201,169,110,0.06)) !important;
    color: var(--gold-light) !important;
    border: 1.5px solid rgba(201,169,110,0.5) !important;
    border-radius: var(--radius-pill) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    padding: 0.85rem 2.5rem !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
    cursor: pointer;
    transition: background 0.3s, border-color 0.3s, box-shadow 0.3s, transform 0.15s !important;
    text-transform: uppercase !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(201,169,110,0.22), rgba(201,169,110,0.1)) !important;
    border-color: var(--gold-light) !important;
    box-shadow: 0 0 28px var(--gold-glow), 0 8px 24px rgba(0,0,0,0.4) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 0 12px var(--gold-dim) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--card-dark) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35), inset 0 1px 0 var(--glass-inner);
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.5), 0 0 20px var(--gold-dim);
}
[data-testid="stMetricLabel"] p {
    font-size: 0.66rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    color: var(--gold-light) !important;
}

/* ── Result cards ── */
.result-good {
    background: linear-gradient(135deg, rgba(62,207,142,0.1), rgba(30,100,68,0.15));
    border: 1px solid rgba(62,207,142,0.35);
    border-left: 4px solid var(--green-neon);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: 0 0 32px var(--green-dim), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: fadeSlide 0.5s ease both;
}
.result-bad {
    background: linear-gradient(135deg, rgba(224,107,107,0.1), rgba(120,40,40,0.12));
    border: 1px solid rgba(224,107,107,0.35);
    border-left: 4px solid var(--red-soft);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: 0 0 32px var(--red-dim), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: fadeSlide 0.5s ease both;
}
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    letter-spacing: -0.01em;
}
.result-sub {
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.75;
}

/* ── Summary table ── */
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.85rem;
}
.summary-row:last-child { border-bottom: none; }
.summary-key {
    color: var(--text-dim);
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
}
.summary-val {
    color: var(--text-bright);
    font-weight: 600;
    font-size: 0.88rem;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] p {
    color: var(--text-dim) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Animations ── */
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGold {
    0%, 100% { box-shadow: 0 0 0 0 var(--gold-dim); }
    50%       { box-shadow: 0 0 0 8px transparent; }
}

/* ── Column gap ── */
[data-testid="stHorizontalBlock"] { gap: 0.85rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: rgba(201,169,110,0.2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── Plotly chart container ── */
[data-testid="stPlotlyChart"] {
    background: transparent !important;
}
[data-testid="stPlotlyChart"] > div {
    border-radius: var(--radius-xl) !important;
}

/* ── Stagger input rows ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    animation: fadeSlide 0.4s ease both;
}
</style>
""", unsafe_allow_html=True)

# ── Helper: confidence ring via Plotly ───────────────────────────────────────
def confidence_ring(confidence: float, label: str, is_good: bool):
    pct = confidence * 100
    fill_color  = "#3ecf8e" if is_good else "#e06b6b"
    track_color = "rgba(255,255,255,0.06)"
    bg          = "rgba(0,0,0,0)"

    fig = go.Figure(go.Pie(
        values=[pct, 100 - pct],
        hole=0.72,
        marker=dict(colors=[fill_color, track_color],
                    line=dict(width=0)),
        showlegend=False,
        textinfo="none",
        sort=False,
        direction="clockwise",
        rotation=90,
    ))

    glow = fill_color.replace(")", ", 0.35)").replace("rgb", "rgba") if fill_color.startswith("rgb") else fill_color

    fig.add_annotation(
        text=f"<b>{pct:.1f}%</b>",
        x=0.5, y=0.55,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(family="Playfair Display, serif", size=30,
                  color="#eeeae0"),
    )
    fig.add_annotation(
        text="Confidence",
        x=0.5, y=0.38,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(family="DM Sans, sans-serif", size=11,
                  color="rgba(160,184,168,0.85)"),
    )

    fig.update_layout(
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        margin=dict(t=0, b=0, l=0, r=0),
        height=220,
        width=220,
    )
    return fig


# ── Load model & encoders ─────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load("extra_trees_credit_model.pkl")
    encoders = {
        col: joblib.load(f"{col}_encoder.pkl")
        for col in ["Sex", "Housing", "Saving accounts", "Checking account"]
    }
    return model, encoders

try:
    model, encoders = load_model()
    model_loaded = True
except Exception:
    model_loaded = False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">
    <span class="icon"></span>
    <h1>Credit Risk <span>Analyzer</span></h1>
</div>
<p class="hero-subtitle">AI-Powered Financial Assessment</p>
""", unsafe_allow_html=True)


# ── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Applicant Profile</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=18, max_value=70, value=30, key="age")
    job = st.slider("Job Level", min_value=0, max_value=3, value=1,
                    help="0 = unskilled, 3 = highly skilled")
with col2:
    sex     = st.selectbox("Sex", ["male", "female"], key="sex")
    housing = st.selectbox("Housing", ["own", "rent", "free"], key="housing")

st.markdown('<p class="section-label" style="margin-top:1.2rem">Financial Details</p>',
            unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    saving_accounts   = st.selectbox("Saving Accounts",
                                     ["little", "moderate", "rich", "quite rich"],
                                     key="saving")
    credit_amount = st.number_input("Credit Amount (€)", min_value=0, value=1000,
                                    step=100, key="credit")
with col4:
    checking_accounts = st.selectbox("Checking Account",
                                     ["little", "moderate", "rich"],
                                     key="checking")
    duration = st.slider("Duration (Months)", min_value=1, max_value=72, value=12,
                         key="duration")

# ── Quick-glance metrics ──────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("💰 Amount",  f"€{credit_amount:,}")
with m2:
    st.metric("📅 Duration", f"{duration} mo")
with m3:
    monthly = round(credit_amount / duration, 2) if duration else 0
    st.metric("📊 Monthly",  f"€{monthly:,}")

# ── Predict ───────────────────────────────────────────────────────────────────
predict_btn = st.button("⬡  Analyze Credit Risk", key="predict")

if predict_btn:
    if not model_loaded:
        st.error("⚠️ Model files not found. Please ensure `extra_trees_credit_model.pkl` and encoder `.pkl` files are in the same directory.")
    else:
        with st.spinner("Running analysis…"):
            time.sleep(0.9)   # deliberate delay for premium feel

        input_df = pd.DataFrame({
            "Age":              [age],
            "Sex":              [encoders["Sex"].transform([sex])[0]],
            "Job":              [job],
            "Housing":          [encoders["Housing"].transform([housing])[0]],
            "Saving accounts":  [encoders["Saving accounts"].transform([saving_accounts])[0]],
            "Checking account": [encoders["Checking account"].transform([checking_accounts])[0]],
            "Credit amount":    [credit_amount],
            "Duration":         [duration]
        })

        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0]

        is_good    = (pred == 1)
        confidence = prob[1] if is_good else prob[0]
        label      = "GOOD" if is_good else "BAD"
        emoji      = "✅" if is_good else "❌"
        css_cls    = "result-good" if is_good else "result-bad"
        color      = "#3ecf8e" if is_good else "#e06b6b"

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Analysis Result</p>',
                    unsafe_allow_html=True)

        # Result card + ring side by side
        res_col, ring_col = st.columns([1.15, 1], gap="medium")

        with res_col:
            st.markdown(f"""
            <div class="{css_cls}">
                <div class="result-label" style="color:{color}">{emoji} {label}</div>
                <div class="result-sub">Credit Risk Assessment</div>
            </div>
            """, unsafe_allow_html=True)

            # Summary table
            st.markdown("<br>", unsafe_allow_html=True)
            fields = {
                "Age": age, "Sex": sex, "Job Level": job,
                "Housing": housing, "Saving Accounts": saving_accounts,
                "Checking Account": checking_accounts,
                "Credit Amount": f"€{credit_amount:,}", "Duration": f"{duration} mo"
            }
            rows_html = "".join(
                f'<div class="summary-row"><span class="summary-key">{k}</span>'
                f'<span class="summary-val">{v}</span></div>'
                for k, v in fields.items()
            )
            st.markdown(f'<div style="margin-top:0.5rem">{rows_html}</div>',
                        unsafe_allow_html=True)

        with ring_col:
            fig = confidence_ring(confidence, label, is_good)
            st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})

            # Advisory note
            note = (
                "Strong repayment likelihood. Low exposure for lender."
                if is_good else
                "Elevated default risk. Consider additional review."
            )
            st.markdown(f"""
            <p style="font-size:0.74rem;color:var(--text-dim);text-align:center;
                      line-height:1.55;margin-top:0.5rem;padding:0 0.5rem">
                {note}
            </p>
            """, unsafe_allow_html=True)