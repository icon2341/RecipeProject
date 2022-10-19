"""
Runs the flask application
Author: Group 7 CSCI 320 01-02

RUNNING INSTRUCTIONS:

if in pycharm
you can do "cntl + shift + f10" and it will attempt to run this file and create a run config, that will run the flask server
note you will need to run

COPY PASTE THIS INTO YOUR TERMINAL (ALT-F12):

pip install flask-wtf flask wtforms flask_sqlalchemy SQLAlchemy

"""
from RecipeProject import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
