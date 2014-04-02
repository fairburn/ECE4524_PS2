from parse import *
import sys

if len(sys.argv) != 2:
    help_msg(True)

# Dictionaries containing the netlist and timing stimulus data.
# The format of these structures is explained in parse.py
net = {}
timing = {}

# Populate the dictionaries
print 'Loading', sys.argv[1] + '...',
parse_netlist(net, sys.argv[1] + '.net')
parse_stimulus(timing, sys.argv[1] + '.in')
print 'Done'

#__________________________________________________________
# Populate the knowledge base
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
    cmd = wait_for_user()
    execute(cmd, net, timing, kb, tp)