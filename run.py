from flask import *
import sqlite3
from functools import wraps

app=Flask(__name__)


app.secret_key="shibin"
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('you need to login first.')
			return redirect(url_for("/"))
	return wrap
@app.route("/",methods=['GET','POST'])
def login():
	error=None
	if request.method =='POST':
		if request.form['username'] != 'shibin' or request.form['password'] != 'justdoit':
			error ='invalid password or user name please try again'
		else:
			session['logged_in'] = True
			flash('your just logged in!')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)



@app.route("/home", methods=['GET','POST'])
@login_required
def home():
	if request.method=='GET':
		db=sqlite3.connect('blog.db')
		cur=db.execute('''SELECT * FROM POSTS''')
		posts = [dict(title=row[0],comment=row[1]) for row in cur.fetchall()]
		#cur=db.execute("SELECT * FROM blogspot ORDER BY id desc")
		#posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in cur.fetchall()]

		db.close()
		return render_template("home.html",posts=posts)

	else:
		db=sqlite3.connect('blog.db')
		db.execute("INSERT INTO POSTS VALUES (?,?)",
				[request.form['title'],request.form['comment']])
		db.commit()
		return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('your just logged out!')
	return redirect(url_for('/'))

@app.route("/guest")
def guest():
	db=sqlite3.connect('blog.db')
	cur=db.execute('''SELECT * FROM POSTS''')
	posts = [dict(title=row[0],comment=row[1]) for row in cur.fetchall()]
	db.close()
	return render_template("home2.html",posts=posts)


app.run(debug=True)
