from json import *
from flask import Flask, flash
from data import db_session
from data.users import User
import os
from flask import render_template, redirect, request
from forms.user import RegisterForm
from forms.profile import ProfileForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms.login import LoginForm
from forms.forget_pass_0 import forget_pass_0
from forms.forget_pass_2 import forget_pass_2
from forms.messages import Message
with open('messages.json') as mess0:
    messages = load(mess0)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
users = []
cnt_messages = dict()


def islow(s: str):
    for i in s:
        if i.isupper():
            return True
    return False


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", flag=True)


@app.route('/sign-up', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    # forms.append(('/register', form))
    if form.validate_on_submit():
        yes = True
        if form.password.data != form.password_again.data:
            yes = False
            flash('Пароли должны совпадать', category='error')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            yes = False
            flash('Такой пользователь уже существует', category='error')
        if len(form.email.data) < 5:
            yes = False
            flash('Email должен содержать хотя бы 5 знаков', category='error')
        if not islow(str(form.password.data)):
            yes = False
            flash('Пароль должен содержать заглавную букву', category='error')
        if len(form.password.data) < 6:
            yes = False
            flash('Пароль должен содержать хотя бы 6 знаков', category='error')
        if yes:
            user = User(
                first_name=form.first_name.data,
                second_name=form.second_name.data,
                email=form.email.data,
                about=form.about.data,
                code=form.code.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            flash('Аккаунт создан!')
            x = messages.get(user.email, 0)
            if not x:
                messages[user.email] = dict()
                with open('messages.json', 'w') as mess1:
                    dump(messages, mess1)
            return redirect('/login')
    return render_template('register.html', form=form, flag=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # forms.append(('/login', form))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            flash('Неправильный логин или пароль', category='error')
            return render_template('login.html', form=form, flag=False)
    return render_template('login.html', form=form, flag=False)


@app.route('/logout')
@login_required
def logout():
    # forms.append(('/', None))
    logout_user()
    return redirect("/")


@app.route('/profile')
@login_required
def profile():
    form = ProfileForm()
    return render_template('profile.html', form=form, flag=True)


@app.route('/forget_pass', methods=['GET', 'POST'])
def forget0():
    form = forget_pass_0()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        yes = False
        for user in db_sess.query(User).all():
            print(form.email.data, user.email)
            print(form.code, user.code)
            if form.email.data == user.email and form.code.data == user.code:
                yes = True
                break
        if not yes:
            flash("Такого email не существует или неправильное кодовое слово", category='error')
        if yes:
            return redirect(f'/forget_pass_1/{form.email.data}')
    return render_template('forget_pass_1.html', form=form, flag=False)


@app.route('/forget_pass_1/<email>', methods=['GET', 'POST'])
def forget(email):
    form = forget_pass_2()
    yes = False
    if form.validate_on_submit():
        if not islow(str(form.newpass1.data)):
            yes = False
            flash('Пароль должен содержать заглавную букву', category='error')
        if len(form.newpass1.data) < 6:
            yes = False
            flash('Пароль должен содержать хотя бы 6 знаков', category='error')
        if form.newpass1.data == form.newpass2.data and not (not islow(str(form.newpass1.data))
                                                             or len(form.newpass1.data) < 6):
            yes = True
        if yes:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == email).first()
            user.set_password(form.newpass1.data)
            db_sess.commit()
            flash('Пароль успешно изменен')
            return redirect('/login')
        else:
            flash('Пароли должны совпадать', category='error')
    return render_template('forget_pass_2.html', form=form, flag=False)


@app.route('/info', methods=['GET', 'POST'])
def info():
    u_email = current_user.email
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == u_email).first()
    if not user.about:
        if request.method == 'POST':
            dat = request.form['date']
            if not dat:
                flash('Вы ничего не ввели', category='error')
                return render_template('info.html', flag=True)
            else:
                user.about = dat
                db_sess.commit()
                return redirect('/')
        return render_template('info.html', flag=True)
    else:
        if request.method == 'POST':
            dat = request.form['date']
            if dat == user.about:
                flash('Вы ничего не изменили', category='error')
                return render_template('info.html', flag=True)
            else:
                user.about = dat
                db_sess.commit()
                return redirect('/')
        return render_template('info.html', flag=True)


@app.route('/friends_request')
def request_():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    req = []
    req1 = []
    if user.requests:
        users = user.requests.split('#$#')
        req = [[db_sess.query(User).filter(User.email == i).first().first_name,
                db_sess.query(User).filter(User.email == i).first().second_name, i] for i in users if i != '']
        req_set = []
        req1 = []
        for i in req:
            if i not in req_set:
                req_set.append(i)
                req1.append(i)
    return render_template('friend_request.html', sp=req1, flag=True, l=len(req1))


@app.route('/decline_f/<email>')
def decl(email):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    user_another = db_sess.query(User).filter(User.email == email).first()
    friends_req = user.requests
    friends_req = friends_req.replace(f'{email}', '')
    if friends_req[:3] == '#$#':
        friends_req.replace('#$#', '')
    else:
        friends_req.replace('#$##$#', '')
    user.requests = friends_req
    db_sess.commit()
    return redirect('/friends_request')


@app.route('/accept_f/<email>')
def accept_f(email):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    user_another = db_sess.query(User).filter(User.email == email).first()
    friends_req = user.requests
    friends_req = friends_req.replace(f'{email}', '')
    if friends_req[:3] == '#$#':
        friends_req.replace('#$#', '')
    else:
        friends_req.replace('#$##$#', '')
    user.requests = friends_req
    if not user.friends:
        user.friends = ''
    user.friends += email
    user.friends += '#$#'
    if not user_another.friends:
        user_another.friends = ''
    user_another.friends += current_user.email
    user_another.friends += '#$#'
    db_sess.commit()
    return redirect('/friends_request')


@app.route('/find')
def find():
    db_sess = db_session.create_session()
    users1 = db_sess.query(User).filter(User.about != '').all()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    flag = False
    req = []
    req1 = []
    users_1 = []
    users_ = []
    if user.friends:
        users_ = user.friends.split('#$#')
        req = [i for i in users_ if i != '']
    if user.requests:
        users_1 = user.requests.split('#$#')
        req1 = [i for i in users_1 if i != '']
    users_norm = []
    for i in users1:
        if i.email == user.email:
            continue
        if i.email != '':
            a = []
            if i.requests != None:
                a = i.requests.split("#$#")
            if user.email not in a:
                b = []
                if i.friends != None:
                    b = i.friends.split("#$#")
                if user.email not in b:
                    flag = True
                    users_norm.append(i)
    return render_template('find_friends.html', users=users_norm, flag1=flag, flag=True, l=len(users_norm))


@app.route('/try_f/<email>')
def add_friend(email):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if not user.requests:
        user.requests = ''
    user.requests += current_user.email
    user.requests += '#$#'
    db_sess.commit()
    return redirect('/find')


@app.route('/friends')
def friend():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    req = []
    if user.requests:
        users = user.friends.split('#$#')
        req = [(i, db_sess.query(User).filter(User.email == i).first().about) for i in users if i != '']
    return render_template('friends.html', sp=req, flag=True, l=len(req))


@app.route('/message')
def mess():
    print(messages)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    req = []
    if user.friends:
        users = user.friends.split('#$#')
        req = [[db_sess.query(User).filter(User.email == i).first().first_name,
                db_sess.query(User).filter(User.email == i).first().second_name, i] for i in users if i != '']
    return render_template('messages.html', sp=req, flag=True, l=len(req))


@app.route('/message_f/<email_>', methods=['GET', 'POST'])
def mess_(email_):
    sp = []
    email = email_
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    n1 = user.first_name
    n2 = user.second_name
    can = False
    if email_[0] == '[':
        sp = email_.split(',')
        for i in range(len(sp)):
            if sp[i][0] == ' ':
                sp[i] = sp[i][1:]
            if sp[i][0] == '[':
                sp[i] = sp[i][1:]
            elif sp[i][-1] == ']':
                sp[i] = sp[i][:-1]
            sp[i] = sp[i][1:-1]
        email = sp[1]
        can = True
    form = Message()
    if can:
        request.form['mess'] = sp[0]
    if request.method == 'GET':
        y = messages[current_user.email].get(email, 0)
        if not y:
            messages[current_user.email][email] = []
            messages[email][current_user.email] = []
            with open('messages.json', 'w') as mess2:
                dump(messages, mess2)
        from_me = messages[current_user.email][email]
        can = False
        if messages[current_user.email][email]:
            can = True
        return render_template('mess_friend.html', n1=n1, n2=n2, mess=from_me, form=form, flag1=can, flag=True)
    if request.method == 'POST':
        a = request.form['mess']
        y = messages[current_user.email].get(email, 0)
        if y == 0:
            messages[current_user.email][email] = []
            messages[email][current_user.email] = []
            with open('messages.json', 'w') as mess3:
                dump(messages, mess3)
        from_me = messages[current_user.email][email]
        if request.form['mess']:
            x = messages[current_user.email].get(email, 0)
            if x == 0:
                messages[current_user.email][email] = [(request.form['mess'], 0)]
                messages[email][current_user.email] = [(request.form['mess'], 1)]
                with open('messages.json', 'w') as mess4:
                    dump(messages, mess4)
            else:
                messages[current_user.email][email].append((request.form['mess'], 0))
                messages[email][current_user.email].append((request.form['mess'], 1))
                with open('messages.json', 'w') as mess5:
                    dump(messages, mess5)
            from_me = messages[current_user.email][email]
        return render_template('mess_friend.html', n1=n1, n2=n2, friend=email, mess=from_me, form=form, flag=True)


def main():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.id >= 1).delete()
    db_sess.commit()


def main1():
    db_session.global_init("db/users.db")


if __name__ == '__main__':
    # main()
    main1()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
