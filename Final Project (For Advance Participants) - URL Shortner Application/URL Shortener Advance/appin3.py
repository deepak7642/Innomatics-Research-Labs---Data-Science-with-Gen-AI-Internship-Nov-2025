from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import string
import random
import validators

app = Flask(__name__)
app.secret_key = "secretkey123"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =======================
# Database Models
# =======================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(9), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =======================
# Utility Functions
# =======================

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# =======================
# Routes
# =======================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 to 9 characters long")
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash("This username already exists...")
            return redirect(url_for('signup'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Signup successful. Please login.")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    short_url = None
    error = None

    if request.method == 'POST':
        original_url = request.form['url']

        if not validators.url(original_url):
            error = "Invalid URL"
        else:
            short_code = generate_short_code()
            while URL.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code()

            new_url = URL(
                original_url=original_url,
                short_code=short_code,
                user_id=current_user.id
            )
            db.session.add(new_url)
            db.session.commit()

            short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url, error=error)

@app.route('/history')
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', urls=urls)

@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

# =======================
# Run App
# =======================

if __name__ == '__main__':
    app.run(debug=True)
