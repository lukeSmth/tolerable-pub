from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, IntegerField, SelectField, BooleanField,
    HiddenField, FieldList, SubmitField, FormField
)
from wtforms.validators import ValidationError, DataRequired, NoneOf

class SettingsForm(FlaskForm):
    setting_n = IntegerField(
        'Simulation Iterations',
        default=5000,
        validators=[DataRequired()],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )

    setting_alpha = FloatField(
        'Confidence Interval Alpha Level',
        default=0.05,
        validators=[DataRequired()],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )

    submit_settings = SubmitField('Update Settings')

