"""
EcoAgent Streamlit Dashboard
Interactive UI for environmental reporting
"""

import streamlit as st
import sys
import os
from io import BytesIO
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eco_agent import EcoAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def init_session_state():
    """Initialize session state variables"""
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = EcoAgent(verbose=False)
        except ValueError as e:
            st.error(f"Failed to initialize EcoAgent: {str(e)}")
            st.session_state.agent = None


def display_header():
    """Display app header"""
    st.set_page_config(
        page_title="EcoAgent - Environmental Reporting",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌍 EcoAgent")
    st.markdown("### AI-Powered Environmental Reporting System")
    st.markdown("Powered by **NVIDIA Nemotron** models")
    st.divider()


def display_sidebar():
    """Display sidebar with information"""
    with st.sidebar:
        st.header("📋 About EcoAgent")
        st.markdown("""
        EcoAgent uses state-of-the-art AI to analyze environmental issues:
        
        **Models Used:**
        - 🔍 **Nemotron VLM 1.5** - Image analysis
        - 🧠 **Nemotron Nano 9B** - Severity reasoning
        - 📝 **Llama 3.3 Nemotron 49B** - Report generation
        
        **How it works:**
        1. Upload an image of waste or pollution
        2. Provide location details
        3. Get instant AI-powered analysis
        4. Receive a civic report for authorities
        """)
        
        st.divider()
        
        st.header("⚙️ Settings")
        use_llm_severity = st.checkbox(
            "Use AI for severity estimation",
            value=True,
            help="Uses LLM reasoning for severity. Uncheck for rule-based estimation."
        )
        
        st.divider()
        
        st.markdown("---")
        st.caption("Built for NVIDIA Hackathon 2025")
        
        return use_llm_severity


def display_upload_section():
    """Display file upload section"""
    st.header("📸 Upload Image")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image of waste or pollution",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            help="Upload a clear image showing the environmental issue"
        )
    
    with col2:
        if uploaded_file is not None:
            st.success("✓ Image uploaded")
        else:
            st.info("Waiting for image...")
    
    return uploaded_file


def display_location_input():
    """Display location input section"""
    st.header("📍 Location Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input(
            "Location",
            placeholder="e.g., Main Street, Downtown, City Park",
            help="Provide the location where the issue was observed"
        )
    
    with col2:
        additional_notes = st.text_area(
            "Additional Notes (Optional)",
            placeholder="Any additional observations or context...",
            height=100,
            help="Add any extra details that might be helpful"
        )
    
    return location, additional_notes


def display_image_preview(uploaded_file):
    """Display uploaded image preview"""
    if uploaded_file is not None:
        st.subheader("📷 Image Preview")
        image = Image.open(uploaded_file)
        
        # Display image with reasonable size
        st.image(image, use_container_width=True, caption="Uploaded Image")
        
        # Reset file pointer for processing
        uploaded_file.seek(0)


def display_analysis_results(results):
    """Display analysis results"""
    if results.get("status") == "error":
        st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
        return
    
    if results.get("status") != "complete":
        st.warning("⚠️ Analysis incomplete")
        return
    
    # Extract results
    classification = results["steps"].get("classification", {})
    severity = results["steps"].get("severity", {})
    report = results["steps"].get("report", {})
    
    st.success("✅ Analysis Complete!")
    st.divider()
    
    # Display key metrics
    st.header("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Waste Type",
            value=classification.get("waste_type", "Unknown")[:20],
        )
    
    with col2:
        severity_level = severity.get("severity", "unknown").upper()
        severity_colors = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "MINIMAL": "🔵"
        }
        st.metric(
            label="Severity",
            value=f"{severity_colors.get(severity_level, '⚪')} {severity_level}"
        )
    
    with col3:
        st.metric(
            label="Confidence",
            value=classification.get("confidence", "unknown").upper()
        )
    
    with col4:
        st.metric(
            label="Report ID",
            value=report.get("report_id", "N/A")[-10:]
        )
    
    st.divider()
    
    # Display detailed sections in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Full Report",
        "🔍 Classification Details",
        "⚠️ Severity Assessment",
        "📄 Raw Data"
    ])
    
    with tab1:
        display_report_tab(report)
    
    with tab2:
        display_classification_tab(classification)
    
    with tab3:
        display_severity_tab(severity)
    
    with tab4:
        display_raw_data_tab(results)


