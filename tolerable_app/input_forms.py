from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, IntegerField, SelectField, BooleanField,
    HiddenField, FieldList, SubmitField, FormField
)
from wtforms.validators import ValidationError, DataRequired, NoneOf

class EmptyInputDetailsForm(FlaskForm):
    class Meta:
        csrf = False

    empty_input_value = HiddenField('')


class ConstantInputDetailsForm(FlaskForm):
    class Meta:
        csrf = False

    constant_input_value = FloatField(
        'Value',
        validators=[DataRequired(message='This field is required.')],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )


class NormInputDetailsForm(FlaskForm):
    class Meta:
        csrf = False

    norm_input_mean = FloatField(
        'Mean',
        validators=[DataRequired(message='This field is required.')],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )

    norm_input_stdev = FloatField(
        'St. Dev.',
        validators=[DataRequired(message='This field is required.')],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )


class UniformInputDetailsForm(FlaskForm):
    class Meta:
        csrf = False

    uniform_input_min = FloatField(
        'Min',
        validators=[DataRequired(message='This field is required.')],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )

    uniform_input_max = FloatField(
        'Max',
        validators=[DataRequired(message='This field is required.')],
        render_kw={
            'onchange': 'this.form.submit()',
            'onkeypress': 'return event.keyCode != 13;'
        }
    )


def input_form_factory(input_type='empty', removable=False, csrf=True, none_of=tuple()):
    class InputForm(FlaskForm):
        if not csrf:
            class Meta:
                csrf = False

        # setup input type choices for drop down list
        input_type_tags = (
            'empty',
            'constant',
            'norm',
            'uniform'
        )

        input_type_labels = (
            '',
            'Constant',
            'Normal',
            'Uniform'
        )

        input_type_choices = tuple(zip(input_type_tags, input_type_labels))

        # setup form choices and labels for input details
        input_detail_field_forms = (
            EmptyInputDetailsForm,
            ConstantInputDetailsForm,
            NormInputDetailsForm,
            UniformInputDetailsForm
            )

        input_detail_field_form_labels = tuple(
        '{} Input Details Form'.format(input_type_label) \
            if not input_type_label == '' else '' \
                for input_type_label in input_type_labels
        )

        keyed_input_detail_field_forms = dict(
            zip(input_type_tags, input_detail_field_forms))
    
        keyed_input_detail_labels = dict(
            zip(input_type_tags, input_detail_field_form_labels))

        # create input fields for generic input form
        input_name = StringField(
            'Input Name',
            default='',
            validators=[
                DataRequired(),
                NoneOf(none_of, message='Input name must be unique. (Cannot be any of: %(values)s.)')
            ],
            render_kw={
                'onchange': 'this.form.submit()',
                'onkeypress': 'return event.keyCode != 13;'
            }
        )

        input_type = SelectField(
            'Input Distribution Type',
            choices=input_type_choices,
            default='empty',
            validators=([NoneOf(('empty'), message='This field is required.')]),
            render_kw={
                'onchange': 'this.form.submit()',
                'onkeypress': 'return event.keyCode != 13;'
            }
        )

    selected_detail_form = InputForm.keyed_input_detail_field_forms[input_type]
    selected_detail_label = InputForm.keyed_input_detail_labels[input_type]

    setattr(InputForm, 'input_detail_fields', FormField(
        selected_detail_form, label=selected_detail_label))

    if removable:
        setattr(InputForm, 'remove_input', SubmitField(
            'Remove Input', render_kw={'onkeypress': 'return event.keyCode != 13;'}
            )
        )
    else:
        setattr(InputForm, 'remove_input', HiddenField(''))

    # return custom import form
    return InputForm


def input_list_form_factory(input_forms, fill=False):
    class InputListForm(FlaskForm):
        input_form_ids = []

        @classmethod
        def add_input_form_id(cls, input_form_id):
            cls.get_input_form_ids().append(input_form_id)

        @classmethod
        def get_input_form_ids(cls):
            return cls.input_form_ids

        def get_next_input_form_id(self):
            return 'inputform_{}'.format(int(max(self.get_input_form_ids()).split('_')[1])+1)

        def remove_input_form_id(self, input_form_id):
            self.get_input_form_ids().remove(input_form_id)
            
        def remove_input_form(self, input_form_id):
            self.remove_input_form_id(input_form_id)
            delattr(self, input_form_id)

    removable = len(input_forms) > 1

    input_names = tuple(input_form_data['input_name'] for input_form_data in input_forms.values())

    for input_form_id, input_form_data in input_forms.items():
        # grab input type
        input_type = input_form_data['input_type']
        # grab input name
        this_input_name = input_form_data['input_name']
        # generate tuple of other input names
        other_names = tuple(input_name for input_name in input_names if not input_name == this_input_name)
        # if the input name exists in the input_names tuple more than once, an error must be rendered
        if input_names.count(this_input_name) > 1:
            other_names = (*other_names, this_input_name)
        # pass unique form class to list of forms as formfield
        setattr(
            InputListForm,
            input_form_id,
            FormField(input_form_factory(
                    input_type,
                    removable=removable,
                    csrf=False,
                    none_of=other_names
                ),
            )
        )
        # add input form id to reference list
        InputListForm.add_input_form_id(input_form_id)

    # add fields to be shown at end of the list
    setattr(
        InputListForm,
        'add_input',
        SubmitField('Add Input', render_kw={'onkeypress': 'return event.keyCode != 13;'})
    )

    setattr(
        InputListForm,
        'submit_inputs',
        SubmitField('Update Input(s)', render_kw={'onkeypress': 'return event.keyCode != 13;'})
    )

    if fill:
        return InputListForm(data=fill)
    else:
        return InputListForm()
