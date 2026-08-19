python
import streamlit as st
import os
from datetime import datetime
from privacypolicy import PrivacyPolicyGenerator
import base64

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

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = PrivacyPolicyGenerator()
if 'policy_generated' not in st.session_state:
    st.session_state.policy_generated = False
if 'policy_content' not in st.session_state:
    st.session_state.policy_content = ""

# Title
st.title("🔒 UK GDPR Privacy Policy Generator")
st.markdown("Generate a complete, UK GDPR-compliant privacy policy with AI usage tracking")

# Main form
with st.form("privacy_policy_form"):
    
    # ===== SECTION 1: BUSINESS INFO =====
    st.markdown("### 🏢 Business Information")
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Business/Company Name *", placeholder="e.g., Acme Ltd")
        website = st.text_input("Website URL *", placeholder="https://yourwebsite.com")
        email = st.text_input("Contact Email *", placeholder="privacy@yourwebsite.com")
        
    with col2:
        phone = st.text_input("Phone Number", placeholder="+44 1234 567890")
        address = st.text_area("Business Address", placeholder="123 High Street, London, UK")
        business_type = st.selectbox(
            "Business Type",
            ["Select one...", "Online/Physical Retail", "Consultancy/Professional Services", 
             "SaaS/Software Provider", "Marketing/Digital Agency", "E-commerce", 
             "Hospitality/Travel", "Health/Wellness", "Education/Training", 
             "Financial Services", "Technology/IT Services", "Other"]
        )
    
    if business_type == "Other":
        business_type_other = st.text_input("Please specify")
    else:
        business_type_other = ""
    
    # ===== SECTION 2: AI USAGE =====
    st.markdown("### 🤖 AI Usage")
    st.info("Select all the ways your business uses AI")
    
    ai_uses = st.multiselect(
        "How does your business use AI?",
        [
            "AI Chatbot for customer interactions",
            "AI for marketing/email personalisation",
            "AI for customer profiling/behaviour analysis",
            "AI for automated decision-making",
            "Using customer/employee data to train AI systems",
            "AI for content generation",
            "AI for analytics/predictive analysis"
        ]
    )
    
    # AI Provider Locations
    if ai_uses:
        st.markdown("#### AI Provider Locations")
        ai_locations = st.multiselect(
            "Where are your AI providers located?",
            ["UK", "United States", "EU/EEA", "Canada", "Australia", "Other"]
        )
        
        if "Other" in ai_locations:
            ai_locations_other = st.text_input("Please specify other locations")
        
        # AI Data Processed
        st.markdown("#### Data Processed by AI")
        ai_data = st.multiselect(
            "What types of data does your AI process?",
            ["Names and contact details", "Payment information", "Order/purchase history",
             "Chatbot conversation logs", "Email content", "Website usage/behaviour data",
             "Customer support tickets", "Sensitive data"]
        )
        
        ai_opt_out = st.checkbox("Do you offer customers the option to opt out of AI processing?")
    
    # ===== SECTION 3: DATA COLLECTION =====
    st.markdown("### 📊 Data Collection")
    
    data_collected = st.multiselect(
        "What personal information does your business collect?",
        ["Name and contact details", "Address information", "Payment/financial information",
         "Order/purchase history", "Website usage and analytics data", "Cookie data",
         "Chatbot/conversation logs", "Email content and preferences", "Customer support enquiries",
         "Social media information", "Employee data", "Sensitive data"]
    )
    
    # ===== SECTION 4: PURPOSES =====
    st.markdown("### 🎯 Processing Purposes")
    
    purposes = st.multiselect(
        "Why do you process personal data?",
        ["Process orders and transactions", "Provide customer service and support",
         "Send marketing communications", "Improve products and services",
         "Analytics and business intelligence", "Fraud prevention and detection",
         "Legal compliance", "AI system training and improvement", 
         "Customer profiling and personalisation"]
    )
    
    # ===== SECTION 5: DATA SHARING =====
    st.markdown("### 🔄 Data Sharing")
    
    sharing = st.multiselect(
        "Do you share data with any third parties?",
        ["Payment processors", "Hosting/cloud providers", "AI service providers",
         "Customer service platforms", "Marketing agencies/tools", "Analytics providers",
         "Email service providers", "Cloud storage providers", "IT support providers",
         "Legal/accounting professionals", "Delivery/courier services"]
    )
    
    # ===== SECTION 6: MARKETING & COOKIES =====
    st.markdown("### 📧 Marketing & Cookies")
    
    col1, col2 = st.columns(2)
    with col1:
        uses_marketing = st.checkbox("Send marketing communications")
        if uses_marketing:
            marketing_methods = st.multiselect(
                "Marketing methods",
                ["Email marketing", "SMS text messages", "Postal mail", "Social media", "Phone calls"]
            )
            marketing_consent = st.checkbox("Get explicit consent before marketing")
    
    with col2:
        uses_cookies = st.checkbox("Use cookies on your website")
        if uses_cookies:
            cookie_types = st.multiselect(
                "Cookie types",
                ["Essential/necessary cookies", "Analytics/performance cookies", 
                 "Functional cookies", "Marketing/targeting cookies"]
            )
        
        uses_analytics = st.checkbox("Use website analytics")
        if uses_analytics:
            analytics_types = st.multiselect(
                "Analytics collected",
                ["Page views and traffic", "User behaviour tracking", 
                 "Conversion tracking", "Referral sources"]
            )
    
    # ===== SECTION 7: RETENTION =====
    st.markdown("### ⏱️ Data Retention")
    retention = st.multiselect(
        "How long do you keep personal data?",
        ["1 year", "2 years", "3 years", "5 years", "7 years (financial records)"]
    )
    
    # ===== Submit Button =====
    st.markdown("---")
    submitted = st.form_submit_button("🚀 Generate Privacy Policy", use_container_width=True)

