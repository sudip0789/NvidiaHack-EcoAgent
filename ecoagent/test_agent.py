"""
Test script for EcoAgent
Demonstrates basic functionality without requiring an actual image
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_environment():
    """Test if environment is properly configured"""
    print("="*60)
    print("EcoAgent Environment Test")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("NVIDIA_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✅ NVIDIA_API_KEY found")
        print(f"   Key preview: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ NVIDIA_API_KEY not configured properly")
        print("   Please update your .env file")
        return False
    
    print()
    
    # Test imports
    print("Testing imports...")
    try:
        from eco_agent import EcoAgent
        print("✅ eco_agent module")
    except ImportError as e:
        print(f"❌ Failed to import eco_agent: {e}")
        return False
    
    try:
        from tools import classify_waste, estimate_severity, generate_civic_report
        print("✅ tools module")
    except ImportError as e:
        print(f"❌ Failed to import tools: {e}")
        return False
    
    try:
        from utils import helpers
        print("✅ utils module")
    except ImportError as e:
        print(f"❌ Failed to import utils: {e}")
        return False
    
    print()
    
    # Test agent initialization
    print("Testing EcoAgent initialization...")
    try:
        agent = EcoAgent(verbose=False)
        print("✅ EcoAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize EcoAgent: {e}")
        return False
    
    print()
    print("="*60)
    print("✅ All tests passed!")
    print("="*60)
    print()
    print("You're ready to use EcoAgent!")
    print()
    print("To start the web interface, run:")
    print("  streamlit run ui/dashboard.py")
    print()
    print("To use the CLI, run:")
    print("  python eco_agent.py <image_path> <location>")
    print()
    
    return True


def test_waste_categories():
    """Display supported waste categories"""
    from tools.waste_classifier import get_waste_categories
    
    print("="*60)
    print("Supported Waste Categories")
    print("="*60)
    
    categories = get_waste_categories()
    for i, category in enumerate(categories, 1):
        print(f"{i:2d}. {category}")
    
    print()


def test_severity_levels():
    """Display severity level information"""
    from tools.severity_estimator import SEVERITY_LEVELS
    
    print("="*60)
    print("Severity Levels")
    print("="*60)
    
    for level, info in SEVERITY_LEVELS.items():
        print(f"\n{level.upper()} (Score: {info['level']})")
        print(f"  Description: {info['description']}")
        print(f"  Response Time: {info['response_time']}")
    
    print()


def main():
    """Run all tests"""
    print("\n🧪 EcoAgent Test Suite\n")
    
    # Test environment
    if not test_environment():
        print("\n⚠️  Please fix the issues above before proceeding.\n")
        return
    
    # Display additional info
    print("\n" + "="*60)
    print("Additional Information")
    print("="*60 + "\n")
    
    test_waste_categories()
    test_severity_levels()
    
    print("="*60)
    print("Test suite completed!")
    print("="*60)


if __name__ == "__main__":
    main()
