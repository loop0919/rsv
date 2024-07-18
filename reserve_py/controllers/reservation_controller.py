from datetime import date as dt

from .utils import close_connection, get_connection, load_json


def get_all_teachers():
    return load_json('teachers')


def get_all_subjects():
    return load_json('subjects')


def get_all_rooms():
    return load_json('rooms')


def get_all_periods():
    return load_json('periods')


def get_teacher_by_id(teacher_id):
    return get_all_teachers().get(teacher_id)


def get_subject_by_id(subject_id):
    return get_all_subjects().get(subject_id)


def get_room_by_id(room_id):
    return get_all_rooms().get(room_id)


def get_period_by_id(period_id):
    return get_all_periods().get(period_id)

def get_schedules_by_date(date):
    conn = get_connection()
    plain_schedules = conn.execute("SELECT * FROM reservations WHERE date = ?", (date,)).fetchall()
    close_connection(conn)
    
    schedules = {
        (schedule['room'], schedule['period']): {
            'room_id': schedule['room'],
            'period_id': schedule['period'],
            'teacher_name': get_teacher_by_id(schedule['teacher']).get('name'),
            'subject_name': get_subject_by_id(schedule['subject']).get('name')
        } for schedule in plain_schedules
    }
    
    return schedules


def get_today_str():
    return str(dt.today())


def save_reservation(data):
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


def get_schedule_by_date_room_period(date, room_id, period_id):
    conn = get_connection()
    schedule = conn.execute(
        "SELECT * FROM reservations WHERE date = ? AND room = ? AND period = ?",
        (date, room_id, period_id)).fetchone()
    close_connection(conn)
    
    return schedule
