"""Blogly application."""

from flask import Flask, request, render_template, redirect, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag, DEFAULT_IMG_URL
from forms import UserForm, PostForm, TagForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'


debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Redirects homepage to user list"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=posts)


####################
# User View Routes #
####################

@app.route('/users')
def show_user_list():
    """Shows list of users"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('user_list.html', users=users)


@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    """Handle add user form"""
    form = UserForm()

    if form.validate_on_submit():
        user = User(first_name=form.data['first_name'],
                    last_name=form.data['last_name'],
                    image_url=form.data['image_url'] or None)
        db.session.add(user)
        db.session.commit()
        flash(f"Added '{user.full_name}'")
        return redirect('/users')
    else:
        return render_template('user_new.html', form=form)


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show user's details"""
    # How to get ordered list of posts?
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Handle edit user form"""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.data['first_name']
        user.last_name = form.data['last_name']
        user.image_url = form.data['image_url'] or DEFAULT_IMG_URL
        db.session.add(user)
        db.session.commit()
        flash(f"Updated '{user.full_name}'")
        return redirect(f'/users/{user_id}')
    else:
        return render_template('user_edit.html', form=form, user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    flash(f"Deleted '{User.query.get(user_id).full_name}'")
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')


####################
# Post View Routes #
####################

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """Handle add post form"""
    form = PostForm()
    user = User.query.get(user_id)
    form.set_choices()  # DO THIS ON EDIT

    # How to add values in checkboxes in wtform?  What is the validation?
    # How to retrieve list of tags?

    if form.validate_on_submit():

        tags = [Tag.query.get(tag_id) for tag_id in form.data['tags']]

        post = Post(title=form.data['title'],
                    content=form.data['content'],
                    user_id=user_id,
                    tags=tags
                    )
        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' added.")
        return redirect(f'/users/{user_id}')
    else:
        return render_template('post_new.html', form=form, user=user)


@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show post's details"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Handle edit post form"""
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.data['title']
        post.content = form.data['content']
        db.session.add(post)
        db.session.commit()
        flash(f"Updated post '{post.title}'")
        return redirect(f'/posts/{post_id}')
    else:
        return render_template('post_edit.html', form=form, post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    flash(f"Deleted post '{post.title}'")
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


###################
# Tag View Routes #
###################

@app.route('/tags')
def show_tags():
    """Shows list of tags"""
    tags = Tag.query.order_by('name').all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/new', methods=["GET", "POST"])
def add_tag():
    """Handle add tag form"""
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.data['name'],
                  )
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag '{tag.name}' added.")
        return redirect(f'/tags')
    else:
        return render_template('tag_new.html', form=form)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show tag's details"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    """Handle edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm(obj=tag)
    if form.validate_on_submit():
        tag.name = form.data['name']
        db.session.add(tag)
        db.session.commit()
        flash(f"Updated Tag '{tag.name}'")
        return redirect(f'/tags/{tag_id}')
    else:
        return render_template('tag_edit.html', form=form, tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.get_or_404(tag_id)
    flash(f"Deleted Tag '{tag.name}'")
    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()
    return redirect(f'/tags')


################
# Error Routes #
################

@app.errorhandler(404)
def page_not_found(e):
    """Show custom 404 error page"""
    return render_template('404.html'), 404
