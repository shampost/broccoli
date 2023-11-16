
class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.parser_token = []

    # TODO: Create the inital ingestion for tokens
    def ingest():
        pass

    def parse():
        pass
    
    def expr():
        pass
    
    # ? Should this method perform token recovery in case there a missing token? Is that possible?
    def error():
        raise Exception('Invalid Syntax')