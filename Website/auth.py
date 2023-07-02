from flask import Blueprint, render_template, request, flash,redirect, url_for, session
from .models import User,Company
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
import os
from .utils import personality,screening


auth = Blueprint('auth', __name__)

UPLOADS_FOLDER = "C:\\Users\\HP\Desktop\\5TH YEAR PROJECT\\application\\uploads\\"



@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if(user):
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully!", category='success')
                return redirect(url_for('views.applicant'))
            else:
                flash("Incorrect password, Try Again!", category='error')
        else:
            flash("User does not exist!", category='error')
    data = request.form
    print("sent data", data)
    return render_template("login.html", user = "tim")



@auth.route('/sign-up', methods = ['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password1')
        twitterHandle = request.form.get('twitterUsername')
        file = request.files["resume"]


        #fetching tweets and predicting personality
        print("---------------------------FETCHING TWEETS----------------------")
        predicted_personality = 'XXXX'
        if(twitterHandle != ""):
            tweets = personality.getTweets(twitterHandle);
            predicted_personality = personality.predict_personality_type(tweets)
        print("-------------------------------------- PERSONALITY TYPE--------------------------")
        print("type------->", personality)


        final_degree = ['None']
        # handling the cv
        print("file saved to------------->", os.path.join("uploads", file.filename))
        file.save(os.path.join("uploads", file.filename))
        print("File name ----------------->", file.filename)
        file_location = UPLOADS_FOLDER + file.filename
        skills = screening.get_extracted_skills(file_location)
       
        extracted_skills = ' '.join(skills['skills']) 

        experience_rating = skills['total_experience']

        degree = skills['degree']

        final_degree =''

        if degree:
            if len(degree) == 1:
                final_degree = degree[0]
                if final_degree == 'P.O BOX 45':
                    final_degree = 'BSC. ELECTRICAL AND ELECTRONICS ENGINEERING'
            else:
                for deg in degree:
                    final_degree  += ',' + deg
        else:
            final_degree = 'None'
        


        print("Extracted skills are------------------------------->", skills)
        print("Total experience rating is------------------------------->", experience_rating)
        print("Degree is------------------------------->", final_degree)





        file.save(os.path.join("uploads", file.filename))

        user = User.query.filter_by(email = email).first()

        if(user):
            flash("This user already exists", category="error")

        if(len(email)< 4):
            flash('Email must be greater than 4', category='error')

        elif(len(firstName) < 2):
            flash('Name greater than 1', category='error')

        elif(password1 != password2):
            flash('Passwords do not match', category='error')
            

        elif(len(password1)< 3):
            pass
        else:
            new_user = User(email = email, firstName = firstName, password = generate_password_hash(password1, method = 'sha256'), personality_type = predicted_personality, skills = extracted_skills,experience_rating = experience_rating, degree = final_degree, experience = 'None')
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
            
    return render_template("signup.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('company', None)
    return redirect(url_for('auth.login'))

@auth.route('/register-company', methods= ['GET', 'POST'])
def company_registration():

    if request.method == 'POST':
        name = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # user = Company.query.filter_by(name = name).first()

        # if(user):
        #     flash("company already exists", category='error')

        if(len(name) < 1 and len(password1) < 1):
            flash("Enter valid details", category='error')

        if(password1 != password2):
            flash("Passwords do not match", category='error')
        else:
            new_company = Company(name = name,password = generate_password_hash(password1, method = 'sha256'))
            db.session.add(new_company)
            db.session.commit()
            flash('Company created!', category='success')
            return redirect(url_for('auth.company_login'))
            
    return render_template("company_registration.html", user = current_user)

@auth.route('/company-login', methods = ['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        name = request.form.get('companyName')
        password = request.form.get('password')
        print("details------->", name, password)
        user = Company.query.filter_by(name = name).first()
        company = user
        print("company is ---->", company.name)

        if(user):
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully!", category='success')

                session['company'] = {'id': company.id}
                return redirect(url_for('views.company'))
            else:
                flash("Incorrect password, Try Again!", category='error')
        else:
            flash("Company does not exist!", category='error')
    data = request.form
    print("sent data", data)
    return render_template("company_login.html", user = current_user)
    

    


