from .extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    prn = db.Column(db.String(20), unique=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100))
    student_phone = db.Column(db.String(15))
    parent_name = db.Column(db.String(100))
    parent_email = db.Column(db.String(100), nullable=False)
    parent_phone = db.Column(db.String(15))
    class_section = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Student {self.roll_number} - {self.student_name}>'