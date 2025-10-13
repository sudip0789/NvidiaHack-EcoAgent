"""
Report Generator Tool
Generates civic environmental reports using NVIDIA Nemotron LLM
"""

from typing import Dict, Any
from datetime import datetime
from utils.helpers import call_nemotron_llm, extract_text_from_response


def generate_civic_report(
    classification: Dict[str, Any],
    severity: Dict[str, Any],
    location: str = "",
    additional_notes: str = ""
) -> Dict[str, Any]:
    """
    Generate a comprehensive civic report for environmental authorities
    
    Args:
        classification: Waste classification result
        severity: Severity assessment result
        location: Location of the incident
        additional_notes: Any additional notes from the reporter
        
    Returns:
        Dict containing formatted report sections
    """
    
    # Prepare context for report generation
    context = f"""
Environmental Issue Report Details:

CLASSIFICATION:
- Waste Type: {classification.get('waste_type')}
- Confidence: {classification.get('confidence')}
- Description: {classification.get('description')}
- Visible Items: {', '.join(classification.get('visible_items', []))}

SEVERITY ASSESSMENT:
- Severity Level: {severity.get('severity')}
- Severity Score: {severity.get('severity_score')}/5
- Response Time: {severity.get('response_time')}
- Health Risk: {severity.get('health_risk', 'Not assessed')}
- Environmental Impact: {severity.get('environmental_impact', 'Not assessed')}

LOCATION:
{location if location else 'Not specified'}

ADDITIONAL NOTES:
{additional_notes if additional_notes else 'None'}
"""

    # System prompt for report generation
    system_prompt = """You are an environmental report specialist. Your job is to create clear, professional, 
actionable reports for civic authorities. Be concise, factual, and focus on what actions need to be taken."""

    # User prompt for report generation
    user_prompt = f"""{context}

Generate a professional environmental incident report with the following sections:

1. **Executive Summary** (2-3 sentences summarizing the key issue)
2. **Detailed Findings** (bullet points of what was observed)
3. **Risk Assessment** (health and environmental risks)
4. **Recommended Actions** (specific steps to address the issue)
5. **Priority Level** (based on severity)

Make the report clear, actionable, and appropriate for submission to environmental authorities.
Format the output in a structured way that can be easily parsed."""

    try:
        # Call Nemotron LLM for report generation
        response = call_nemotron_llm(
            prompt=user_prompt,
            model="nvidia/llama-3_3-nemotron-super-49b-v1_5",
            temperature=0.7,
            max_tokens=2048,
            system_prompt=system_prompt
        )
        
        # Extract text from response
        report_text = extract_text_from_response(response)
        
        if report_text.startswith("ERROR:"):
            return _create_fallback_report(classification, severity, location, report_text)
        
        # Parse the report into sections
        report_sections = _parse_report_sections(report_text)
        
        # Generate report metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "report_id": f"ECO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": timestamp,
            "location": location,
            "waste_type": classification.get('waste_type'),
            "severity": severity.get('severity'),
            "full_report": report_text,
            "sections": report_sections,
            "metadata": {
                "classification_confidence": classification.get('confidence'),
                "severity_score": severity.get('severity_score'),
                "response_time": severity.get('response_time')
            }
        }
        
    except Exception as e:
        return _create_fallback_report(
            classification, 
            severity, 
            location, 
            f"Exception during report generation: {str(e)}"
        )


def _parse_report_sections(report_text: str) -> Dict[str, str]:
    """
    Parse report text into sections
    
    Args:
        report_text: Full report text
        
    Returns:
        Dict of report sections
    """
    sections = {
        "executive_summary": "",
        "detailed_findings": "",
        "risk_assessment": "",
        "recommended_actions": "",
        "priority_level": ""
    }
    
    # Try to extract sections using common headers
    import re
    
    # Define section patterns
    patterns = {
        "executive_summary": r"(?:Executive Summary|Summary)[:\s]+(.*?)(?=\n\n|\*\*|#{1,2}\s|$)",
        "detailed_findings": r"(?:Detailed Findings|Findings|Observations)[:\s]+(.*?)(?=\n\n\*\*|#{1,2}\s|$)",
        "risk_assessment": r"(?:Risk Assessment|Risks?)[:\s]+(.*?)(?=\n\n\*\*|#{1,2}\s|$)",
        "recommended_actions": r"(?:Recommended Actions?|Actions?|Recommendations?)[:\s]+(.*?)(?=\n\n\*\*|#{1,2}\s|$)",
        "priority_level": r"(?:Priority Level|Priority)[:\s]+(.*?)(?=\n\n|\*\*|#{1,2}\s|$)"
    }
    
    for section_key, pattern in patterns.items():
        match = re.search(pattern, report_text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section_key] = match.group(1).strip()
    
    # If parsing fails, store full text in executive summary
    if not any(sections.values()):
        sections["executive_summary"] = report_text
    
    return sections


