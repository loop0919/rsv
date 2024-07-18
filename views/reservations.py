from datetime import date as dt

from flask import Blueprint, redirect, render_template, request, url_for

from .utils import close_connection, get_connection, load_json

reservation_bp = Blueprint('reservations', __name__)


@reservation_bp.route('/list/<date>')
def list_reservations(date):
    teachers = load_json('teachers')
    subjects = load_json('subjects')
    rooms = load_json('rooms')
    periods = load_json('periods')

    conn = get_connection()
    schedules = conn.execute("SELECT * FROM reservations WHERE date = ?", (date,)).fetchall()
    close_connection(conn)

    schedules_dict = {
        (schedule['room'], schedule['period']): {
            'room_id': schedule['room'],
            'period_id': schedule['period'],
            'teacher_name': teachers[schedule['teacher']]['name'],
            'subject_name': subjects[schedule['subject']]['name']
        } for schedule in schedules
    }
    
    return render_template(
        'list.html', 
        date=date, 
        rooms=rooms, 
        periods=periods, 
        schedules_dict=schedules_dict
    )


@reservation_bp.route('/list/', methods=['GET'])
def list_default():
    return list_reservations(str(dt.today()))


@reservation_bp.route('/apply', methods=['GET'])
def apply():
    date = request.args.get("date")
    room_id = request.args.get("room_id")
    period_id = request.args.get("period_id")

    if not date or not room_id or not period_id:
        return render_template('error/400.html'), 400

    teachers = load_json('teachers')
    subjects = load_json('subjects')
    rooms = load_json('rooms')
    periods = load_json('periods')

    return render_template(
        'apply.html',
        date=date,
        teachers=teachers,
        subjects=subjects,
        room=rooms[room_id],
        period=periods[period_id],
    )


@reservation_bp.route('/apply', methods=['POST'])
def apply_post():
    data = request.form
    teacher = data['teacher']
    date = data['date']
    period = data['period']
    room = data['room']
    subject = data['subject']
    people = data['people']
    comment = data['comment']

    conn = get_connection()
    conn.execute("""
        INSERT INTO reservations (teacher, date, period, room, subject, people, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (teacher, date, period, room, subject, people, comment))
    conn.commit()
    close_connection(conn)
    
    return redirect(url_for("reservations.list_reservations", date=date))


@reservation_bp.route("/detail/", methods=["GET"])
def detail():
    date = request.args.get("date")
    room_id = request.args.get("room_id")
    period_id = request.args.get("period_id")

    if not date or not room_id or not period_id:
        return render_template('error/400.html'), 400

    teachers = load_json('teachers')
    subjects = load_json('subjects')
    rooms = load_json('rooms')
    periods = load_json('periods')

    conn = get_connection()
    schedule = conn.execute(
        "SELECT * FROM reservations WHERE date = ? AND room = ? AND period = ?",
        (date, room_id, period_id)).fetchone()
    close_connection(conn)

    if not schedule:
        return render_template('error/404.html'), 404

    return render_template(
        'detail.html',
        date=date,
        teacher=teachers[schedule['teacher']],
        subject=subjects[schedule['subject']],
        room=rooms[room_id],
        period=periods[period_id],
        people=schedule['people'],
        comment=schedule['comment']
    )
