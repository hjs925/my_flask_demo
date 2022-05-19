# -*- coding: UTF-8 -*-
import config
from exts import db, mail
from flask import Flask, session, g
from Blueprints import user_bp
from Blueprints import qa_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_reques():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get('user_id')
            g.user = user
        except:
            g.user = None

@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}



if __name__ == '__main__':
    app.run()
