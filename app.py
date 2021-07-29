from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the database for the app (Here, I am using SQLAlchemy as I found is easy to configure)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# Creates database file in current folder(we gave the relative path) while running the app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Now, we create a class for the todo list item which has properties like id, name and state(finished or not)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))			# Maximum of 50 characters
	state = db.Column(db.Boolean) 			# Only 2 states  ( finished/not finished )


@app.route("/")
def main():
	all_items = Todo.query.all()
	return render_template("index.html", all_items=all_items)
	
	
@app.route("/add-item", methods=["post"])
def add_item():
	text = request.form.get("data")
	new_item = Todo(name=text, state=False)
	db.session.add(new_item)
	db.session.commit()
	return redirect("/")
	
	
if __name__ == "__main__" :
	db.create_all()						# Creates the data structure of given class
	app.run(debug=True)
