from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import *
from wtforms.fields.core import DateField, IntegerField, SelectField
 
class signUpForm(FlaskForm):
    user_code = StringField('User ID', validators=[DataRequired(), Length(min=5, message=('Your id is too short.'))])
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rePassword = PasswordField('Retype Password',  validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_userId(self, userCode):
        userId = User.query.filter_by(user_code=userCode.data).first()
        if userId is not None:
            raise ValidationError("Username has been already used! Please use different username.") 

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("email has been already used! Please use different email.")

class loginForm(FlaskForm):
    user_code = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class createSubjectsForm(FlaskForm):
    subject_name = StringField("Subject Name", validators=[DataRequired()])
    lecturer_name = StringField("Lecturer Name", validators=[DataRequired()])
    submit = SubmitField('Create Subject')

class createClassForm(FlaskForm):
    subject = SelectField('Select Subject', choices=[(g.id, g.name) for g in Subject.query.all()])
    name = StringField('Class Name', validators=[DataRequired()])
    seats = IntegerField('Seat Number', validators=[DataRequired()])
    lesson = IntegerField('Lesson Number', validators=[DataRequired()])
    lesson_start = IntegerField('Lesson Start', validators=[DataRequired()])
    # date_start = DateField('Date Start', validators=[DataRequired()], format='%d-%m-%Y')
    # date_end = DateField('Date End', validators=[DataRequired()], format='%d-%m-%Y')
    submit = SubmitField('Add to Class')




        