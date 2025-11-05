from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "admin"  

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        if username == "admin" and password == "123":
            session['user'] = username
            flash("Login successful ", "success")
            return redirect('/')
        else:
            flash("Invalid username or password ", "danger")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully ", "info")
    return redirect('/login')


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added ", "success")
        return redirect('/')

    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

 
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'user' not in session:
        return redirect('/login')
    
    todo = Todo.query.get_or_404(sno)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        flash("Todo updated ✅", "success")
        return redirect('/')

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    if 'user' not in session:
        return redirect('/login')

    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted 🗑", "warning")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
