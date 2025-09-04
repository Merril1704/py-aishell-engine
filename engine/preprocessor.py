"""
Handles input pre-processing and normalization.
"""
import re
import os

def preprocess_input(user_input):
    """
    Detect mode and normalize input
    Returns: (normalized_input, mode, parsed_components)
    mode: 'direct' for shell commands, 'nl' for natural language
    parsed_components: dict with extracted information
    """
    if not user_input:
        return "", "direct", {}
    
    # Normalize input
    normalized = user_input.strip()
    
    # Parse natural language components
    components = parse_nl_components(normalized)
    
    # Detect mode based on patterns
    mode = detect_input_mode(normalized)
    
    return normalized, mode, components

def parse_nl_components(input_text):
    """
    Extract meaningful components from natural language input
    Returns dict with action, target, location, modifiers, etc.
    """
    components = {
        'action': None,
        'target': None,
        'location': None,
        'drive': None,
        'filename': None,
        'destination': None,
        'modifiers': []
    }
    
    text_lower = input_text.lower()
    
    # Extract drive information - improved pattern
    drive_patterns = [
        r'\bdrive\s+([a-z])\b',
        r'\bon\s+drive\s+([a-z])\b',
        r'\bin\s+drive\s+([a-z])\b'
    ]
    
    for pattern in drive_patterns:
        drive_match = re.search(pattern, text_lower)
        if drive_match:
            components['drive'] = drive_match.group(1).upper() + ':'
            break
    
    # Extract folder/directory names - improved patterns
    folder_patterns = [
        r'\bfolder\s+called\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bfolder\s+named\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bfolder\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bdirectory\s+called\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bdirectory\s+named\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bdirectory\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bto\s+(?:folder\s+)?([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
        r'\bto\s+([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)'
    ]
    
    for pattern in folder_patterns:
        folder_match = re.search(pattern, text_lower)
        if folder_match:
            target = folder_match.group(1).strip()
            # Clean up common words that shouldn't be in target
            target = re.sub(r'\b(in|on|at|from|to)\b.*$', '', target).strip()
            if target and len(target) > 0:
                components['target'] = target
                break
    
    # Extract file names with extensions
    file_patterns = [
        r'\bfile\s+([\w\.-]+\.[\w]{1,4})\b',
        r'\bdocument\s+([\w\.-]+\.[\w]{1,4})\b',
        r'\bnamed\s+([\w\.-]+\.[\w]{1,4})\b',
        r'\bcalled\s+([\w\.-]+\.[\w]{1,4})\b',
        r'\bfile\s+called\s+([\w\.-]+\.[\w]{1,4})\b'
    ]
    
    for pattern in file_patterns:
        file_match = re.search(pattern, text_lower)
        if file_match:
            components['filename'] = file_match.group(1)
            break
    
    # Extract actions with priority order
    action_patterns = [
        (r'\b(go|navigate|change)\s+to\b', 'navigate'),
        (r'\b(cd)\b', 'navigate'),
        (r'\b(list|show|display|see|view)\b.*\b(files?|contents?|directory|folder)\b', 'list'),
        (r'\b(dir|ls)\b', 'list'),
        (r'\b(create|make|new)\b', 'create'),
        (r'\b(mkdir)\b', 'create'),
        (r'\b(delete|remove|erase)\b', 'delete'),
        (r'\b(del|rm)\b', 'delete'),
        (r'\b(copy|duplicate|cp)\b', 'copy'),
        (r'\b(move|relocate|mv)\b', 'move'),
        (r'\b(find|search|locate)\b', 'find'),
        (r'\b(read|open|cat|type)\b', 'read'),
        (r'\b(run|execute|start|launch)\b', 'run')
    ]
    
    for pattern, action in action_patterns:
        if re.search(pattern, text_lower):
            components['action'] = action
            break
    
    # Extract destination for move/copy operations
    if components['action'] in ['copy', 'move']:
        dest_patterns = [
            r'\bto\s+(?:folder\s+)?([\w\s]+?)(?:\s+in\s+drive|\s+on\s+drive|\s*$)',
            r'\binto\s+(?:folder\s+)?([\w\s]+?)(?:\s+in\s+drive|\s*$)',
            r'\bdestination\s+([\w\s]+?)(?:\s*$)'
        ]
        
        for pattern in dest_patterns:
            dest_match = re.search(pattern, text_lower)
            if dest_match:
                dest = dest_match.group(1).strip()
                # Don't use target as destination
                if dest != components.get('target'):
                    components['destination'] = dest
                    break
    
    return components

def detect_input_mode(input_text):
    """
    Detect if input is a direct command or natural language
    """
    # Direct command patterns
    direct_patterns = [
        r'^(cd|ls|dir|mkdir|rmdir|rm|del|cp|copy|mv|move|cat|type|echo|pwd|ps|kill|grep|find|curl|wget)\b',
        r'^[a-zA-Z]:[/\\]',  # Windows path
        r'^[/~]',  # Unix path
        r'^\w+\.(exe|bat|sh|py|js)\b',  # Executable files
        r'^[a-zA-Z_]\w*\s*=',  # Variable assignment
    ]
    
    # Check for direct command patterns
    for pattern in direct_patterns:
        if re.match(pattern, input_text, re.IGNORECASE):
            return 'direct'
    
    # Natural language indicators
    nl_patterns = [
        r'\b(please|can you|could you|help me|i want to|i need to|show me|tell me|go to|navigate to)\b',
        r'\b(what|where|how|why|when)\b',
        r'\b(folder|directory|file|document|drive)\b',
        r'\b(create|delete|remove|list|find|show|display|see|view)\b'
    ]
    
    # Check for natural language patterns
    for pattern in nl_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return 'nl'
    
    # Default to natural language if unclear
    return 'nl'
