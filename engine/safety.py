"""
Safety net and command validation logic.
"""
import re
import os

# Risky commands that require confirmation
RISKY_COMMANDS = {
    'windows': [
        'del', 'erase', 'rmdir', 'rd', 'format', 'fdisk', 'diskpart',
        'reg delete', 'taskkill', 'shutdown', 'restart'
    ],
    'unix': [
        'rm', 'rmdir', 'mv', 'dd', 'mkfs', 'fdisk', 'kill', 'killall',
        'shutdown', 'reboot', 'halt', 'init', 'chmod 777'
    ]
}

# Protected paths that should never be deleted
PROTECTED_PATHS = [
    '/', '/bin', '/boot', '/dev', '/etc', '/lib', '/proc', '/root', '/sbin', '/sys', '/usr', '/var',
    'C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)', 'C:\\System32'
]

def is_safe_command(command):
    """
    Check if a command is safe to execute
    Returns: (is_safe, risk_level, message)
    """
    if not command:
        return True, 'safe', ''
    
    command_lower = command.lower().strip()
    
    # Check for extremely dangerous commands
    if is_extremely_dangerous(command_lower):
        return False, 'critical', f'CRITICAL: Command "{command}" is extremely dangerous and blocked.'
    
    # Check for risky commands that need confirmation
    if is_risky_command(command_lower):
        return False, 'high', f'WARNING: "{command}" is a risky operation. Confirmation required.'
    
    # Check for protected paths
    if targets_protected_path(command):
        return False, 'high', f'WARNING: Command targets protected system paths. Confirmation required.'
    
    return True, 'safe', ''

def is_extremely_dangerous(command):
    """Check for extremely dangerous commands that should be blocked"""
    dangerous_patterns = [
        r'rm\s+-rf\s+/',
        r'rm\s+-rf\s+\*',
        r'del\s+/s\s+/q\s+c:\\',
        r'format\s+c:',
        r'dd\s+if=.*\s+of=/dev/',
        r':\(\)\{\s*:\|\:&\s*\};\:',  # Fork bomb
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def is_risky_command(command):
    """Check if command contains risky operations"""
    import platform
    
    os_type = 'windows' if platform.system().lower() == 'windows' else 'unix'
    risky_cmds = RISKY_COMMANDS.get(os_type, [])
    
    # Skip cd commands - navigation should be safe
    if command.lower().startswith('cd ') or command.lower().startswith('cd /d'):
        return False
    
    # Skip dir and ls commands - listing should be safe
    if command.lower().startswith('dir ') or command.lower().startswith('ls '):
        return False
    
    # Skip mkdir commands - creating directories should be safe
    if command.lower().startswith('mkdir '):
        return False
    
    for risky_cmd in risky_cmds:
        if command.startswith(risky_cmd.lower()):
            return True
    
    # Check for wildcards with delete operations
    if re.search(r'(rm|del).*\*', command, re.IGNORECASE):
        return True
    
    return False

def targets_protected_path(command):
    """Check if command targets protected system paths"""
    # Only check for delete/remove operations, not navigation
    if not re.search(r'\b(del|rm|rmdir|rd|erase|delete)\b', command, re.IGNORECASE):
        return False
        
    for protected_path in PROTECTED_PATHS:
        if protected_path.lower() in command.lower():
            return True
    return False

def validate_path_exists(path):
    """Validate that a path exists"""
    return os.path.exists(path)

def get_confirmation_prompt(command, risk_level):
    """Generate appropriate confirmation prompt based on risk level"""
    if risk_level == 'critical':
        return f"CRITICAL OPERATION BLOCKED: {command}"
    elif risk_level == 'high':
        return f"Are you sure you want to execute '{command}'? This operation cannot be undone. (yes/no): "
    else:
        return f"Confirm execution of '{command}' (y/n): "
