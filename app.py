from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'production'			# To be changed to production when it needs to be deployed

if ENV == 'development':
	# Configuring the database for the app (Here, I am using SQLAlchemy as I found is easy to configure)
	# Creates database file in current folder(we gave the relative path) while running the app
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sai12345@localhost/todo'  #'sqlite:///db.sqlite'
	app.debug = True
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://htficbrwxniwib:f5eb46c659aeeee038ef275726a836b741e3302aa08d1ce9c591a45fbc81d2c9@ec2-54-83-82-187.compute-1.amazonaws.com:5432/del4mdljo8oc8a'	# Address of the heroku database


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Now, we create a class for the todo list item which has properties like id, name and state(finished or not)

class Todo(db.Model):
	__tablename__ = 'tasks'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))			# Maximum of 100 characters
	state = db.Column(db.Boolean) 			# Only 2 states  ( finished/not finished )

	def __init__(self, name, state):
		self.name = name
		self.state = state


@app.route("/")
def main():
	all_tasks = Todo.query.all()
	return render_template("index.html", all_tasks=all_tasks)
	
	
@app.route("/add-item", methods=["post"])
def add_task():
	text = request.form.get("data")			# Requesting form data which is posted to /add-item url
	new_task = Todo(name=text, state=False)
	all_tasks = Todo.query.all()
	task = Todo.query.filter_by(name=text).first()		# Checking whether there exists a same task in the database already
	if text == '':
		return render_template("index.html", message = 'Please enter required fields to create a task.', all_tasks=all_tasks )
	else:
		if task:
			return render_template("index.html", message = 'This task already exists, Please create another task.', all_tasks=all_tasks )
		else:
			db.session.add(new_task)
			db.session.commit()
			return redirect("/")
	

@app.route("/mark-item/<int:task_id>")
def mark_task(task_id):						# Catching data which is posted to /mark-item url by the html button
	task = Todo.query.filter_by(id=task_id).first()
	task.state = not (task.state)
	db.session.commit()
	return redirect("/")

	
@app.route("/delete-item/<int:task_id>")
def delete_task(task_id):					# Catching data which is posted to /mark-item url by the html button
	task = Todo.query.filter_by(id=task_id).first()
	db.session.delete(task)
	db.session.commit()
	return redirect("/")
	
	
if __name__ == "__main__" :			# Don't run the app when this module is imported by any other program
	db.create_all()					# Creates the data structure(table) of given class
	app.run()
