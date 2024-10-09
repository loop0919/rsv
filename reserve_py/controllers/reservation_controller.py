from flask import Blueprint, redirect, render_template, request, url_for

from reserve_py.services import reservation_service as service

reservation_bp = Blueprint('reservations', __name__)


@reservation_bp.route('/list/<date>')
def list(date):
    disabled = request.args.get("disabled") is not None
    
    if not service.match_date_format(date):
        return render_template('error/400.html'), 400
    return render_template(
        'list.html', 
        date=date,
        rooms=service.get_all_rooms(), 
        periods=service.get_all_periods(), 
        schedules=service.get_schedules_by_date(date),
        disabled=disabled
    )


@reservation_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('reservations.list', date=service.get_today_str()))


@reservation_bp.route('/list/', methods=['GET'])
def list_default():
    return redirect(url_for('reservations.list', date=service.get_today_str()))


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
        teachers=service.get_all_teachers(),
        subjects=service.get_all_subjects(),
        room=service.get_room_by_id(room_id),
        period=service.get_period_by_id(period_id),
        data=dict(),
        errors=[]
    )


@reservation_bp.route('/apply', methods=['POST'])
def apply_post():
    data = request.form
    
    is_valid, error_msg = service.save_reservation(data)
    if is_valid:
        return redirect(url_for("reservations.list", date=data['date']))
    else:
        return render_template(
            'apply.html',
            date=data['date'],
            teachers=service.get_all_teachers(),
            subjects=service.get_all_subjects(),
            room=service.get_room_by_id(data['room']),
            period=service.get_period_by_id(data['period']),
            data=data,
            errors=[error_msg]
        )


@reservation_bp.route("/detail/", methods=["GET"])
def detail():
    date = request.args.get("date")
    room_id = request.args.get("room_id")
    period_id = request.args.get("period_id")

    if not date or not room_id or not period_id:
        return render_template('error/400.html'), 400

    if not service.match_date_format(date):
        return render_template('error/400.html'), 400

    schedule = service.get_schedule_by_date_room_period(date, room_id, period_id)

    if not schedule:
        return render_template('error/404.html'), 404
    
    teacher = service.get_teacher_by_id(schedule['teacher'])
    subject = service.get_subject_by_id(schedule['subject'])
    room = service.get_room_by_id(room_id)
    period = service.get_period_by_id(period_id)
    
    if not teacher or not subject or not room or not period:
        return render_template('error/404.html'), 404
    

    return render_template(
        'detail.html',
        date=date,
        teacher=teacher,
        subject=subject,
        room=room,
        period=period,
        people=schedule['people'],
        comment=schedule['comment']
    )


@reservation_bp.route('/delete', methods=['POST'])
def delete_post():
    data = request.form
    
    service.delete_reservation(data)
    return redirect(url_for("reservations.list", date=data['date']))


@reservation_bp.route('/change_schedule', methods=['GET'])
def change_schedule():
    date = request.args.get("date")

    if not date:
        return render_template('error/400.html'), 400

    return render_template(
        'chenge_schedule.html',
        date=date
    )
