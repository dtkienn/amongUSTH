from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Password(FlaskForm):
	current_password = PasswordField('Current Password',validators=[DataRequired()])
	new_password = PasswordField('New Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('new_password')])
	submit = SubmitField('Change!')

class BookPost(FlaskForm):
	file_name = StringField('File Name',validators=[DataRequired()])
	description = StringField('Description',validators=[DataRequired()])
	file = StringField('File',validators=[DataRequired()])
	submit = SubmitField('Post !')

class CommentPost(FlaskForm):
	comment_content = StringField('Content', validators=[DataRequired()])
	submit = SubmitField('Post !')

