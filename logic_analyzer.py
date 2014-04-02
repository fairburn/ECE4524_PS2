from parse import *
from os import path
import sys
import time

# Handle command line args
if len(sys.argv) != 3:
    help_msg(True)
netfile = ex_path + sys.argv[1]
infile = ex_path + sys.argv[2]

# Make sure files exist
if not path.isfile(netfile):
    print netfile, 'could not be found.'
    exit()
if not path.isfile(infile):
    print infile, 'could not be found.'
    exit()

# Dictionaries containing the netlist and timing stimulus data.
# The format of these structures is explained in parse.py
net = {}
timing = {}

# Populate the dictionaries
print 'Parsing', netfile, 'and', infile + '...',
parse_netlist(net, netfile)
parse_stimulus(timing, infile)
print 'Done'

#__________________________________________________________
# Populate the knowledge base and begin polling user input.

kb = logic.PropKB()

# Tell the KB all of the input values at the discrete points in time.
# The amount of time points should always be the same for every input, need to have that next for telling KB the
#   gate outputs. If the number of time points is not the same for every input, unexpected behavior will occur.
# Note: tp refers to the number of discrete time points in which the inputs are changed. This should be the
#   same for each input. I just set it in the for loop since timing is indexed by an arbitrary string. It is
#   needed for putting the gate outputs in the KB.
tp = 0
for inp in timing:
    tp = len(timing[inp])
    for t in range(len(timing[inp])):
        kb.tell(('~' if timing[inp][t] == 0 else '') + inp + '_' + str(t))

# Tell the KB the gate outputs
for gate in net:
    for t in range(tp):
        kb.tell(tell_format(net[gate][TYPE], net[gate][INPUT], net[gate][OUTPUT], t))

# Wait for a user command and then execute
while True:
    cmd = wait_for_user().split(' ')

    # See if the user wants to view execution time
    time_exec = False
    if cmd[0] == 'time':
        time_exec = True
        start_time = time.time()
        cmd.remove('time')

    # Execute the command
    execute(' '.join(cmd), net, timing, kb, tp)

    # Show the execution time if asked to do so
    if time_exec:
        end_time = time.time()
        print 'Finished in', end_time - start_time, 'seconds.'