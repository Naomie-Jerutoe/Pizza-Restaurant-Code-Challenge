from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String, nullable=False)
    
    # Relationship mapping the restaurant to related restaurant_pizza
    restaurant_pizzas = db.relationship(
            'RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Restaurant {self.id}, {self.name}, {self.address}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    
    # Relationship mapping the Pizza to related restaurant_pizza
    restaurant_pizzas = db.relationship(
            'RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pizza {self.id}, {self.name}, {self.ingredients}>'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    #Relationship mapping the restaurant_pizza to related restaurant
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    
    #Relationship mapping the restaurant_pizza to related pizza
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    
    def __repr__(self):
        return f'<RestaurantPizza {self.id}, {self.price}, {self.pizza_id}, {self.restaurant_id} >'
    
    __table_args__ = (
        CheckConstraint('price >= 1 AND price <= 30', name='check_price_range'),
    )