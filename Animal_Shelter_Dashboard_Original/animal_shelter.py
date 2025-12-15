from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username='aacuser', password='Mongo123', host='nv-desktop-services.apporto.com', port=34532):
        """Initialize MongoDB connection"""
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/?authSource=admin')
        self.database = self.client['AAC']
        self.collection = self.database['animals']

    def create(self, data):
        """Insert a new document into the animals collection"""
        if data is not None:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"Insert Error: {e}")
                return False
        else:
            return False

    def read(self, query):
        """Find documents that match the query"""
        if query is not None:
            try:
                result = list(self.collection.find(query))
                return result
            except Exception as e:
                print(f"Read Error: {e}")
                return []
        else:
            return []
            
    def update(self, query, new_values):
        """Update documents that match the query with new values"""
        if query and new_values:
            try:
                result = self.collection.update_many(query, {"$set": new_values})
                return result.modified_count
            except Exception as e:
                print(f"Update Error: {e}")
                return 0
        return 0

    def delete(self, query):
        """Delete documents that match the query"""
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Delete Error: {e}")
                return 0
        return 0
