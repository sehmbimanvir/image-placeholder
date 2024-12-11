from flask import Flask, jsonify
from controllers.misc_controller import misc_controller
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        'status': 'OK',
        'time': date_time_str
    })

# Register Blueprints
app.register_blueprint(misc_controller, url_prefix='/api')

if __name__ == '__main__':
    app.run()