# we will set our routes here 
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views',__name__)
# we created our views called blueprint 

@views.route('/', methods=['GET', 'POST'])   # that means that whenver we go to / we will see the text HELLO apppear 
@login_required # now the user will not be able to acess the home page unless he is logged in
def home():
    if request.method =='POST':
     note_data = request.form.get('note')
     if len(note_data)<1:
        flash(' note is too short !', category='error')
     else:
        new_note = Note(data=note_data, user_id =current_user.id) 
        db.session.add(new_note)
        db.session.commit()
        flash('note added!', category='success')    
    return render_template('home.html', user= current_user)

""" this is just an example of another route inside the views blueprint
@views.route('/me')
def me():
    return "<h2>this is me</h2>"
"""

@views.route('/delete-note', methods=['POST'])
def deleteNote():
  if request.method =='POST': 
   note = json.loads(request.data)
   noteId = note['noteId']
   note = Note.query.get(noteId) 
   if note: 
      if note.user_id == current_user.id:
         db.session.delete(note)
         db.session.commit()
         
   return jsonify({})