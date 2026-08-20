import streamlit as st
import os
from datetime import datetime
from privacypolicy import PrivacyPolicyGenerator

# Page configuration for better embedding
st.set_page_config(
    page_title="Privacy Policy Generator",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better embedding
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stDownloadButton > button {
        width: 100%;
    }
    .policy-preview {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        max-height: 500px;
        overflow-y: scroll;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
    .section-header {
        background-color: #2E86AB;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 20px 0 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---- Canonical option lists (kept identical to the CLI generator so the
#      display text matches what generate_privacy_policy() expects) ----

BUSINESS_TYPES = [
    "Select one...", "Online/Physical Retail", "Consultancy/Professional Services",
    "SaaS/Software Provider", "Marketing/Digital Agency", "E-commerce",
    "Hospitality/Travel", "Health/Wellness", "Education/Training",
    "Financial Services", "Technology/IT Services", "Other"
]

AI_USE_OPTIONS = [
    "AI Chatbot for customer interactions",
    "AI for marketing/email personalisation",
    "AI for customer profiling/behaviour analysis",
    "AI for automated decision-making",
    "Using customer/employee data to train AI systems",
    "AI for content generation",
    "AI for analytics/predictive analysis"
]

AI_LOCATION_OPTIONS = [
    "UK", "United States", "EU/EEA", "Canada", "Australia",
    "Not sure / it varies depending on the AI tool", "Other"
]

AI_DATA_OPTIONS = [
    "Names and contact details", "Payment information", "Order/purchase history",
    "Chatbot conversation logs", "Email content", "Website usage/behaviour data",
    "Customer support tickets", "Sensitive data"
]

DATA_COLLECTED_OPTIONS = [
    "Name and contact details", "Address information", "Payment/financial information",
    "Order/purchase history", "Website usage and analytics data", "Cookie data",
    "Chatbot/conversation logs", "Email content and preferences", "Customer support enquiries",
    "Social media information", "Employee data", "Sensitive data"
]

DATA_SOURCE_OPTIONS = [
    "Directly from the individual (e.g. forms, purchases, account signup)",
    "Automatically from website/app activity (cookies, usage data)",
    "From partners or other businesses (e.g. referrals, resellers)",
    "Publicly available sources",
    "From an individual's employer",
    "Generated or inferred by AI/automated systems"
]

ARTICLE9_BASIS_OPTIONS = [
    "Not applicable / not selected",
    "Explicit consent from the data subject",
    "Employment, social security, or social protection law",
    "Protection of vital interests",
    "Substantial public interest",
    "Health or social care",
    "Legal claims or court proceedings"
]

PURPOSE_OPTIONS = [
    "Process orders and transactions",
    "Provide customer service and support",
    "Send marketing communications (with consent)",
    "Improve products and services",
    "Analytics and business intelligence",
    "Fraud prevention and detection",
    "Legal compliance",
    "AI system training and improvement",
    "Customer profiling and personalisation"
]

ARTICLE6_BASIS_OPTIONS = [
    "Not selected",
    "Consent",
    "Necessary for a contract with the individual",
    "Necessary to comply with a legal obligation",
    "Necessary to protect someone's vital interests",
    "Necessary for a public task",
    "Legitimate interests"
]

SHARING_OPTIONS = [
    "Payment processors", "Hosting/cloud providers", "AI service providers",
    "Customer service platforms", "Marketing agencies/tools", "Analytics providers",
    "Email service providers", "Cloud storage providers", "IT support providers",
    "Legal/accounting professionals", "Delivery/courier services"
]

TRANSFER_COUNTRY_OPTIONS = [
    "United States", "Ireland", "Germany", "France", "Netherlands",
    "Canada", "Australia", "Singapore"
]

TRANSFER_SAFEGUARD_OPTIONS = [
    "Standard Contractual Clauses (SCCs)", "Adequacy decision (EU/EEA)",
    "Binding Corporate Rules", "Explicit consent from data subjects"
]

MARKETING_METHOD_OPTIONS = [
    "Email marketing", "SMS text messages", "Postal mail", "Social media", "Phone calls"
]

COOKIE_TYPE_OPTIONS = [
    "Essential/necessary cookies", "Analytics/performance cookies",
    "Functional cookies", "Marketing/targeting cookies"
]

ANALYTICS_TYPE_OPTIONS = [
    "Page views and traffic", "User behaviour tracking",
    "Conversion tracking", "Referral sources"
]

RETENTION_OPTIONS = ["1 year", "2 years", "3 years", "5 years", "7 years (financial records)"]

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = PrivacyPolicyGenerator()
if 'policy_generated' not in st.session_state:
    st.session_state.policy_generated = False
if 'policy_content' not in st.session_state:
    st.session_state.policy_content = ""

# Title
st.title("🔒 UK GDPR Privacy Policy Generator")
st.markdown("Generate a draft UK GDPR privacy policy with AI usage covered.")
st.info(
    "This produces a **draft**. Anything left blank is marked "
    "**[TO CONFIRM]** in the output rather than guessed at. Have a "
    "solicitor or data protection professional review the final policy "
    "before you publish it.",
    icon="⚠️"
)

# NOTE ON FORM DESIGN: every field below is always visible rather than
# conditionally shown based on other answers in the same form. Streamlit
# forms don't rerun on widget interaction until Submit is pressed, so
# fields that only "appear" once an earlier checkbox is ticked can't be
# filled in on the same submission - the user would need to submit twice.
# Showing everything up front avoids that trap; helper captions explain
# which fields only matter if a related option above is selected.

with st.form("privacy_policy_form"):

    # ===== SECTION 1: BUSINESS INFO =====
    st.markdown("### 🏢 Business Information")
    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Business/Company Name *", placeholder="e.g., Acme Ltd")
        website = st.text_input("Website URL *", placeholder="https://yourwebsite.com")
        email = st.text_input("Contact Email *", placeholder="privacy@yourwebsite.com")
        phone = st.text_input("Phone Number", placeholder="+44 1234 567890")

    with col2:
        address = st.text_area("Business Address", placeholder="123 High Street, London, UK")
        business_type = st.selectbox("Business Type", BUSINESS_TYPES)
        company_registration = st.text_input("Company Registration Number (optional)")
        ico_registration = st.text_input("ICO Registration Number (optional)")

    if business_type == "Other":
        business_type_other = st.text_input("Please specify business type")
    else:
        business_type_other = ""

    dpo_details = st.text_input(
        "Data Protection Officer contact details (leave blank if you don't have a DPO)"
    )

    st.markdown("---")

    # ===== SECTION 2: AI USAGE =====
    st.markdown("### 🤖 AI Usage")
    st.caption("Select all the ways your business uses AI. Leave blank if you don't use AI.")

    ai_uses = st.multiselect("How does your business use AI?", AI_USE_OPTIONS)

    st.markdown("#### AI provider locations")
    st.caption(
        "No need to name specific suppliers - just where processing broadly "
        "takes place. If you use several AI tools (e.g. a standalone chatbot "
        "AND AI features built into other software like Salesforce or "
        "Microsoft Copilot), select all that apply - or 'Not sure' if you "
        "haven't checked yet."
    )
    ai_locations = st.multiselect("Where are your AI providers located?", AI_LOCATION_OPTIONS)
    ai_locations_other = ""
    if "Other" in ai_locations:
        ai_locations_other = st.text_input("Please specify other AI provider location(s)")

    st.markdown("#### Data processed by AI")
    ai_data = st.multiselect("What types of data does your AI process?", AI_DATA_OPTIONS)
    ai_opt_out = st.checkbox("We offer customers the option to opt out of AI processing")

    with st.expander("Automated decision-making details (only if selected above)"):
        auto_decision_types_raw = st.text_input(
            "Types of automated decisions (comma-separated)",
            placeholder="e.g. job applications, refund decisions"
        )
        auto_decision_solely_automated = st.checkbox(
            "Some decisions are made WITHOUT any human involvement (solely automated)"
        )
        auto_decision_human_review = st.checkbox(
            "A person can review or reconsider the decision on request"
        )
        auto_decision_consequences = st.text_area(
            "Practical effect of these decisions on the person",
            placeholder="e.g. may result in application being rejected"
        )

    with st.expander("AI training details (only if 'training AI systems' selected above)"):
        ai_training_details = st.text_area(
            "What data is used to train/improve AI, and why?"
        )

    st.markdown("---")

    # ===== SECTION 3: DATA COLLECTION =====
    st.markdown("### 📊 Data Collection")

    data_collected = st.multiselect(
        "What personal information does your business collect?",
        DATA_COLLECTED_OPTIONS
    )

    data_sources = st.multiselect(
        "Where does this personal data come from?",
        DATA_SOURCE_OPTIONS
    )

    with st.expander("Special category (sensitive) data details (only if 'Sensitive data' selected above)"):
        sensitive_data_types_raw = st.text_input(
            "What sensitive data do you collect? (comma-separated)",
            placeholder="e.g. health information, religious beliefs"
        )
        sensitive_data_basis = st.multiselect(
            "Article 9 condition(s) relied on",
            [o for o in ARTICLE9_BASIS_OPTIONS if o != "Not applicable / not selected"]
        )

    st.markdown("---")

    # ===== SECTION 4: PURPOSES =====
    st.markdown("### 🎯 Processing Purposes")

    purposes = st.multiselect("Why do you process personal data?", PURPOSE_OPTIONS)

    st.markdown("#### Lawful basis (UK GDPR Article 6) for each purpose")
    st.caption("Only set a basis for the purposes you actually selected above.")
    purpose_basis_choices = {}
    for p in PURPOSE_OPTIONS:
        purpose_basis_choices[p] = st.selectbox(
            f"Lawful basis for: {p}", ARTICLE6_BASIS_OPTIONS, key=f"basis_{p}"
        )

    st.markdown("---")

    # ===== SECTION 5: DATA SHARING =====
    st.markdown("### 🔄 Data Sharing")

    sharing = st.multiselect("Do you share data with any third parties?", SHARING_OPTIONS)
    shared_data_description = st.text_area(
        "In a sentence, what type of information is shared and why? (no need to name suppliers)"
    )
    processor_contracts = st.checkbox(
        "We have written contracts (Article 28) with these data processors"
    )

    st.markdown("#### International data transfers")
    transfer_countries = st.multiselect(
        "Does personal data leave the UK? Select destination countries",
        TRANSFER_COUNTRY_OPTIONS
    )
    transfer_safeguards = st.multiselect(
        "Safeguards used for these transfers (only if countries selected above)",
        TRANSFER_SAFEGUARD_OPTIONS
    )

    st.markdown("---")

    # ===== SECTION 6: MARKETING & COOKIES =====
    st.markdown("### 📧 Marketing & Cookies")

    col1, col2 = st.columns(2)
    with col1:
        uses_marketing = st.checkbox("We send marketing communications")
        marketing_methods = st.multiselect(
            "Marketing methods (only if checked above)", MARKETING_METHOD_OPTIONS
        )
        marketing_consent = st.checkbox("We get explicit consent before marketing")

    with col2:
        uses_cookies = st.checkbox("Our website uses cookies")
        cookie_types = st.multiselect(
            "Cookie types (only if checked above)", COOKIE_TYPE_OPTIONS
        )

        uses_analytics = st.checkbox("We use website analytics")
        analytics_types = st.multiselect(
            "Analytics collected (only if checked above)", ANALYTICS_TYPE_OPTIONS
        )

    st.markdown("---")

    # ===== SECTION 7: RETENTION =====
    st.markdown("### ⏱️ Data Retention")
    retention = st.multiselect("How long do you keep personal data?", RETENTION_OPTIONS)

    # ===== Submit Button =====
    st.markdown("---")
    submitted = st.form_submit_button("🚀 Generate Privacy Policy", use_container_width=True)

# ===== PROCESS THE FORM =====
if submitted:
    if not company_name or not website or not email:
        st.error("Please fill in Business Name, Website and Contact Email - these are required.")
    else:
        with st.spinner("Generating your privacy policy..."):
            gen = PrivacyPolicyGenerator()
            st.session_state.generator = gen

            # ---- Business info ----
            gen.company_name = company_name
            gen.website = website
            gen.email = email
            gen.phone = phone
            gen.address = address
            gen.business_type = business_type_other if (business_type == "Other" and business_type_other) else business_type
            gen.company_registration = company_registration
            gen.ico_registration = ico_registration
            gen.has_dpo = bool(dpo_details)
            gen.data_protection_officer = dpo_details

            # ---- AI usage: set both the raw list AND the boolean flags the
            #      generator actually checks when building each section ----
            gen.ai_use_cases = ai_uses
            gen.uses_chatbot = "AI Chatbot for customer interactions" in ai_uses
            gen.uses_ai_marketing = "AI for marketing/email personalisation" in ai_uses
            gen.uses_profiling = "AI for customer profiling/behaviour analysis" in ai_uses
            gen.uses_automated_decisions = "AI for automated decision-making" in ai_uses
            gen.trains_ai_on_data = "Using customer/employee data to train AI systems" in ai_uses
            gen.uses_ai_content_gen = "AI for content generation" in ai_uses
            gen.uses_ai_analytics = "AI for analytics/predictive analysis" in ai_uses

            resolved_locations = [loc for loc in ai_locations if loc not in ("Other", "Not sure / it varies depending on the AI tool")]
            if "Other" in ai_locations and ai_locations_other:
                resolved_locations.append(ai_locations_other)
            gen.ai_provider_locations = resolved_locations
            gen.ai_provider_location_unconfirmed = "Not sure / it varies depending on the AI tool" in ai_locations

            gen.ai_data_processed = ai_data
            gen.ai_opt_out_available = ai_opt_out

            if gen.uses_automated_decisions:
                gen.auto_decision_types = [d.strip() for d in auto_decision_types_raw.split(",") if d.strip()]
                gen.auto_decision_solely_automated = auto_decision_solely_automated
                gen.auto_decision_human_review = auto_decision_human_review
                gen.auto_decision_consequences = auto_decision_consequences

            if gen.trains_ai_on_data:
                gen.ai_training_details = ai_training_details

            # ---- Data collection ----
            gen.data_collected = data_collected
            gen.data_sources = data_sources

            gen.uses_sensitive_data = "Sensitive data" in data_collected
            if gen.uses_sensitive_data:
                types_list = [s.strip() for s in sensitive_data_types_raw.split(",") if s.strip()]
                gen.sensitive_data_types = types_list
                if types_list:
                    # Reflect the described types in the collected-data list too
                    gen.data_collected = [d for d in gen.data_collected if d != "Sensitive data"] + types_list
                gen.sensitive_data_basis = "; ".join(sensitive_data_basis) if sensitive_data_basis else ""

            # ---- Purposes + lawful basis ----
            gen.purposes = purposes
            gen.purpose_lawful_basis = {
                p: purpose_basis_choices[p]
                for p in purposes
                if purpose_basis_choices.get(p) and purpose_basis_choices[p] != "Not selected"
            }

            # ---- Sharing ----
            gen.shared_with_categories = sharing
            gen.shared_data_description = shared_data_description
            gen.processor_contracts = processor_contracts if sharing else False

            gen.transfer_countries = transfer_countries
            gen.international_transfers = bool(transfer_countries)
            gen.transfer_safeguards = transfer_safeguards if transfer_countries else []

            # ---- Marketing & cookies ----
            gen.uses_marketing = uses_marketing
            gen.marketing_methods = marketing_methods if uses_marketing else []
            gen.marketing_consent = marketing_consent if uses_marketing else False

            gen.uses_cookies = uses_cookies
            gen.cookie_types = cookie_types if uses_cookies else []

            gen.uses_analytics = uses_analytics
            gen.analytics_types = analytics_types if uses_analytics else []

            # ---- Retention ----
            gen.retention_periods = retention

            # ---- Generate ----
            policy = gen.generate_privacy_policy()
            st.session_state.policy_content = policy
            st.session_state.policy_generated = True

        st.success("✅ Privacy Policy Draft Generated")

# ===== DISPLAY RESULTS (persists across reruns via session state) =====
if st.session_state.policy_generated and st.session_state.policy_content:
    policy = st.session_state.policy_content
    gen = st.session_state.generator
    safe_name = (gen.company_name or "policy").replace(' ', '_')

    to_confirm_count = policy.count("[TO CONFIRM")
    if to_confirm_count:
        st.warning(
            f"This draft has **{to_confirm_count}** section(s) marked "
            "[TO CONFIRM] where information wasn't provided. Fill those in "
            "before publishing."
        )

    st.markdown("### 📄 Your Privacy Policy")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📥 Download TXT",
            data=policy,
            file_name=f"privacy_policy_{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        try:
            docx_path = f"/tmp/temp_{safe_name}.docx"
            docx_saved = gen.save_docx(policy, docx_path)
            if docx_saved:
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                os.remove(docx_path)
                st.download_button(
                    label="📥 Download DOCX",
                    data=docx_bytes,
                    file_name=f"privacy_policy_{safe_name}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.download_button(
                    label="📥 Download DOCX (unavailable)",
                    data=policy,
                    file_name=f"privacy_policy_{safe_name}.txt",
                    disabled=True,
                    help="python-docx is not installed on the server. Install with: pip install python-docx",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Could not generate DOCX: {e}")

    # Preview
    with st.expander("📖 Preview Policy (Click to expand)", expanded=True):
        st.markdown(policy)

# Footer
st.markdown("---")
st.markdown(
    "*This tool produces a draft privacy policy. Please review it with a "
    "solicitor or data protection professional before publishing.*"
)
