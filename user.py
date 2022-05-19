# -*- coding: UTF-8 -*-
import random
import string
from datetime import datetime
from exts import mail, db
from models import Email_captchaModel, UserModel
from flask_mail import Message
from .froms import RegisterForm, LoginForm
from flask import Blueprint, render_template, request, redirect, jsonify, session,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                flash("账户和密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("帐号或密码格式错误！")
            return redirect(url_for("user.login"))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            # return 555
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))
            # return 666

@bp.route('/logout')
def logout():
    # 清除session中所有数据
    session.clear()
    return redirect(url_for("user.login"))





@bp.route('/captcha', methods=['GET', 'POST'])
def get_captcha():
    email = request.form.get('email')
    letters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(letters, 4))
    if mail:
        message = Message(
            subject="邮箱测试",
            recipients=[email],
            body=f"[欢迎来到我的世界]你的验证码是：{captcha},请不要告诉其他人！"
        )
        mail.send(message)
        captcha_model = Email_captchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = Email_captchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print('captcha', captcha)
        # code: 200 ,成功的正常的请求
        return jsonify({"code": 200})
    else:
        # code: 400 ,客户端错误
        return jsonify({"code": 400, "message": "请先传递邮箱！"})
