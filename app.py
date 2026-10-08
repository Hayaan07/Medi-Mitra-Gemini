import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Interactive Healthcare Assistant",
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
    .body-box {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 30
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "Select"
if "symptoms_text" not in st.session_state:
    st.session_state.symptoms_text = ""
if "selected_parts" not in st.session_state:
    st.session_state.selected_parts = set()
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
st.markdown('<div class="main-header">🩺 Healthcare Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Follow the steps below to record your details, pinpoint discomfort areas, and generate a medical assessment report.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Medical Disclaimer:</strong> This application is an informational tool only and does NOT provide professional medical advice, diagnosis, or treatment. 
    If you are experiencing severe symptoms, chest pain, difficulty breathing, or a medical emergency, seek immediate emergency care.
</div>
""", unsafe_allow_html=True)

# Step Progress Bar
progress_labels = ["1️⃣ Basic Info", "2️⃣ Symptom & Body Map", "3️⃣ Hospitals & Report"]
st.progress(st.session_state.current_step / 3)
st.caption(f"**Current Step:** Step {st.session_state.current_step} of 3 — {progress_labels[st.session_state.current_step - 1]}")
st.markdown("---")

# =============================================================================
# PAGE 1: BASIC DETAILS
# =============================================================================
if st.session_state.current_step == 1:
    st.markdown("### 👤 Page 1: Personal Details")
    st.write("Please complete all required fields to proceed to the next step.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_name = st.text_input(
            "Full Name *", 
            value=st.session_state.user_name, 
            placeholder="e.g., Alex Johnson"
        )
        st.session_state.user_age = st.number_input(
            "Age *", 
            min_value=1, 
            max_value=120, 
            value=st.session_state.user_age
        )
    
    with col2:
        gender_options = ["Select", "Male", "Female", "Non-Binary", "Prefer not to say"]
        gender_idx = gender_options.index(st.session_state.user_gender) if st.session_state.user_gender in gender_options else 0
        st.session_state.user_gender = st.selectbox(
            "Gender *", 
            options=gender_options, 
            index=gender_idx
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Validation Check
    p1_valid = bool(st.session_state.user_name.strip()) and st.session_state.user_gender != "Select"
    
    if not p1_valid:
        st.warning("⚠️ Please fill in your Name and select a Gender to unlock the Next page.")
    
    if st.button("Next ➡️ (Go to Page 2)", type="primary", disabled=not p1_valid):
        st.session_state.current_step = 2
        st.rerun()

# =============================================================================
# PAGE 2: SYMPTOM CHECKER & INTERACTIVE BODY MAP
# =============================================================================
elif st.session_state.current_step == 2:
    st.markdown("### 🩺 Page 2: Symptom Checker & Interactive Body Map")
    st.write("Click on any body part button to mark pain areas, or describe your symptoms below.")

    col_text, col_map = st.columns([1, 1.2], gap="large")

    with col_text:
        st.markdown("#### Describe Your Symptoms")
        st.session_state.symptoms_text = st.text_area(
            "State how you are feeling:",
            value=st.session_state.symptoms_text,
            placeholder="e.g., Sharp headache, discomfort in chest, fatigue...",
            height=180
        )

    with col_map:
        st.markdown("#### Interactive Full Body Map")
        st.caption("Click any body region button below to toggle selection (Selected areas turn RED):")

        # Full Body Illustration + Interactive Buttons
        st.markdown("""
        <div style="text-align: center; margin-bottom: 10px;">
            <svg width="180" height="260" viewBox="0 0 200 450" style="background: #F1F5F9; border-radius: 8px; border: 1px solid #CBD5E1;">
                <circle cx="100" cy="40" r="28" fill="#94A3B8"/> <!-- Head -->
                <rect x="94" y="68" width="12" height="15" fill="#94A3B8"/> <!-- Neck -->
                <path d="M 60,83 L 140,83 L 155,190 L 140,200 L 135,130 L 135,230 L 65,230 L 65,130 L 45,200 L 45,190 Z" fill="#64748B"/> <!-- Torso/Arms -->
                <rect x="70" y="230" width="25" height="180" rx="10" fill="#475569"/> <!-- Leg L -->
                <rect x="105" y="230" width="25" height="180" rx="10" fill="#475569"/> <!-- Leg R -->
            </svg>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Streamlit Buttons for each Body Part
        grid = st.columns(2)
        for idx, part in enumerate(KNOWLEDGE_BASE.keys()):
            col_target = grid[idx % 2]
            is_selected = part in st.session_state.selected_parts
            btn_label = f"🔴 {part}" if is_selected else f"⚪ {part}"
            
            if col_target.button(btn_label, key=f"btn_{part}", use_container_width=True):
                if is_selected:
                    st.session_state.selected_parts.remove(part)
                else:
                    st.session_state.selected_parts.add(part)
                st.rerun()

        if st.session_state.selected_parts:
            st.success(f"**Selected Areas:** {', '.join(st.session_state.selected_parts)}")
        else:
            st.info("No body region selected yet. Click the buttons above.")

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Validation Check
    p2_valid = len(st.session_state.selected_parts) > 0 or bool(st.session_state.symptoms_text.strip())
    
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("⬅️ Back (Page 1)"):
            st.session_state.current_step = 1
            st.rerun()
            
    with col_nav2:
        if not p2_valid:
            st.warning("⚠️ Select at least one body part OR enter symptom details to proceed.")
        if st.button("Next ➡️ (Go to Page 3)", type="primary", disabled=not p2_valid):
            st.session_state.current_step = 3
            st.rerun()

# =============================================================================
# PAGE 3: HOSPITALS & GENERATE REPORT
# =============================================================================
elif st.session_state.current_step == 3:
    st.markdown("### 🏥 Page 3: Location, Hospitals & Report Generation")

    # Emergency & Location Section
    st.markdown("#### 🚨 Urgent Care & Hospital Lookup")
    st.session_state.is_emergency = st.checkbox(
        "Check here if you consider this an EMERGENCY",
        value=st.session_state.is_emergency
    )
    
    st.session_state.user_location = st.text_input(
        "Enter your City / Town / Area:",
        value=st.session_state.user_location,
        placeholder="e.g., New York, London, Delhi..."
    )

    if st.session_state.user_location:
        matched_city = next(
            (city for city in HOSPITAL_DATABASE if city.lower() in st.session_state.user_location.lower()), 
            None
        )
        st.markdown(f"##### Nearby Hospitals around '{st.session_state.user_location}':")
        
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
                <strong style="color: #1E3A8A; font-size: 1.05rem;">🏥 General Emergency & Community Hospital</strong><br/>
                <span style="color: #4B5563;">📍 Address: Medical Hub, {st.session_state.user_location}</span><br/>
                <span style="color: #059669; font-weight: 600;">📞 Emergency Services: 911 / 112 / 102</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("⬅️ Back (Page 2)"):
            st.session_state.current_step = 2
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Generate Assessment Report
    if st.button("📋 Generate My Assessment Report", type="primary", use_container_width=True):
        st.markdown("## 📄 Comprehensive Health Summary Report")
        
        st.markdown(f"""
        **Patient Name:** {st.session_state.user_name} | **Age:** {st.session_state.user_age} | **Gender:** {st.session_state.user_gender}  
        **Location:** {st.session_state.user_location if st.session_state.user_location else "Not specified"}  
        **Reported Symptoms:** {st.session_state.symptoms_text if st.session_state.symptoms_text else "None described"}  
        **Selected Pain Areas:** {', '.join(st.session_state.selected_parts) if st.session_state.selected_parts else "Unspecified"}
        """)
        st.markdown("---")

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
            st.markdown("### 🧪 Recommended Tests")
            for item in list(dict.fromkeys(tests)):
                st.markdown(f"- {item}")
        with c3:
            st.markdown("### 💡 Wellness & Treatment Tips")
            for item in list(dict.fromkeys(tips)):
                st.markdown(f"- {item}")

        st.success("✅ Assessment report generated! You can present this summary to a medical practitioner.")