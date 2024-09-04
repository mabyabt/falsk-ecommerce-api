from flask import Flask, jsonify, request, abort
from models import db, User, Category, Item
from database import create_app

app = create_app()

# Route to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

# Route to create a new category
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    if not data or not 'name' in data:
        abort(400, description="Category name is required.")
    
    new_category = Category(name=data['name'], is_active=data.get('is_active', True))
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify(new_category.to_dict()), 201

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# Route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data or not all(k in data for k in ('name', 'description', 'price', 'category_id')):
        abort(400, description="Missing required fields.")
    
    new_item = Item(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        images=','.join(data.get('images', [])),
        category_id=data['category_id']
    )
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify(new_item.to_dict()), 201

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not all(k in data for k in ('name', 'email')):
        abort(400, description="Missing required fields.")
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        cart=data.get('cart', '')
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

# Route to update a user's cart
@app.route('/users/<int:user_id>/cart', methods=['PUT'])
def update_cart(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found.")
    
    user.cart = data.get('cart', '')
    db.session.commit()
    
    return jsonify(user.to_dict())

# Error handling for common errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True)
