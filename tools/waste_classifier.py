"""
Waste Classifier Tool
Uses NVIDIA Nemotron VLM to classify waste types from images
"""

from typing import Dict, Any
from utils.helpers import call_nemotron_vlm, extract_text_from_response, parse_json_from_text


# Waste categories
WASTE_CATEGORIES = [
    "Plastic waste",
    "Organic waste",
    "Electronic waste (e-waste)",
    "Metal waste",
    "Glass waste",
    "Paper/Cardboard waste",
    "Textile waste",
    "Hazardous waste (chemicals, batteries, etc.)",
    "Construction debris",
    "General litter/mixed waste",
    "Water pollution (oil, sewage, etc.)",
    "Air pollution (smoke, emissions)",
    "Other"
]


def classify_waste(image_base64: str) -> Dict[str, Any]:
    """
    Classify waste type from an image using Nemotron VLM
    
    Args:
        image_base64: Base64 encoded image of waste/pollution
        
    Returns:
        Dict containing:
        - waste_type: Primary waste category
        - confidence: Confidence level (high/medium/low)
        - description: Detailed description of what's visible
        - tags: List of relevant tags
    """
    
    # Construct prompt for waste classification
    prompt = f"""Analyze this image and identify the type of waste or pollution visible.

Possible categories:
{chr(10).join(f"- {cat}" for cat in WASTE_CATEGORIES)}

Provide your analysis in the following JSON format:
{{
    "waste_type": "primary category from the list above",
    "confidence": "high/medium/low",
    "description": "detailed description of what you see (50-100 words)",
    "tags": ["relevant", "tags", "here"],
    "visible_items": ["specific items you can identify"]
}}

Be specific and objective. Focus on observable facts."""

    try:
        # Call Nemotron VLM
        response = call_nemotron_vlm(
            image_base64=image_base64,
            prompt=prompt,
            model="nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
            temperature=0.2,
            max_tokens=1024
        )
        
        # Extract text from response
        text_response = extract_text_from_response(response)
        
        if text_response.startswith("ERROR:"):
            return _create_fallback_classification(text_response)
        
        # Try to parse JSON
        parsed_json = parse_json_from_text(text_response)
        
        if parsed_json and all(k in parsed_json for k in ["waste_type", "confidence", "description"]):
            # Ensure all required fields exist
            result = {
                "waste_type": parsed_json.get("waste_type", "Unknown"),
                "confidence": parsed_json.get("confidence", "low"),
                "description": parsed_json.get("description", ""),
                "tags": parsed_json.get("tags", []),
                "visible_items": parsed_json.get("visible_items", []),
                "raw_response": text_response
            }
            return result
        else:
            # Fallback: use text response directly
            return {
                "waste_type": "General litter/mixed waste",
                "confidence": "low",
                "description": text_response,
                "tags": [],
                "visible_items": [],
                "raw_response": text_response
            }
            
    except Exception as e:
        return _create_fallback_classification(f"Exception during classification: {str(e)}")


def _create_fallback_classification(error_msg: str) -> Dict[str, Any]:
    """
    Create a fallback classification result when VLM fails
    
    Args:
        error_msg: Error message
        
    Returns:
        Fallback classification dict
    """
    return {
        "waste_type": "Unknown - Classification Failed",
        "confidence": "low",
        "description": "Unable to classify waste due to an error. Please try again or provide a clearer image.",
        "tags": ["error", "unclassified"],
        "visible_items": [],
        "raw_response": error_msg,
        "error": True
    }


def get_waste_categories() -> list:
    """Return list of supported waste categories"""
    return WASTE_CATEGORIES.copy()
