from app import app

from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Delete all rows in tables
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()
    
    # Add Restaurants
    r1 = Restaurant(name='Pizza Palace', address='123 Main St')
    r2 = Restaurant(name='Pasta House', address='456 Elm St')
    db.session.add_all([r1, r2])
    db.session.commit()
    
    # Add Pizzas
    p1 = Pizza(name='Margherita', ingredients='Tomato, Mozzarella, Basil')
    p2 = Pizza(name='Pepperoni', ingredients='Onions, Cheddar, Pepperoni')
    p3 = Pizza(name='Vegetarian', ingredients='Tomato, Cottage, Vegetables')
    db.session.add_all([p1, p2, p3])
    db.session.commit()
    
    # Add Restaurant Pizzas
    rp1 = RestaurantPizza(price=10.99, pizza=p1, restaurant=r1)
    rp2 = RestaurantPizza(price=12.99, pizza=p2, restaurant=r1)
    rp3 = RestaurantPizza(price=11.99, pizza=p3, restaurant=r2)
    db.session.add_all([rp1, rp2, rp3])
    db.session.commit()