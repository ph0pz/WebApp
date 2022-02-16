from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note,User
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
        while True:
            return redirect(url_for("views.match"))
        
    return render_template("Personal.html", user=current_user)

@views.route('/match', methods=['GET', 'POST'])
def match():
    
    flash("dd")
    Notes = Note.query.all()
    for data in Notes:
        if current_user.id == data.user_id:
            personal=data.data
            flash(personal)
            if personal =="ENTJ": return creatematch("ISFP","INFP","ESFP")
            elif personal =="ENTP":return creatematch("ISFJ","ISTJ","ENTP") 
            elif personal =="INTJ":return creatematch("ESFP","ESTP","ISFP")  
            elif personal =="INTP":return creatematch("ESFJ","ENFJ","ISFJ")  
            elif personal =="ESTJ":return creatematch("INFP","ISFP","INTP")  
            elif personal =="ESFJ":return creatematch("INTP","ISTP","ENTP")  
            elif personal =="ISTJ":return creatematch("ENFP","ENTP","ISFP")  
            elif personal =="ISFJ":return creatematch("EMTP","ENFP","INTP")  
            elif personal =="ENFJ":return creatematch("ISTP","INTP","ESTP")  
            elif personal =="ENFP":return creatematch("ISTJ","ISFJ","ESFJ")  
            elif personal =="INTJ":return creatematch("ESTP","ESFP","ISTP")  
            elif personal =="INFP":return creatematch("ESTJ","ENTJ","INTJ")  
            elif personal =="ESTP":return creatematch("INFJ","INTJ","ENFJ")  
            elif personal =="ESFP":return creatematch("INTJ","INFJ","ENTJ")  
            elif personal =="ISTP":return creatematch("ENFJ","ESFJ","INFJ") 
            elif personal =="ISFP":return creatematch("ENTJ","ESTJ","INTJ") 
    

@views.route('/creatematch', methods=['GET', 'POST'])
def creatematch(type1,type2,type3):
    Notes = Note.query.all()
    Users  = User.query.all()
    result=[]
    for data_in_notes in Notes: #เรียกข้อมูลจากNote
        if type1 == data_in_notes.data: #ถ้าtype1==นิสัย
            for User_in_user in Users: #ดึงข้อมูลจากuserทั้งหมด
                if User_in_user.id==data_in_notes.user_id: #เทียบไอดีของuser ถ้าเท่ากับidของnote
                    result.append(User_in_user.first_name) #ใส่ชื่อไปในlist

    for data_in_notes in Notes:
        if type2 == data_in_notes.data:
            for User_in_user in Users:
                if User_in_user.id==data_in_notes.user_id:
                    result.append(User_in_user.first_name)

    for data_in_notes in Notes:
        if type3 == data_in_notes.data:
            for User_in_user in Users:
                if User_in_user.id==data_in_notes.user_id:
                    result.append(User_in_user.first_name)
    flash(result)
    
    return render_template("mainApp.html", user=current_user)

def result():
    return result




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

