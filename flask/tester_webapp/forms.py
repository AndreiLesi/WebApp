from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange
import os


class New_Request(FlaskForm):
    """
    Defines the New Request form field. Its Shape to match the table columns,
     excetion of request_id which is generated automatically by the db.
    """
    requested_by = StringField('Requester', validators=[
                               DataRequired(), Length(min=2, max=20)])
    env_id = IntegerField('Envrionment ID', validators=[
        DataRequired(), NumberRange(1, 100)])
    test_path = StringField('Test Path', validators=[DataRequired()])
    created_at = "filledIn_routes.py"
    details = ""
    submit = SubmitField('Submit')

    # Extra validation for test_path: check if file or folder exists
    def validate_test_path(form, field):
        msg = 'Test does not exist! Please choose an'\
              'existing test file or directory!'
        if not os.path.exists("tester_webapp/PyTests/" + str(field.data)):
            raise ValidationError(msg)
