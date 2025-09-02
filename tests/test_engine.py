"""
Basic tests for the command engine.
"""
def test_preprocess():
    from engine.preprocessor import preprocess_input
    assert preprocess_input('  Hello  ') == 'hello'
