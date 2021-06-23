from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import Courses, User
from .. import db,photos
from .forms import UpdateProfile,CourseForm
from flask_login import login_required,current_user
# import datetime

@main.route('/')
def index():

    title = 'Home - Welcome to Admission System'
  
    return render_template('index.html',title = title,current_user=current_user)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,date = user_joined)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/apply')
def apply():

    title = 'Apply Now'
  
    return render_template('apply.html',title = title)

@main.route('/programmes')
def programmes():

    title = 'Programmes'
  
    return render_template('programmes.html',title = title)

@main.route('/addCourse', methods = ['GET','POST'])
@login_required
def new_course():
    course_form = CourseForm()
    if course_form.validate_on_submit():
        course = Courses(title=course_form.title.data,description=course_form.description.data,institution=course_form.institution.data)
        db.session.add(course)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('main.programmes'))
    return render_template('create_course.html' , title='New Course', form=course_form ,  legend ='Create Course')
  
    

@main.route('/singleCourse')
def course():

    title = 'Course'
  
    return render_template('single_course.html',title = title)