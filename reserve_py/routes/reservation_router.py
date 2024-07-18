from flask import Blueprint, redirect, render_template, request, url_for

from reserve_py.controllers import reservation_controller as controller

reservation_bp = Blueprint('reservations', __name__)


@reservation_bp.route('/list/<date>')
def list(date):
    return render_template(
        'list.html', 
        date=date,
        rooms=controller.get_all_rooms(), 
        periods=controller.get_all_periods(), 
        schedules=controller.get_schedules_by_date(date)
    )


@reservation_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('reservations.list', date=controller.get_today_str()))


@reservation_bp.route('/list/', methods=['GET'])
def list_default():
    return redirect(url_for('reservations.list', date=controller.get_today_str()))


@reservation_bp.route('/apply', methods=['GET'])
def apply():
    date = request.args.get("date")
    room_id = request.args.get("room_id")
    period_id = request.args.get("period_id")

    if not date or not room_id or not period_id:
        return render_template('error/400.html'), 400

    return render_template(
        'apply.html',
        date=date,
        teachers=controller.get_all_teachers(),
        subjects=controller.get_all_subjects(),
        room=controller.get_room_by_id(room_id),
        period=controller.get_period_by_id(period_id),
    )


@reservation_bp.route('/apply', methods=['POST'])
def apply_post():
    data = request.form
    controller.save_reservation(data)
    return redirect(url_for("reservations.list", date=data['date']))


@reservation_bp.route("/detail/", methods=["GET"])
def detail():
    date = request.args.get("date")
    room_id = request.args.get("room_id")
    period_id = request.args.get("period_id")

    if not date or not room_id or not period_id:
        return render_template('error/400.html'), 400

    schedule = controller.get_schedule_by_date_room_period(date, room_id, period_id)

    if not schedule:
        return render_template('error/404.html'), 404

    return render_template(
        'detail.html',
        date=date,
        teacher=controller.get_teacher_by_id(schedule['teacher']),
        subject=controller.get_subject_by_id(schedule['subject']),
        room=controller.get_room_by_id(room_id),
        period=controller.get_period_by_id(period_id),
        people=schedule['people'],
        comment=schedule['comment']
    )
