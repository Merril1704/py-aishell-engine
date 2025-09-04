"""
Test GUI integration with Command Engine
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui_integration():
    """Test that GUI can import and use the Command Engine"""
    try:
        # Test Command Engine import
        from engine import CommandEngine
        print("✅ Command Engine imported successfully")
        
        # Test engine functionality
        engine = CommandEngine()
        success, output, error = engine.process_input("list files")
        print(f"✅ Command Engine test: Success={success}")
        
        # Test GUI imports
        try:
            from PyQt5.QtWidgets import QApplication
            print("✅ PyQt5 available")
        except ImportError:
            print("❌ PyQt5 not installed. Run: pip install PyQt5")
            return False
            
        # Test GUI integration
        from gui.window import TerminalWidget, TerminalWindow
        print("✅ GUI components imported successfully")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def run_gui():
    """Run the GUI application"""
    try:
        from gui.window import start_gui
        print("🚀 Starting GUI application...")
        start_gui()
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")

if __name__ == "__main__":
    print("=== GUI Integration Test ===")
    if test_gui_integration():
        response = input("\nWould you like to start the GUI? (y/n): ")
        if response.lower() == 'y':
            run_gui()
    else:
        print("\n❌ Please fix the issues above before running the GUI")
