import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This Field cannot be left blank')

    @jwt_required()
    def get(self, name):

        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE name = ?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return{"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def post(self, name):

        if self.find_by_name(name):
            return{"message": "Item with name '{}' already Exist".format(name)}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occured while inserting item"}, 500
        return item, 201

    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item Deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error encountered while insertion of item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error encountered while insertion of item"}, 500
        return item


class Itemlist(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        item = []
        for row in result:
            item.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"item": item}, 200
