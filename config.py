import os

basedir = os.path.abspath(os.path.dirname(_file_))

class Config:
    SECRET_KEY = 'kpi-secret-key'  # নিরাপত্তার জন্য পরিবর্তন করে নিও
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/kpi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')