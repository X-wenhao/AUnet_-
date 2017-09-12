from . import fd
from .models import HttpAuth
from flask import request,render_template,redirect,flash
auth=HttpAuth()

@fd.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        if auth.login_user():
            return redirect('/')
        else:
            flash('please login first')
            return redirect('login')


@fd.route('/')
@auth.login_required
def index():
    return 'hello '

