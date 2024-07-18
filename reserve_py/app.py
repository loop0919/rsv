import json
import sqlite3
from datetime import date as dt
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from reserve_py import app, db

db.create_reservation_table()


# dict_factoryの定義
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.errorhandler(400)
def error_400(error):
    return render_template('error/400.html')


@app.errorhandler(404) # 404エラーが発生した場合の処理
def error_404(error):
    return render_template('error/404.html')


@app.route('/list/<date>')
def list(date):
    f_teachers = open(Path('./json/teachers.json'), mode="r")
    f_subjects = open(Path('./json/subjects.json'), mode="r")
    f_rooms = open(Path('./json/rooms.json'), mode="r")
    f_periods = open(Path('./json/periods.json'), mode="r")
    
    teachers = json.load(f_teachers)
    subjects = json.load(f_subjects)
    rooms = json.load(f_rooms)
    periods = json.load(f_periods)
    
    conn = sqlite3.connect(db.DATABASE)
    conn.row_factory = dict_factory
    schedules = conn.execute("SELECT * FROM reservations WHERE date = ?", (date,)).fetchall()
    
    schedules_dict = dict()
    for schedule in schedules:
        arranged = {
            'room_id': schedule['room'],
            'period_id': schedule['period'],
            'teacher_name': teachers[schedule['teacher']]['name'],
            'subject_name': subjects[schedule['subject']]['name']
        }
        schedules_dict[(schedule['room'], schedule['period'])] = arranged
    
    conn.close()
    
    f_subjects.close()
    f_subjects.close()
    f_rooms.close()
    f_periods.close()
    
    return render_template('list.html', date=date, rooms=rooms, periods=periods, schedules_dict=schedules_dict)


@app.route('/list', methods=['GET'])
def list_default():
    return list(str(dt.today()))


@app.route('/apply/', methods=['GET'])
def apply():
    f_teachers = open(Path('./json/teachers.json'), mode='r')
    f_subjects = open(Path('./json/subjects.json'), mode='r')
    f_rooms = open(Path('./json/rooms.json'), mode="r")
    f_periods = open(Path('./json/periods.json'), mode="r")

    try:
        date = request.args["date"]
        room_id = request.args["room_id"]
        period_id = request.args["period_id"]
    
        teachers = json.load(f_teachers)
        subjects = json.load(f_subjects)
        room = json.load(f_rooms)[room_id]
        period = json.load(f_periods)[period_id]
    
    except TypeError as e:
        return error_400(e)
    
    except KeyError as e:
        return error_400(e)
    
    finally:
        f_teachers.close()
        f_subjects.close()
        f_rooms.close()
        f_periods.close()
    
    return render_template(
        'apply.html', 
        
        date=date,
        teachers=teachers, 
        subjects=subjects, 
        room=room,
        period=period,
    )


@app.route('/apply', methods=['POST'])
def apply_post():
    teacher = request.form['teacher']
    date = request.form['date']
    period = request.form['period']
    room = request.form['room']
    subject = request.form['subject']
    people = request.form['people']
    comment = request.form['comment']
    
    conn = sqlite3.connect(db.DATABASE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservations(teacher, date, period, room, subject, people, comment)
        VALUES(?, ?, ?, ?, ?, ?, ?);
    """,
    (teacher, date, period, room, subject, people, comment)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for("list", date=date))


@app.route("/detail/", methods=["GET"])
def detail():
    f_teachers = open(Path('./json/teachers.json'), mode='r')
    f_subjects = open(Path('./json/subjects.json'), mode='r')
    f_rooms = open(Path('./json/rooms.json'), mode="r")
    f_periods = open(Path('./json/periods.json'), mode="r")

    try:
        date = request.args["date"]
        room_id = request.args["room_id"]
        period_id = request.args["period_id"]

        teachers = json.load(f_teachers)
        subjects = json.load(f_subjects)
        room = json.load(f_rooms)[room_id]
        period = json.load(f_periods)[period_id]

        conn = sqlite3.connect(db.DATABASE)
        conn.row_factory = dict_factory
        schedule = conn.execute(
            "SELECT * FROM reservations WHERE date = ? AND room = ? AND period = ?", 
            (date, room_id, period_id)).fetchone()
        
        teacher = teachers[schedule['teacher']]
        subject = subjects[schedule['subject']]
        people = schedule['people']
        comment = schedule['comment']
        
        conn.close()
    
    except TypeError as e:
        return error_400(e)
    
    except KeyError as e:
        return error_400(e)
    
    finally:
        f_teachers.close()
        f_subjects.close()
        f_rooms.close()
        f_periods.close()
    
    return render_template(
        'detail.html', 
        
        date=date,
        teacher=teacher, 
        subject=subject, 
        room=room,
        period=period,
        people=people,
        comment=comment
    )

if __name__ == '__main__':
    app.run()

