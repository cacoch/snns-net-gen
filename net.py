#!/usr/bin/env python
# Generate SNNS net file
# input No 
# number of nodes in each hidden layer
# number output 

from itertools import pairwise
import argparse
import sys

"""
no. | typeName | unitName | act      | bias     | st | position | act func | out func | sites
----|----------|----------|----------|----------|----|----------|----------|----------|-------
  1 |          |          |  0.00000 |  0.00000 | i  |  2, 2, 0 |||
"""
test= """
  1 |          |          |  0.00000 |  0.00000 | i  |  2, 2, 0 |||
"""

print("##########################")

def snns_header(units=128, connections=1071):
    h = """
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

    return h

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
    stop = input_no
    print(f"DATA {data}")
    

    for el in data:
        print(f"range({start}, {stop}+1)")
        layer = [n for n in range(start, stop+1)]
        start += el
        stop += el +1
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

    print(data.items())
    (k, v), = data.items()
    result =  f"{k:>6} |      |"

    x = v[0]

    layer = [f"{n:>4}: 0.00000" for n in v]
    #print(layer)
    s = ",".join(layer)
    length = 112
    s1 = [s[0+i:length+i] for i in range(0, len(s), length)]
    #print(s1[0])

    result +=  "\n               ".join(s1)

    return result

def print_all_connection(data):
    result =""

    while data:
        el = data.popitem()
        result += print_connection(dict([el])) + "\n"

    return result

conn_separtor = """
-------|------|----------------------------------------------------------------------------------------------------------------
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

    layers = split_by_layers(args.input, args.hidden, args.output)     

    print(f"Layers: {layers}")
    list_conn = list_of_connection(layers)
    print(list_conn)
    result += print_all_connection(list_conn)

    print("##### Start ###########") 
    print(result)
    print("###### END  ###########") 



#( '{}:0.000, '*len(a) ).format(*a)
new_unit = unit_definiton(1,"i","2, 2, 0") 
new_unit1 = unit_definiton(10,"i","2, 2, 0") 

x = list_of_connection([[1,2],[3,4],[5,6]])
#print(x)
#print(test)
#print(new_unit)
#print(new_unit1)
#
#print(print_all_connection({3: [1, 2], 4: [1, 2], 5: [3, 4], 6: [3, 4]}))

#print(unit_definition_table_rows(2,3,5))



