from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, abort
from flask_module.user.forms import RegistraionForm, LoginForm
from flask_module.user.models import User, Role
from flask_module.posts.models import Post
from flask_login import current_user, login_user, logout_user
from flask_module import bcrypt, db, app
from bs4 import BeautifulSoup
import secrets, os, requests, base64

user = Blueprint("user", __name__)

# db.drop_all()
# db.create_all()

@user.route("/")
@user.route("/index")
def home():
    db.create_all()
    # db.drop_all()
    if "user" in session:
        loged_in_user = session['user']
        return redirect(url_for('user.profile', username=loged_in_user))
    else:
        return render_template("home.html")
    

@user.route("/register", methods=["POST", "GET"])
def register():
    form = RegistraionForm()
    if "user" in session:
        loged_in_user = session['user']
        return redirect(url_for('user.profile', username=loged_in_user))
    else:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            if form.profile_picture.data:
                hex_image = secrets.token_hex(8)
                f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
                image_name = hex_image + f_ext
                image_path = os.path.join(app.root_path, 'static\images', image_name)
                form.profile_picture.data.save(image_path)
                user = User(username=form.username.data, email=form.email.data, profile_picture=image_name, password=hashed_password)
            else:
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        return render_template("user/register.html", form=form)


@user.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if "user" in session:
        loged_in_user = session['user']
        return redirect(url_for('user.profile', username=loged_in_user))
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user'] = user.username
                return redirect(url_for("user.profile", username=user.username))
        return render_template("user/login.html", form=form)


@user.route("/logout")
def logout():
    logout_user()
    session.pop("user", None)
    return redirect(url_for("user.login"))


@user.route("/profile/<string:username>", methods=["POST", "GET"])
def profile(username):
    page  = request.args.get('page', 1, type=int)
    if "user" in session:
        user = User.query.filter_by(username=username).first()
        post = Post.query.filter_by(user_id=user.id).paginate(per_page=2, page=page)
        return render_template("user/profile.html", user=user, posts=post)
    else:
        return redirect(url_for("user.login"))


@user.route("/<int:user_id>/update", methods=["POST", "GET"])
def update(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = RegistraionForm()
    if "user" in session:
        if request.method == "POST":
            if form.validate_on_submit:
                if form.profile_picture.data:
                    hex_image = secrets.token_hex(8)
                    f_name, f_ext = os.path.splitext(form.profile_picture.data.filename)
                    image_name = hex_image + f_ext
                    image_path = os.path.join(app.root_path, 'static\images', image_name)
                    form.profile_picture.data.save(image_path)
                    user.profile_picture = image_name
                user.username = form.username.data
                user.email = form.email.data
                db.session.commit()
                return redirect(url_for("user.profile", username=user.username))
        else:
            form.username.data = user.username
            form.email.data = user.email
            form.profile_picture.data = user.profile_picture
            form.submit.label.text = "Update Profile"
            return render_template("user/update_profile.html", user=user, form=form)
    else:
        return redirect(url_for("user.login"))
    

@user.route("/users", methods=['POST', 'GET'])
def users():
    if "user" in session:
        page  = request.args.get('page', 1, type=int)
        users = User.query.filter(User.id != current_user.id).paginate(per_page=1, page=page)
        return render_template("user/all_users.html", users=users)
    else:
        abort(401)
        # return redirect(url_for("user.login"))


@user.route("/profile_detail/<string:username>", methods=["POST", "GET"])
def profile_detail(username):
    page  = request.args.get('page', 1, type=int)
    if "user" in session:
        user = User.query.filter_by(username=username).first()
        post = Post.query.filter_by(user_id=user.id).paginate(per_page=2, page=page)
        return render_template("user/profile_detail.html", user=user, posts=post)
    else:
        return redirect(url_for("user.login"))
    

@user.route("/follow_user/<int:user_id>", methods=["POST", "GET"])
def follow_user(user_id):
    authenticated_user = User.query.filter_by(id=current_user.id).first()
    user = User.query.filter_by(id=user_id).first()
    authenticated_user.following.append(user)
    db.session.commit()
    return redirect(url_for('user.users'))


@user.route("/remove_user/<int:user_id>", methods=["POST", "GET"])
def remove_user(user_id):
    authenticated_user = User.query.filter_by(id=current_user.id).first()
    user = User.query.filter_by(id=user_id).first()
    authenticated_user.following.remove(user)
    db.session.commit()
    return redirect(url_for('user.users'))


@user.route('/scrape_images')
def scrape_images():
    url = request.args.get('url')
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    images = soup.find_all('img')
    
    img_scr = []
    for img in images:
        img_scr.append(img['src'])
    print(img_scr)
    return jsonify(img_scr)


@user.route('/post_scraped_image/', methods=["POST", "GET"])
def post_scraped_image():
    src_ = request.args.get('src')
    src = base64.b64decode(src_).decode('ascii')
    hex_image = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(src)
    image_name = hex_image + ".jpg"
    image_path = os.path.join(app.root_path, 'static\images', image_name)
    with open(image_path, 'wb') as f:
        im = requests.get(src)
        f.write(im.content)
    post = Post(image=image_name, caption="", user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("user.profile", username=current_user.username))


@user.route('/post_scraped', methods=["POST", "GET"])
def post_scraped():
    src = request.args.get('src')
    hex_image = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(src)
    image_name = hex_image + ".jpg"
    image_path = os.path.join(app.root_path, 'static\images', image_name)
    with open(image_path, 'wb') as f:
        im = requests.get(src)
        f.write(im.content)
    post = Post(image=image_name, caption="", user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return jsonify(src)