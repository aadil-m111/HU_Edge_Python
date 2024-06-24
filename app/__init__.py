from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hashkart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # to start the different extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # to register blueprints (automatically it will take app before .)
    from .auth.routes import auth_bp
    from .product.routes import product_bp
    from .cart.routes import cart_bp
    from .order.routes import order_bp
    from .payment.routes import payment_bp

    # registering the flask app endpoints(flask app blueprints)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(payment_bp, url_prefix='/payments')

    return app

