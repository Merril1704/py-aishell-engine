"""
Safety net and command validation logic.
"""
def is_safe_command(command):
    # Dummy safety check
    return not command.startswith('rm -rf')
