from flask import Blueprint, render_template, request, flash, jsonify, request, redirect
from flask_login import login_required, current_user

from .mail import send_email
from .models import User, Availability, Appointment
from . import db
import json
from collections import defaultdict
from datetime import datetime, timedelta

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        type = request.form.get('type') #Gets the note from the HTML
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')


        # date = datetime.strptime(date, "%Y-%m-%d").date()
        # start_time = datetime.strptime(start_time, "%H:%M").time()
        # end_time = datetime.strptime(end_time, "%H:%M").time()


        if type==None:
            flash('Please select an appointment type.', category='error') 
        elif start_time==None or end_time==None:
            flash('Please select a start and end time.', category='error')
        elif start_time > end_time:
            flash('Please ensure start time is before end time.', category='error')
        else:
            new_availability = Availability(type=type, user_id=current_user.id, date=date,
                                            start_time=start_time, end_time=end_time)  #providing the schema for the note 
            db.session.add(new_availability) #adding the note to the database 
            db.session.commit()

            print("new_availability.id: ", new_availability.id)

            # Generate appointment events
            start_datetime = datetime.strptime(start_time, "%H:%M")
            end_datetime = datetime.strptime(end_time, "%H:%M")

            while start_datetime + timedelta(minutes=30) <= end_datetime:
                new_appointment = Appointment(
                    type=type,
                    mentor_id=current_user.id,
                    appointment_date=date,
                    start_time=start_datetime.strftime("%H:%M"),  # Convert time back to string
                    end_time=(start_datetime + timedelta(minutes=30)).strftime("%H:%M"),  # Convert time back to string
                    status="posted",
                    availability_id=new_availability.id
                )
                start_datetime += timedelta(minutes=30)
                db.session.add(new_appointment)
            db.session.commit()

            flash('Availability added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-availability', methods=['POST'])
def delete_availability():
    availability_data = json.loads(request.data)
    availability_id = availability_data['availabilityId']
    availability = Availability.query.get(availability_id)
    
    if availability and availability.user_id == current_user.id:
        # Delete associated appointments along with availability

        print("Deleting availability:", availability.id)
        print("Associated appointments:", availability.appointments)

        db.session.delete(availability)
        db.session.commit()

    return jsonify({})


@views.route('/admin', methods=['GET'])
@login_required
def display_users():
    users = User.query.all()  # Fetch all users from the database.
    return render_template('admin.html', user=current_user, users=users)


def get_availability_by_date(user):
    availabilities_by_date = defaultdict(list)
    for availability in user.availabilities:
        date = datetime.strptime(availability.start_time, "%Y-%m-%dT%H:%M:%S").date()
        availabilities_by_date[str(date)].append(availability)
    return availabilities_by_date


@views.route('/student-view', methods=['GET'])
@login_required
def student_view():

    # Fetch appointments associated with the current user
    appointments = Appointment.query.all()
    
    return render_template('student_view.html', user=current_user, appointments=appointments)


@views.route('/reserve/<appointment_id>', methods=['POST'])
@login_required
def reserve(appointment_id):
    student_id = request.form.get('student_id')
    appointment = Appointment.query.get(appointment_id)  # Use the correct parameter name
    
    if appointment and appointment.status == "posted":
        appointment.status = "reserved"
        appointment.student_id = student_id
        db.session.commit()

        student = User.query.get(appointment.student_id)
        mentor = User.query.get(appointment.mentor_id)

        if student and mentor:
            student_email = student.email
            student_email_subject = '{appointment_type} confirmation: {appointment_date} at {appointment_time}.'.format(appointment_type=appointment.type, appointment_date=appointment.appointment_date, appointment_time=appointment.start_time)
            student_email_content = 'Your {appointment_type} appointment with {mentor_name} is confirmed for {appointment_date} at {appointment_time}.'.format(appointment_type=appointment.type, mentor_name=mentor.first_name, appointment_date=appointment.appointment_date, appointment_time=appointment.start_time)

            mentor_email = mentor.email            
            mentor_email_subject = '{appointment_type} confirmation: {appointment_date} at {appointment_time}.'.format(appointment_type=appointment.type, appointment_date=appointment.appointment_date, appointment_time=appointment.start_time)
            mentor_email_content = 'Your {appointment_type} appointment with {student_name} is confirmed for {appointment_date} at {appointment_time}.'.format(appointment_type=appointment.type, student_name=student.first_name, appointment_date=appointment.appointment_date, appointment_time=appointment.start_time)

            send_email(mentor_email, mentor_email_subject, mentor_email_content) 
            send_email(student_email, student_email_subject, student_email_content)
            print("Email sent to student and mentor.")
        else:
            print("Student or mentor not found.")

    return redirect("/student-view")