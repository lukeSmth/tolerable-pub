import copy
from flask import current_app as app
from flask import render_template, request, url_for, session, redirect
from .forms import input_list_form_factory
from .util import generate_empty_input_data, generate_empty_input, capture_input_list_form_items

# hello world
@app.route('/hello')
def hello():
    return app.root_path

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new():
    session.clear()
    return redirect(url_for('input'))

@app.route('/input', methods=['POST', 'GET'])
def input():
    # INITIALIZE FORM #
    if not session.get('input_forms'):
        session['input_forms'] = generate_empty_input(input_form_id_num=0)
    
    # initialize form to pull data
    input_list_form = input_list_form_factory(session['input_forms'])

    # CAPTURE INCOMING FORM DATA #
    # get input data from input list form
    input_forms = capture_input_list_form_items(input_list_form)

    # STORE FORM DATA #
    # (also used to regenerate input form list with correct types) #
    session['input_forms'] = copy.deepcopy(input_forms)

    # CHECK AND PROCESS SUBMISSION #
    if input_list_form.submit_inputs.data:
        if input_list_form.validate_on_submit():
            # add each input as a valid input for use in output definitions
            # form defintion needs to include validators for unique names
            # use session var for now, redis in future
            # store input and output params in session before simulate is called
            # store input and output params AND simulated data is redis after sim call
            # upon later simulate calls, check input params in session against input params for simulated data
            # if they vary, update redis row for given input id and resimulated input data
            # (ensure input ids are removed from redis when removed in session)
            # for outputs, check if definition is session has changed AND whether any referenced inputs (independent vars) have changed
            # if so, update redis row for given output id and resimulated output data
            return redirect(url_for('output'))

    # otherwise, check for added and removed inputs and update form for rendering
    # ADD INPUT #
    if input_list_form.add_input.data:
        session['input_forms'].setdefault(input_list_form.get_next_input_form_id(), generate_empty_input_data())

    # REMOVE INPUT #
    # can be removed during capture step... for now, explicit is better than abstracted
    for input_form_id, input_form_data in input_forms.items():
        if input_form_data['remove_input']:
            session['input_forms'].pop(input_form_id, None)

    # REGENERATE FORM #
    # generate form with changes made (type, add, remove) for rendering
    input_list_form = input_list_form_factory(session['input_forms'])

    return render_template('input.html', form=input_list_form)

@app.route('/output')
def output():
    # check evaluable status with form validator (True, False)
    # can show list of valid inputs
    # and can also make suggestions (autocomplete option)
    return render_template('output.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/simulate')
def simulate():
    pass

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/report')
def report():
    return render_template('report.html')