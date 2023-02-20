from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    entries=[]

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            app.db.entries.insert_one({
                "content": entry_content,
                "date": formatted_date
            })
            entries.append((entry_content, formatted_date))

        entries_with_date = [
            (
                entry["content"]
                ,entry["date"]
                ,datetime.datetime.today().strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app