from flask import Flask
from waitress import  serve
from data.users import User
import datetime
from data.news import News
from flask import render_template, redirect, request, make_response, session, abort, jsonify
from forms.user import RegisterForm
from forms.news import NewsForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms.login import LoginForm
from data import db_session, news_api
from flask_restful import reqparse, abort, Api, Resource
from data import news_resources
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs1.db")
    app.register_blueprint(news_api.blueprint)
    app.run()
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')


if __name__ == '__main__':
    main()
    # app.run(port=5000, host='127.0.0.1')
    serve(app,host='127.0.0.1', port=5000)