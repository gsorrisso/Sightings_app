from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route('/profile_page')
def profile_page():
    
    user = User.get_all(
        {
            'id' : session['user_id']
        }
    )

    if 'user_id' not in session:
        return redirect('/')
    sightings = Sighting.get_all()
    return render_template('user_page.html', user=user,sightings=sightings)

@app.route('/new_sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('new_sighting.html')

@app.route('/add_sighting', methods=['POST'])
def add_sighting():
    
    Sighting.save(
        {
        'user_id': session['user_id'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date': request.form['date'],
        'num_of_sas': request.form['num_of_sas'],
        } 
    )
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new_sighting')
    return redirect('/profile_page')

@app.route('/sighting/<int:id>')
def view_sighting(id):
    
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_id({'id': id})
    return render_template('view_sighting.html',sighting=sighting)

@app.route('/edit_sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_id( { 'id': id } )
    return render_template('edit_sighting.html',sighting=sighting)

@app.route('/update_sighting/<int:id>', methods=['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect('/edit_sighting/<int:id>')

    sighting_data = {
        'id': id,
        'location': request.form['location'],
        'description': request.form['description'],
        'date': request.form['date'],
        'num_of_sas': request.form['num_of_sas'],
    }
    Sighting.update_sighting(sighting_data)
    return redirect('/profile_page')

@app.route('/delete_sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')

    Sighting.delete_sighting({'id':id})
    return redirect('/profile_page')