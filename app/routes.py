from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Student
from app.extensions import db
from datetime import datetime
import pandas as pd

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    class_filter = request.args.get('class_filter')
    query = Student.query
    
    if class_filter:
        query = query.filter(Student.class_section == class_filter)
    
    students = query.order_by(Student.roll_number).all()
    class_sections = db.session.query(Student.class_section).distinct().all()
    class_sections = [section[0] for section in class_sections]
    
    return render_template('students.html',
                         students=students,
                         class_sections=class_sections,
                         selected_class=class_filter,
                         datetime=datetime)

@main_bp.route('/send-email', methods=['POST'])
def send_emails():
    selected_students = request.form.getlist('student_ids')
    today = datetime.now().strftime("%Y-%m-%d")
    
    for student_id in selected_students:
        student = Student.query.get(student_id)
        if student:
            # In a real implementation, this would use Outlook API
            print(f"Sending email to {student.parent_email}")
            print(f"Subject: Attendance Alert for {student.student_name}")
            print(f"Body: Your child was absent on {today}")
    
    flash(f"Emails sent to {len(selected_students)} parents", 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/send-test-email/<int:student_id>')
def send_test_email(student_id):
    student = Student.query.get_or_404(student_id)
    
    # This is just for testing - in production use Outlook API
    print("="*50)
    print(f"TEST EMAIL TO: {student.parent_email}")
    print(f"SUBJECT: Attendance Notification for {student.student_name}")
    print(f"BODY:")
    print(f"Dear {student.parent_name},")
    print(f"\nYour child {student.student_name} (Roll No: {student.roll_number})")
    print(f"was absent from class today ({datetime.now().strftime('%Y-%m-%d')}).")
    print("\nRegards,\nSchool Administration")
    print("="*50)
    
    flash(f"Test email content printed to console for {student.student_name}", 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_details.html', student=student)

@main_bp.route('/send-batch-emails', methods=['POST'])
def send_batch_emails():
    from app.outlook import send_outlook_email
    from app.email_templates import get_absentee_template
    
    student_ids = request.form.getlist('student_ids')
    absent_date = request.form.get('absent_date', datetime.now().strftime('%Y-%m-%d'))
    
    success_count = 0
    for student_id in student_ids:
        student = Student.query.get(student_id)
        if student:
            email_sent = send_outlook_email(
                parent_email=student.parent_email,
                subject=f"Absence Notification - {absent_date}",
                body=get_absentee_template(student, absent_date)
            )
            if email_sent:
                success_count += 1
    
    flash(f"Successfully sent {success_count}/{len(student_ids)} emails", 'success')
    return redirect(url_for('main.index'))
