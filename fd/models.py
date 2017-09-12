from functools import wraps
from flask import session,request,flash,abort
from . import admin
from . import db
from xpinyin import Pinyin

from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required

class HttpAuth(object):
    '''
    用户认证相关
    只有管理员账户，简单故未遵守restful
    '''
    def login_required(self,f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('account')=='admin':
                return f(*args, **kwargs)
            else:
                abort(401)
        return decorated

    def login_user(self):
        print(request.form.get('password'))
        if request.form.get('account')!=admin['account'] or\
            request.form.get('password')!=admin['password']:
            flash('your account or password is error')
            return False
        else:
            session['account']=admin['account']
            return True



class LoginForm(FlaskForm):
    account=StringField('Account',validators=[Required()])
    password=PasswordField('Password',validators=[Required()])
    #recaptcha=RecaptchaField()
    submit=SubmitField('Submit')

class Book(db.Model):
    __tablename__='books'
    id=db.Column(db.Integer,primary_key=True)
    organization=db.Column(db.CHAR)
    time=db.Column(db.TEXT)

    def __init__(self,organization,time):
        self.organization=organization
        self.time=time

    def is_existance(self):
        book_model=type(self)
        if book_model.query.filter_by(time=self.time,
                                      organization=self.organization).first():
            return False
        else:
            return True

class Data():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    details = db.Column(db.String(40))
    time=db.Column(db.Text)
    income = db.Column(db.Integer)
    outcome = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    name_pinyin=db.Column(db.String)

    def __init__(self, name, details,time, income, outcome, balance, other):
        self.name = name
        self.details = details
        self.time=time
        self.income = income
        self.outcome = outcome
        self.balance = balance
        self.other = other
        p=Pinyin()
        self.name_pinyin=p.get_pinyin(name)

    def is_existance(self):
        data_model=type(self)
        if data_model.query.filter_by(name=self.name,
                                      details=self.details,
                                      time=self.time,
                                      income=self.income,
                                      outcome=self.outcome,
                                      balance=self.outcome,
                                      other=self.other).first():
            return False
        else:
            return True




class Fd_data(Data,db.Model):
    __tablename__ = 'fd_datas'
    other=db.Column(db.Integer)


class Fc_data(Data,db.Model):
    __tablename__ = 'fc_datas'
    other = db.Column(db.String)


