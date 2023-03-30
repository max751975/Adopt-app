"""Adopt application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def home():
    pets = Pet.query.all()
    return render_template("pets/pet_list.html", pets=pets)

@app.route("/pets/new", methods=["GET", "POST"])
def add_new_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        
        pet = Pet(name=name, species=species, age=age, photo_url=photo_url, notes=notes)
        
        db.session.add(pet)
        db.session.commit()
        
        return redirect("/")
    else:
        return render_template("pets/new_pet_form.html", form=form)

@app.route("/pets/<int:pet_id>")
def show_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template("/pets/show_pet.html", pet=pet)
        
@app.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form =  EditPetForm(obj=pet)
    species = pet.species
    age = pet.age
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        
        return redirect(f"/pets/{pet.id}")
    else:
        return render_template("pets/edit_pet_form.html", form=form, pet=pet)
    
@app.route('/pets/<int:pet_id>/delete', methods=["POST"])
def pet_delete(pet_id):    
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()

    return redirect("/")