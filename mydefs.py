#__________________________________________________________
#
# Global definitions
#__________________________________________________________

# Path that contains test files
ex_path = 'logic_analyzer_examples/'

# Indexes for netlist value
TYPE = 0
INPUT = 1
OUTPUT = 2

# Valid gate types for netlist
VALID = ('AND', 'OR', 'NOR', 'NAND', 'NOT')

# Operator character for gates
OP = {'AND': '&', 'OR': '|', 'NOR': '|', 'NAND': '&'}

###########################################################
# End global definitions
###########################################################


#__________________________________________________________
#
# Public functions
#__________________________________________________________

def help_msg(quit):
    """
    Print a help message to the screen.
    If quit == True, exit the program
    """
    print \
"""\
Usage: logic_analyzer.py <netlist_file> <timing_file>
    Replace the arguments with the netlist and timing files you would like to open. The files are loaded
    from the local 'logic_analyzer_examples' directory. For example:

        > logic_analyzer.py test1.net test1.in
        (loads test1.net as the netlist and test1.in as the timing input from ./logic_analyzer_examples/)

    After starting the program, you can use these commands:
    (Note: type 'time' without the quotes in front of your command to view the execution time)

    COMMAND	    DESCRIPTION
    list	    Print circuit node labels as a comma separated list.
    probe V_n	Print the value of circuit node V (0,1,?) at time n.
    probe V	    Print the time sequence of node values as a comma separated list.
    check EXPR	Print the value of the logical expression containing valid time-indexed node variables.
    help	    Print usage instructions
    quit	    Exit the shell and program
"""
    if quit:
        exit()

def get_nodes(netlist, timing):
    """
    Return a list of the nodes in the netlist
    """
    assert isinstance(netlist, dict)
    assert isinstance(timing, dict)

    nodes = []

    # Append the input nodes first
    for inp in timing:
        nodes.append(inp)

    # Now append the output nodes
    for key in netlist:
        nodes.append(netlist[key][OUTPUT])

    return nodes


from collections import deque


def tell_format(gate_type, inp, output, t):
    """
    Returns a sentence which is formatted to tell to a KB.
    Inputs: gate_type: string, type of logic gate
            inp: iterable, nodes (strings) which are inputs to the gate
            output: string, node which is the output of the gate
            t: time point at which nodes are being stimulated/probed
    """
    result = '('
    inputs = list(inp)

    # Add the time point to all the inputs
    for node in range(len(inputs)):
        inputs[node] += '_' + str(t)

    # NOT is the only unary gate and its format is different, so handle that first
    if gate_type == 'NOT':
        result += '~' + inputs[0] + ')<=>' + output

    # Handle other cases
    else:
        for node in range(len(inputs)):
            result += inputs[node]
            if node < (len(inputs) - 1):
                result += OP[gate_type]
        result += ')<=>' + ('~' if gate_type in ('NAND', 'NOR') else '') + output

    # Add the time point to the output
    result += '_' + str(t)
    return result

def wait_for_user():
    return raw_input('> ')

###########################################################
# End public functions
###########################################################