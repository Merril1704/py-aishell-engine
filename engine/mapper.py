"""
Maps natural language to shell/system commands.
"""
def map_nl_to_command(nl_input):
    # Dummy mapping
    if 'list files' in nl_input:
        return 'dir'
    return nl_input
