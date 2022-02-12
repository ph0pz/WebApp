from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# @views.route('/Personal', methods=['GET', 'POST'])
# @login_required
# def Personal():
#     return render_template("Personal.html", user=current_user)


# @views.route('/YourProfile', methods=['GET', 'POST'])
# @login_required
# def YourProfile():
#     return render_template("YourProfile.html", user=current_user)



@views.route('/', methods=['GET', 'POST'])
@login_required
def Personal():
    if request.method == 'POST':
        note = request.form.get('foo')
        flash(note)
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Type added!', category='success')

    return render_template("Personal.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

