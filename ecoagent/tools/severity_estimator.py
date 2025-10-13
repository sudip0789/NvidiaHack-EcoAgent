"""
Severity Estimator Tool
Estimates the severity of environmental issues
Uses rule-based logic with optional LLM enhancement
"""

from typing import Dict, Any
from utils.helpers import call_nemotron_llm, extract_text_from_response, parse_json_from_text


# Severity levels and their definitions
SEVERITY_LEVELS = {
    "critical": {
        "level": 5,
        "description": "Immediate threat to public health or environment",
        "response_time": "Immediate (within 24 hours)"
    },
    "high": {
        "level": 4,
        "description": "Significant environmental or health concern",
        "response_time": "Urgent (within 3 days)"
    },
    "medium": {
        "level": 3,
        "description": "Moderate concern requiring attention",
        "response_time": "Standard (within 1 week)"
    },
    "low": {
        "level": 2,
        "description": "Minor issue, routine cleanup needed",
        "response_time": "Regular schedule (within 2 weeks)"
    },
    "minimal": {
        "level": 1,
        "description": "Minimal impact, preventive action suggested",
        "response_time": "As resources permit"
    }
}


def estimate_severity_rule_based(classification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate severity using rule-based logic
    
    Args:
        classification: Waste classification result
        
    Returns:
        Severity assessment dict
    """
    waste_type = classification.get("waste_type", "").lower()
    confidence = classification.get("confidence", "low").lower()
    description = classification.get("description", "").lower()
    tags = [tag.lower() for tag in classification.get("tags", [])]
    
    # Default to medium
    severity_score = 3
    
    # Critical keywords
    critical_keywords = ["hazardous", "chemical", "toxic", "oil spill", "sewage", "battery", "medical"]
    high_keywords = ["e-waste", "electronic", "metal", "large amount", "widespread", "river", "water body"]
    low_keywords = ["minimal", "small", "single item", "paper", "cardboard"]
    
    # Check for critical severity
    if any(keyword in waste_type for keyword in critical_keywords):
        severity_score = 5
    elif any(keyword in description for keyword in critical_keywords):
        severity_score = 5
    
    # Check for high severity
    elif "hazardous" in waste_type or any(keyword in waste_type for keyword in high_keywords):
        severity_score = 4
    elif any(keyword in description for keyword in high_keywords):
        severity_score = 4
    
    # Check for low severity
    elif any(keyword in waste_type for keyword in low_keywords):
        severity_score = 2
    elif any(keyword in description for keyword in low_keywords):
        severity_score = 2
    
    # Adjust based on confidence
    if confidence == "low":
        severity_score = max(2, severity_score - 1)
    
    # Determine severity level
    severity_level = "medium"
    if severity_score >= 5:
        severity_level = "critical"
    elif severity_score >= 4:
        severity_level = "high"
    elif severity_score == 2:
        severity_level = "low"
    elif severity_score == 1:
        severity_level = "minimal"
    
    severity_info = SEVERITY_LEVELS[severity_level]
    
    return {
        "severity": severity_level,
        "severity_score": severity_score,
        "description": severity_info["description"],
        "response_time": severity_info["response_time"],
        "method": "rule-based"
    }


def estimate_severity_with_llm(
    classification: Dict[str, Any],
    location: str = ""
) -> Dict[str, Any]:
    """
    Estimate severity using LLM reasoning
    Falls back to rule-based if LLM fails
    
    Args:
        classification: Waste classification result
        location: Location of the waste
        
    Returns:
        Severity assessment dict
    """
    
    try:
        # Construct prompt for severity estimation
        prompt = f"""Assess the severity of this environmental issue:

Waste Type: {classification.get('waste_type')}
Description: {classification.get('description')}
Location: {location if location else 'Not specified'}
Confidence: {classification.get('confidence')}

Severity Levels:
- critical: Immediate threat to public health or environment
- high: Significant environmental or health concern
- medium: Moderate concern requiring attention
- low: Minor issue, routine cleanup needed
- minimal: Minimal impact, preventive action suggested

Provide your assessment in JSON format:
{{
    "severity": "critical/high/medium/low/minimal",
    "severity_score": 1-5,
    "reasoning": "explain your assessment in 2-3 sentences",
    "health_risk": "description of potential health risks",
    "environmental_impact": "description of environmental impact",
    "urgency_factors": ["list", "of", "factors"]
}}

Be objective and consider public health, environmental impact, and urgency."""

        # Call Nemotron LLM (using the nano model for faster reasoning)
        response = call_nemotron_llm(
            prompt=prompt,
            model="nvidia/nvidia-nemotron-nano-9b-v2",
            temperature=0.3,
            max_tokens=1024
        )
        
        # Extract and parse response
        text_response = extract_text_from_response(response)
        
        if text_response.startswith("ERROR:"):
            # Fallback to rule-based
            return estimate_severity_rule_based(classification)
        
        parsed_json = parse_json_from_text(text_response)
        
        if parsed_json and "severity" in parsed_json:
            severity_level = parsed_json.get("severity", "medium")
            severity_info = SEVERITY_LEVELS.get(severity_level, SEVERITY_LEVELS["medium"])
            
            return {
                "severity": severity_level,
                "severity_score": parsed_json.get("severity_score", severity_info["level"]),
                "description": severity_info["description"],
                "response_time": severity_info["response_time"],
                "reasoning": parsed_json.get("reasoning", ""),
                "health_risk": parsed_json.get("health_risk", "Assessment pending"),
                "environmental_impact": parsed_json.get("environmental_impact", "Assessment pending"),
                "urgency_factors": parsed_json.get("urgency_factors", []),
                "method": "llm-based"
            }
        else:
            # Fallback to rule-based
            return estimate_severity_rule_based(classification)
            
    except Exception as e:
        # Fallback to rule-based on any error
        result = estimate_severity_rule_based(classification)
        result["llm_error"] = str(e)
        return result


def estimate_severity(
    classification: Dict[str, Any],
    location: str = "",
    use_llm: bool = True
) -> Dict[str, Any]:
    """
    Main function to estimate severity
    
    Args:
        classification: Waste classification result
        location: Location of the waste
        use_llm: Whether to use LLM (defaults to True, falls back to rules)
        
    Returns:
        Severity assessment dict
    """
    if use_llm:
        return estimate_severity_with_llm(classification, location)
    else:
        return estimate_severity_rule_based(classification)
