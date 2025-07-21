from datetime import datetime

def get_absentee_template(student, absent_date=None):
    absent_date = absent_date or datetime.now().strftime('%Y-%m-%d')
    return f"""
    <html>
        <body>
            <p>Dear {student.parent_name},</p>
            <p>Your child <strong>{student.student_name}</strong> (Roll No: {student.roll_number}) 
            was absent from class on <strong>{absent_date}</strong>.</p>
            <p>If this is unexpected, please contact the school office.</p>
            <p>Regards,<br>School Administration</p>
        </body>
    </html>
    """
