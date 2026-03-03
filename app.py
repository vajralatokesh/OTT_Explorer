from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import requests
import os

# =====================================
# LOAD ENVIRONMENT VARIABLES
# =====================================

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")

IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# =====================================
# FLASK SETUP
# =====================================

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================================
# LOGIN MANAGER
# =====================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =====================================
# DATABASE MODELS
# =====================================

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))


class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer)  # Movie or Anime ID
    content_type = db.Column(db.String(20))  # movie / anime
    title = db.Column(db.String(200))
    poster = db.Column(db.String(500))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =====================================
# MOVIE API FUNCTIONS
# =====================================

def get_movies(search=None, language=None, genre=None):
    try:
        if search:
            url = "https://api.themoviedb.org/3/search/movie"
            params = {"api_key": TMDB_API_KEY, "query": search}
        else:
            url = "https://api.themoviedb.org/3/discover/movie"
            params = {
                "api_key": TMDB_API_KEY,
                "sort_by": "popularity.desc",
                "page": 1
            }
            if language:
                params["with_original_language"] = language
            if genre:
                params["with_genres"] = genre

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])

    except requests.exceptions.RequestException as e:
        print("Movie API Error:", e)
        return []


def get_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(url, params={"api_key": TMDB_API_KEY}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Movie Detail Error:", e)
        return None


# =====================================
# ANIME API FUNCTIONS (JIKAN)
# =====================================

def get_anime(search=None, genre=None):
    try:
        if search:
            url = f"https://api.jikan.moe/v4/anime?q={search}"
        else:
            url = "https://api.jikan.moe/v4/top/anime"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        anime_list = response.json().get("data", [])

        if genre:
            anime_list = [
                a for a in anime_list
                if any(genre.lower() == g["name"].lower()
                       for g in a.get("genres", []))
            ]

        return anime_list

    except requests.exceptions.RequestException as e:
        print("Anime API Error:", e)
        return []


# =====================================
# ROUTES
# =====================================

@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------- LOGIN ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------- REGISTER ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------- LOGOUT ----------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------- DASHBOARD (MOVIES) ----------

@app.route("/dashboard")
@login_required
def dashboard():
    movies = get_movies(
        request.args.get("search"),
        request.args.get("language"),
        request.args.get("genre")
    )

    return render_template(
        "dashboard.html",
        movies=movies,
        image_base=IMAGE_BASE
    )


# ---------- MOVIE DETAILS ----------

@app.route("/movie/<int:id>")
@login_required
def movie_details(id):
    movie = get_movie_details(id)
    return render_template(
        "detail.html",
        movie=movie,
        image_base=IMAGE_BASE
    )


# ---------- ADD MOVIE TO WATCHLIST ----------

@app.route("/watchlist/add_movie/<int:id>")
@login_required
def add_movie_watchlist(id):
    movie = get_movie_details(id)

    if not movie:
        return redirect(url_for("dashboard"))

    exists = Watchlist.query.filter_by(
        user_id=current_user.id,
        content_id=id,
        content_type="movie"
    ).first()

    if not exists:
        item = Watchlist(
            user_id=current_user.id,
            content_id=id,
            content_type="movie",
            title=movie.get("title"),
            poster=movie.get("poster_path")
        )
        db.session.add(item)
        db.session.commit()

    return redirect(request.referrer or url_for("dashboard"))


# ---------- ADD ANIME TO WATCHLIST ----------

@app.route("/watchlist/add_anime/<int:id>")
@login_required
def add_anime_watchlist(id):
    try:
        url = f"https://api.jikan.moe/v4/anime/{id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json().get("data", {})

        exists = Watchlist.query.filter_by(
            user_id=current_user.id,
            content_id=id,
            content_type="anime"
        ).first()

        if not exists:
            item = Watchlist(
                user_id=current_user.id,
                content_id=id,
                content_type="anime",
                title=data.get("title"),
                poster=data.get("images", {}).get("jpg", {}).get("image_url")
            )
            db.session.add(item)
            db.session.commit()

    except requests.exceptions.RequestException as e:
        print("Anime Watchlist Error:", e)

    return redirect(request.referrer or url_for("anime"))


# ---------- REMOVE FROM WATCHLIST ----------

@app.route("/watchlist/remove/<int:id>")
@login_required
def remove_watchlist(id):
    item = Watchlist.query.filter_by(
        user_id=current_user.id,
        id=id
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("watchlist"))


# ---------- WATCHLIST PAGE ----------

@app.route("/watchlist")
@login_required
def watchlist():
    items = Watchlist.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "watchlist.html",
        items=items,
        image_base=IMAGE_BASE
    )


# ---------- ANIME PAGE ----------

@app.route("/anime")
@login_required
def anime():
    anime_list = get_anime(
        request.args.get("search"),
        request.args.get("genre")
    )
    return render_template("anime.html", anime=anime_list)


# =====================================
# RUN SERVER
# =====================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)