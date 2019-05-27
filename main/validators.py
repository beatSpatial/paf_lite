import csv
import os
import io

from django.core.exceptions import ValidationError

#REQUIRED_HEADER = ['username', 'password', 'firstname', 'lastname', 'preferredname', 'email', 'course', 'group']
REQUIRED_HEADER = ['username','password',
                   'firstname','lastname','preferredname',
                   'email','city','country',
                   'idnumber',
                   'course1','group1','role1',
                   'course2','group2','role2',
                   'course3','group3','role3',
                   'course4','group4','role4',
                   'course5','group5','role5',
                   'course6','group6','role6',
                   'course7','group7','role7',
                   'course8','group8','role8',
                   'course9','group9','role9',
                   'course10','group10','role10',
                   'course11','group11','role11',
                   'course12','group12','role12',
                   'course13','group13','role13']


def csv_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if str(ext) != '.csv':
        raise ValidationError("Must be a csv file")
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')
    header_ = next(reader)[0].split(',')
    if header_[-1] == '':
        header_.pop()
    required_header = REQUIRED_HEADER
    if required_header != header_:
        raise ValidationError('Invalid File. Valid header is :\
                              "username","password",\
                   "firstname","lastname","preferredname",\
                   "email","city","country",\
                   "idnumber",\
                   "course1","group1","role1",\
                   "course2","group2","role2",\
                   "course3","group3","role3",\
                   "course4","group4","role4",\
                   "course5","group5","role5",\
                   "course6","group6","role6",\
                   "course7","group7","role7",\
                   "course8","group8","role8",\
                   "course9","group9","role9",\
                   "course10","group10","role10",\
                   "course11","group11","role11",\
                   "course12","group12","role12",\
                   "course13","group13","role13"')
    return True
