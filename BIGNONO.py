"""
Running this script will mess with tables in the database,
only use it if you have just added new entities to the database
"""

from RecipeProject import app, bcrypt
from RecipeProject.DatabaseEntities import *

with app.app_context():
    db.create_all()

    user = User(email="brendan.battisti@gmail.com",
                username="BrendanBattisti",
                password=bcrypt.generate_password_hash("passw").decode('utf-8'))
    admin = User(email="admin@admin.com",
                username="admin",
                password=bcrypt.generate_password_hash("admin").decode('utf-8'))
    db.session.add(user)
    db.session.add(admin)
    db.session.commit()
