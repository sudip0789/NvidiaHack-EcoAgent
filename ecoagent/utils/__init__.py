"""
EcoAgent Utilities Package
Contains helper functions for NVIDIA API interactions
"""

from .helpers import (
    get_nvidia_api_key,
    encode_image_to_base64,
    call_nemotron_vlm,
    call_nemotron_llm,
    extract_text_from_response,
    parse_json_from_text
)

__all__ = [
    'get_nvidia_api_key',
    'encode_image_to_base64',
    'call_nemotron_vlm',
    'call_nemotron_llm',
    'extract_text_from_response',
    'parse_json_from_text'
]
