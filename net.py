#!/usr/bin/env python
# Generate SNNS net file
# input No 
# number of nodes in each hidden layer
# number output 

from itertools import pairwise
import argparse

"""
no. | typeName | unitName | act      | bias     | st | position | act func | out func | sites
----|----------|----------|----------|----------|----|----------|----------|----------|-------
  1 |          |          |  0.00000 |  0.00000 | i  |  2, 2, 0 |||
"""
test= """
  1 |          |          |  0.00000 |  0.00000 | i  |  2, 2, 0 |||
"""

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
    st_array = ['i'] * input_no + ["h"] * hidden_no + ["o"] * output_no
    for i in range(1, input_no + hidden_no + output_no +1):
        result += unit_definiton(i, st_array.pop(0),"2, 2, 0") + "\n"

    return result

def split_by_layers(input_no, hidden_layers, output_no):     
    """Set units per layer

    Parameters
    ----------
    input_no : Integer
        number of input units
    hidden_layers: list of Integers
        number of units per hidden layer
    output_no : Integer
        number of output units

    Returns
    -------
    list of list
        A list of each node per layer
    """
    result = []

    data = [input_no] + hidden_layers + [output_no]
    start = 1
    stop = input_no
    #print(f"DATA {data}")
    

    for el in data:
        print(f"range({start}, {stop}+1)")
        layer = [n for n in range(start, stop+1)]
        start += el
        stop += el
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
    strin 
        SNNS format for one connection
    """

    (k, v), = data.items()
    result = '\n' + f"{k:>6} |      |"

    x = v[0]

    layer = [f"{n:>4}: 0.00000" for n in v]
    #print(layer)
    s = ",".join(layer)
    length = 112
    s1 = [s[0+i:length+i] for i in range(0, len(s), length)]
    #print(s1[0])

    result += ( s1[0] + "\n               " +  s1[1]
    + "\n               " +  s1[2]
    + "\n               " +  s1[3]
    + "\n               " +  s1[4]
    + "\n               " +  s1[5]
    + "\n               " +  s1[6]
    + "\n               " +  s1[7]
    + "\n               " +  s1[8]
    + "\n               " +  s1[9]
    + "\n               " +  s1[10]
               )


    #print(result)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create SNNS net file.')
    parser.add_argument('--input', '-i', required=True,type=int,  help='Number of input nodes')
    parser.add_argument('--hidden', '-H', required=True, type=str,  help='Number of hidden nodes per layer')
    parser.add_argument('--output', '-o',  required=True,type=int, help='Number of output nodes')
    #parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    args = parser.parse_args()
    print(args)



#( '{}:0.000, '*len(a) ).format(*a)
new_unit = unit_definiton(1,"i","2, 2, 0") 
new_unit1 = unit_definiton(10,"i","2, 2, 0") 

x = list_of_connection([[1,2],[3,4],[5,6]])
print(x)
print(test)
print(new_unit)
print(new_unit1)
#print(snns_header())
#print(unit_definition_table_rows(2,3,5))



