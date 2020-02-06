from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class FileNameForm(FlaskForm):
    filename = StringField('new filename:', validators=[DataRequired()])
    submit = SubmitField('change filename')


class SeedSelection(FlaskForm):
    row1 = SelectField(label="Row 1", choices=[("universal", "universal"), ("tomato_dummy", "tomato_dummy"), ("ginger_dummy", "ginger_dummy")])
    row2 = SelectField(label="Row 2", choices=[("universal", "universal"), ("tomato_dummy", "tomato_dummy"), ("ginger_dummy", "ginger_dummy")])
    row3 = SelectField(label="Row 3", choices=[("universal", "universal"), ("tomato_dummy", "tomato_dummy"), ("ginger_dummy", "ginger_dummy")])
    row4 = SelectField(label="Row 4", choices=[("universal", "universal"), ("tomato_dummy", "tomato_dummy"), ("ginger_dummy", "ginger_dummy")])

    submit = SubmitField('submit seed selection')