def display_report_tab(report):
    """Display report details"""
    st.subheader("📋 Civic Report")
    
    sections = report.get("sections", {})
    metadata = report.get("metadata", {})
    
    # Executive Summary
    st.markdown("#### Executive Summary")
    st.info(sections.get("executive_summary", "Not available"))
    
    # Detailed Findings
    st.markdown("#### Detailed Findings")
    st.markdown(sections.get("detailed_findings", "Not available"))
    
    # Risk Assessment
    st.markdown("#### Risk Assessment")
    st.warning(sections.get("risk_assessment", "Not available"))
    
    # Recommended Actions
    st.markdown("#### Recommended Actions")
    st.success(sections.get("recommended_actions", "Not available"))
    
    # Priority Level
    st.markdown("#### Priority Level")
    priority = sections.get("priority_level", "MEDIUM")
    st.markdown(f"**{priority}**")
    
    st.divider()
    
    # Download button for full report
    full_report_text = report.get("full_report", "")
    if full_report_text:
        st.download_button(
            label="📥 Download Full Report",
            data=full_report_text,
            file_name=f"{report.get('report_id', 'report')}.txt",
            mime="text/plain"
        )


def display_classification_tab(classification):
    """Display classification details"""
    st.subheader("🔍 Waste Classification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Waste Type:**")
        st.markdown(f"`{classification.get('waste_type', 'Unknown')}`")
        
        st.markdown("**Confidence Level:**")
        st.markdown(f"`{classification.get('confidence', 'unknown').upper()}`")
    
    with col2:
        st.markdown("**Tags:**")
        tags = classification.get('tags', [])
        if tags:
            st.markdown(", ".join(f"`{tag}`" for tag in tags))
        else:
            st.markdown("_No tags_")
        
        st.markdown("**Visible Items:**")
        items = classification.get('visible_items', [])
        if items:
            for item in items[:5]:  # Limit to 5 items
                st.markdown(f"- {item}")
        else:
            st.markdown("_No items identified_")
    
    st.markdown("**Description:**")
    st.write(classification.get('description', 'No description available'))


def display_severity_tab(severity):
    """Display severity assessment details"""
    st.subheader("⚠️ Severity Assessment")
    
    # Severity gauge
    severity_score = severity.get("severity_score", 3)
    severity_level = severity.get("severity", "medium")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Visual severity indicator
        st.progress(severity_score / 5.0)
        st.markdown(f"**Severity Score: {severity_score}/5** ({severity_level.upper()})")
    
    st.divider()
    
    # Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Response Time Required:**")
        st.info(severity.get("response_time", "Standard"))
        
        st.markdown("**Assessment Method:**")
        st.markdown(f"`{severity.get('method', 'unknown')}`")
    
    with col2:
        if "health_risk" in severity:
            st.markdown("**Health Risk:**")
            st.warning(severity.get("health_risk", "Not assessed"))
        
        if "environmental_impact" in severity:
            st.markdown("**Environmental Impact:**")
            st.warning(severity.get("environmental_impact", "Not assessed"))
    
    # Reasoning (if available from LLM)
    if "reasoning" in severity and severity["reasoning"]:
        st.markdown("**AI Reasoning:**")
        st.write(severity["reasoning"])
    
    # Urgency factors
    if "urgency_factors" in severity and severity["urgency_factors"]:
        st.markdown("**Urgency Factors:**")
        for factor in severity["urgency_factors"]:
            st.markdown(f"- {factor}")


def display_raw_data_tab(results):
    """Display raw JSON data"""
    st.subheader("📄 Raw Analysis Data")
    st.json(results)


def main():
    """Main application function"""
    # Initialize
    init_session_state()
    display_header()
    
    # Check if agent is initialized
    if st.session_state.agent is None:
        st.error("⚠️ EcoAgent could not be initialized. Please check your NVIDIA_API_KEY in the .env file.")
        st.stop()
    
    # Sidebar
    use_llm_severity = display_sidebar()
    
    # Main content
    uploaded_file = display_upload_section()
    
    if uploaded_file is not None:
        display_image_preview(uploaded_file)
        
        location, additional_notes = display_location_input()
        
        st.divider()
        
        # Analyze button
        if st.button("🚀 Analyze Image", type="primary", use_container_width=True):
            if not location:
                st.warning("⚠️ Please provide a location before analyzing.")
            else:
                with st.spinner("🔄 Analyzing image... This may take 30-60 seconds..."):
                    # Read image bytes
                    image_bytes = uploaded_file.read()
                    
                    # Run analysis
                    results = st.session_state.agent.analyze_image(
                        image_path_or_bytes=image_bytes,
                        location=location,
                        additional_notes=additional_notes,
                        use_llm_severity=use_llm_severity
                    )
                    
                    st.session_state.analysis_results = results
        
        # Display results if available
        if st.session_state.analysis_results is not None:
            st.divider()
            display_analysis_results(st.session_state.analysis_results)
    
    else:
        st.info("👆 Please upload an image to get started")


if __name__ == "__main__":
    main()
