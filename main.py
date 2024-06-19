from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import setuptools

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe's Image", validators=[DataRequired(), URL()])
    location = StringField("Cafe's Location", validators=[DataRequired()])
    has_sockets = SelectField("Do they have sockets?", choices=["Yes", "No"])
    has_toilet = SelectField("Is there a toilet?", choices=["Yes", "No"])
    has_wifi = SelectField("Is Wifi Available?", choices=["Yes", "No"])
    can_take_calls = SelectField("Do they take calls?", choices=["Yes", "No"])
    seats = StringField("How many seats are there?", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def show_all_cafes():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    return render_template("cafes.html", cafes=cafes)

@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=setuptools._distutils.util.strtobool(form.has_sockets.data),
            has_toilet=setuptools._distutils.util.strtobool(form.has_toilet.data),
            has_wifi=setuptools._distutils.util.strtobool(form.has_wifi.data),
            can_take_calls=setuptools._distutils.util.strtobool(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('show_all_cafes'))
    return render_template("add.html", form=form, is_edit=False)

@app.route("/delete/<int:id>")
def delete_cafe(id):
    cafe_to_delete = db.get_or_404(Cafe, id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('show_all_cafes'))

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_cafe(id):
    cafe = db.get_or_404(Cafe, id)
    if cafe.has_sockets:
        cafe.has_sockets = "Yes"
    else:
        cafe.has_sockets = "No"
    if cafe.has_toilet:
        cafe.has_toilet = "Yes"
    else:
        cafe.has_toilet = "No"
    if cafe.has_wifi:
        cafe.has_wifi = "Yes"
    else:
        cafe.has_wifi = "No"
    if cafe.can_take_calls:
        cafe.can_take_calls = "Yes"
    else:
        cafe.can_take_calls = "No"
    edit_from = CafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_from.validate_on_submit():
        cafe.name = edit_from.name.data
        cafe.map_url = edit_from.map_url.data
        cafe.img_url = edit_from.img_url.data
        cafe.location = edit_from.location.data
        cafe.has_sockets = setuptools._distutils.util.strtobool(edit_from.has_sockets.data)
        cafe.has_toilet = setuptools._distutils.util.strtobool(edit_from.has_toilet.data)
        cafe.has_wifi = setuptools._distutils.util.strtobool(edit_from.has_wifi.data)
        cafe.can_take_calls = setuptools._distutils.util.strtobool(edit_from.can_take_calls.data)
        cafe.seats = edit_from.seats.data
        cafe.coffee_price = edit_from.coffee_price.data
        db.session.commit()
        return redirect(url_for("show_all_cafes"))

    return render_template("add.html", form=edit_from, is_edit=True)

if __name__ == "__main__":
    app.run(debug=True)