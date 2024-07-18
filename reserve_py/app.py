from flask import Flask

from reserve_py.routes.errors import register_error_handlers
from reserve_py.routes.reservation_router import reservation_bp

app = Flask(__name__)
app.register_blueprint(reservation_bp)

register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
