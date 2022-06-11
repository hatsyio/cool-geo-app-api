class QueryLoader:
    @staticmethod
    def load_query(filename) -> str:
        with open("app/database/queries/" + filename) as f:
            return f.read()
