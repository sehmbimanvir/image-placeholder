from flask import Flask
from controllers.misc_controller import misc_controller

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(misc_controller, url_prefix='/api')

if __name__ == '__main__':
    app.run()