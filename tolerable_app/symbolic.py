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
    name_likes = find_name_like(hum_defn)
    return tuple(name_like for name_like in name_likes if not name_like in valid_names)


# search output definition for instances of (human readable) input names
# replace each input name with a reference to the machine readable input
def parse_definition(hum_defn, translation):
    """Takes an output definition as a string and 
    replaces instances of human readable input names
    with machine readable references using the translation
    table provided as a dictionary (translation)"""

    mach_defn = hum_defn
    hum_input_names = translation.keys()
    for hum_input_name in hum_input_names:
        mach_defn = mach_defn.replace(
            hum_input_name,
            translation[hum_input_name]
        )

    return mach_defn


# find name like substrings (will be used to evaluate each on their own so the user will be aware
# of all non-valid substrings in dependent definitions after first submission attempt)
def find_name_like(hum_defn):
    name_like_re = re.compile(r"((?:[a-zA-z] *(?:\w+\s?)+))")

    return tuple(name_like.strip() for name_like in name_like_re.findall(hum_defn))


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

    pass