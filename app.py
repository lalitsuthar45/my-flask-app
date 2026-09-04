from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///lalit.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Myapp(db.Model):
     sno = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(200), nullable=False)
     desc = db.Column(db.String(500), nullable=False)
     date_created =  db.Column(db.DateTime, default=datetime.utcnow)

     def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST': 
        title=(request.form['title'])
        desc=(request.form['desc'])
        lalit = Myapp(title=title, desc=desc)
        db.session.add(lalit)
        db.session.commit()
    
    allMyapp = Myapp.query.all()
    return render_template('index.html', allMyapp=allMyapp)

@app.route('/show')
def products():  # <-- Changed to a unique function name
     allMyapp = Myapp.query.all()
     print(allMyapp)
     return 'This is the products page'
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  

    # 2. Agar form submit hua hai (POST)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        lalit = Myapp.query.filter_by(sno=sno).first()
        lalit.title = title
        lalit.desc = desc
        db.session.add(lalit)
        db.session.commit()
        return redirect("/")   # Update hone ke baad home page par redirect karein
  # 1. Pehle data ko find karein (Ye GET aur POST dono ke liye kaam karega)
    lalit = Myapp.query.filter_by(sno=sno).first()
    # 3. Agar page sirf khola gaya hai (GET)
    return render_template('update.html', lalit=lalit)
@app.route("/delete/<int:sno>")
def delete(sno):
    # Pehle us record ko database se sno ke zariye dhoondho:
    lalit = Myapp.query.filter_by(sno=sno).first()
    
    # Phir delete karo:
    if lalit:
        db.session.delete(lalit)
        db.session.commit()
        
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)