# ===== PROCESS THE FORM =====
if submitted:
    with st.spinner("Generating your privacy policy..."):
        gen = st.session_state.generator
        
        # Set all the values
        gen.company_name = company_name
        gen.website = website
        gen.email = email
        gen.phone = phone
        gen.address = address
        gen.business_type = business_type_other if business_type == "Other" and business_type_other else business_type
        gen.ai_use_cases = ai_uses
        gen.ai_provider_locations = [loc for loc in ai_locations if loc != "Other"] + ([ai_locations_other] if "Other" in ai_locations and ai_locations_other else [])
        gen.ai_data_processed = ai_data
        gen.ai_opt_out_available = ai_opt_out
        gen.data_collected = data_collected
        gen.purposes = purposes
        gen.shared_with_categories = sharing
        gen.retention_periods = retention
        
        # Generate the policy
        policy = gen.generate_privacy_policy()
        st.session_state.policy_content = policy
        st.session_state.policy_generated = True
        
        st.success("✅ Privacy Policy Generated Successfully!")
        
        # Display policy
        st.markdown("### 📄 Your Privacy Policy")
        st.markdown("---")
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download TXT",
                data=policy,
                file_name=f"privacy_policy_{company_name.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Try to save as DOCX
            try:
                docx_path = f"temp_{company_name.replace(' ', '_')}.docx"
                docx_saved = gen.save_docx(policy, docx_path)
                if docx_saved:
                    with open(docx_path, "rb") as f:
                        st.download_button(
                            label="📥 Download DOCX",
                            data=f.read(),
                            file_name=f"privacy_policy_{company_name.replace(' ', '_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    os.remove(docx_path)
            except:
                st.download_button(
                    label="📥 Download DOCX",
                    data=policy,
                    file_name=f"privacy_policy_{company_name.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    disabled=True,
                    help="python-docx not installed. Install with: pip install python-docx",
                    use_container_width=True
                )
        
        with col3:
            # Copy to clipboard button
            st.button("📋 Copy to Clipboard", use_container_width=True, 
                     help="Select all text and copy manually")
        
        # Preview
        with st.expander("📖 Preview Policy (Click to expand)"):
            st.markdown("---")
            st.markdown(policy)

# Footer
st.markdown("---")
st.markdown("*This privacy policy generator is for informational purposes. Please review with a legal professional before publishing.*")
