from flask import Flask, render_template, request, session, redirect, url_for
import random
import json
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"


def load_tracks():
    with open("tracks.json") as f:
        return json.load(f)


def load_stats():
    if not os.path.exists("stats.json"):
        return {"visits": 0, "completed": 0, "results": []}
    try:
        with open("stats.json") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {"visits": 0, "completed": 0, "results": []}


def save_stats(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f)


def get_options():
    """Extract unique genres, subgenres, and decades from tracks."""
    tracks = load_tracks()
    genres = sorted(set(t["genre"] for t in tracks))
    subgenres = sorted(set(t["subgenre"] for t in tracks))
    decades = sorted(set(t["decade"] for t in tracks))
    return {
        "genres": genres,
        "subgenres": subgenres,
        "decades": decades,
    }


def build_dependency_data():
    tracks = load_tracks()
    seen = set()
    dependency_data = []
    for track in tracks:
        key = (track["genre"], track["subgenre"], track["decade"])
        if key in seen:
            continue
        seen.add(key)
        dependency_data.append({
            "genre": track["genre"],
            "subgenre": track["subgenre"],
            "decade": track["decade"],
        })
    return dependency_data


def build_dependency_map():
    tracks = load_tracks()
    dependency_map = {}
    for track in tracks:
        decade = track["decade"]
        genre = track["genre"]
        subgenre = track["subgenre"]
        dependency_map.setdefault(decade, {})
        dependency_map[decade].setdefault(genre, set()).add(subgenre)
    return {
        decade: {
            genre: sorted(subgenres)
            for genre, subgenres in genres.items()
        }
        for decade, genres in dependency_map.items()
    }


@app.route("/")
def index():
    stats = load_stats()
    stats["visits"] += 1
    save_stats(stats)

    tracks = load_tracks()
    selected = random.sample(tracks, min(15, len(tracks)))
    session["tracks"] = selected
    session["current"] = 0
    session["score"] = 0
    session["results"] = []

    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    tracks = session.get("tracks")
    current = session.get("current", 0)
    if not tracks or current >= len(tracks):
        return redirect(url_for("index"))

    track = tracks[current]
    options = get_options()
    return render_template(
        "index.html",
        track=track,
        index=current + 1,
        total=len(tracks),
        genres=options["genres"],
        subgenres=options["subgenres"],
        decades=options["decades"],
        dependency_data=build_dependency_data(),
    )


@app.route("/submit", methods=["POST"])
def submit():
    tracks = session.get("tracks")
    current = session.get("current", 0)
    if not tracks or current >= len(tracks):
        return redirect(url_for("index"))

    user_genre = request.form.get("genre")
    user_sub = request.form.get("sub")
    user_decade = request.form.get("decade")
    real = tracks[current]

    correct = (
        user_genre == real["genre"] and
        user_sub == real["subgenre"] and
        user_decade == real["decade"]
    )

    score = session.get("score", 0) + (1 if correct else 0)
    session["score"] = score

    results = session.get("results", [])
    results.append({
        "correct": correct,
        "real": real,
        "user": {
            "genre": user_genre,
            "sub": user_sub,
            "decade": user_decade,
        },
    })
    session["results"] = results
    session["current_result"] = len(results) - 1

    return redirect(url_for("check_answer"))


@app.route("/check_answer")
def check_answer():
    results = session.get("results", [])
    current_result = session.get("current_result", 0)
    tracks = session.get("tracks", [])
    current = session.get("current", 0)
    
    if current_result >= len(results):
        return redirect(url_for("quiz"))
    
    result = results[current_result]
    total_tracks = len(tracks)
    
    return render_template(
        "check.html",
        result=result,
        index=current_result + 1,
        total=total_tracks,
    )


@app.route("/next_question")
def next_question():
    tracks = session.get("tracks")
    current = session.get("current", 0)
    session["current"] = current + 1

    if current + 1 >= len(tracks):
        stats = load_stats()
        stats["completed"] += 1
        score = session.get("score", 0)
        stats["results"].append(score)
        save_stats(stats)
        return redirect(url_for("result"))

    return redirect(url_for("quiz"))


@app.route("/result")
def result():
    score = session.get("score", 0)
    results = session.get("results", [])
    total = len(results)
    return render_template("result.html", score=score, total=total, results=results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
