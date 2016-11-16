# -*-coding:utf-8-*-
from app import db
from app.models import Role,User

#db.drop_all()
db.create_all()
'''user_role = Role(name='U34r')
user_anmf = User(username='af',role=user_role)
db.session.add(user_role)
db.session.add(user_anmf)
db.session.commit()

#print (User.query.filter_by(role = user_role).all())

print (Role.query.filter_by(name = 'User').first())

x = user_role.users
print x
print (x[0].role)'''
