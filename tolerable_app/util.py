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