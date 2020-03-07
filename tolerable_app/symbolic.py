from sympy.parsing.sympy_parser import parse_expr, standard_transformations, auto_symbol
from sympy import (
                Abs,
                Max,
                Min,
                acos,
                acosh,
                acot,
                acoth,
                acsc,
                acsch,
                asec,
                asech,
                asin,
                asinh,
                atan,
                atan2,
                atanh,
                cos,
                cosh,
                cot,
                coth,
                csc,
                csch,
                exp,
                ln,
                log,
                pi,
                sec,
                sin,
                sinc,
                sinh,
                sqrt,
                tan,
                tanh
)

from numpy import linspace
import re

# SETUP GENERAL SYMBOLS #
reserved_values = (
        Abs,
        Max,
        Min,
        acos,
        acosh,
        acot,
        acoth,
        acsc,
        acsch,
        asec,
        asech,
        asin,
        asinh,
        atan,
        atan2,
        atanh,
        cos,
        cosh,
        cot,
        coth,
        csc,
        csch,
        exp,
        ln,
        log,
        pi,
        sec,
        sin,
        sinc,
        sinh,
        sqrt,
        tan,
        tanh
)

reserved_names = (
        'abs',
        'max',
        'min',
        'acos',
        'acosh',
        'acot',
        'acoth',
        'acsc',
        'acsch',
        'asec',
        'asech',
        'asin',
        'asinh',
        'atan',
        'atan2',
        'atanh',
        'cos',
        'cosh',
        'cot',
        'coth',
        'csc',
        'csch',
        'exp',
        'ln',
        'log',
        'pi',
        'sec',
        'sin',
        'sinc',
        'sinh',
        'sqrt',
        'tan',
        'tanh'
)

reserved_dict = dict(zip(reserved_names, reserved_values))

# DEFINE SYMBOLIC HELPER FUNCTIONS #
def get_valid_names(defined_names=tuple()):
    return (*reserved_names, *defined_names)


def find_bad_names(hum_defn, valid_names):
    name_likes = find_name_like(hum_defn, get_span=False)
    return tuple(name_like for name_like in name_likes if not name_like in valid_names)


# search output definition for instances of (human readable) input names
# replace each input name with a reference to the machine readable input
def parse_definition(hum_defn, translation):
    """Takes an output definition as a string and 
    replaces instances of human readable input names
    with machine readable references using the translation
    table provided as a dictionary (translation)"""

    mach_defn = hum_defn

    name_likes = find_name_like(hum_defn)
    for (name_like, name_like_start, name_like_end) in name_likes:
        mach_defn[name_like_start:name_like_end] = translation.get(name_like, name_like)

    return mach_defn


# find name like substrings (will be used to evaluate each on their own so the user will be aware
# of all non-valid substrings in dependent definitions after first submission attempt)
def find_name_like(hum_defn, get_span=True):
    name_like_re = re.compile(r"((?:[a-zA-z] *(?:\w+\s?)+))")

    if get_span:
        return tuple((name_like.group().strip(), name_like.span()[0], name_like.span()[0] + len(name_like.group())) \
            for name_like in name_like_re.finditer(hum_defn))
    else:
        return (name_like.strip() for name_like in name_like_re.findall(hum_defn))


# if a bad name is found, find similar valid names from the name list
# rank the valid names by similarity and return
def find_similar(bad_name, valid_names):

    valid_name_rank = dict(zip(valid_names, linspace(0, 0, len(valid_names))))
    for valid_name in valid_names:
        last_good_char = 0
        for char_num, __ in enumerate(bad_name):
            if bad_name[last_good_char:char_num+1] in valid_name:
                valid_name_rank[valid_name] += 1
            else:
                last_good_char = char_num+1

    similar_names = tuple(ranked_item[0] for ranked_item in (
        sorted(valid_name_rank.items(), key=lambda x: x[1], reverse=True)))
    
    return similar_names


def evaluate(mach_defn, local_dict=None, global_dict=None, transformation=None):
    if not transformation:
        transformations = tuple(transformation for transformation in standard_transformations \
            if not transformation == auto_symbol)

    return parse_expr(mach_defn,
                      local_dict=local_dict,
                      global_dict=global_dict,
                      transformations=transformations)


# TODO:
# simulate independent values
# store simulated data in session and then redis
# replace defined value names with 0s so definitions can be evaluated in a lightweight way
# (what about multiplying array values, shape must be compatible -- should always be case if simulations are
# re-run when N is changed and / or definitions are changed)


if __name__ == "__main__":
    # Set names of all independent AND dependent vars as sympy symbols
    # Take user definition input
    # Convert to sympy expression
    # Attempt to evaluate (each term?)
    # Catch terms causing errors
    # Search valid symbols for similar term
    # Return error to user with suggested valid terms

    from sympy import symbols, sympify, lambdify
    import numpy as np
    
    inputs = {
        'inputform_0': {'input_details': {'constant_input_value': 5.0}, 'input_name': 'Hello', 'input_type': 'constant'},
        'inputform_1': {'input_details': {'normal_input_mean': 5.0, 'normal_input_stdev': 10.0},'input_name': 'Hello 2', 'input_type': 'normal'},
        'inputform_2': {'input_details': {'uniform_input_max': 5.0, 'uniform_input_min': -5.0}, 'input_name': 'Hello 3', 'input_type': 'uniform'}
    }

    # inputs_data = {
    #     'inputform_0': {'input_name': 'Hello', 'input_data': np.array([5., 5., 5., 5., 5.])},
    #     'inputform_1': {'input_name': 'Hello 2', 'input_data': np.array([15.13925948,  7.21411871,  6.04247014, 12.46550976, 13.57085401])},
    #     'inputform_2': {'input_name': 'Hello 3', 'input_data': np.array([-1.09475729, -3.62952259, -2.19693445,  0.72031821,  1.25388151])}
    # }

    inputs_data = {
        'inputform_0': np.array([5., 5., 5., 5., 5.]),
        'inputform_1': np.array([15.13925948,  7.21411871,  6.04247014, 12.46550976, 13.57085401]),
        'inputform_2': np.array([-1.09475729, -3.62952259, -2.19693445,  0.72031821,  1.25388151])
    }

    hum_defn = '(Hello 2 + Hello 2 + Hello) * pi'

    # mach_defn = parse_definition(hum_defn, {input_spec['input_name']: input_id for input_id, input_spec in inputs.items()})

    # f = lambdify(inputs_data.keys(), mach_defn, 'numpy')
    # print(f(*inputs_data.values()))

    print(find_name_like(hum_defn))

    print(find_bad_names('Hello 3 + Hello 2', ('Hello', 'Hello 2', 'Hello 3')))

    # user definitions can only include defined names or global names (whitelisted) packaged in a mathematically
    # valid string* (the string is eval'd to ensure it's mathematically valid). Is it possible to name an input 
    # after a target function in order to execute the target function? Don't know, depends on how good my 'find_name_like'
    # method is. If it is effective at finding all name like substrings and comparing them to whitelisted substrings,
    # we should be good. Basically, if the input isn't a grouping symbol like '(', '{', '[' or a math symbol like
    # '+', '**', '//', it should show as a name like object and should then be compared to the local and global name
    # dictionaries (whitelist) (perhaps rebuilding 'find_name_like' to look for groupers and math symbols is better than
    # the current implemenation?).