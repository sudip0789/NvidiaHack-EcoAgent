"""
EcoAgent Tools Package
Contains all analysis tools for waste classification, severity estimation, and report generation
"""

from .waste_classifier import classify_waste, get_waste_categories
from .severity_estimator import estimate_severity
from .report_generator import generate_civic_report, format_report_for_display

__all__ = [
    'classify_waste',
    'get_waste_categories',
    'estimate_severity',
    'generate_civic_report',
    'format_report_for_display'
]
