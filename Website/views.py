from flask import Blueprint, render_template, request,flash,redirect,url_for, session
from flask_login import login_required,current_user
from .models import User,Company,Job,Application
from . import db
import json
from .utils import scoring



views = Blueprint('views', __name__)

@views.route('/', methods = ['GET'])
def home():
    return redirect(url_for('auth.login'))


@views.route('/company', methods = ['GET', 'POST'])
# @login_required
def company():

    if "company" not in session:
        return redirect(url_for('auth.login'))
    
    company = session['company']
    logged_in_company = company['id']
    company_name = Company.query.filter_by(id = logged_in_company).first().name

 
    if request.method == 'POST':
        jobName = request.form.get('jobName')
        jobDescription = request.form.get('jobDescription')
        skills = request.form.get('skills')
        personalityType = request.form.get('personalityType')
        education = request.form.get('education')
        experience = request.form.get('experience')

        skillsContribution = request.form.get('skillsPercentage')
        experienceContribution = request.form.get('experiencePercentage')
        educationContribution = request.form.get('educationPercentage')
        personalityPercentage = request.form.get('personalityPercentage')

        new_job = Job(name = jobName, description = jobDescription, skills_required = skills, personality_required = personalityType,education_required = education,experience_required = experience, skills_contribution = skillsContribution,experience_contribution = experienceContribution, education_contribution = educationContribution,personality_contribution = personalityPercentage ,company_id = logged_in_company);
        db.session.add(new_job)
        db.session.commit()
        flash('Job created successfully', category='success')
        return redirect(url_for('views.company'))

    
    jobs = Job.query.filter_by(company_id = logged_in_company)
    # jobs = {}
    print("Logged in user is", current_user)
    return render_template("company.html", user = current_user, jobs = jobs, company_name = company_name )
 

@views.route('/applicant', methods = ['GET', 'POST'])
def applicant():
    jobs = Job.query.all()
    applications = Application.query.all()

    for application in applications:
        print("application-------------->", application)


    full_job_response = []

    for job in jobs:
        company_linked = Company.query.filter_by(id=job.company_id).first()
        jobResponse = JobResponse(id = job.id,name=job.name, description=job.description, skills_required = job.skills_required, company= company_linked.name)
        full_job_response.append(jobResponse)

    appliedIds = []
    for application in applications:
        if (application.user_id == current_user.id):
            appliedIds.append(application.job_id)

    print(f"Jobs applied to by {current_user.id} ======>",appliedIds)

    for job in full_job_response:
        if (job.id in appliedIds):
            print("I have applied to this job ===> ", job)
            job.user_has_applied = True
            application = Application.query.filter_by(job_id = job.id, user_id = current_user.id).first();
            job.matchPercentage = application.overall_percentage
            # job.matchPercentage = (application.percentage_score_skills + application.percentage_score_personality)/2

    jobs = full_job_response
    return render_template("applicant.html", user = current_user, jobs = jobs)


@views.route('/delete-job', methods = ['POST'])
def deleteJob():
    data = json.loads(request.data)
    jobId = data['jobId']
    job  = Job.query.get(jobId)

    if job:
        db.session.delete(job)
        db.session.commit()
        flash("Deleted job successfully", category="success")
    return "deleted"

@views.route('/apply-job', methods = ['POST'])
def applyJob():
    data = json.loads(request.data)
    jobId = data['jobId']
    job = Job.query.get(jobId)
    user = current_user

    print("-------------------------------------APPLYING JOB PROCESS--------------------------------------")
    print("Job requirements------------------------->", job.skills_required)
    print("user personality type----------------->", user.personality_type)
    print("user skills----------------->", user.skills)
    print("Job personality----------------->", job.personality_required)

    # calculate matching skills percentage
    skills_percentage = scoring.cosine_distance_countvectorizer_method(job.skills_required, user.skills)

    # calculate matching personality percentage
    personality_percentage = scoring.personality_matching_percentage(job.personality_required, user.personality_type)
    
    # calculating experience matching

    user_experience = user.experience_rating
    required_experience = job.experience_required
    print("User experience------------------------------->", user.experience)
    print("Required experience------------------------------->", job.experience_required)
    experience_percentage = ((float(user_experience)/ float(required_experience)) * 100)%100

    #education matching percentage
    user_education = user.degree
    required_education = job.education_required
    education_percentage = scoring.cosine_distance_countvectorizer_method(user_education, required_education)
    
    total_score = (0.5)*skills_percentage + (0.10)*personality_percentage + (0.10)*education_percentage + (0.30)*experience_percentage

    print("--------------------------------------PERCENTAGES--------------------------------------------")
    print("Skills percentage------------------------>", skills_percentage)
    print("Personality percentage------------------------>", personality_percentage)

    print("-----------------------------------END OF PERCENTAGES--------------------------------------")

    new_application = Application(user_id = user.id, job_id = job.id,percentage_score_skills = skills_percentage,percentage_score_personality = personality_percentage, percentage_score_education = education_percentage, percentage_score_experience = experience_percentage, overall_percentage = total_score);
    db.session.add(new_application)
    db.session.commit()
    flash("Job applied successfully", category='success')

    return {'total_score': total_score}



@views.route('/modal')
def modal():
    db.drop_all()
    full_job = {}
    jobs = Job.query.all()
    return render_template('modal.html', jobs = jobs, user = current_user)


@views.route('/viewCandidates/<int:job_id>', methods = ['GET', 'POST'])
def view_applied(job_id):
    applications = Application.query.filter_by(job_id = job_id);

    totalApplication = 0
    for application in applications:
        totalApplication += 1

    total_applicants = []

    if(totalApplication == 0):
        flash("No applied candidates currently", category="error")
        return redirect(url_for('views.company'))

    for application in applications :
        job = Job.query.filter_by(id = application.job_id).first()
        user = User.query.filter_by(id = application.user_id).first()

        applicant =  ApplicationResponse(applicant_name=user.firstName, 
                                        applicant_skills=user.skills,
                                        applicant_personality=user.personality_type,
                                        job_name = job.name,
                                        job_personality=job.personality_required,
                                        email = user.email,
                                        skills_percentage= application.percentage_score_skills,
                                        personality_percentage = application.percentage_score_personality,
                                        education_percentage= application.percentage_score_education,
                                        experience_percentage= application.percentage_score_experience,
                                        total_score= application.overall_percentage)
        total_applicants.append(applicant)
    
    applicants = total_applicants
    applicants.sort(key=  lambda applicant:applicant.total_score, reverse=True)
     
    position = 1

    for application in applicants:
        application.position = position
        position += 1

    return render_template("viewCandidates.html", applicants = applicants)



    

class ApplicationResponse:

    def __init__(self, applicant_name, applicant_skills, applicant_personality, job_name, job_personality, email, skills_percentage, personality_percentage, education_percentage, experience_percentage, total_score):
        self.applicant_name = applicant_name
        self.applicant_skills = applicant_skills
        self.applicant_personality = applicant_personality
        self.job_name = job_name
        self.job_personality = job_personality
        self.skills_percentage = skills_percentage
        self.personality_percentage =   round(personality_percentage,2)
        self.experience_percentage = round(experience_percentage,2)
        self.education_percentage = round(education_percentage,2)
        self.email = email;
        self.total_score = total_score;
        # self.total_score = (self.skills_percentage + self.personality_percentage) / 2 
        self.position = 0



class JobResponse:

    def __init__(self,id, name, description, skills_required, company):
        self.id = id
        self.name = name
        self.description = description
        self.skills_required = skills_required
        self.company = company
        self.user_has_applied = False;
        self.matchPercentage = 0