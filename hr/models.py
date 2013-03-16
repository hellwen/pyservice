from flask.ext.login import UserMixin
from pyservice.extensions import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.dept_name


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.job_name


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    emp_code = db.Column(db.String(20), unique=True)
    emp_name = db.Column(db.String(50), unique=True)

    ## public info
    work_email = db.Column(db.String(100))
    work_phone = db.Column(db.String(50))
    work_mobile = db.Column(db.String(50))
    office_location = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey(Department.id))
    department = db.relationship(Department, foreign_keys=department_id, backref='dept+')
    job_id = db.Column(db.Integer, db.ForeignKey(Job.id))
    job = db.relationship(Job, foreign_keys=job_id, backref='job+')

    ## personal info
    gender_id = db.Column(db.Integer)
    id_card = db.Column(db.String(50))
    home_addr = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    ## other info
    remark = db.Column(db.Text)
    date_of_leaved = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.emp_name
