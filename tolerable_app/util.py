def generate_empty_input_data():
    return {
            'input_name': '',
            'input_type': 'empty',
            'input_detail_fields': {'empty_input_value': ''},
            'remove_input': False
    }


def generate_empty_input(input_form_id_num):
    input_form_id = 'inputform_{}'.format(input_form_id_num)
    return {input_form_id: generate_empty_input_data()}


def capture_input_list_form_items(input_list_form):
    # get input data from input list form
    input_forms = {}
    for input_formfield in input_list_form:
        # ensure each submitted formfield id exists in the designed input list form
        # before capturing formfield data
        if (input_formfield.id in input_list_form.get_input_form_ids()):
            input_forms.setdefault(input_formfield.id, input_formfield.data)

    return input_forms


def update_session_inputs(session_input_forms, input_list_form):
    """Check each for each shape modification case (add, remove, change type).
    Only one shape modifying update can be made at a time.
    Only one input can be added a time, but up to all of the inputs can be deleted (needs to be up to n-1) or type-modified at once"""

    shape_mod_update_made = None

    # grab the input forms from the list form data
    input_forms = capture_input_list_form_items(input_list_form)

    # ID for removed inputs
    removed_input_ids = tuple(input_form_id for input_form_id, input_form_data in input_forms.items() if input_form_data['remove_input'] == True)

    # ID session types and posted input types
    session_types = tuple(session_input_form_data['input_type'] for session_input_form_data in session_input_forms.values())
    input_types = tuple(input_form_data['input_type'] for input_form_data in input_forms.values())

    # complete a general update of the session_input_forms based on the input forms posted
    session_input_forms = input_forms

    # check for any shape modifying edits to the form
    # check for added inputs
    if input_list_form.add_input.data:
        session_input_forms.setdefault(input_list_form.get_next_input_form_id(), generate_empty_input_data())
        shape_mod_update_made = 'Added empty input'
    # check for removed inputs
    elif any(removed_input_ids):
        for removed_input_id in removed_input_ids:
            session_input_forms.pop(removed_input_id, None)
        
        shape_mod_update_made = 'Removed inputs {}'.format(', '.join(removed_input_ids))
    # check for input type updates
    elif not session_types == input_types:
        # for session_input_form_data, new_input_type in zip(session_input_forms.values(), input_types):
        #     session_input_form_data.update(input_type = new_input_type)
        
        shape_mod_update_made = 'Updated inputs types to {}'.format(', '.join(input_types))

    return session_input_forms, shape_mod_update_made


def generate_empty_output_data():
    return {
            'output_name': '',
            'output_defn': '',
            'output_vis': True,
            'remove_output': False
    }


def generate_empty_output(output_form_id_num):
    output_form_id = 'outputform_{}'.format(output_form_id_num)
    return {output_form_id: generate_empty_output_data()}


def capture_output_list_form_items(output_list_form):
    # get output data from output list form
    output_forms = {}
    for output_formfield in output_list_form:
        # ensure each submitted formfield id exists in the designed output list form
        # before capturing formfield data
        if (output_formfield.id in output_list_form.get_output_form_ids()):
            output_forms.setdefault(output_formfield.id, output_formfield.data)

    return output_forms


def update_session_outputs(output_list_form):
    """Check each for each shape modification case (add, remove).
    Only one shape modifying update can be made at a time.
    Only one output can be added a time, but up to all of the outputs can be deleted (needs to be up to n-1) or type-modified at once"""

    shape_mod_update_made = None

    # grab the output forms from the list form data
    output_forms = capture_output_list_form_items(output_list_form)

    # ID for removed outputs
    removed_output_ids = tuple(output_form_id for output_form_id, output_form_data in output_forms.items() if output_form_data['remove_output'] == True)

    # complete a general update of the session_output_forms based on the output forms posted
    session_output_forms = output_forms

    # check for any shape modifying edits to the form
    # check for added outputs
    if output_list_form.add_output.data:
        session_output_forms.setdefault(output_list_form.get_next_output_form_id(), generate_empty_output_data())
        shape_mod_update_made = 'Added empty output'
    # check for removed outputs
    elif any(removed_output_ids):
        for removed_output_id in removed_output_ids:
            session_output_forms.pop(removed_output_id, None)
        
        shape_mod_update_made = 'Removed outputs {}'.format(', '.join(removed_output_ids))

    return session_output_forms, shape_mod_update_made


def capture_settings(settings_form):
    return {setting_name: setting_value for setting_name, setting_value in settings_form.data.items() \
        if 'setting_' in setting_name}


def fig_to_bin(fig, img_format='png'):
    from io import BytesIO
    bin_buffer = BytesIO()
    fig.savefig(bin_buffer, format=img_format)
    bin_buffer.seek(0)
    return bin_buffer

def bin_to_base64(bin_buffer):
    from base64 import b64encode
    return b64encode(bin_buffer.read())

def fig_to_base64(fig, img_format='png'):
    return bin_to_base64(fig_to_bin(fig, img_format))


if __name__ == "__main__":
    pass