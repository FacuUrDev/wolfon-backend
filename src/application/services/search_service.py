class SearchService:
    def __init__(self, db):
        self.db = db

    def find(self, collection: str, **kwargs):
        results = list(self.db[collection].find(kwargs))
        for i, result in enumerate(results):
            results[i]['_id'] = str(result['_id'])
        return results

    def find_one(self, collection: str, **kwargs):
        results = self.db[collection].find_one(kwargs)
        for i, result in enumerate(results):
            results[i]['_id'] = str(result['_id'])
        return results
