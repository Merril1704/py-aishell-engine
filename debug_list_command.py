"""
Test the specific command that's not working correctly
"""
from engine.executor import CommandEngine
from engine.preprocessor import parse_nl_components
from engine.mapper import map_nl_to_command

def debug_command():
    user_input = "show me the files in games folder in d drive"
    
    print(f"User Input: '{user_input}'")
    print("=" * 50)
    
    # Step 1: Parse components
    components = parse_nl_components(user_input)
    print("Parsed Components:")
    for key, value in components.items():
        if value:
            print(f"  {key}: {value}")
    
    # Step 2: Generate command
    command = map_nl_to_command(user_input, components)
    print(f"\nGenerated Command: {command}")
    
    # Step 3: Execute
    engine = CommandEngine()
    success, output, error = engine.process_input(user_input)
    
    print(f"\nExecution Results:")
    print(f"Success: {success}")
    if output:
        print(f"Output: {output[:200]}...")
    if error:
        print(f"Error: {error}")
    
    engine.cleanup()

if __name__ == "__main__":
    debug_command()
