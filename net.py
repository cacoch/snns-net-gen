#!/usr/bin/env python

# Generate SNNS net file
# input No 
# number of nodes in each hidden layer
# number output 


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

    


new_unit = unit_definiton(1,"i","2, 2, 0") 
new_unit1 = unit_definiton(10,"i","2, 2, 0") 

print(test)
print(new_unit)
print(new_unit1)
print(snns_header())
print(unit_definition_table_rows(2,3,5))


