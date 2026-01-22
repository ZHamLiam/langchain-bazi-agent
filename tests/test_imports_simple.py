"""Simple test to check if imports work"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    # Test basic imports
    from bazi_calculator.core.calendar import BaziCalendar
    from bazi_calculator.core.wuxing import WuxingAnalyzer
    from bazi_calculator.tools.bazi.time_parser import parse_birth_time
    
    # Test BaziAgent import
    from bazi_calculator.chains.bazi_agent import BaziAgent
    
    print("✓ All imports successful")

if __name__ == "__main__":
    test_imports()
