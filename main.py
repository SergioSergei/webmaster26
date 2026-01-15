import json
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


def contains_number(input_string):
    for character in input_string:
        if character.isdigit():
            return True
    return False


def contains_uppercase(input_string):
    for character in input_string:
        if character.isupper():
            return True
    return False


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


# =============================================================================
# MAIN PAGE ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/about')
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route('/business')
def business():
    suggestions = load_suggestions()
    print(suggestions)
    return render_template("business.html", sugestions=suggestions)



    suggestion = suggestions[index]
    return render_template('resource.html',
                           title=suggestion[0],
                           image=suggestion[1],
                           category=suggestion[2],
                           info=suggestion[3],
                           link=suggestion[4],
                           address=suggestion[5],
                           phone=suggestion[6],
                           email=suggestion[7],
                           btype=suggestion[8],
                           area=suggestion[9],
                           comments=suggestion[10] if len(suggestion) > 10 else [],
                           index=index,
                           logged_in=current_user.is_authenticated)

@app.route('/suggest')
def suggest():
    return render_template("suggest.html", logged_in=current_user.is_authenticated)
    
@app.route('/references')
def references():
    return render_template("references.html", logged_in=current_user.is_authenticated)


@app.route('/profile')
def profile():
    return render_template("profile.html", logged_in=current_user.is_authenticated)


@app.route('/resources')
def resources():
    suggestions = load_suggestions()
    print(suggestions)
    return render_template("resources.html", sugestions=suggestions)

    suggestion = suggestions[index]
    return render_template('resource.html',
                           title=suggestion[0],
                           image=suggestion[1],
                           category=suggestion[2],
                           info=suggestion[3],
                           link=suggestion[4],
                           address=suggestion[5],
                           phone=suggestion[6],
                           email=suggestion[7],
                           btype=suggestion[8],
                           area=suggestion[9],
                           comments=suggestion[10] if len(suggestion) > 10 else [],
                           index=index,
                           logged_in=current_user.is_authenticated)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # TODO: Implement search logic here
    return render_template("search.html", query=query, logged_in=current_user.is_authenticated)


# =============================================================================
# SUGGESTIONS / RESOURCES ROUTES
# =============================================================================

def load_suggestions():
    with open('suggestions.json', 'r') as f:
        return json.load(f)


def save_suggestions(suggestions):
    with open('suggestions.json', 'w') as f:
        json.dump(suggestions, f, indent=2)


@app.route('/suggestions')
def suggestions():
    suggestions = load_suggestions()
    return render_template('suggestions.html', suggestions=suggestions, logged_in=current_user.is_authenticated)


@app.route('/user/<int:index>')
def show_user_profile(index):
    suggestions = load_suggestions()
    if index < 0 or index >= len(suggestions):
        return "Resource not found", 404

    suggestion = suggestions[index]
    return render_template('resource.html',
                           title=suggestion[0],
                           image=suggestion[1],
                           category=suggestion[2],
                           info=suggestion[3],
                           link=suggestion[4],
                           address=suggestion[5],
                           phone=suggestion[6],
                           email=suggestion[7],
                           btype=suggestion[8],
                           area=suggestion[9],
                           comments=suggestion[10] if len(suggestion) > 10 else [],                           index=index,
                           logged_in=current_user.is_authenticated)


@app.route('/add_comment/<int:index>', methods=['POST'])
def add_comment(index):
    suggestions = load_suggestions()

    if index < 0 or index >= len(suggestions):
        return jsonify({'error': 'Resource not found'}), 404

    data = request.get_json()
    username = data.get('username', 'Anonymous')
    comment_text = data.get('comment', '')

    if not comment_text.strip():
        return jsonify({'error': 'Comment cannot be empty'}), 400

    # Ensure comments array exists
    if len(suggestions[index]) < 11:
        suggestions[index].append([])

    # Create comment object
    comment = {
        'username': username,
        'text': comment_text,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    suggestions[index][10].append(comment)
    save_suggestions(suggestions)

    return jsonify({'success': True, 'comment': comment})


# =============================================================================
# AUTHENTICATION ROUTES
# =============================================================================

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('profile'))

        if not contains_number(request.form.get('password')):
            flash("Your password should have at least 1 number")
            return redirect(url_for('profile'))

        if not contains_uppercase(request.form.get('password')):
            flash("Your password should have at least 1 uppercase letter")
            return redirect(url_for('profile'))

        if len(request.form.get('password')) < 7:
            flash("Your password should be at least 7 characters long")
            return redirect(url_for('profile'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=(request.form.get('first_name')+" "+request.form.get('last_name')),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('profile'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('profile'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")


# =============================================================================
# FOOTER FORM ROUTE
# =============================================================================


if __name__ == "__main__":
    app.run(debug=True)