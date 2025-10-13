"""
EcoAgent - Main Orchestrator
Coordinates waste classification, severity estimation, and report generation
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import tools
from tools.waste_classifier import classify_waste
from tools.severity_estimator import estimate_severity
from tools.report_generator import generate_civic_report, format_report_for_display

# Import utilities
from utils.helpers import encode_image_to_base64


class EcoAgent:
    """
    Main EcoAgent class that orchestrates the environmental reporting pipeline
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize EcoAgent
        
        Args:
            verbose: Whether to print detailed status messages
        """
        self.verbose = verbose
        
        # Load environment variables
        load_dotenv()
        
        # Verify API key is present
        if not os.getenv("NVIDIA_API_KEY"):
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
        
        if self.verbose:
            print("✓ EcoAgent initialized successfully")
    
    def analyze_image(
        self,
        image_path_or_bytes,
        location: str = "",
        additional_notes: str = "",
        use_llm_severity: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze an environmental issue from an image
        
        Args:
            image_path_or_bytes: Path to image file or image bytes
            location: Location of the incident
            additional_notes: Additional notes from the reporter
            use_llm_severity: Whether to use LLM for severity estimation
            
        Returns:
            Dict containing full analysis and report
        """
        
        if self.verbose:
            print("\n" + "="*60)
            print("Starting EcoAgent Analysis Pipeline")
            print("="*60)
        
        results = {
            "status": "in_progress",
            "steps": {}
        }
        
        try:
            # Step 1: Encode image
            if self.verbose:
                print("\n[1/4] Encoding image...")
            
            image_base64 = encode_image_to_base64(image_path_or_bytes)
            results["steps"]["encoding"] = {"status": "success"}
            
            if self.verbose:
                print("✓ Image encoded successfully")
            
            # Step 2: Classify waste
            if self.verbose:
                print("\n[2/4] Classifying waste using Nemotron VLM...")
            
            classification = classify_waste(image_base64)
            results["steps"]["classification"] = classification
            
            if self.verbose:
                print(f"✓ Waste classified as: {classification.get('waste_type')}")
                print(f"  Confidence: {classification.get('confidence')}")
            
            # Step 3: Estimate severity
            if self.verbose:
                print("\n[3/4] Estimating severity...")
            
            severity = estimate_severity(
                classification=classification,
                location=location,
                use_llm=use_llm_severity
            )
            results["steps"]["severity"] = severity
            
            if self.verbose:
                print(f"✓ Severity estimated as: {severity.get('severity').upper()}")
                print(f"  Score: {severity.get('severity_score')}/5")
                print(f"  Method: {severity.get('method')}")
            
            # Step 4: Generate report
            if self.verbose:
                print("\n[4/4] Generating civic report using Nemotron LLM...")
            
            report = generate_civic_report(
                classification=classification,
                severity=severity,
                location=location,
                additional_notes=additional_notes
            )
            results["steps"]["report"] = report
            
            if self.verbose:
                print(f"✓ Report generated: {report.get('report_id')}")
            
            # Mark as complete
            results["status"] = "complete"
            results["summary"] = {
                "report_id": report.get("report_id"),
                "waste_type": classification.get("waste_type"),
                "severity": severity.get("severity"),
                "location": location
            }
            
            if self.verbose:
                print("\n" + "="*60)
                print("Analysis Complete!")
                print("="*60)
            
            return results
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            
            if self.verbose:
                print(f"\n✗ Error during analysis: {str(e)}")
            
            return results
    
    def get_formatted_report(self, results: Dict[str, Any]) -> Optional[str]:
        """
        Get formatted report from analysis results
        
        Args:
            results: Results from analyze_image()
            
        Returns:
            Formatted report string or None if no report available
        """
        if results.get("status") != "complete":
            return None
        
        report = results["steps"].get("report")
        if not report:
            return None
        
        return format_report_for_display(report)


def run_ecoagent_cli():
    """
    Command-line interface for EcoAgent
    For testing purposes
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python eco_agent.py <image_path> [location]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    location = sys.argv[2] if len(sys.argv) > 2 else "Unknown location"
    
    print("="*60)
    print("EcoAgent - Environmental Reporting System")
    print("="*60)
    
    # Initialize agent
    agent = EcoAgent(verbose=True)
    
    # Analyze image
    results = agent.analyze_image(
        image_path_or_bytes=image_path,
        location=location
    )
    
    # Print formatted report
    if results.get("status") == "complete":
        print("\n" + agent.get_formatted_report(results))
    else:
        print(f"\n✗ Analysis failed: {results.get('error', 'Unknown error')}")


if __name__ == "__main__":
    run_ecoagent_cli()
