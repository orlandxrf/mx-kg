import networkx as nx

def getData(path, limit, verbose=True):
	import sys

	print ('\tObteniendo datos ...')
	triples = []
	with open(path, 'r') as f:
		for i, row in enumerate(f):
			if i==0: continue # skip header
			if i==limit: break
			if verbose:
				sys.stdout.write( '\tProcesando {} tripletas ...\r'.format( format(i,',d') ) )
				sys.stdout.flush()
			__, __, triple = row.replace('\n','').split('\t')
			triples.append( eval(triple) )
	f.close()
	if verbose: print ('\n\tTerminado!!\n')
	return triples

def cleanAndExtractEntityClass(entity):
	entity = entity.split('_')
	tag = entity.pop()
	entity = ' '.join(entity)
	return (entity, tag)


def makeKG(triples):
	import networkx as nx

	print ('\tConstruyendo el KG')
	G = nx.MultiDiGraph()
	for i, triple in enumerate(triples):
		ent1 = cleanAndExtractEntityClass(triple[0])
		ent2 = cleanAndExtractEntityClass(triple[1])
		rel = ' '.join(triple[2].split('_'))
		if ent1[0] not in G: G.add_node(ent1[0], type=ent1[1])
		if ent2[0] not in G: G.add_node(ent2[0], type=ent2[1])
		G.add_edge(ent1[0], ent2[0], relation=rel)
	return G


def showKG(G):
	import matplotlib.pyplot as plt
	import networkx as nx

	print ('\tGraficando KG ...')
	plt.figure(figsize=(12,12))

	pos =nx.spring_layout(G)
	nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos, font_size=8)
	# plt.show()
	plt.savefig(fname="mx-kg.pdf", format="pdf", bbox_inches='tight', dpi=200, transparent=True)
	plt.savefig(fname="mx-kg.png", format="png", bbox_inches='tight', dpi=200, transparent=True)
	print ('\tImagen salvada!')



path = '/home/orlando/data/triples_15_entidades_mayo1.txt'
limit = 1000
triples = []
triples = getData(path, limit, False)
G = makeKG(triples)
showKG(G)


# print ('-'*100)

# nodes = list(G.nodes(data=True))
# edges = list(G.edges(data=True))
# for x in nodes:
# 	print (x)

# print ('-'*100)

# for x in edges:
# 	print (x)







