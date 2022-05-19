import wtforms
from models import Email_captchaModel,UserModel
from wtforms.validators import length, email, EqualTo

class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    password = wtforms.StringField(validators=[(length(min=6, max=20))])

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[(length(min=6, max=20))])
    captcha = wtforms.StringField(validators=[(length(min=4, max=4))])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha=field.data
        captcha_model=Email_captchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower()!=captcha.lower():
            raise wtforms.ValidationError('验证码错误!')

    def validate_email(self, field):
        email=field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经存在!')