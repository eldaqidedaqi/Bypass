from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes.main import main_bp
    from app.routes.wda import wda_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(wda_bp)
    
    return app
