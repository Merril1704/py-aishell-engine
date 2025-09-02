"""
OS shell interaction utilities.
"""
def run_shell_command(cmd):
    import subprocess
    return subprocess.getoutput(cmd)
