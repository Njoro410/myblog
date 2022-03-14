from flask import Blueprint, render_template, request, redirect, abort, url_for
from flask_login import current_user, login_required
from app.models import Categories, Comments, Posts, User
from app.forms import CommentForm, UpdateProfile
from email.message import EmailMessage
import psycopg2
import smtplib
from . import db, photos
from app.request import get_quotes


views = Blueprint('views', __name__)
conn = psycopg2.connect(
    'dbname=d34993vdvhpf6o user=fbohtwdnvfhgny password=070c1842edff64c8eb7002afefb02c40e52840dcd93579b20c472cf72a067849 host=ec2-52-44-209-165.compute-1.amazonaws.com')

cur = conn.cursor()
email = cur.execute("SELECT email FROM users;")
email_list = cur.fetchall()


@views.route('/')
def index():
    quote = get_quotes()
    post = Posts.get_posts()

    return render_template('index.html', quote=quote, posts=post, user=current_user)


@views.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        sub_title = request.form.get('sub_title')
        description = request.form.get('description')
        content = request.form.get('content')
        category = request.form.get('catselect')

        new_post = Posts(title=title, sub_title=sub_title, description=description, content=content,
                         categories_id=category, user_id=current_user.id, likes=0, dislikes=0)
        new_post.save_post()

        server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
        server.starttls()
        server.login("brian.lyonne@gmail.com", "Njoroge1.")
        for email in email_list:
            msg = EmailMessage()
            msg.set_content("Hey, there's a new post, go check it out")
            msg.add_alternative("""\
                <!DOCTYPE html>
                    <html>
                        <body>
                            <h1 style="color:SlateGray;">Don't miss a thing, go check the new post</h1>
                        </body>
                    </html>
                """, subtype='html')
            msg['Subject'] = "New Post Alert"
            msg['From'] = "brian.lyonne@gmail.com"
            msg['To'] = email
            server.send_message(msg)
        server.quit()

        return redirect('all_posts')

    return render_template('add_post.html', user=current_user)


@views.route('/post/<int:id>', methods=['GET', 'POST'])
def single_post(id):
    post = Posts.query.get(id)
    coms = Comments.get_comments(id)
    if request.args.get("like"):
        post.likes = post.likes + 1

        db.session.add(post)
        db.session.commit()

        return redirect("/post/{post_id}".format(post_id=post.id))

    elif request.args.get("dislike"):
        post.dislikes = post.dislikes + 1

        db.session.add(post)
        db.session.commit()

        return redirect("/post/{post_id}".format(post_id=post.id))
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.content.data

        new_comment = Comments(
            comment=comment, user_id=current_user.id, post_id=id)

        new_comment.save_comment()
        return redirect(request.referrer)

    return render_template('post.html', user=current_user, post=post, comment_form=comment_form, comments=coms)


@views.route('/delete/<int:id>')
def delete(id):
    comment = Comments.query.filter_by(id=id).one()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)


@views.route('/delete_post/<int:id>')
def delete_post(id):
    postd = Posts.query.filter_by(id=id).one()
    post = Posts.get_posts()
    quote = get_quotes()
    db.session.delete(postd)
    db.session.commit()
    # return redirect(request.referrer)

    return redirect('all_posts')


@views.route('/category/<id>')
def category(id):
    posts = Posts.query.filter_by(categories_id=id).all()
    cat = Categories.query.filter_by(id=id).first()

    return render_template('category.html', posts=posts, category=cat)


@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    pid = Posts.query.get_or_404(id)
    title_to_update = Posts.query.get_or_404(id)
    sub_title_to_update = Posts.query.get_or_404(id)
    description_to_update = Posts.query.get_or_404(id)
    content_to_update = Posts.query.get_or_404(id)
    category_to_update = Posts.query.get_or_404(id)
    if request.method == 'POST':
        title_to_update.title = request.form.get('title')
        sub_title_to_update.sub_title = request.form.get('sub_title')
        description_to_update.description = request.form.get('description')
        content_to_update.content = request.form.get('content')

        db.session.commit()
        # return redirect('post/pid')

    return render_template('update.html', title_to_update=title_to_update, sub_title_to_update=sub_title_to_update, description_to_update=description_to_update, content_to_update=content_to_update)


@views.route('/user/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()
    post = Posts.query.filter_by(user_id=id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, posts=post)


@views.route('/user/<id>/update', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', id=user.id))

    return render_template('profile/update.html', form=form)


@views.route('/user/<id>/update/pic', methods=['POST'])
@login_required
def update_pic(id):
    user = User.query.filter_by(id=id).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('views.profile', id=id))


@views.route('/all_posts')
def all_posts():
    posts = Posts.get_posts()

    return render_template('all_posts.html', user=current_user, posts=posts)
