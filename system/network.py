"""
Networking utilities.
"""
def ping(host):
    import os
    return os.system(f'ping {host}')
