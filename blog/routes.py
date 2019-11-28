from flask import render_template, request, escape, url_for, make_response, jsonify, session, redirect, flash
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


@app.route("/<firstname>/<lastname>")
def hellos(firstname, lastname):
    return f"Hello, let this be last time to do basics {firstname} {lastname}"

@app.route("/", methods=["POST", "GET"])
@login_required
def home():
    return render_template("index.html", title="Home")

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(os.path.splitext(form_picture.filename))
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Account updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics" + current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form, title="Account")

@app.route('/api')
def api():
    return {
        "name" : "Emma",
        "age" : 30,
        "height" : "10fts"
    }

@app.route('/japi')
def japi():
    return jsonify({
        "name" : "Emma",
        "age" : 30,
        "height" : "10fts"
    })

# @app.route('/login')
# def login():
#     if request.method == "POST":
#         session['username'] = request.form["username"]
#         return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#---------------------------------------
@app.route('/signup', methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        print("in the register route")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Horray you got an account now: {form.username.data}!", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form, title="signup")

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"Login successful", "success")
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            return redirect(url_for('home'))
        flash(f"Login unsuccessful, check email or password")
    return render_template("login.html", form=form, title="Login")

@app.route("/post/new", methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(f"Post Created", "success")
        return redirect(url_for('posts'))
    return render_template("create_post.html", form=form, title="New Post")

@app.route("/posts")
@login_required
def posts():
    posts = Post.query.all()
    return render_template("posts.html", title="Posts", posts=posts) 

@app.route("/post/<int:post_id>", methods=["POST", "GET"])
@login_required
def post(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).first()
    comments = Comment.query.filter_by(post_id = post.id).all()
    if form.validate_on_submit():
        comment = Comment(content = form.comment.data, post_id = post.id, user_id = current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment Added", "success")
        return redirect(url_for('post', post_id=post.id))
    return render_template("post.html", title="Post", post=post, form=form, comments=comments) 

@app.route("/post/edit/<int:post_id>", methods=["POST", "GET"])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post.author == current_user:   
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Post has been updated", "success")
            return redirect(url_for('posts'))
        form.title.data = post.title
        form.content.data = post.content
        return render_template("edit_post.html", title="Post", form=form)
    flash("You are not authorised for this operation")
    return redirect(url_for('post', post_id=post_id))

@app.route("/post/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted", "success")
        return redirect(url_for("posts"))
    flash("You don't the rights to delete this post", "success")
    return redirect(url_for("posts"))