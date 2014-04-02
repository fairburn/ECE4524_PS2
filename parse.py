from mydefs import *
import logic


def parse_netlist(netlist, netfile):
    """
    Populate the netlist dictionary from an input file.
    """
    assert isinstance(netlist, dict)
    assert isinstance(netfile, str)
    
    gate_strlist = []
    with open(ex_path + netfile) as f:
        for line in f:
            # Clean up gate string so it can be formatted for netlist addition
            gate_strlist.append(line.replace(' ', '').replace('(', '').replace(')', '').strip())

    # Create netlist from test file
    key = 0  # key of dictionary
    for gate in gate_strlist:
        assert (isinstance(gate, str))
        # Clean up gate so it can be formatted for netlist addition
        gate = gate.split(',')

        # Assert that gate type is valid.
        assert (gate[TYPE] in VALID)

        # Format the gate
        # Keys are ascending integers starting at 0
        # Values are tuples with: gate type (string), input nodes (tuple), and output node (string)
        gate = tuple([gate[TYPE],                                       # insert type
                      tuple(gate[x] for x in range(1, len(gate) - 1)),  # insert input nodes
                      gate[len(gate) - 1]])                             # insert output node

        netlist[key] = gate
        key += 1


def parse_stimulus(stimulus, infile):
    """
    Populate the timing stimulus dictionary from and input file.
    """
    assert isinstance(stimulus, dict)

    # Get timing information from file, being sure to ignore whitespace
    timing = ''
    with open(ex_path + infile) as f:
        for line in f:
            timing += line.replace(' ', '').strip()

    # Split input into a list and convert the one and zero characters to numbers.
    # Also initialize the stimulus dict.
    timing = timing.split(',')
    for x in range(len(timing)):
        if timing[x] in ('0', '1'):
            timing[x] = int(timing[x])
        else:
            stimulus[timing[x]] = []

    # Assert that the first value in the timing stimulus is a node and not a logical value.
    # This is necessary due to the way that I populate the dictionary in the following loop.
    assert isinstance(timing[0], str)

    # Populate the timing stimulus
    # Keys are the node names
    # Values are lists containing the timing waveform
    key = ''
    for val in timing:
        if isinstance(val, str):
            key = val
        if val in (0, 1):
            stimulus[key].append(val)



def execute(cmd, net, timing, kb, tp):
    """
    Carry out the user command.
    Inputs: cmd: string, user's typed command
            net: dict, netlist (see parse_netlist)
            timing: dict, input stimulus (see parse_stimulus)
            kb: logic.PropKB, knowledge base
            tp: int, number of discrete time points in which the inputs are stimulated
    """
    assert isinstance(cmd, str)
    assert isinstance(net, dict)
    assert isinstance(timing, dict)
    assert isinstance(kb, logic.PropKB)
    cmd = cmd.split(' ')
    if not cmd[0]:
        return

    if cmd[0] == 'list':
        print get_nodes(net, timing)
        return

    elif cmd[0] == 'help':
        help_msg(False)
        return

    elif cmd[0] == 'quit':
        exit()

    # Note: for probing, I bypass the KB if the node is found in the timing stimulus. It is much faster to do it
    #   this way.
    elif cmd[0] == 'probe':
        if len(cmd) != 2:
            print 'Error: incorrect command, type help to see command format.'
            return

        # node[0] = node name
        # node[1] = time point
        node = cmd[1].split('_')
        if node[0] not in get_nodes(net, timing):
            print 'Error: node', node[0], 'does not exist'
            return
        if len(node) == 2:
            if int(node[1]) not in range(tp):
                print 'Error: time point out of range (indexing starts at 0).'
                return
            print 'Node', node[0], 'at time', node[1] + ':',
            if node[0] in timing:
                print timing[node[0]][int(node[1])]
            else:
                tr = logic.pl_resolution(kb, logic.expr('_'.join(node)))
                print '1' if tr else '0'
            return
        elif len(node) == 1:
            if node[0] in timing:
                print node[0] + ':', timing[node[0]]
            else:
                print 'Finding values for node', node[0] + '...'
                temp = []
                for x in range(tp):
                    tr = logic.pl_resolution(kb, logic.expr(node[0] + '_' + str(x)))
                    temp.append(1 if tr else 0)
                print node[0] + ':', temp
            return
        else:
            print 'Error: incorrect node format.'
            return

    elif cmd[0] == 'check':
        if len(cmd) != 2:
            print 'Error: incorrect command, type help to see command format.'
            return
        print 'Finding value of', cmd[1] + '...'
        print logic.pl_resolution(kb, logic.expr(cmd[1]))
        return

    else:
        print 'Error: incorrect command, type help to see command format.'
        return