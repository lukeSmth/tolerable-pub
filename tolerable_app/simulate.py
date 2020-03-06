# DISTRIBUTION SIMULATION #
import numpy as np

def sim_constant(input_details=None, settings=None):
    """Simulates constant inputs.

    - Accepts input_details of the form {'constant_input_value': ...}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""

    return np.full(
                shape=(settings['setting_n']),
                fill_value=input_details['constant_input_value'])


def sim_normal(input_details=None, settings=None):
    """Simulates normal inputs.

    - Accepts input_details of the form {'normal_input_mean': ..., 'normal_input_stdev': ...}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""

    return np.random.normal(
                        loc=input_details['normal_input_mean'],
                        scale=input_details['normal_input_stdev'],
                        size=(settings['setting_n']))


def sim_uniform(input_details=None, settings=None):
    """Simulates uniform inputs.

    - Accepts input_details of the form {'uniform_input_min': ..., 'uniform_input_max': ...}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""

    return np.random.uniform(
                        low=input_details['uniform_input_min'],
                        high=input_details['uniform_input_max'],
                        size=(settings['setting_n']))


def sim_triangle():
    pass


def sim_pareto():
    pass


def sim_poisson():
    pass


def sim_binomial():
    pass


def sim_pert():
    pass


def sim_discrete():
    pass


def sim_inputs(inputs=None, settings=None):
    """Simulates inputs according to the input type and details.

    - Accepts inputs of the form {input_id: {'input_name': ..., 'input_type': ..., 'input_details': {...}}}
        - Valid input types: 'constant', 'normal', 'uniform'
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""

    if not settings:
        settings = {'setting_alpha': 0.05, 'setting_n': 100}
    
    if inputs:
        sim_input = {'constant': sim_constant, 'normal': sim_normal, 'uniform': sim_uniform}

        for input_id, input_spec in inputs.items():
            sim_data = sim_input[input_spec['input_type']](
                                            input_details=input_spec['input_details'],
                                            settings=settings)
            
            print(sim_data)


def sim_outputs(outputs=None, settings=None):
    """Simulates outputs according to the output definition.

    - Accepts outputs of the form {output_id: {'output_name': ..., 'output_defn': ..., 'output_vis': ...}}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""


def sim(inputs=None, outputs=None, settings=None):
    """Simulates inputs and outputs according to the input type and details and output definition.

    - Accepts inputs of the form {input_id: {'input_name': ..., 'input_type': ..., 'input_details': {...}}}
    - Accepts outputs of the form {output_id: {'output_name': ..., 'output_defn': ..., 'output_vis': ...}}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""


# TODO #
# SENSITIVITY ANALYSIS #

# SCENARIO MODELING #

# CORRELATION PARAMETERS #
# (Relate independent variables to each other -- some go down as others go up)
# May be able to do via dependent variables -> dependent = Norm(mean, std.dev = f(independent_value))
# I.e. define a dependent distribution with a std. dev. dependent on corresponding value of another distribution (independent or dependent)


if __name__ == "__main__":
    inputs = {
        'inputform_0': {'input_details': {'constant_input_value': 5.0}, 'input_name': 'Hello', 'input_type': 'constant'},
        'inputform_1': {'input_details': {'normal_input_mean': 5.0, 'normal_input_stdev': 10.0},'input_name': 'Hello2', 'input_type': 'normal'},
        'inputform_2': {'input_details': {'uniform_input_max': 5.0, 'uniform_input_min': -5.0}, 'input_name': 'Hello3', 'input_type': 'uniform'}
    }

    settings = {'setting_alpha': 0.05, 'setting_n': 5000}

    sim_inputs(inputs, settings)