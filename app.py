import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="Healthcare Assistant App",
    page_icon="🩺",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .disclaimer-box {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 20px;
        color: #991B1B;
        font-size: 0.9rem;
    }
    .hospital-card {
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 30
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "Select"
if "symptoms_text" not in st.session_state:
    st.session_state.symptoms_text = ""
if "selected_parts" not in st.session_state:
    st.session_state.selected_parts = []
if "is_emergency" not in st.session_state:
    st.session_state.is_emergency = False
if "user_location" not in st.session_state:
    st.session_state.user_location = ""

# -----------------------------------------------------------------------------
# MEDICAL KNOWLEDGE BASE
# -----------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "Head / Scalp": {
        "causes": [
            "Tension Headache (Stress/Fatigue)",
            "Migraine Episode",
            "Dehydration or Caffeine Withdrawal",
            "Sinusitis / Upper Respiratory Infection"
        ],
        "tests": [
            "Comprehensive Eye Examination",
            "Neurological Evaluation",
            "CT/MRI Scan of the Brain (if symptoms persist)",
            "Basic Metabolic Panel (Blood Test)"
        ],
        "wellness_tips": [
            "Maintain proper hydration (at least 2-3L water daily).",
            "Rest in a quiet, dark room.",
            "Apply a cold or warm compress to forehead or neck.",
            "Ensure 7-8 hours of sound sleep."
        ]
    },
    "Eyes / Ears / Nose": {
        "causes": [
            "Allergic Rhinitis or Conjunctivitis",
            "Sinusitis",
            "Otitis Media (Ear Infection)",
            "Digital Eye Strain"
        ],
        "tests": [
            "Ophthalmic Exam / Acuity Test",
            "Otoscopy (Ear exam)",
            "Nasal Endoscopy or Allergy Skin Test"
        ],
        "wellness_tips": [
            "Use steam inhalation for nasal congestion.",
            "Follow 20-20-20 rule for screen time.",
            "Avoid touching eyes/ears with unwashed hands."
        ]
    },
    "Chest / Heart": {
        "causes": [
            "Acid Reflux (GERD)",
            "Musculoskeletal Chest Strain",
            "Asthma / Bronchitis",
            "Cardiovascular Disease (Requires urgent evaluation)"
        ],
        "tests": [
            "Electrocardiogram (ECG / EKG)",
            "Chest X-Ray",
            "Troponin and Cardiac Enzyme Panel",
            "Pulmonary Function Test (PFT)"
        ],
        "wellness_tips": [
            "Avoid heavy meals right before lying down.",
            "Practice deep breathing and relaxation techniques.",
            "Refrain from smoking or exposure to second-hand smoke."
        ]
    },
    "Abdomen / Stomach": {
        "causes": [
            "Gastritis or Peptic Ulcer",
            "Irritable Bowel Syndrome (IBS)",
            "Gastroenteritis (Food Poisoning)",
            "Gallbladder / Appendicitis issues (if severe)"
        ],
        "tests": [
            "Abdominal Ultrasound",
            "Complete Blood Count (CBC) and LFT",
            "Stool Culture",
            "Endoscopy (if chronic)"
        ],
        "wellness_tips": [
            "Eat smaller, more frequent meals.",
            "Stay hydrated with clear fluids or electrolyte solutions.",
            "Avoid overly spicy, oily, or highly acidic foods."
        ]
    },
    "Arms / Hands": {
        "causes": [
            "Repetitive Strain Injury (e.g., Carpal Tunnel Syndrome)",
            "Arthritis or Tendonitis",
            "Peripheral Neuropathy",
            "Muscle Strain"
        ],
        "tests": [
            "Nerve Conduction Study (NCS) / EMG",
            "X-Ray of Affected Joints",
            "Inflammatory Markers (CRP, ESR, Rheumatoid Factor)"
        ],
        "wellness_tips": [
            "Take regular ergonomic breaks during manual work.",
            "Apply ice for acute swelling or heat for stiffness.",
            "Gentle stretching exercises."
        ]
    },
    "Legs / Feet": {
        "causes": [
            "Muscular Strain or Overexertion",
            "Venous Insufficiency or Poor Circulation",
            "Osteoarthritis or Sprain",
            "Electrolyte Imbalance"
        ],
        "tests": [
            "Venous Doppler Ultrasound",
            "X-Ray or MRI of Joints",
            "Electrolyte Panel (Potassium, Magnesium, Calcium)"
        ],
        "wellness_tips": [
            "Elevate legs above heart level when resting.",
            "Wear supportive footwear.",
            "Engage in low-impact movement like walking or swimming."
        ]
    },
    "Back / Spine": {
        "causes": [
            "Poor Posture / Lumbar Strain",
            "Herniated / Bulging Disc",
            "Sciatica",
            "Muscular Spasm"
        ],
        "tests": [
            "Lumbar Spine MRI / CT Scan",
            "X-Ray of the Spine",
            "Physical Therapy Biomechanical Assessment"
        ],
        "wellness_tips": [
            "Maintain ergonomic posture while sitting and standing.",
            "Core strengthening and hamstring stretching exercises.",
            "Avoid heavy lifting without bending knees."
        ]
    }
}

