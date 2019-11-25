import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('issues.sqlite')

class User(UserMixin, Model):
	name = CharField()
	department = CharField()
	email = CharField(unique=True)
	password = CharField()

	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE

class Issue(Model):
	subject = CharField()
	created_at = DateTimeField(default= datetime.datetime.now)
	user = ForeignKeyField(User, related_name='issues')
	class Meta:
		db_table = 'issues'
		database = DATABASE




class Comment(Model):
	issue = ForeignKeyField(Issue, related_name='comments') #represents one to many OR
															#backref = 'comments'
	class Meta:
		db_table = 'comments'
		database = DATABASE





def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Issue, User, Comment], safe=True) 
	print("TABLES CREATED")
	DATABASE.close()
