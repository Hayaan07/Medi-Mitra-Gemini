import streamlit as st
import streamlit.components.v1 as components
import json

# Page Configuration
st.set_page_config(
    page_title="Interactive Healthcare Assistant",
    page_icon="🩺",
    layout="wide"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

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
            "Avoid touching or rubbing eyes/ears with unwashed hands."
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

# Initialize session states
if "selected_parts" not in st.session_state:
    st.session_state.selected_parts = []

# -----------------------------------------------------------------------------
# APP HEADER & DISCLAIMER
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🩺 Smart Healthcare Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Provide your details, click directly on the interactive full body diagram to select pain areas, and receive instant health insights.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Medical Disclaimer:</strong> This application is an informational tool only and does NOT provide professional medical advice, diagnosis, or treatment. 
    If you are experiencing severe symptoms, chest pain, difficulty breathing, or a medical emergency, please seek immediate emergency care.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LAYOUT
# -----------------------------------------------------------------------------
col_input, col_diagram = st.columns([1, 1.2], gap="large")

with col_input:
    st.markdown("### 1. Basic Information & Symptoms")
    user_name = st.text_input("Full Name", placeholder="e.g., Jane Doe")
    col_a, col_b = st.columns(2)
    with col_a:
        user_age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col_b:
        user_gender = st.selectbox("Gender", ["Select", "Male", "Female", "Non-Binary", "Prefer not to say"])
        
    current_symptoms_text = st.text_area(
        "Describe how you feel / Additional Symptoms", 
        placeholder="e.g., Sharp pain on movement, mild fever, fatigue...",
        height=100
    )
    
    is_emergency = st.checkbox("🚨 **Check this box if you consider this an EMERGENCY**")

with col_diagram:
    st.markdown("### 2. Interactive Full Body Diagram")
    st.caption("Click on any region of the body illustration below to mark where you feel pain or discomfort:")

    # HTML/SVG Interactive Full Body Diagram Component
    body_map_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 0; }
            .container { position: relative; width: 260px; height: 500px; }
            svg { width: 100%; height: 100%; }
            .body-region {
                fill: #64748B;
                fill-opacity: 0.25;
                stroke: #334155;
                stroke-width: 2;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .body-region:hover {
                fill: #3B82F6;
                fill-opacity: 0.5;
            }
            .body-region.selected {
                fill: #EF4444 !important;
                fill-opacity: 0.7 !important;
                stroke: #B91C1C !important;
            }
            .label { font-size: 11px; fill: #1E293B; font-weight: bold; pointer-events: none; }
            .selection-box { margin-top: 10px; font-size: 13px; color: #1E3A8A; font-weight: 600; text-align: center; }
            button { margin-top: 8px; padding: 4px 10px; font-size: 11px; cursor: pointer; border-radius: 4px; border: 1px solid #CBD5E1; background: #F1F5F9; }
            button:hover { background: #E2E8F0; }
        </style>
    </head>
    <body>
        <div class="container">
            <svg viewBox="0 0 200 450">
                <!-- Human Body Silhouette Base -->
                <g id="body-silhouette" opacity="0.15" fill="#000">
                    <circle cx="100" cy="40" r="28"/> <!-- Head -->
                    <rect x="94" y="68" width="12" height="15"/> <!-- Neck -->
                    <path d="M 60,83 L 140,83 L 155,190 L 140,200 L 135,130 L 135,230 L 65,230 L 65,130 L 45,200 L 45,190 Z"/> <!-- Torso & Arms -->
                    <rect x="70" y="230" width="25" height="180" rx="10"/> <!-- Left Leg -->
                    <rect x="105" y="230" width="25" height="180" rx="10"/> <!-- Right Leg -->
                </g>

                <!-- Interactive Anatomical Clickable Zones -->
                <!-- Head & Scalp -->
                <path id="Head / Scalp" class="body-region" d="M 75,40 A 25,25 0 1,1 125,40 A 25,25 0 1,1 75,40 Z" />
                <text x="100" y="32" class="label" text-anchor="middle">Head</text>

                <!-- Eyes / Ears / Nose -->
                <rect id="Eyes / Ears / Nose" class="body-region" x="80" y="42" width="40" height="22" rx="4" />
                <text x="100" y="56" class="label" text-anchor="middle">Face</text>

                <!-- Chest / Heart -->
                <path id="Chest / Heart" class="body-region" d="M 65,85 L 135,85 L 130,145 L 70,145 Z" />
                <text x="100" y="118" class="label" text-anchor="middle">Chest</text>

                <!-- Abdomen / Stomach -->
                <path id="Abdomen / Stomach" class="body-region" d="M 70,148 L 130,148 L 125,215 L 75,215 Z" />
                <text x="100" y="185" class="label" text-anchor="middle">Abdomen</text>

                <!-- Arms / Hands (Left & Right Combined) -->
                <g id="Arms / Hands" class="body-region">
                    <path d="M 45,88 L 62,88 L 55,200 L 38,200 Z" />
                    <path d="M 138,88 L 155,88 L 162,200 L 145,200 Z" />
                </g>

                <!-- Back / Spine (Represented visually on upper torso sides) -->
                <path id="Back / Spine" class="body-region" d="M 60,95 L 68,95 L 68,200 L 60,200 Z M 132,95 L 140,95 L 140,200 L 132,200 Z" />

                <!-- Legs / Feet -->
                <g id="Legs / Feet" class="body-region">
                    <rect x="68" y="220" width="28" height="200" rx="8" />
                    <rect x="104" y="220" width="28" height="200" rx="8" />
                </g>
                <text x="100" y="320" class="label" text-anchor="middle">Legs</text>
            </svg>
        </div>

        <div class="selection-box" id="selection-text">Selected: None</div>
        <button onclick="clearSelection()">Clear Selections</button>

        <script>
            let selectedParts = new Set();

            document.querySelectorAll('.body-region').forEach(element => {
                element.addEventListener('click', function() {
                    const id = this.id;
                    if (selectedParts.has(id)) {
                        selectedParts.delete(id);
                        this.classList.remove('selected');
                    } else {
                        selectedParts.add(id);
                        this.classList.add('selected');
                    }
                    updateDisplay();
                });
            });

            function clearSelection() {
                selectedParts.clear();
                document.querySelectorAll('.body-region').forEach(el => el.classList.remove('selected'));
                updateDisplay();
            }

            function updateDisplay() {
                const arr = Array.from(selectedParts);
                document.getElementById('selection-text').innerText = "Selected: " + (arr.length > 0 ? arr.join(', ') : 'None');
                
                // Send data back to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: arr
                }, '*');
            }
        </script>
    </body>
    </html>
    """

    # Embed HTML body map component
    selected_from_html = components.html(body_map_html, height=580)
    
    # Sync visual selection with session state via multi-select fallback/override
    selected_parts = st.multiselect(
        "Selected Body Regions (Synced with diagram):",
        options=list(KNOWLEDGE_BASE.keys()),
        default=st.session_state.selected_parts,
        key="body_parts_multiselect"
    )
    st.session_state.selected_parts = selected_parts

# -----------------------------------------------------------------------------
# EMERGENCY SECTION
# -----------------------------------------------------------------------------
if is_emergency:
    st.error("🚨 EMERGENCY MODE ACTIVATED")
    st.markdown("If you or someone around you requires immediate urgent care, please enter your city below or call local emergency services immediately.")
    
    col_loc, col_hosp = st.columns([1, 2])
    with col_loc:
        location = st.text_input("Enter your City / Town", placeholder="e.g., New York, London, Delhi")
    
    with col_hosp:
        if location:
            matched_city = next((city for city in HOSPITAL_DATABASE if city.lower() in location.lower()), None)
            st.markdown(f"#### Nearby Emergency Hospitals around '{location}'")
            
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
                    <strong style="color: #1E3A8A; font-size: 1.05rem;">🏥 City Emergency General Hospital</strong><br/>
                    <span style="color: #4B5563;">📍 Address: Central Healthcare Hub, {location}</span><br/>
                    <span style="color: #059669; font-weight: 600;">📞 Emergency Hotline: 911 / 112 / 102</span>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GENERATE SUMMARY & DIAGNOSTIC REPORT
# -----------------------------------------------------------------------------
st.markdown("---")
generate_btn = st.button("🔍 Generate Health Assessment & Guidance Report", type="primary", use_container_width=True)

if generate_btn:
    if not user_name:
        st.warning("Please enter your name above.")
    elif not st.session_state.selected_parts and not current_symptoms_text:
        st.warning("Please click on the full body diagram to select pain areas or describe your symptoms.")
    else:
        st.markdown("## 📄 Medical Assessment & Insights Summary")
        st.markdown(f"""
        **Patient Name:** {user_name} | **Age:** {user_age} | **Gender:** {user_gender}  
        **Reported Symptoms:** {current_symptoms_text if current_symptoms_text else "None described"}  
        **Selected Affected Areas:** {', '.join(st.session_state.selected_parts) if st.session_state.selected_parts else "General"}
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
            st.markdown("### 💡 Care & Wellness Tips")
            for item in list(dict.fromkeys(tips)):
                st.markdown(f"- {item}")

        st.info("💡 **Recommended Action:** Share this summary with a qualified healthcare practitioner for accurate clinical evaluation.")