#!/usr/bin/env python

# Generate SNNS net file feed forward network 

# version 0.1

from itertools import pairwise
import argparse
import sys


conn_separtor = """-------|------|----------------------------------------------------------------------------------------------------------------
"""

conn_header = """
connection definition section :

target | site | source:weight
"""

default_unit_section = """
unit default section :

act      | bias     | st | subnet | layer | act func     | out func
---------|----------|----|--------|-------|--------------|-------------
 0.00000 |  0.00000 | h  |      0 |     1 | Act_Logistic | Out_Identity 
---------|----------|----|--------|-------|--------------|-------------
"""

unit_definition_header = """
unit definition section :

no. | typeName | unitName | act      | bias     | st | position | act func | out func | sites
----|----------|----------|----------|----------|----|----------|----------|----------|-------
"""


def snns_header(units=128, connections=1071):
    header = """
SNNS network definition file V1.4-3D
generated at Wed Apr  2 15:29:03 2008

network name : r10_tv2_1C_BP1-11_e41-81_0a_5X1x9.net
source files :
no. of units : {units}
no. of connections : {connections}
no. of unit types : 0
no. of site types : 0


learning function : BackpropChunk
update function   : Serial_Order
""".format(units=units, connections=connections)

    return header

def unit_definiton( no, st, position, 
                 bias=0.00000,act_func=None, out_func=None, sites=None):

    act=0

    result = ""
    result += '{:>3} |'.format(no) # no
    result +="          |"              # typeName
    result +="          |"              # unitName
    result += '  {:6.5f} |'.format(act) # act
    result += '  {:6.5f} |'.format(bias) # bias
    result += ' ' + st + "  |" #st
    result += '  ' + position + " |" #position
    result += '||' # 0ut_func + sites
    return result
        
def unit_definition_table_rows(input_no, hidden_no, output_no):
    
    result =""
    hidden_total = sum(hidden_no)
    st_array = ['i'] * input_no + ["h"] * hidden_total + ["o"] * output_no
    for i in range(1, input_no + hidden_total + output_no +1):
        result += unit_definiton(i, st_array.pop(0),"2, 2, 0") + "\n"

    return result

def split_by_layers(input_no, hidden_layers, output_no):     
    """Set units per layer

    Parameters
    ----------
    input_no : Integer
        number of input neurons
    hidden_layers: list of Integers
        number of neurons per hidden layer
    output_no : Integer
        number of output neurons

    Returns
    -------
    list of list
        A list of each neurons per layer
    """
    result = []

    data = [input_no] + hidden_layers + [output_no]
    start = 1
    stop = 0
    #print(f"DATA {data}")
    

    for el in data:
        stop += el
        #print(f"range({start}, {stop}+1)")
        layer = [n for n in range(start, stop+1)]
        start += el
        result.append(layer)



    return result

def list_of_connection(data):
    """list of all connections

    Parameters
    ----------
    input_no : Integer
        number of input units

    Returns
    -------
    list of dictionries
        A list all connections 
    """

    result = []

    data = list(pairwise(data))
    for el in data:
        (source, target) = el
        for el1 in target:
            result.append((el1,source))

    return dict(result)

def print_connection(data):
    """print one connection in SNNS format

    Parameters
    ----------
    input : dict {N:[x1,x2,...x_m]}
        connection for one unit

    Returns
    -------
    string
        SNNS format for one connection
    """

    (k, v), = data.items()
    result =  f"{k:>6} |      |"

    x = v[0]

    layer = [f"{n:>4}: 0.00000" for n in v]
    
    s = ",".join(layer)
    length = 112
    s1 = [s[0+i:length+i] for i in range(0, len(s), length)]
   

    result +=  "\n               ".join(s1)

    return result

def print_all_connection(data):
    result =""

    while data:
        el = data.popitem()
        result += print_connection(dict([el])) + "\n"

    return result


def hidden_layer(string):
    return list(map(int, string.split(',')))

    return int(string) 

def parse_args(args):
    parser = argparse.ArgumentParser(description='Create SNNS net file.')
    parser.add_argument('--input', '-i', required=True,type=int,  help='Number of input neurons')
    parser.add_argument('--hidden', '-H', required=True, type=hidden_layer,  help='Number of hidden neurons per layer')
    parser.add_argument('--output', '-o',  required=True,type=int, help='Number of output neurons')

    return parser.parse_args(args)

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    result =  snns_header()
    result += default_unit_section
    result += unit_definition_header
    result += unit_definition_table_rows(args.input, args.hidden, args.output)
    result += conn_header
    result += conn_separtor

    layers = split_by_layers(args.input, args.hidden, args.output)     

    
    list_conn = list_of_connection(layers)
   
    result += print_all_connection(list_conn)
    result += conn_separtor

    print(result)






