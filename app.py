#these following lines to import some libraries
from flask import Flask , render_template, request,redirect , session
import dataset

#this line to define flask
app =  Flask(__name__)

#this line to connect the app to database
db = dataset.connect('sqlite:///scholars6.db')

#this line to make the password unique
app.secret_key= "s90183192083810298apsoduaspdiohashk"
def start():
	db = dataset.connect('sqlite:///scholars6.db')
	studentsTable = db["students"]

	students_entry = {"name" : "akram" ,"desc": "Akram is studying computer science in one of the top schools in the world",
	 "img":"ak11.jpg"}
	students_entry2={"name":"Ramadan Alagha","desc":"Ramadan is student who study Accounting at the American university in Cairo"
	 , "img":"ramc.jpg"}
	students_entry3={"name":"Khaled Alhendawi","desc":"Khaled is the most intellegent student who is studying computer science"
	,"img":"khaled.jpg"}
	studentsTable.insert(students_entry)
	studentsTable.insert(students_entry2)
	studentsTable.insert(students_entry3)
# start()
#these following lines to give the homepage a route
@app.route('/')
def home():
	return render_template('homepage.html')

@app.route("/register" , methods=["POST" , "GET"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		#these lines to request data which filled in the html page
		form=request.form
		email = form["email"]
		username = form["username"]
		password = form["password"]
		firstname=form["firstname"]
		gender = form["radios"]
		lastname=form["lastname"]
		email = form["email"]
		hometown = form["hometown"]
		website = form["website"]
		password = form["password"]
		#this to put them in a table
		db = dataset.connect('sqlite:///scholars5.db')

		usersTable = db["users"]
		entry = {"email" : email ,"username":username , "password":password , "firstname" : firstname , "lastname":lastname , "hometown":hometown , "website" : website , "gender":gender}
		#this to check if the username available or not, if available> insert it and return the data
		if len(list(usersTable.find(username=username)))==0:
			print 'sike'
			usersTable.insert(entry)
			return render_template("register.html" , value=False, email=email ,username=username , password=password , firstname=firstname , lastname=lastname  , hometown=hometown , website=website , gender=gender)
		#this > if the user name taken, return the register page
		else:
			print 'nope', username
			# taken = 1
			# return  '<div class="w3-container w3-green"><p> Sorry this user is not available <a href="/login">click here to login</a></p></div>'
			return render_template("register.html",value=True)


@app.route("/login" , methods=["POST" , "GET"])
def login():
	if request.method == "GET":
		if "failed" in session:
			failed =True
			session.pop("failed", None)
			return render_template("login.html"  , failed=failed )
		if "erorr" in session:
			message= True
			session.pop("erorr", None)
			return render_template("login.html" , message=message )
		if "username" in session:
			return redirect ("/")
		return render_template("login.html")
	else:
			form=request.form
			username = form["username"]

			password = form["password"]
			db = dataset.connect('sqlite:///scholars6.db')
			usersTable = db["users"]

			if len(list(usersTable.find(username=username , password=password)))==0:
				session["failed"]="failed"
				return redirect("/login")
			else:
				session["username"]=username
				return redirect ("/")
@app.route('/germany')
def germany():
	db = dataset.connect('sqlite:///scholars6.db')

	studentsTable = db["students"]
	data = studentsTable.find_one(name="Khaled Alhendawi")
	return render_template('germany.html', data=data)

@app.route('/khaled',methods=["POST","GET"])
def khaled():

	if request.method=="GET":
		return render_template ('mhma.html' )
	elif request.method=="POST":
		db = dataset.connect('sqlite:///scholars6.db')

		name= request.form['name']
		subject=request.form['subject']
		email=request.form['email']
		message=request.form['message']
		scholars_contact=db["contactus"]
		table_entry={"message":message, "email":email,"subject":subject,"name":name}
		scholars_contact.insert(table_entry)
		return render_template('khaled.html')
@app.route('/america')
def america():
	db = dataset.connect('sqlite:///scholars6.db')
	studentsTable = db["students"]
	data = studentsTable.find_one(name="akram")

	return render_template('america.html' , data = data)

@app.route('/akram', methods =["POST" , "GET"])

def akram():

	if request.method=="GET":
		return render_template ('akram.html' )
	elif request.method=="POST":
		db = dataset.connect('sqlite:///scholars6.db')
		name= request.form['name']
		subject=request.form['subject']
		email=request.form['email']
		message=request.form['message']
		scholars_contact=db["contactus"]
		table_entry={"message":message,"email":email,"subject":subject,"name":name}
		scholars_contact.insert(table_entry)
		return render_template("akram.html",message=message,email=email,subject=subject,name=name)

@app.route('/egypt')
def egypt():
	db = dataset.connect('sqlite:///scholars6.db')

	studentsTable = db["students"]
	data = studentsTable.find_one(name="Ramadan Alagha")
	return render_template('egypt.html', data=data)
@app.route('/mhma',methods=["POST","GET"])
def mhma():
	print request.method
	if request.method=="GET":
		return render_template ('mhma.html' )
	elif request.method=="POST":
		db = dataset.connect('sqlite:///scholars6.db')

		name= request.form['name']
		subject=request.form['subject']
		email=request.form['email']
		message=request.form['message']
		scholars_contact=db["contactus"]
		table_entry={"message":message, "email":email,"subject":subject,"name":name}
		scholars_contact.insert(table_entry)
		return render_template("mhma.html")
@app.route("/logout")
def logout():
	if "username" in session:
   		session.pop("username", None)
   		return redirect ("/")
	else:
		return redirect("/")
@app.route("/list")
def showAll():
	if "username" in session:
		users=db["users"]
		allUsers =list(users.all())
		return render_template("lists.html" , users =allUsers)
	else:
		session["erorr"]="Please login first"
		return redirect("/login")
if __name__ =='__main__':
	app.run(debug= True,port=5910)		