HOSPITAL_DATABASE = {
    "New York": [
        {"name": "NewYork-Presbyterian Hospital", "address": "525 E 68th St", "phone": "(212) 746-5454", "type": "Level 1 Trauma Center"},
        {"name": "Mount Sinai Hospital", "address": "1468 Madison Ave", "phone": "(212) 241-6500", "type": "General Emergency"}
    ],
    "London": [
        {"name": "St Thomas' Hospital", "address": "Westminster Bridge Rd", "phone": "+44 20 7188 7188", "type": "A&E Department"},
        {"name": "University College Hospital", "address": "235 Euston Rd", "phone": "+44 20 3456 7890", "type": "Emergency Care"}
    ],
    "Delhi": [
        {"name": "AIIMS New Delhi", "address": "Sri Aurobindo Marg, Ansari Nagar", "phone": "+91 11 2658 8500", "type": "Super Speciality / Emergency"},
        {"name": "Max Super Speciality Hospital", "address": "Saket, Press Enclave Road", "phone": "+91 11 2651 5050", "type": "24/7 Emergency"}
    ]
}

# -----------------------------------------------------------------------------
# HEADER & DISCLAIMER
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🩺 Interactive Healthcare Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Complete the 3-step process to receive personalized health insights and emergency hospital options.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Medical Disclaimer:</strong> This application is an informational tool only and does NOT provide professional medical advice, diagnosis, or treatment. 
    If you are experiencing severe symptoms, chest pain, difficulty breathing, or a medical emergency, seek immediate emergency care.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE NAVIGATION (3 PAGES / TABS)
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "👤 Page 1: Basic Info", 
    "🩺 Page 2: Symptom Checker & Body Map", 
    "🏥 Page 3: Hospitals & Generate Report"
])

# =============================================================================
# PAGE 1: BASIC INFORMATION
# =============================================================================
with tab1:
    st.markdown("### Step 1: Personal Details")
    st.write("Please provide your basic information below to personalize your healthcare report.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_name = st.text_input(
            "Full Name", 
            value=st.session_state.user_name, 
            placeholder="e.g., Alex Johnson"
        )
        st.session_state.user_age = st.number_input(
            "Age", 
            min_value=1, 
            max_value=120, 
            value=st.session_state.user_age
        )
    
    with col2:
        gender_options = ["Select", "Male", "Female", "Non-Binary", "Prefer not to say"]
        gender_index = gender_options.index(st.session_state.user_gender) if st.session_state.user_gender in gender_options else 0
        st.session_state.user_gender = st.selectbox(
            "Gender", 
            options=gender_options, 
            index=gender_index
        )

    st.info("👉 Once filled, proceed to **Page 2: Symptom Checker & Body Map** tab above.")

