# from . import symbolic as sym
import numpy as np
from sympy import lambdify

# DISTRIBUTION SIMULATION #
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

    - Accepts inputs of the form {input id: {'input_name': ..., 'input_type': ..., 'input_details': {...}}}
        - Valid input types: 'constant', 'normal', 'uniform'
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""

    if not settings:
        settings = {'setting_alpha': 0.05, 'setting_n': 100}
    
    if inputs:
        sim_input = {'constant': sim_constant, 'normal': sim_normal, 'uniform': sim_uniform}
        inputs_data = {}

        for input_id, input_spec in inputs.items():
            input_data = sim_input[input_spec['input_type']](input_details=input_spec['input_details'],
                                                            settings=settings)
            
            inputs_data.setdefault(input_spec['input_name'], input_data)

        return inputs_data

    return None


def sim_outputs(outputs=None, inputs=None, inputs_data=None, settings=None):
    """Simulates outputs according to the output definition.

    - Accepts outputs of the form {output id: {'output_name': ..., 'output_defn': ..., 'output_vis': ...}}
    - Accepts inputs_data of the form {input name: array-like input data}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}
    
    *Variables referenced in output definition will be simulated if they have not been already."""

    if not settings:
        settings = {'setting_alpha': 0.05, 'setting_n': 100}
    
    if outputs:
        outputs_data = {}
        translation = {input_spec['input_name']: input_id for input_id, input_spec in inputs.items()}
        for output_id, output_spec in outputs.items():
            hum_defn = output_spec['output_defn']
            mach_defn = sym.parse_definition(hum_defn, translation)
            f = lambdify(inputs.keys(), mach_defn, 'numpy')
            output_data = f(*inputs_data.values())

            outputs_data.setdefault(output_spec['output_name'], output_data)

        return outputs_data

    return None

def sim(inputs=None, outputs=None, settings=None):
    """Simulates inputs and outputs according to the input type and details and output definition.

    - Accepts inputs of the form {input id: {'input_name': ..., 'input_type': ..., 'input_details': {...}}}
    - Accepts outputs of the form {output id: {'output_name': ..., 'output_defn': ..., 'output_vis': ...}}
    - Accepts settings of the form {'setting_alpha': ..., 'setting_n': ...}"""


def plot_sim_data(sims_data=None, normalize=True, bin_width=None):
    if not bin_width:
        # Generate bin edges for each input
        all_bin_edges = []
        for sim_data in sims_data.values():
            all_bin_edges.append(np.histogram_bin_edges(sim_data, bins='fd'))

        # Discover bin intervals for each input
        all_bin_widths = []
        for input_bin_edges in all_bin_edges:
            all_bin_widths.append(input_bin_edges[1] - input_bin_edges[0])

        # Determine max bin interval
        bin_width = max(all_bin_widths)

    fig, ax = plt.subplots()

    prop_iter = iter(plt.rcParams['axes.prop_cycle'])

    for sim_name, sim_data in sims_data.items():
        # if input type is constant (all values in array match), plot as bar, not histogram
        if not all(sim_data == sim_data[0]):
            # Create bin edges for each input using calculated max bin interval
            input_bin_edges = np.arange(min(sim_data), max(sim_data), bin_width)
            ax.hist(sim_data, bins=input_bin_edges, density=normalize, color=next(prop_iter)['color'], alpha=0.5, label=sim_name)
        else:
            if normalize:
                ax.bar(sim_data[0], 1.0, bin_width, color=next(prop_iter)['color'], alpha=0.5, label=sim_name)
            else:
                ax.bar(sim_data[0], len(sim_data), bin_width, color=next(prop_iter)['color'], alpha=0.5, label=sim_name)

    return fig, ax


# TODO #
# SENSITIVITY ANALYSIS #

# SCENARIO MODELING #

# CORRELATION PARAMETERS #
# (Relate independent variables to each other -- some go down as others go up)
# May be able to do via dependent variables -> dependent = Norm(mean, std.dev = f(independent_value))
# I.e. define a dependent distribution with a std. dev. dependent on corresponding value of another distribution (independent or dependent)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import symbolic as sym
    

    inputs = {
        'inputform_0': {'input_details': {'constant_input_value': 5.0}, 'input_name': 'Hello', 'input_type': 'constant'},
        'inputform_1': {'input_details': {'normal_input_mean': 5.0, 'normal_input_stdev': 10.0},'input_name': 'Hello 2', 'input_type': 'normal'},
        'inputform_2': {'input_details': {'uniform_input_max': 5.0, 'uniform_input_min': -5.0}, 'input_name': 'Hello 3', 'input_type': 'uniform'}
    }

    outputs = {
        'outputform_0': {'output_defn': 'pi * (Hello 2 * Hello) + Hello 3', 'output_name': 'Pi', 'output_vis': True},
        'outputform_1': {'output_defn': 'Hello 2 * 2', 'output_name': 'Test', 'output_vis': False}
    }

    settings = {'setting_alpha': 0.05, 'setting_n': 5000}

    inputs_data = sim_inputs(inputs, settings)

    outputs_data = sim_outputs(outputs=outputs, inputs=inputs, inputs_data=inputs_data)

    fig, ax = plot_sim_data(inputs_data)

    ax.legend()
    plt.show()

    fig2, ax2 = plot_sim_data(outputs_data)

    ax2.legend()
    plt.show()

