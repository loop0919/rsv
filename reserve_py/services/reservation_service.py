from datetime import datetime
import pytz
import re

from .utils import close_connection, get_connection, load_json


OTHER_TEACHER = "999"


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


def match_date_format(date):
    if not re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
        return False
    
    year, month, day = map(int, date.split("-"))
    match month:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            return 1 <= day <= 31
        case 4 | 6 | 9 | 11:
            return 1 <= day <= 30
        case 2:
            if year % 400 == 0:
                return 1 <= day <= 29
            elif year % 100 == 0:
                return 1 <= day <= 28
            elif year % 4 == 0:
                return 1 <= day <= 29
            else:
                return 1 <= day <= 28
        case _:
            return False


def get_today_str():
    jst = pytz.timezone('Asia/Tokyo')
    now_jst = datetime.now(jst)
    return str(now_jst.date())


def check_double_booking(teacher, date, period):
    conn = get_connection()
    if teacher == OTHER_TEACHER:
        return False
    else:
        count_booking = conn.execute("SELECT COUNT(*) AS count FROM reservations WHERE teacher = ? AND date = ? AND period = ?", (teacher, date, period)).fetchone()['count']
    
    return count_booking >= 1


def check_over_capacity(people, room_id):
    return int(people) > int(get_room_by_id(room_id)["capacity"])


def save_reservation(data):
    teacher = data['teacher']
    date = data['date']
    period = data['period']
    room = data['room']
    subject = data['subject']
    people = data['people']
    comment = data['comment']
    
    if check_over_capacity(people, room):
        return False, '使用人数が教室の収容人数を超えています！'
    
    if check_double_booking(teacher, date, period):
        return False, 'その教員は既に同じ時間帯に予約が入っています！'
    
    conn = get_connection()
    conn.execute("""
        INSERT INTO reservations (teacher, date, period, room, subject, people, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, 
        (teacher, date, period, room, subject, people, comment)
    )
    conn.commit()
    close_connection(conn)
    
    return True, None


def delete_reservation(data):
    date = data['date']
    period = data['period']
    room = data['room']
    
    conn = get_connection()
    conn.execute("""
        DELETE FROM reservations
        WHERE date = ? AND period = ? AND room = ?
        """,
        (date, period, room)
    )
    conn.commit()
    close_connection(conn)
    
    return True


def get_schedule_by_date_room_period(date, room_id, period_id):
    conn = get_connection()
    schedule = conn.execute(
        "SELECT * FROM reservations WHERE date = ? AND room = ? AND period = ?",
        (date, room_id, period_id)).fetchone()
    close_connection(conn)
    
    return schedule
