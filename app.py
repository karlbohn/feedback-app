from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.app_context().push()

connect_db(app)

@app.route('/')
def root():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Shows & handles form to register a user"""

    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username
        
        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Shows & handles form to log in an existing user"""

    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Username/password combination not recognized"]
            return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/")

@app.route('/users/<username>')
def show_user_page(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("user.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show & handle form for new feedback"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("new_feedback.html", form=form)
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show & handle form to update feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")