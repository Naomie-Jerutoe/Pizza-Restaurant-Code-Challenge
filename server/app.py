from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
  return '<h1>Welcome to Pizza Restaurant</h1>'

@app.route('/restaurants')
def restaurants():
  restaurants = Restaurant.query.all()
  formatted_restaurants = [{
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    } for restaurant in restaurants]
  return jsonify(formatted_restaurants), 200

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
  restaurant = Restaurant.query.filter_by(id=id).first()
  
  if request.method == 'GET':
    if restaurant:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in restaurant.pizzas]
        }
        return jsonify(restaurant_data), 200
    else:
          response_body = {
            "error": "Restaurant not found"
          }
          response = make_response(
            response_body,
            404
          )
          return response
          
  
  elif request.method == 'DELETE':
    db.session.delete(restaurant)
    db.session.commit()
    
    response_body = {}
    response = make_response(
      response_body,
      200
    )
    return response
  
@app.route('/pizzas')
def pizzas():
  pizzas = Pizza.query.all()
  formatted_pizzas = [{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in pizzas]
  return jsonify(formatted_pizzas), 200
  
@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def restaurant_pizzas():
  restaurant_pizzas = RestaurantPizza.query.all()
  
  if request.method == 'GET':
    formatted_restaurant_pizzas = [{
        "price": restaurant_pizza.price,
        "pizza_id": restaurant_pizza.pizza_id,
        "restaurant_id": restaurant_pizza.restaurant_id
    } for restaurant_pizza in restaurant_pizzas]
    return jsonify(formatted_restaurant_pizzas), 200

  elif request.method == 'POST':
    data = request.get_json()
    
    # Check if the provided pizza_id exists in the database
    existing_pizza = Pizza.query.get(data['pizza_id'])
    if existing_pizza is None:
        return make_response({'error': 'Invalid pizza_id'}, 400)

    # Check if the provided restaurant_id exists in the database
    existing_restaurant = Restaurant.query.get(data['restaurant_id'])
    if existing_restaurant is None:
        return make_response({'error': 'Invalid restaurant_id'}, 400)

    # Create the new RestaurantPizza object
    new_restaurant_pizza = RestaurantPizza(
        price=data['price'],
        pizza_id=data['pizza_id'],
        restaurant_id=data['restaurant_id']
    )
    db.session.add(new_restaurant_pizza)
    
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return make_response(
          {"errors": ["validation errors"]},
          500
          )

    # Fetch the related pizza object associated with the newly created restaurant_pizza
    related_pizza = Pizza.query.get(data['pizza_id'])

    response_data = {
        "id": related_pizza.id,
        "name": related_pizza.name,
        "ingredients": related_pizza.ingredients
    }

    return make_response(response_data, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)