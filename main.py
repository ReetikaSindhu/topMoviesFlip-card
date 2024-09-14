from flask import Flask, render_template, redirect, url_for, request
import requests
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField
from wtforms.validators import DataRequired
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB

class base(DeclarativeBase):
    pass
# CREATE TABLE
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movie.db'
db=SQLAlchemy(model_class=base)
db.init_app(app)

class Movie(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    title:Mapped[String]=mapped_column(String(50),unique=True,nullable=False)
    year:Mapped[Integer]=mapped_column(Integer,nullable=False)
    rating:Mapped[Float]=mapped_column(Float,nullable=True)
    description:Mapped[String]=mapped_column(String(250),nullable=False)
    ranking:Mapped[Integer]=mapped_column(Integer,nullable=False)
    review:Mapped[String]=mapped_column(String(250),nullable=True)
    img_url:Mapped[String]=mapped_column(String(100),nullable=True)
    

# with app.app_context():
#     db.create_all()
# new_movie = Movie(
#     title="DDLJ1",
#      year=2002,
#      description="Romance movie ",
#      rating=7.3,
#      ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#  )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()
class findform(FlaskForm):
     title=StringField(label="Title of movie:",validators=[DataRequired()])
class Ratemovie(FlaskForm):
     rating=StringField(label='NEW RATING',validators=[DataRequired()])
class confirm(FlaskForm):
     pass
class addmovie(FlaskForm):
     title=StringField(label="MOVIE TITLE",validators=[DataRequired()])
     year=StringField(label="Year :",validators=[DataRequired()])
     ranking=StringField(label="Ranking :",validators=[DataRequired()])
     rating=FloatField(label="Rating" ,validators=[DataRequired()])
     review=StringField(label="Review",validators=[DataRequired()])
     description=StringField(label="Description",validators=[DataRequired()])
     img_url=StringField(label='ADD image url',validators=[DataRequired()])
@app.route("/")
def home():
        result=db.session.execute(db.select(Movie).order_by(Movie.rating))
        all_movies=result.scalars().all()
        for i in range(len(all_movies)):
             all_movies[i].ranking=len(all_movies)-i
        db.session.commit()
        return render_template("index.html",movie=all_movies)

@app.route('/edit',methods=['GET','POST'])
def editfun():
     
     rateform=Ratemovie()
     abc=request.args.get("id")
     print("now editing 1..............")
     movie1212=db.get_or_404(Movie,abc)
     print("movie")
     print(movie1212)
     print("movie1nnnnnnnnnnnn")
     if request.method=='POST':
          if rateform.validate_on_submit():
               print("validate")
               movie1212.rating=float(rateform.rating.data)
               db.session.commit()
               print("now editing 2..............")
               return (redirect(url_for('home')))
     return  render_template('edit.html',movie=movie1212,form=rateform)
@app.route('/delete',methods=['GET'])
def deletefun():
     abc=request.args.get("id")
     moviie32=db.get_or_404(Movie,abc)
     db.session.delete(moviie32)
     db.session.commit()
     return redirect(url_for('home'))
@app.route('/add_movie',methods=['GET','POST'])
def addmovie_fun():
     add=addmovie()
     if request.method=='POST':
          if add.validate_on_submit():
               new_movie=Movie(
                    title=add.title.data,
                    year=add.year.data,
                    rating=add.rating.data,
                    ranking=add.ranking.data,
                    description=add.description.data,
                    review=add.review.data,
                    img_url=add.img_url.data
               )              
               db.session.add(new_movie)
               db.session.commit()
     return render_template('add.html',form=add)
@app.route('/find_movie',methods=['GET','POST'])
def findmovie():
    find = findform()
    if request.method == 'POST':
        print("Request method is POST")
        print(f"Form data: {request.form}")

        if find.validate_on_submit():
            print("Form validation passed")
            query = find.title.data
            try:
                movielist = Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()
                print("Movies found")

                if not movielist:
                    print("No movies found")
                    return render_template('find.html', form=find, message="No movies found.")
                
                return render_template('confirm.html', movie=movielist)
            except Exception as e:
                print(f"Error occurred: {e}")
                return render_template('find.html', form=find, message="An error occurred. Please try again.")
    
    # Handle GET request or form validation failure
    return render_template('find.html', form=find)
     # find=findform()
     # if request.method=='POST':
     #      print("Request method is POST")
     #      print(f"Form data: {request.form}")
     #      if find.validate_on_submit():
     #        print("validate find")
     #        query=find.title.data
     #        try:
     #         movielist=Movie.query.filter(Movie.title.ilike(f'{query}')).all()
     #         print("found movie")
     #         if not movielist:
     #              print("11")
     #              return render_template('find.html',form=find)
     #         print("1")
             
     #         return render_template('confirm.html',movie=movielist)
            
     #        except Exception as e:
     #           print("2")
     #           return render_template('find.html',form=find)
           

     # return render_template('find.html',form=find)
if __name__ == '__main__':
    app.run(debug=True)