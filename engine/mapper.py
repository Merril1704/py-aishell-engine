"""
Maps natural language to shell/system commands using intelligent parsing.
"""
import platform
import re
import os

def map_nl_to_command(nl_input, components=None):
    """
    Map natural language input to system commands using parsed components
    Supports both Windows and Unix-like systems
    """
    if not nl_input:
        return nl_input
    
    # Determine OS for appropriate command mapping
    is_windows = platform.system().lower() == 'windows'
    
    # If components not provided, do basic parsing
    if not components:
        components = parse_basic_components(nl_input)
    
    # Handle different actions based on parsed components
    action = components.get('action')
    target = components.get('target')
    drive = components.get('drive')
    filename = components.get('filename')
    destination = components.get('destination')
    
    # Navigation commands
    if action == 'navigate':
        return build_navigation_command(target, drive, is_windows)
    
    # List/Display commands
    elif action == 'list':
        return build_list_command(target, drive, is_windows)
    
    # Create commands
    elif action == 'create':
        return build_create_command(target, filename, drive, is_windows)
    
    # Delete commands
    elif action == 'delete':
        return build_delete_command(target, filename, is_windows)
    
    # Copy commands
    elif action == 'copy':
        return build_copy_command(target or filename, destination, is_windows)
    
    # Move commands
    elif action == 'move':
        return build_move_command(target or filename, destination, is_windows)
    
    # Find commands
    elif action == 'find':
        return build_find_command(target or filename, drive, is_windows)
    
    # Read/View commands
    elif action == 'read':
        return build_read_command(target or filename, is_windows)
    
    # Run/Execute commands
    elif action == 'run':
        return build_run_command(target or filename)
    
    # Fallback to legacy pattern matching
    return legacy_pattern_matching(nl_input, is_windows)

def build_navigation_command(target, drive, is_windows):
    """Build navigation command (cd) with intelligent path construction"""
    if not target and not drive:
        return 'cd'  # Show current directory
    
    path_parts = []
    
    # Add drive if specified
    if drive:
        path_parts.append(drive)
        if not target:
            # Just go to drive root
            return f'cd /d {drive}\\' if is_windows else f'cd {drive}'
    
    # Add target folder/path
    if target:
        # Handle spaces in folder names
        if ' ' in target:
            target = f'"{target}"'
        path_parts.append(target)
    
    # Construct full path
    if is_windows:
        if drive:
            full_path = f'{drive}\\{target}' if target else drive + '\\'
            return f'cd /d "{full_path}"'
        else:
            return f'cd {target}' if target else 'cd'
    else:
        full_path = '/'.join(path_parts) if path_parts else '.'
        return f'cd {full_path}'

def build_list_command(target, drive, is_windows):
    """Build list/display command with path awareness"""
    path_parts = []
    
    # Add drive if specified
    if drive:
        path_parts.append(drive)
    
    # Add target folder if specified
    if target:
        if ' ' in target:
            target = f'"{target}"'
        path_parts.append(target)
    
    # Construct command
    if is_windows:
        if path_parts:
            if drive:
                full_path = f'{drive}\\{target}' if target else drive + '\\'
                return f'dir "{full_path}"'
            else:
                return f'dir {target}'
        else:
            return 'dir'
    else:
        if path_parts:
            full_path = '/'.join(path_parts)
            return f'ls -la "{full_path}"'
        else:
            return 'ls -la'

def build_create_command(target, filename, drive, is_windows):
    """Build create command for files or directories"""
    if filename:
        # Create file
        name = filename
    elif target:
        # Create directory
        name = target
    else:
        return 'echo "Please specify what to create"'
    
    # Handle spaces in names
    if ' ' in name:
        name = f'"{name}"'
    
    # Add drive prefix if specified
    if drive and is_windows:
        name = f'{drive}\\{name}' if not name.startswith('"') else f'{drive}\\{name[1:-1]}'
        name = f'"{name}"'
    
    # Determine if creating file or directory
    if filename or '.' in (target or ''):
        # Creating a file
        return f'type nul > {name}' if is_windows else f'touch {name}'
    else:
        # Creating a directory
        return f'mkdir {name}'

