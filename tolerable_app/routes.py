import copy
from .forms import SettingsForm
from flask import current_app as app
from flask import render_template, request, url_for, session, redirect
from .input_forms import input_list_form_factory
from .output_forms import output_list_form_factory
from .util import (
    generate_empty_input_data,
    generate_empty_input,
    capture_input_list_form_items,
    update_session_inputs,
    generate_empty_output_data,
    generate_empty_output,
    capture_output_list_form_items,
    update_session_outputs,
    capture_settings
)


# TODO / NOTES #

# modify input and output form implementation so that blank session objects are not created?
# or just handle blank inputs / outputs in simulation attempt
# a blank input will allow an output definition of "1 +   * 2" because there's an implicit ''?

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
    if request.method == 'GET':
        input_list_form = input_list_form_factory(session['input_forms'], fill=session['input_forms'])
        shape_mod_update_made = None
    else:
        input_list_form = input_list_form_factory(session['input_forms'])
        session['input_forms'], shape_mod_update_made = update_session_inputs(session['input_forms'], input_list_form)

    # CHECK AND PROCESS SUBMISSION #
    if input_list_form.submit_inputs.data:
        if input_list_form.validate_on_submit():
            input_names = (input_data['input_name'] for input_data in session['input_forms'].values())
            session['input_references'] = dict(zip(input_names, session['input_forms'].keys()))
            return redirect(url_for('output'))
    elif shape_mod_update_made:
        # REGENERATE FORM #
        # generate form with changes made (type, add, remove) for rendering
        input_list_form = input_list_form_factory(session['input_forms'])

    return render_template('input.html', form=input_list_form)


@app.route('/output', methods=['POST', 'GET'])
def output():
    # INITIALIZE FORM #
    if not session.get('output_forms'):
        session['output_forms'] = generate_empty_output(output_form_id_num=0)

    input_references = session.get('input_references')
    output_names = tuple(output_data['output_name'] for output_data in session['output_forms'].values())

    # defined names will be blank by default
    session['defined_names'] = tuple(output_name for output_name in output_names if not output_name == '')

    # get valid input names
    if session.get('input_references'):
        session['defined_names'] = (*tuple(input_references.keys()), *session['defined_names'])
    
    # initialize form to pull data
    if request.method == 'GET':
        output_list_form = output_list_form_factory(
            session['output_forms'],
            defined_names=session['defined_names'],
            fill=session['output_forms'])
        shape_mod_update_made = None
    else:
        output_list_form = output_list_form_factory(
            session['output_forms'],
            defined_names=session['defined_names'])
        session['output_forms'], shape_mod_update_made = update_session_outputs(output_list_form)

    # CHECK AND PROCESS SUBMISSION #
    if output_list_form.submit_outputs.data:
        if output_list_form.validate_on_submit():
            session['output_references'] = dict(zip(output_names, session['output_forms'].keys()))
            return redirect(url_for('settings'))
    elif shape_mod_update_made:
        # REGENERATE FORM #
        # generate form with changes made (add, remove) for rendering
        output_list_form = output_list_form_factory(
            session['output_forms'],
            defined_names=session['defined_names'])

        print(output_list_form.data)
    
    return render_template('output.html', form=output_list_form, inputs=session['input_forms'])


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    settings_form = SettingsForm()

    if settings_form.validate_on_submit():
        session['settings'] = capture_settings(settings_form)
        return redirect(url_for('result'))

    return render_template('settings.html', form=settings_form)


@app.route('/simulate')
def simulate():
    pass


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/report')
def report():
    return render_template('report.html')