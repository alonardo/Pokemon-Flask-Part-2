from flask import render_template, request, redirect, url_for, flash
import requests
from app import app
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import EditProfileForm, LoginForm, RegisterForm

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print('Code is here!')
    if request.method == 'POST':
        print('POST successful!')
        if form.validate_on_submit():
            print('I"M TRYING TO RUN!!!')
            try:
                new_user_data={
                    "first_name": form.first_name.data.title(),
                    "last_name": form.last_name.data.title(),
                    "email": form.email.data.lower(),
                    "password" : form.password.data,
                    "icon":form.icon.data
                }
                new_user_object = User()

                new_user_object.from_dict(new_user_data)

                new_user_object.save()
            except:
                print('I"M IN THE EXCEPT!')
                # Flash user Error
                flash("An Unexpected Error occurred", "danger")
                return render_template('register.html.j2', form=form)
            # Flash user here telling you have been register
            flash("Successfully registered, welcome to Pokemon Search! Please login to continue.", "success")
            return redirect(url_for('login'))

    return render_template('register.html.j2', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        edited_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                "icon":int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
            }
        user = User.query.filter_by(email=edited_user_data['email']).first()
        if user and user.email != current_user.email:
            flash('Email already exists!', 'danger')
            return redirect('edit_profile')
        try:
            current_user.from_dict(edited_user_data)
            current_user.save()
            flash('Profile updated!', 'success')
        except:
            flash('Error updating profile!', 'danger')
            return redirect('edit_profile')
        return redirect(url_for('index'))
    return render_template('register.html.j2', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print('login POST success')
        if form.validate_on_submit():
            email = form.email.data.lower()
            print(email)
            password = form.password.data
            print(password)

            u = User.query.filter_by(email=email).first()
            print('form validated!!')
            if u:
                print('u printed')
            if u.check_hashed_password(password):
                print('u.check printed')
                flash('Successfully logged in','success')
                login_user(u)
                return redirect(url_for('index'))
            flash("Incorrect Email/password Combo", "warning")
            return render_template('login.html.j2', form=form)

    return render_template('login.html.j2', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'info')
    return redirect(url_for('index'))

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string)
        
        data = response.json()
        poke_dict={
            "name": data['name'].title(),
            "ability":data['abilities'][0]["ability"]["name"].title(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"]
        }
            
        return render_template('pokemon.html.j2', pokemon=poke_dict)
        
    else:
        error = 'error'
        return render_template('pokemon.html.j2', poke=error)


