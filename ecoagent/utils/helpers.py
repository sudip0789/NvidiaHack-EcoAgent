"""
NVIDIA API Helper Functions
Handles all API calls to NVIDIA Nemotron models
"""

import os
import json
import base64
import requests
from typing import Dict, Any, Optional
from io import BytesIO
from PIL import Image


def get_nvidia_api_key() -> str:
    """Get NVIDIA API key from environment variables"""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not found in environment variables")
    return api_key


def encode_image_to_base64(image_path_or_bytes) -> str:
    """
    Encode an image to base64 string
    
    Args:
        image_path_or_bytes: Either a file path (str) or image bytes
        
    Returns:
        Base64 encoded string of the image
    """
    try:
        if isinstance(image_path_or_bytes, str):
            # It's a file path
            with open(image_path_or_bytes, "rb") as img_file:
                image_bytes = img_file.read()
        else:
            # It's already bytes (e.g., from Streamlit upload)
            image_bytes = image_path_or_bytes
        
        # Optionally resize large images to reduce token usage
        img = Image.open(BytesIO(image_bytes))
        
        # Resize if too large (max dimension 1024px)
        max_size = 1024
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            buffer = BytesIO()
            img.save(buffer, format=img.format or "JPEG")
            image_bytes = buffer.getvalue()
        
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to encode image: {str(e)}")


def call_nemotron_vlm(
    image_base64: str,
    prompt: str,
    model: str = "nvidia/nemotron-vlm-1.5",
    temperature: float = 0.2,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    Call NVIDIA Nemotron Vision-Language Model
    
    Args:
        image_base64: Base64 encoded image
        prompt: Text prompt for the model
        model: Model identifier
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        
    Returns:
        Dict containing the model response
    """
    api_key = get_nvidia_api_key()
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "message": f"VLM API call failed: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None)
        }


def call_nemotron_llm(
    prompt: str,
    model: str = "nvidia/llama-3_3-nemotron-super-49b-v1_5",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Call NVIDIA Nemotron Language Model
    
    Args:
        prompt: Text prompt for the model
        model: Model identifier
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt
        
    Returns:
        Dict containing the model response
    """
    api_key = get_nvidia_api_key()
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "message": f"LLM API call failed: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None)
        }


def extract_text_from_response(response: Dict[str, Any]) -> str:
    """
    Extract text content from NVIDIA API response
    
    Args:
        response: API response dictionary
        
    Returns:
        Extracted text content or error message
    """
    if response.get("error"):
        return f"ERROR: {response.get('message', 'Unknown error')}"
    
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        return f"ERROR: Failed to parse response - {str(e)}"


def parse_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Attempt to extract and parse JSON from text response
    Handles cases where model outputs markdown code blocks
    
    Args:
        text: Text that may contain JSON
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    try:
        # Try direct JSON parse first
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    import re
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Try to find any JSON-like structure
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None
