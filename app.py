import os
import secrets

from flask import Flask, render_template, request, Response, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db import db_init, db
from tables import Img, User, Upvote
from forms import LoginForm, RegisterForm, AvatarForm, UploadForm, PointsForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SECRET_KEY'] = 'Kot w Butach: Ta informacja jest zastrzeżona, compadre. Osioł: Ściśle tajne, łamane przez nie wiem.'

Bootstrap(app)
db_init(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        current_user.username = "Gość"
        current_user.image_file = "default-avatar.jpg"
    form = PointsForm()
    imgs = Img.query
    upvotes = Upvote.query
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('index.html', name=current_user.username, imgs=imgs, image_file=image_file, form=form, upvotes=upvotes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')

        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = UploadForm()
    if form.validate_on_submit():
        pic = form.picture.data
        if not pic:
            return 'No pic uploaded!', 400

        filename = form.title.data
        mimetype = pic.mimetype
        autor = current_user.username
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype, autor=autor, points=1, user_id=current_user.id)
        db.session.add(img)
        db.session.commit()

        return redirect('/')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('addMeme.html', form=form, name=current_user.username, image_file=image_file)


@app.route('/<int:number>')
def get_img(number):
    img = Img.query.filter_by(id=number).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and not "default-avatar.jpg":
        os.remove(prev_picture)

    return picture_fn


@app.route('/avatar', methods=['GET', 'POST'])
@login_required
def avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect("/")
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('avatar.html', image_file=image_file, name=current_user.username, form=form)


@app.route('/vote', methods=['POST'])
@login_required
def vote():
    img = int(request.data)
    vote = Upvote(img_id=img, user_id=current_user.id)
    db.session.add(vote)
    update = Img.query.filter_by(id=img).first()
    update.points += 1
    db.session.commit()

    return jsonify()


if __name__ == '__main__':
    app.run()
