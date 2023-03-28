from random import choice
import string
from datetime import datetime
from core.models import ShortUrls
from core import app,db
from flask import render_template, redirect, request, url_for, flash

def generate_short_id():
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(8))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        short_id = generate_short_id()
        if not url:
            flash("The URL is required!")
            return redirect(url_for("index"))

        newlink = ShortUrls(original_url = url,short_id = short_id,created_at=datetime.now())
        db.session.add(newlink)
        db.session.commit()
        short_url = request.host_url + short_id

        return render_template("index.html",short_url=short_url)
    return render_template("index.html")

@app.route("/<short_id>")
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash("Invalid URL!")
        return redirect(url_for("index"))