def _create_fallback_report(
    classification: Dict[str, Any],
    severity: Dict[str, Any],
    location: str,
    error_msg: str
) -> Dict[str, Any]:
    """
    Create a fallback report when LLM fails
    
    Args:
        classification: Classification result
        severity: Severity result
        location: Location
        error_msg: Error message
        
    Returns:
        Fallback report dict
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate a basic report using template
    waste_type = classification.get('waste_type', 'Unknown')
    severity_level = severity.get('severity', 'unknown')
    description = classification.get('description', 'No description available')
    
    fallback_text = f"""ENVIRONMENTAL INCIDENT REPORT (Auto-Generated)

Executive Summary:
{waste_type} detected at {location if location else 'unspecified location'} with {severity_level} severity level.

Detailed Findings:
- Waste Type: {waste_type}
- Description: {description}
- Confidence Level: {classification.get('confidence', 'unknown')}

Risk Assessment:
- Severity Level: {severity_level.upper()}
- Severity Score: {severity.get('severity_score', 'N/A')}/5
- Response Time Required: {severity.get('response_time', 'Standard')}

Recommended Actions:
- Dispatch appropriate cleanup crew
- Assess the extent of contamination
- Implement containment measures if necessary
- Follow standard protocols for {waste_type}

Priority Level: {severity_level.upper()}

Note: This is an auto-generated report. Manual review recommended."""

    return {
        "report_id": f"ECO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": timestamp,
        "location": location,
        "waste_type": waste_type,
        "severity": severity_level,
        "full_report": fallback_text,
        "sections": {
            "executive_summary": f"{waste_type} detected with {severity_level} severity",
            "detailed_findings": description,
            "risk_assessment": f"{severity_level.upper()} priority",
            "recommended_actions": "Standard cleanup and assessment required",
            "priority_level": severity_level.upper()
        },
        "metadata": {
            "classification_confidence": classification.get('confidence'),
            "severity_score": severity.get('severity_score'),
            "response_time": severity.get('response_time'),
            "is_fallback": True,
            "error": error_msg
        }
    }


def format_report_for_display(report: Dict[str, Any]) -> str:
    """
    Format report for human-readable display
    
    Args:
        report: Report dict
        
    Returns:
        Formatted string
    """
    sections = report.get("sections", {})
    metadata = report.get("metadata", {})
    
    formatted = f"""
╔══════════════════════════════════════════════════════════════╗
║           ENVIRONMENTAL INCIDENT REPORT                       ║
╚══════════════════════════════════════════════════════════════╝

Report ID: {report.get('report_id', 'N/A')}
Timestamp: {report.get('timestamp', 'N/A')}
Location: {report.get('location', 'Not specified')}

─────────────────────────────────────────────────────────────
EXECUTIVE SUMMARY
─────────────────────────────────────────────────────────────
{sections.get('executive_summary', 'Not available')}

─────────────────────────────────────────────────────────────
DETAILED FINDINGS
─────────────────────────────────────────────────────────────
{sections.get('detailed_findings', 'Not available')}

─────────────────────────────────────────────────────────────
RISK ASSESSMENT
─────────────────────────────────────────────────────────────
{sections.get('risk_assessment', 'Not available')}

─────────────────────────────────────────────────────────────
RECOMMENDED ACTIONS
─────────────────────────────────────────────────────────────
{sections.get('recommended_actions', 'Not available')}

─────────────────────────────────────────────────────────────
PRIORITY LEVEL: {sections.get('priority_level', 'MEDIUM')}
─────────────────────────────────────────────────────────────

Metadata:
- Classification Confidence: {metadata.get('classification_confidence', 'N/A')}
- Severity Score: {metadata.get('severity_score', 'N/A')}/5
- Expected Response Time: {metadata.get('response_time', 'N/A')}
"""
    return formatted
