#!/usr/bin/env python

import sys, os

filename = sys.argv[1] if len(sys.argv) >= 2 else raw_input("Filename? ")

inlines = os.popen("sed -f stripgraphfile.sed " + filename)

nodes = []
nodelabels = {}
outneighbors = {}
inneighbors = {}
nodevalues = {}

for inline in inlines:
	if inline.rstrip() == "":
		continue
	firstword = inline[:inline.find(" ")]
	rest = inline[inline.find(" ")+1:].rstrip()
	if firstword == "NODE":
		nodes.append(rest)
		outneighbors[rest] = []
		inneighbors[rest] = []
	elif firstword == "LABEL":
		nodelabels[nodes[-1]] = rest
	elif firstword == "BORDER":
		split = rest.find(" ")
		linetype = rest[:split]
		linewidth = float(rest[split+1:])
		nodevalue = (1 if linetype == "line" else -1) * (linewidth ** 3)
		nodevalues[nodes[-1]] = nodevalue
	elif firstword == "EDGE":
		split = rest.find(" ")
		source = rest[:split]
		target = rest[split+1:]
		outneighbors[source].append(target)
		inneighbors[target].append(source)
		

def toposort(Nodes, Out):
	"Return Nodes in topologically-sorted order; Out is a dictionary from each node to a list of that node's out-neighbors."
	Nodes = Nodes[:]
	Out = Out.copy()
	R = []
	while Nodes:
		for k,v in Out.items():
			if len(v) == 0:
				R.append(k)
				for source in Nodes:
					while k in Out[source]: #WHILE rather than IF, because I sometimes use multiple arrows from A to B to show that A was a major causal factor in B
						del Out[source][Out[source].index(k)]
				del Nodes[Nodes.index(k)]
				del Out[k]
				break
		else:
			print "LOOP with nodes", Nodes
			print "LOOPING nodes are called: ", [nodelabels[n] for n in Nodes]
			sys.exit(1)
	return R
			

nodeseq = toposort(nodes, outneighbors)

for currnode in nodeseq:
	if len(inneighbors[currnode]) == 0:
		continue
	valuetoeach = nodevalues[currnode] / len(inneighbors[currnode])
	for sourcenode in inneighbors[currnode]:
		nodevalues[sourcenode] += valuetoeach

print "NODES AND THEIR VALUES"
SortedNodeValues = [(nodevalues[node], nodelabels[node]) for node in nodes]
SortedNodeValues.sort(reverse=True)
for v, n in SortedNodeValues:
	print n.ljust(70) + ("%.2f" % v).rjust(10)

