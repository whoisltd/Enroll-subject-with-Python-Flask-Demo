from app import app
from app.models import *
from flask import request, render_template, redirect
from flask.helpers import flash, url_for
from flask_wtf import *
from app.forms import createClassForm, createSubjectsForm, loginForm, signUpForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask.wrappers import Response
from app.moduels import admin_required
import datetime
from sqlalchemy import and_, or_
from flask.json import jsonify
import json
# from sqlalchemy.sql.functions import user


@app.route("/")
def index():
    subjects = Subject.query.all()
    return render_template("index.html", subjects=subjects)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_code=form.user_code.data).first()
        check = user.check_password(form.password.data)
        if user is None or not check:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # login_user(passenger, remember=form.remember_me.data)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@ app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """show sign up form"""
    form = signUpForm()
    if form.validate_on_submit():
        user_code = form.user_code.data
        name = form.name.data
        password = form.password.data
        email = form.email.data
        # try:
        newUser = Student(user_code=user_code, name=name,
                          password=password, email=email)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        # except Exception:
        #     db.session.rollback()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template("signup.html", form=form)

# @app.route("/createSubject")
# def createSubjects():
#     return render_template("createSubject.html", form=form)


@app.route("/createSubject", methods=["GET", "POST"])
@admin_required
def createSubject():
    form = createSubjectsForm()
    if form.validate_on_submit():
        name = request.form.get("subject_name")
        lecturers_name = request.form.get("lecturer_name")

        subject = Subject(name=name, lecturers_name=lecturers_name)
        db.session.add(subject)
        db.session.commit()
        flash('Congratulations, you have successfully created subject')
        return redirect(url_for('index'))
    return render_template('createSubject.html', form=form)


@app.route("/createClass", methods=["GET", "POST"])
@admin_required
def createClass():
    form = createClassForm()
    if form.validate_on_submit():
        name = request.form.get("name")
        seats = request.form.get("seats")
        subject_id = request.form.get("subject")
        lesson = request.form.get("lesson")
        lesson_start = request.form.get("lesson_start")
        date_start = request.form.get("date_start")
        date_end = request.form.get("date_end")
        newClass = Class_(name=name, seats=seats, lesson=lesson, lesson_start=lesson_start, date_start=date_start, date_end=date_end, subject_id=subject_id)
        db.session.add(newClass)
        db.session.commit()
        flash('Congratulations, you have successfully created class')
        return redirect(url_for('index'))
    return render_template('createClass.html', form=form)

@app.route("/detailsClass/<int:subject_id>")
def detailsClass(subject_id):
    classes = Class_.query.filter_by(subject_id=subject_id).all()
    return render_template('detailsClass.html', classes=classes)

@app.route("/viewmyClass")
def viewmyClass():
    # classes = db.query.join(Subject).join(Student_Class).join(User)\
    #     .filter(Student_Class.student_id == current_user.id, User.role != 'admin', Subject.id).all()
    q = (db.session.query(Class_, Subject, Student_Class, User)
        .join(Subject)
        .join(Student_Class)
        .join(User)
        .filter(User.id == current_user.id)
        .order_by(Subject.id)
        ).all()
    return render_template("viewmyClass.html", q=q)

@app.route("/chooseClass/<int:class_id>")
def chooseClass(class_id):
    class_ = Class_.query.get(class_id)
    
    student_class = Student_Class(
        class_id=class_id, student_id=current_user.id)
    db.session.add(student_class)
    db.session.commit()
    return render_template("success.html", message="Has successfully sign up class")

@app.route("/editClass/<int:class_id>")
def editClass(class_id):
    form=createClassForm()
    class_ = Class_.query.get(class_id)
    return render_template("editClass.html", class_=class_, form=form)
@app.route("/updateClass/<int:class_id>", methods=['POST'])
def updateClass(class_id):
    form=createClassForm()
    class_ = Class_.query.get(class_id)
    if form.validate_on_submit():
        class_.name = request.form.get("name")
        class_.seats = request.form.get("seats")
        class_.subject_id = request.form.get("subject")
        class_.lesson = request.form.get("lesson")
        class_.lesson_start = request.form.get("lesson_start")
        class_.date_start = request.form.get("date_start")
        class_.date_end = request.form.get("date_end")
        db.session.commit()
        flash('Congratulations, you have successfully edit class')
        return redirect(url_for('index'))
    return render_template("editClass.html", class_=class_, form=form)

@app.route("/deleteClass/<int:class_id>")
def deleteClass(class_id):
    class_ = Class_.query.get(class_id)
    db.session.delete(class_)
    db.session.commit()
    return render_template("success.html", message="Has successfully delete class")


@app.route("/api/v1/subject/all", methods=["GET"])
def getAllSubject():
    subjects = Subject.query.all()
    subject = [{"id": subject.id,
                "subject_name" : subject.name,
                "lecturer_name" : subject.lecturers_name} for subject in subjects]
    return jsonify(subject)

@app.route("/api/v1/subject/<int:id>", methods=["GET"])
def getSubject(id):
    subject = Subject.query.get(id)
    if not subject:
        return jsonify({'error': 'data not found'})
    return jsonify(subject.to_json('get'))

@app.route("/api/v1/subject/<int:id>", methods=["POST"])
def postSubject(id):
    record = request.get_json()
    subject = Subject.query.filter_by(id=id).first()
    if not subject:
        return jsonify({'error': 'data not found'})
    subject.name = record[0]['subject_name']
    subject.lecturers_name = record[0]['lecturer_name']
    db.session.commit()
    return jsonify(subject.to_json('update'))

@app.route('/api/v1/subject/<int:id>', methods=['PUT'])
# @login_required
def putSubject(id):
    record = request.get_json()
    subject = Subject(name=record[0]['subject_name'], lecturers_name=record[0]['lecturer_name'])
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_json('create'))

@app.route('/api/v1/subject/<int:id>', methods=['DELETE'])
def deleteSubject(id):
    record = request.get_json()
    subject = Subject.query.filter_by(id=id).first()
    if not subject:
        return jsonify({'error': 'data not found'})
    db.session.delete(subject)
    db.session.commit()
    return jsonify(subject.to_json('delete'))
