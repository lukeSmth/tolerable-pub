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

    print(input_forms)
    return input_forms

def update_session_inputs(session_input_forms, input_list_form):
    """Check each for each shape modification case (add, remove, change type).
    Only one shape modification mode can be executed at once.
    Only one input can be added a time, but up to all of the inputs can be deleted (needs to be up to n-1) or type-modified at once"""

    shape_mod_update_made = None

    input_forms = capture_input_list_form_items(input_list_form)

    # ID for removed inputs
    removed_input_ids = tuple(input_form_id for input_form_id, input_form_data in input_forms.items() if input_form_data['remove_input'])

    # ID session types and posted input types
    session_types = tuple(session_input_form_data['input_type'] for session_input_form_data in session_input_forms.values())
    input_types = tuple(input_form_data['input_type'] for input_form_data in input_forms.values())

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
        for session_input_form_data, new_input_type in zip(session_input_forms.values(), input_types):
            session_input_form_data.update(input_type = new_input_type)
        
        shape_mod_update_made = 'Updated inputs types to {}'.format(', '.join(input_types))
    # if no inputs have been added or removed and no types have been changed, no shape modification is needed
    # just overrite the session inputs value
    else:
        session_input_forms = input_forms

    return session_input_forms, shape_mod_update_made