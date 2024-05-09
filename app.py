from flask import Flask, render_template, redirect, session, flash, request
from models import db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(f'/users/{user.username}')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_detail(username):
    if 'username' not in session or session['username'] != username:
        flash("You must be logged in to view that page!")
        return redirect('/')
    user = User.query.get_or_404(username)
    return render_template('user.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session or session['username'] != username:
        flash("You don't have permission to view this page!")
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback_form.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash("You don't have permission to view this page!")
        return redirect('/')
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('feedback_form.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash("You don't have permission to do that!")
        return redirect('/')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session['username'] != username:
        flash("You don't have permission to do that!")
        return redirect('/')
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')
