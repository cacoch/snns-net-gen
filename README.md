# Description
The script to create feed forward SNNS net file.

# Usage
./net -i 10 -H 1,2,2 -o 3
We create network with input 10 neurons, 3 hidden layers with 1,2,2 each neuron and output 3 neurons



# Development notes
tested with python 3.12


while sleep 0.1; do ls *.py | entr -d ./net.py {args} ; done

pip install pytest-watcher


run pytest in current directory

ptw .
