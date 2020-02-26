# import dependences
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create app instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# mongo connection

import sys

# set up routes
@app.route('/')
def home():
    # query all data in db and set to a variable
    mars_data = mongo.db.mars_collection.find_one()
   # print(mars_data)
    print(mars_data, file=sys.stderr)
    # render template - pass mars data into html template to display data
    return render_template('index.html', mars_db=mars_data)

@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape() # scrape function off scrape_mars.py file
    mars_data = mongo.db.mars_collection # connect to mongo db
    mars_data.replace_one({}, mars, upsert=True) # pull data to db
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)