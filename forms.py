from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, InputRequired, Length

class RegisterUserForm(FlaskForm):
    """Form to register new user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20)])
    email = StringField("Email Address", validators=[InputRequired(), Email(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class LoginUserForm(FlaskForm):
    """Form to login user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20)])

class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Empty form used for deletion"""