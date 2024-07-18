from flask import Flask

from reserve_py import db
from views.errors import register_error_handlers
from views.reservations import reservation_bp

app = Flask(__name__)
app.register_blueprint(reservation_bp)

db.create_reservation_table()

register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
