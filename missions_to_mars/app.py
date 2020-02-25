# import dependences
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create app instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)




# set up routes
@app.route('/')
def home():
    # query all data in db and set to a variable
    mars_data = mongo.db.collection.find()
    print(mars_data)

    # render template - pass mars data into html template to display data
    return render_template('index.html', mars=mars_data)

@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()
    mongo.db.collection.update({}, mars, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)