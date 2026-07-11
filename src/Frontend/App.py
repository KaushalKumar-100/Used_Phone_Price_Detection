import sys
from pathlib import Path

import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.Backend.config.path import PROJECT_ROOT  # noqa: E402  (kept for backend path resolution)
from src.Frontend.config.setting import Settings  # noqa: E402

sys.path.append(str(PROJECT_ROOT))

setting = Settings()
API_URL = setting.api_url

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Used Phone Price Predictor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Global styling — dark navy glassmorphic theme
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 10%, rgba(45, 212, 191, 0.10), transparent 40%),
                radial-gradient(circle at 85% 0%, rgba(99, 102, 241, 0.14), transparent 45%),
                linear-gradient(180deg, #060B18 0%, #0A0F1F 100%);
        }

        /* Hide default chrome */
        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* Hero header */
        .app-hero {
            text-align: center;
            margin-bottom: 2rem;
        }
        .app-hero h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2.4rem;
            background: linear-gradient(90deg, #2DD4BF, #818CF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        .app-hero p {
            color: #94A3B8;
            font-size: 1rem;
            font-weight: 400;
        }

        /* Section labels above each glass column */
        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.05rem;
            color: #E2E8F0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.9rem;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        }

        /* Glassmorphic panel around each column's contents */
        div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 18px;
            padding: 1.4rem 1.3rem 1.6rem 1.3rem;
            backdrop-filter: blur(14px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
        }

        /* Inputs */
        .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input,
        .stTextInput input {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 10px !important;
            color: #E2E8F0 !important;
        }

        label, .stSlider label, .stNumberInput label, .stSelectbox label, .stTextInput label {
            color: #CBD5E1 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }

        /* Slider accent */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #2DD4BF !important;
            box-shadow: 0 0 0 4px rgba(45, 212, 191, 0.2) !important;
        }
        .stSlider [data-baseweb="slider"] > div > div {
            background: linear-gradient(90deg, #2DD4BF, #818CF8) !important;
        }

        /* Predict button */
        div.stButton {
            display: flex;
            justify-content: center;
            margin-top: 1.8rem;
        }
        div.stButton > button {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.05rem;
            color: #060B18;
            background: linear-gradient(90deg, #2DD4BF, #818CF8);
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2.8rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 6px 20px rgba(45, 212, 191, 0.25);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 26px rgba(129, 140, 248, 0.35);
            color: #060B18;
        }

        /* Result card */
        .result-card {
            margin-top: 2rem;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(45, 212, 191, 0.35);
            box-shadow: 0 10px 40px rgba(45, 212, 191, 0.12);
            backdrop-filter: blur(16px);
        }
        .result-card .label {
            color: #94A3B8;
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .result-card .value {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 3rem;
            background: linear-gradient(90deg, #2DD4BF, #818CF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .result-card .sub {
            color: #64748B;
            font-size: 0.9rem;
            margin-top: 0.6rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-hero">
        <h1>📱 Used Phone Price Predictor</h1>
        <p>Estimate the resale value of a used smartphone from its specs and condition</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Input form
# ----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown('<div class="section-title">🔧 Device Specs</div>', unsafe_allow_html=True)

    brand = st.selectbox(
        "Phone Brand",
        ["Apple", "Samsung", "Xiaomi", "Realme", "OnePlus", "Vivo", "Oppo", "Motorola", "Google", "Nothing"],
    )
    model = st.text_input("Phone Model", placeholder="e.g. iPhone 13, Galaxy S22")
    release_year = st.number_input("Release Year", min_value=2015, max_value=2026, value=2022)
    ram_gb = st.selectbox("RAM (GB)", [2, 4, 6, 8, 12, 16], index=3)
    storage_gb = st.selectbox("Storage (GB)", [32, 64, 128, 256, 512, 1024], index=2)
    screen_size_inches = st.number_input("Screen Size (Inches)", min_value=4.0, max_value=8.0, value=6.5, step=0.1)
    battery_capacity = st.number_input("Battery Capacity (mAh)", min_value=1000, max_value=7000, value=5000)
    processor_score = st.slider("Processor Score", 0, 100, 80)

with col2:
    st.markdown('<div class="section-title">🛒 Purchase Details</div>', unsafe_allow_html=True)

    camera_score = st.slider("Camera Score", 0, 100, 80)
    os_type = st.selectbox("Operating System", ["Android", "iOS"])
    has_5g = st.selectbox("5G Support", [0, 1], format_func=lambda x: "Yes" if x else "No")
    original_price = st.number_input("Original Price (₹)", min_value=5000, max_value=300000, value=30000, step=500)
    purchase_year = st.number_input("Purchase Year", min_value=2015, max_value=2030, value=2024)
    age_months = st.number_input("Age (Months)", min_value=0, max_value=120, value=12)
    usage_hours_per_day = st.slider("Usage Hours Per Day", 0.0, 24.0, 5.0, step=0.5)
    condition = st.selectbox("Phone Condition", ["Excellent", "Good", "Fair", "Poor"])

with col3:
    st.markdown('<div class="section-title">🩺 Condition Details</div>', unsafe_allow_html=True)

    battery_health = st.slider("Battery Health (%)", 0, 100, 90)
    screen_cracked = st.selectbox("Screen Cracked", [0, 1], format_func=lambda x: "Yes" if x else "No")
    body_damage = st.selectbox("Body Damage", [0, 1], format_func=lambda x: "Yes" if x else "No")
    repair_history = st.selectbox("Repair History", [0, 1], format_func=lambda x: "Yes" if x else "No")
    water_damage = st.selectbox("Water Damage", [0, 1], format_func=lambda x: "Yes" if x else "No")
    warranty_remaining_months = st.number_input("Warranty Remaining (Months)", min_value=0, max_value=36, value=6)
    box_available = st.selectbox("Original Box Available", [0, 1], format_func=lambda x: "Yes" if x else "No")
    charger_available = st.selectbox("Original Charger Available", [0, 1], format_func=lambda x: "Yes" if x else "No")
    market_demand_score = st.slider("Market Demand Score", 0, 100, 75)

# ----------------------------------------------------------------------------
# Predict
# ----------------------------------------------------------------------------
button = st.button("✨ Predict Price")

if button:
    if not model.strip():
        st.warning("Please enter the phone model before predicting.")
        st.stop()

    input_features = {
        "brand": brand,
        "model": model,
        "release_year": release_year,
        "ram_gb": ram_gb,
        "storage_gb": storage_gb,
        "screen_size_inches": screen_size_inches,
        "battery_capacity": battery_capacity,
        "processor_score": processor_score,
        "camera_score": camera_score,
        "os_type": os_type,
        "has_5g": has_5g,
        "original_price": original_price,
        "purchase_year": purchase_year,
        "age_months": age_months,
        "usage_hours_per_day": usage_hours_per_day,
        "condition": condition,
        "battery_health": battery_health,
        "screen_cracked": screen_cracked,
        "body_damage": body_damage,
        "repair_history": repair_history,
        "water_damage": water_damage,
        "warranty_remaining_months": warranty_remaining_months,
        "box_available": box_available,
        "charger_available": charger_available,
        "market_demand_score": market_demand_score,
    }

    try:
        with st.spinner("Estimating resale value..."):
            response = requests.post(
                                    API_URL,
                                    json=input_features,
                                    timeout=15
                                )
            response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Couldn't reach the prediction service: {e}")
        st.stop()

    try:
        result = response.json()
        prediction = float(result["prediction"])
    except (ValueError, KeyError, TypeError) as e:
        st.error(f"Unexpected response from the prediction service: {e}")
        st.stop()

    depreciation_pct = max(0.0, (1 - prediction / original_price) * 100) if original_price else 0.0

    st.markdown(
        f"""
        <div class="result-card">
            <div class="label">Estimated Resale Price</div>
            <div class="value">₹{prediction:,.0f}</div>
            <div class="sub">≈ {depreciation_pct:.1f}% depreciation from the original price of ₹{original_price:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )