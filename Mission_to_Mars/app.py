# ----------------Mongo and Flask app for Mars Scrape----------------------

# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create flask app
app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
	mars = mongo.db.mars
	data = scrape_mars.scrape()

	# Update the mongo database
	mars.update({}, data, upsert=True)
	# Redirect back to home page
	return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)