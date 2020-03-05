from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, IntegerField, SelectField, BooleanField,
    HiddenField, FieldList, SubmitField, FormField
)
from wtforms.validators import ValidationError, DataRequired, NoneOf
from .symbolic import find_bad_names, get_valid_names, parse_definition, evaluate

import sys  


def use_valid_names(defined_names=tuple()):
    if defined_names:
        message_1 = 'Undefined names and / or mathematical references: {}.'
        message_2 = ' Did you mean to use one of these: {}?'
    else:
        message_1 = 'Undefined names and / or mathematical references: {}.'
        message_2 = '{}'
    
    def _use_valid_names(form, field):
        this_name = form.output_name.data
        non_circ_defined_names = tuple(defined_name for defined_name in defined_names if not defined_name == this_name)
        
        if len(non_circ_defined_names) > 1:
            message = message_1 + message_2
        else:
            message = message_1
        
        hum_defn = field.data
        
        bad_names = find_bad_names(hum_defn, get_valid_names(defined_names=non_circ_defined_names))
        
        if bad_names:
            raise ValidationError(message.format(', '.join(bad_names), ', '.join(non_circ_defined_names)))

    return _use_valid_names


def can_evaluate(defined_names=tuple(), message=None):
    if not message:
        message = 'Definition cannot be mathematically evaluated.'
    else:
        message = message

    translation = {defined_name: '1' for defined_name in defined_names}

    def _can_evaluate(form, field):
        hum_defn = field.data
        mach_defn = parse_definition(hum_defn, translation)
        try:
            evaluate(mach_defn)
        except:
            raise ValidationError(message)

    return _can_evaluate



def output_form_factory(removable=False, csrf=True, none_of=tuple(), defined_names=tuple()):
    class OutputForm(FlaskForm):
        if not csrf:
            class Meta:
                csrf = False
                
        # create output name field
        output_name = StringField(
            'Output Name',
            default='',
            validators=[
                DataRequired(),
                NoneOf(none_of, message='Output name must be unique. (Cannot be any of: %(values)s.)')
            ],
            render_kw={
                'onchange': 'this.form.submit()',
                'onkeypress': 'return event.keyCode != 13;'
            }
        )

        # create output definition field
        output_defn = StringField(
            'Output Definition',
            default='',
            validators=[
                DataRequired(),
                use_valid_names(defined_names=defined_names),
                can_evaluate(defined_names=defined_names)],
            render_kw={
                'onchange': 'this.form.submit()',
                'onkeypress': 'return event.keyCode != 13;'
            }
        )

        # create 'show by default' option
        output_vis = BooleanField(
            'Show in Report by Default<br>(can be changed in report)',
            default=True,
            render_kw={
                'onchange': 'this.form.submit()',
                'onkeypress': 'return event.keyCode != 13;'
            }
        )

    if removable:
        setattr(OutputForm, 'remove_output', SubmitField(
            'Remove Output', render_kw={'onkeypress': 'return event.keyCode != 13;'}
            )
        )
    else:
        setattr(OutputForm, 'remove_output', HiddenField(''))

    # return custom import form
    return OutputForm

def output_list_form_factory(output_forms, defined_names=tuple(), fill=False):
    class OutputListForm(FlaskForm):
        output_form_ids = []

        @classmethod
        def add_output_form_id(cls, output_form_id):
            cls.get_output_form_ids().append(output_form_id)

        @classmethod
        def get_output_form_ids(cls):
            return cls.output_form_ids

        def get_next_output_form_id(self):
            return 'outputform_{}'.format(int(max(self.get_output_form_ids()).split('_')[1])+1)

        def remove_output_form_id(self, output_form_id):
            self.get_output_form_ids().remove(output_form_id)
            
        def remove_output_form(self, output_form_id):
            self.remove_output_form_id(output_form_id)
            delattr(self, output_form_id)

    removable = len(output_forms) > 1

    output_names = tuple(output_form_data['output_name'] for output_form_data in output_forms.values())

    for output_form_id, output_form_data in output_forms.items():
        # grab output name
        this_output_name = output_form_data['output_name']
        # generate tuple of other output names
        other_names = tuple(output_name for output_name in output_names if not output_name == this_output_name)
        # if the output name exists in the output_names tuple more than once, an error must be rendered
        if output_names.count(this_output_name) > 1:
            other_names = (*other_names, this_output_name)
        # pass unique form class to list of forms as formfield
        setattr(
            OutputListForm,
            output_form_id,
            FormField(output_form_factory(
                    removable=removable,
                    csrf=False,
                    none_of=other_names,
                    defined_names=defined_names
                ),
            )
        )
        # add output form id to reference list
        OutputListForm.add_output_form_id(output_form_id)

    # add fields to be shown at end of the list
    setattr(
        OutputListForm,
        'add_output',
        SubmitField('Add Output', render_kw={'onkeypress': 'return event.keyCode != 13;'})
    )

    setattr(
        OutputListForm,
        'submit_outputs',
        SubmitField('Update Output(s)', render_kw={'onkeypress': 'return event.keyCode != 13;'})
    )

    if fill:
        return OutputListForm(data=fill)
    else:
        return OutputListForm()