# =============================================================================
# PAGE 2: SYMPTOM CHECKER & INTERACTIVE FULL BODY MAP
# =============================================================================
with tab2:
    st.markdown("### Step 2: Symptom Checker & Body Map")
    col_text, col_map = st.columns([1, 1.2], gap="large")

    with col_text:
        st.markdown("#### Describe Your Current Symptoms")
        st.session_state.symptoms_text = st.text_area(
            "State how you are feeling:",
            value=st.session_state.symptoms_text,
            placeholder="e.g., Sharp headache, discomfort in chest, fatigue...",
            height=150
        )

    with col_map:
        st.markdown("#### Interactive Full Body Map")
        st.caption("Click on the anatomical body diagram or select the body regions below:")

        body_map_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 0; }
                .container { position: relative; width: 240px; height: 440px; }
                svg { width: 100%; height: 100%; }
                .body-region {
                    fill: #64748B;
                    fill-opacity: 0.25;
                    stroke: #334155;
                    stroke-width: 2;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                .body-region:hover { fill: #3B82F6; fill-opacity: 0.5; }
                .body-region.selected { fill: #EF4444 !important; fill-opacity: 0.7 !important; stroke: #B91C1C !important; }
                .label { font-size: 11px; fill: #1E293B; font-weight: bold; pointer-events: none; }
                .selection-box { margin-top: 8px; font-size: 12px; color: #1E3A8A; font-weight: 600; text-align: center; }
            </style>
        </head>
        <body>
            <div class="container">
                <svg viewBox="0 0 200 450">
                    <g opacity="0.15" fill="#000">
                        <circle cx="100" cy="40" r="28"/>
                        <rect x="94" y="68" width="12" height="15"/>
                        <path d="M 60,83 L 140,83 L 155,190 L 140,200 L 135,130 L 135,230 L 65,230 L 65,130 L 45,200 L 45,190 Z"/>
                        <rect x="70" y="230" width="25" height="180" rx="10"/>
                        <rect x="105" y="230" width="25" height="180" rx="10"/>
                    </g>

                    <!-- Interactive Regions -->
                    <path id="Head / Scalp" class="body-region" d="M 75,40 A 25,25 0 1,1 125,40 A 25,25 0 1,1 75,40 Z" />
                    <text x="100" y="32" class="label" text-anchor="middle">Head</text>

                    <rect id="Eyes / Ears / Nose" class="body-region" x="80" y="42" width="40" height="22" rx="4" />
                    <text x="100" y="56" class="label" text-anchor="middle">Face</text>

                    <path id="Chest / Heart" class="body-region" d="M 65,85 L 135,85 L 130,145 L 70,145 Z" />
                    <text x="100" y="118" class="label" text-anchor="middle">Chest</text>

                    <path id="Abdomen / Stomach" class="body-region" d="M 70,148 L 130,148 L 125,215 L 75,215 Z" />
                    <text x="100" y="185" class="label" text-anchor="middle">Abdomen</text>

                    <g id="Arms / Hands" class="body-region">
                        <path d="M 45,88 L 62,88 L 55,200 L 38,200 Z" />
                        <path d="M 138,88 L 155,88 L 162,200 L 145,200 Z" />
                    </g>

                    <g id="Legs / Feet" class="body-region">
                        <rect x="68" y="220" width="28" height="200" rx="8" />
                        <rect x="104" y="220" width="28" height="200" rx="8" />
                    </g>
                    <text x="100" y="320" class="label" text-anchor="middle">Legs</text>
                </svg>
            </div>
            <div class="selection-box">Click regions to mark pain/uneasiness</div>
        </body>
        </html>
        """
        components.html(body_map_html, height=480)

        st.session_state.selected_parts = st.multiselect(
            "Selected Pain / Discomfort Areas:",
            options=list(KNOWLEDGE_BASE.keys()),
            default=st.session_state.selected_parts
        )

    st.info("👉 Proceed to **Page 3: Hospitals & Generate Report** tab above.")

# =============================================================================
# PAGE 3: HOSPITALS & REPORT GENERATION
# =============================================================================
with tab3:
    st.markdown("### Step 3: Nearby Area Hospitals & Report Generation")
    
    # Emergency & Location Selection Section
    st.markdown("#### 🚨 Emergency Check & Location Selection")
    st.session_state.is_emergency = st.checkbox(
        "Is this an urgent / emergency situation?",
        value=st.session_state.is_emergency
    )
    
    st.session_state.user_location = st.text_input(
        "Enter your City / Town / Nearby Area:",
        value=st.session_state.user_location,
        placeholder="e.g., New York, London, Delhi, or your town name"
    )

    if st.session_state.user_location:
        matched_city = next(
            (city for city in HOSPITAL_DATABASE if city.lower() in st.session_state.user_location.lower()), 
            None
        )
        st.markdown(f"##### Nearby Hospitals in/around '{st.session_state.user_location}':")
        
        if matched_city:
            for hosp in HOSPITAL_DATABASE[matched_city]:
                st.markdown(f"""
                <div class="hospital-card">
                    <strong style="color: #1E3A8A; font-size: 1.05rem;">🏥 {hosp['name']}</strong><br/>
                    <span style="color: #4B5563;">📍 Address: {hosp['address']}</span><br/>
                    <span style="color: #059669; font-weight: 600;">📞 Phone: {hosp['phone']}</span> | <em>{hosp['type']}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="hospital-card">
                <strong style="color: #1E3A8A; font-size: 1.05rem;">🏥 Community General Emergency Hospital</strong><br/>
                <span style="color: #4B5563;">📍 Address: Central Medical Zone, {st.session_state.user_location}</span><br/>
                <span style="color: #059669; font-weight: 600;">📞 Emergency Hotline: 911 / 112 / 102</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Generate Report Button
    if st.button("📋 Generate My Healthcare Report", type="primary", use_container_width=True):
        if not st.session_state.user_name:
            st.warning("⚠️ Please fill in your name on **Page 1** first.")
        elif not st.session_state.selected_parts and not st.session_state.symptoms_text:
            st.warning("⚠️ Please select affected body areas or describe symptoms on **Page 2** first.")
        else:
            st.markdown("## 📄 Comprehensive Patient Summary Report")
            
            st.markdown(f"""
            **Patient Profile:** {st.session_state.user_name} | **Age:** {st.session_state.user_age} | **Gender:** {st.session_state.user_gender}  
            **Current Location:** {st.session_state.user_location if st.session_state.user_location else "Not provided"}  
            **Reported Symptoms:** {st.session_state.symptoms_text if st.session_state.symptoms_text else "None described"}  
            **Affected Body Areas:** {', '.join(st.session_state.selected_parts) if st.session_state.selected_parts else "General / Unspecified"}
            """)
            st.markdown("---")

            # Collect summary insights
            causes, tests, tips = [], [], []
            parts = st.session_state.selected_parts if st.session_state.selected_parts else list(KNOWLEDGE_BASE.keys())[:2]

            for part in parts:
                if part in KNOWLEDGE_BASE:
                    causes.extend(KNOWLEDGE_BASE[part]["causes"])
                    tests.extend(KNOWLEDGE_BASE[part]["tests"])
                    tips.extend(KNOWLEDGE_BASE[part]["wellness_tips"])

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("### 🔍 Potential Causes")
                for item in list(dict.fromkeys(causes)):
                    st.markdown(f"- {item}")
            with c2:
                st.markdown("### 🧪 Potential Diagnostic Tests")
                for item in list(dict.fromkeys(tests)):
                    st.markdown(f"- {item}")
            with c3:
                st.markdown("### 💡 Wellness & Treatment Tips")
                for item in list(dict.fromkeys(tips)):
                    st.markdown(f"- {item}")

            st.success("✅ Report successfully generated! Show this summary to your consulting medical doctor.")