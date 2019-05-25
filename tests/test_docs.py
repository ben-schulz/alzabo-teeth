"""
these tests verify that the working examples
used by the notebooks in the 'docs' folder
do, in fact, work.

if they fail, then either the code is broke
or the docs need to be updated.

(2019.05.22) \0
"""

import os

this_file = os.path.abspath( __file__ )
this_dir = os.path.join( os.path.dirname( this_file ) )
parent_dir = os.path.join( this_dir, '..' )

raw_text_path = os.path.join( parent_dir, 'docs/moby_dick.txt' )

def test__array_module__examples_work():

    with open( raw_text_path, 'r') as f:
        raw_text = f.read()

    assert 'MOBY-DICK;\n\nor, THE WHALE.\n' == raw_text[ 0 : 27 ]

    from teeth.array import TextStrata

    t = TextStrata( raw_text )

    assert 'MOBY-DICK;\n\nor, THE WHALE.\n' == t[ 0 : 27 ]
