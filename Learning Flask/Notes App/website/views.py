from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#define as a blueprint (kinda like urls.py from django)
views = Blueprint('views', __name__)

##-----------------------------------------------------------HOME:
@views.route('/')
def home():
    notes = Note.query.all()
    return render_template('home.html', user=current_user, notes=notes)


##----------------------------------------------------------NOTES:
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('An empty note cannot be added!', category='error')
        else:
            newNote = Note(text=note, userID=current_user.id)
            db.session.add(newNote)
            db.session.commit()
            flash('Note added!', category='success')
    
    return render_template('notes.html', user=current_user)


##-----------------------------------------------------DELETE_NOTE:
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteID']
    note = Note.query.get(noteID)
    
    if note:
        if note.userID == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')

    return jsonify({})