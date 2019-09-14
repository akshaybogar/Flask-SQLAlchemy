import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('price',
    type = float,
    required = True,
    help = 'Enter price of the item')

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if(ItemModel.find_by_name(name)):
            return {'message':'Item with {} name already exists'.format(name)}, 400

        data = Item.request_parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {'message':'An error occured'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': 'Item with this name does not exist'}
        else:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            delete_query = 'DELETE FROM ITEMS WHERE name=?'
            cursor.execute(delete_query, (name,))
            conn.commit()
            conn.close()
            return {'message':'Item deleted'}

    def put(self, name):
        data = Item.request_parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel(name, data['price'])
        if item is None:
            try:
                update_item.insert()
            except:
                return {'message': 'An error occured while inserting'},500
        else:
            try:
                update_item.update()
            except:
                return {'message':'An error occured while updating'},500

        return update_item.json()


class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = 'SELECT * FROM ITEMS'
        result = cursor.execute(query).fetchall()
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        conn.commit()
        conn.close()

        return {'items':items}
