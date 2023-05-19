from flask import Flask,render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
     sr_no = db.Column(db.Integer,primary_key=True)
     title = db.Column(db.String(100),nullable=False)
     desc = db.Column(db.String(100),nullable=False)
     date_created = db.Column(db.DateTime,default=datetime.utcnow)

     def __resp__(self) -> str:
          return f"{self.title} - {self.desc}"
     
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sr_no>', methods=['GET', 'POST'])
def update(sr_no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', todo=todo)


if __name__=="__main__":
    
    app.run(debug=True)