from flask import Flask

from reserve_py.controllers.errors import register_error_handlers
from reserve_py.controllers.reservation_controller import reservation_bp

app = Flask(__name__)
app.register_blueprint(reservation_bp)

register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)

