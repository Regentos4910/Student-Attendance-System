from flask import Blueprint, request, flash, redirect, url_for, render_template
import pandas as pd
from app.models import Student
from app.extensions import db

import_bp = Blueprint('import', __name__)

@import_bp.route('/', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
            
        if file and file.filename.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(file)
                new_students = 0
                
                for _, row in df.iterrows():
                    # Check if student already exists
                    if not Student.query.filter_by(roll_number=row['Roll Number']).first():
                        student = Student(
                            roll_number=row['Roll Number'],
                            prn=row['PRN'],
                            student_name=row['Student Name'],
                            student_email=row['Student Email'],
                            student_phone=row['Student Phone'],
                            parent_name=row['Parent Name'],
                            parent_email=row['Parent Email'],
                            parent_phone=row['Parent Phone'],
                            class_section=row['Class']
                        )
                        db.session.add(student)
                        new_students += 1
                
                db.session.commit()
                flash(f'Successfully imported {new_students} new students!', 'success')
                return redirect(url_for('main.index'))  # Redirect to main student list
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error importing data: {str(e)}', 'error')
                return redirect(request.url)
                
    return render_template('import.html')