def build_delete_command(target, filename, is_windows):
    """Build delete command for files or directories"""
    item = filename or target
    if not item:
        return 'echo "Please specify what to delete"'
    
    # Handle spaces
    if ' ' in item:
        item = f'"{item}"'
    
    return f'del {item}' if is_windows else f'rm {item}'

def build_copy_command(source, destination, is_windows):
    """Build copy command"""
    if not source:
        return 'echo "Please specify source file"'
    if not destination:
        return 'echo "Please specify destination"'
    
    # Handle spaces
    if ' ' in source:
        source = f'"{source}"'
    if ' ' in destination:
        destination = f'"{destination}"'
    
    return f'copy {source} {destination}' if is_windows else f'cp {source} {destination}'

def build_move_command(source, destination, is_windows):
    """Build move command"""
    if not source:
        return 'echo "Please specify source"'
    if not destination:
        return 'echo "Please specify destination"'
    
    # Handle spaces
    if ' ' in source:
        source = f'"{source}"'
    if ' ' in destination:
        destination = f'"{destination}"'
    
    return f'move {source} {destination}' if is_windows else f'mv {source} {destination}'

def build_find_command(target, drive, is_windows):
    """Build find command"""
    if not target:
        return f'dir /s' if is_windows else 'find .'
    
    # Handle spaces
    search_term = target
    if ' ' in search_term:
        search_term = f'"{search_term}"'
    
    if is_windows:
        if drive:
            return f'dir {drive}\\*{target}* /s'
        else:
            return f'dir *{target}* /s'
    else:
        return f'find . -name "*{target}*"'

def build_read_command(target, is_windows):
    """Build read/view file command"""
    if not target:
        return 'echo "Please specify file to read"'
    
    # Handle spaces
    if ' ' in target:
        target = f'"{target}"'
    
    return f'type {target}' if is_windows else f'cat {target}'

def build_run_command(target):
    """Build run/execute command"""
    if not target:
        return 'echo "Please specify what to run"'
    
    # Handle spaces
    if ' ' in target:
        target = f'"{target}"'
    
    return target

def parse_basic_components(nl_input):
    """Basic component parsing for fallback"""
    components = {'action': None, 'target': None, 'drive': None}
    
    text_lower = nl_input.lower()
    
    # Basic action detection
    if any(word in text_lower for word in ['go', 'navigate', 'cd']):
        components['action'] = 'navigate'
    elif any(word in text_lower for word in ['list', 'show', 'dir', 'ls']):
        components['action'] = 'list'
    elif any(word in text_lower for word in ['create', 'make', 'mkdir']):
        components['action'] = 'create'
    
    return components

def legacy_pattern_matching(nl_input, is_windows):
    """Legacy pattern matching for backward compatibility"""
    nl_lower = nl_input.lower().strip()
    
    # File listing commands
    if re.search(r'\b(list|show|display)\b.*\b(files?|contents?|directory|folder)\b', nl_lower):
        return 'dir' if is_windows else 'ls -la'
    
    # Process management
    if re.search(r'\b(show|list)\b.*\b(process|processes|running)\b', nl_lower):
        return 'tasklist' if is_windows else 'ps aux'
    
    # System information
    if re.search(r'\b(system info|computer info|hardware)\b', nl_lower):
        return 'systeminfo' if is_windows else 'uname -a'
    
    # If no mapping found, return original input
    return nl_input

def get_command_aliases():
    """
    Return common aliases for commands
    """
    return {
        'ls': 'list files',
        'll': 'list files detailed',
        'pwd': 'show current directory',
        'mkdir': 'create directory',
        'rmdir': 'remove directory',
        'cp': 'copy file',
        'mv': 'move file',
        'cat': 'show file content',
        'grep': 'search in files',
        'ps': 'show processes',
        'kill': 'terminate process',
        'ping': 'test network connection',
        'df': 'show disk usage',
    }
