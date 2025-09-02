"""
File system API utilities.
"""
def list_files(path):
    import os
    return os.listdir(path)
