from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
items = [
    {"id": 1, "name": "Pen", "quantity": 10, "price": 15.5},
    {"id": 2, "name": "Book", "quantity": 5, "price": 120.0},
    {"id": 3, "name": "Pencil", "quantity": 20, "price": 10.0}
]

# GET /api/items - Retrieve all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items)


# GET /api/items/<id> - Retrieve one item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


# POST /api/items - Create a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()

    # Validation
    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or quantity is None or price is None:
        return jsonify({"error": "Missing required fields: name, quantity, price"}), 400
    if not isinstance(quantity, int) or quantity < 0:
        return jsonify({"error": "Quantity must be an integer"}), 400
    if not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a number"}), 400

    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": name,
        "quantity": quantity,
        "price": price
    }

    items.append(new_item)
    return jsonify(new_item), 201


# PUT /api/items/<id> - Update existing item (no partial updates required)
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in items if item["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or quantity is None or price is None:
        return jsonify({"error": "Missing required fields: name, quantity, price"}), 400
    if not isinstance(quantity, int) or quantity < 0:
        return jsonify({"error": "Quantity must be an integer"}), 400
    if not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Price must be a number"}), 400

    item["name"] = name
    item["quantity"] = quantity
    item["price"] = price

    return jsonify(item)


# DELETE /api/items/<id> – Not required, but useful for testing
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
