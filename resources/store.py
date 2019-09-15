from flask_restful import Resource
from models.store_model import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found'}, 400

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message':'Store with "{}" already exists'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'Error while adding a store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message':'Error occured while deleting the store'}, 500
        return {'message':'Item deleted'}


class StoreList(Resource):
    def get(self):
        return {'Stores':[store.json() for store in StoreModel.query.all()]}
