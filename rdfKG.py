from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD, NamespaceManager
from rdflib import Namespace


def getData(path, limit, verbose=True):
	import sys

	# print ('\tObteniendo datos ...')
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
	tag = entity.pop().lower()
	entity = '_'.join(entity)
	return (entity, tag)

def setFOAF(g, clase, entity, text):
	text = ' '.join(text.split('_'))
	g.add( (entity, RDF.type, FOAF[clase]) )
	g.add( (entity, FOAF.name, Literal(text, lang="es")) )

def setDBPediaClass(g, clase, entity, text):
	text = ' '.join(text.split('_'))
	g.add( (entity, RDF.type, dbpedia[clase]) )
	g.add( (entity, FOAF.name, Literal(text, lang="es")) )

def setRelation(g, text):
	text = ' '.join(text.split('_'))
	g.add( (predicade, RDF.type, dbpedia.Relationship) )
	g.add( (predicade, FOAF.name, Literal(text)) )

path = '/home/orlando/data/triples_15_entidades_mayo1.txt'
limit = 10
triples = getData(path, limit, False)


# ====================================================================
# namespaces
dbpedia = Namespace('http://dbpedia.org/ontology/')
lke = Namespace('http://mx-kg.com/')
nmng = NamespaceManager(Graph())
nmng.bind('dbp', dbpedia, override=False)
nmng.bind('foaf', FOAF, override=False)
nmng.bind('lke', lke, override=False)
# ====================================================================
# --------------------------------------------------------------------

g = Graph()

g.namespace_manager = nmng
all_ns = [n for n in g.namespace_manager.namespaces()]
assert ('lke', URIRef('http://mx-kg.com/')) in all_ns
# print (all_ns)


# --------------------------------------------------------------------

# --------------------------------------------------------------------
# schema definition with all named entities
# per = Namespace('http://mx-kg.com/people/')
# org = Namespace('http://mx-kg.com/organization/')
# dat = Namespace('http://mx-kg.com/date/')
# tit = Namespace('http://mx-kg.com/job/')
# gpe = Namespace('http://mx-kg.com/geopolitical/')
# pex = Namespace('http://mx-kg.com/politicalparty/')
# tim = Namespace('http://mx-kg.com/time/')
# fac = Namespace('http://mx-kg.com/facility/')
# evt = Namespace('http://mx-kg.com/event/')
# mny = Namespace('http://mx-kg.com/money/')
# doc = Namespace('http://mx-kg.com/document/')
# pro = Namespace('http://mx-kg.com/product/')
# dem = Namespace('http://mx-kg.com/demonym/')
# age = Namespace('http://mx-kg.com/age/')
# loc = Namespace('http://mx-kg.com/location/')
# rel = Namespace('http://mx-kg.com/relation/')
nspaces = {
	'per': 'people',
	'org': 'organization',
	'dat': 'date',
	'tit': 'job',
	'gpe': 'geopolitical',
	'pex': 'politicalparty',
	'tim': 'time',
	'fac': 'facility',
	'evt': 'event',
	'mny': 'money',
	'doc': 'document',
	'pro': 'product',
	'dem': 'demonym',
	'age': 'age',
	'loc': 'location',
	'rel': 'relation',
}
# --------------------------------------------------------------------



for triple in triples:
	ent1 = cleanAndExtractEntityClass(triple[0])
	ent2 = cleanAndExtractEntityClass(triple[1])
	relation = triple[2]
	# entity2 = eval('{}.{}'.format(ent2[1], ent2[0]))
	entity1 = lke['{}/{}'.format(nspaces[ent1[1]], ent1[0])]
	entity2 = lke['{}/{}'.format(nspaces[ent2[1]], ent2[0])]

	predicade = lke['{}/{}'.format('relation', relation)]
	# print ( entity1, entity2, predicade )

	if ent1[1] == 'per': setFOAF(g, 'Person', entity1, ent1[0])
	if ent2[1] == 'per': setFOAF(g, 'Person', entity2, ent2[0])

	if ent1[1] == 'org': setDBPediaClass(g, 'Organization', entity1, ent1[0])
	if ent2[1] == 'org': setDBPediaClass(g, 'Organization', entity2, ent2[0])

	# date

	# job title

	if ent1[1] == 'gpe': setDBPediaClass(g, 'PopulatedPlace', entity1, ent1[0])
	if ent2[1] == 'gpe': setDBPediaClass(g, 'PopulatedPlace', entity2, ent2[0])

	if ent1[1] == 'pex': setDBPediaClass(g, 'PoliticalParty', entity1, ent1[0])
	if ent2[1] == 'pex': setDBPediaClass(g, 'PoliticalParty', entity2, ent2[0])

	# time

	if ent1[1] == 'fac': setDBPediaClass(g, 'Building', entity1, ent1[0])
	if ent2[1] == 'fac': setDBPediaClass(g, 'Building', entity2, ent2[0])

	if ent1[1] == 'evt': setDBPediaClass(g, 'Event', entity1, ent1[0])
	if ent2[1] == 'evt': setDBPediaClass(g, 'Event', entity2, ent2[0])

	# money

	if ent1[1] == 'doc': setFOAF(g, 'Document', entity1, ent1[0])
	if ent2[1] == 'doc': setFOAF(g, 'Document', entity2, ent2[0])

	# product

	# demonym

	# age

	if ent1[1] == 'loc': setDBPediaClass(g, 'Place', entity1, ent1[0])
	if ent2[1] == 'loc': setDBPediaClass(g, 'Place', entity2, ent2[0])


	setRelation(g, relation)

	g.add( (entity1, predicade, entity2) )

	# g.add( (entity1, RDF.type, FOAF.Person) )
	# g.add( (entity1, predicade, entity2) )
	# g.add( (entity1, RDF.type, FOAF.Person) )

# # create a Graph

# # Create an RDF URI node to use as the subject for multiple triples
# orlando = URIRef("http://arcturus.cs.bua.mx/kg")

# # Add triples using store's add() method.
# g.add((orlando, RDF.type, FOAF.Person))
# g.add((orlando, FOAF.nick, Literal("orlando", lang="es")))
# g.add((orlando, FOAF.name, Literal("Orlando Ramos Flores")))
# g.add((orlando, FOAF.mbox, URIRef("mailto:orlandxrf@gmail.com")))

# # Add another person
# ed = URIRef("http://example.org/edward")

# # Add triples using store's add() method.
# g.add((ed, RDF.type, FOAF.Person))
# g.add((ed, FOAF.nick, Literal("ed", datatype=XSD.string)))
# g.add((ed, FOAF.name, Literal("Edward Scissorhands")))
# g.add((ed, FOAF.mbox, URIRef("mailto:e.scissorhands@example.org")))

# # Iterate over triples in store and print them out.
# print("--- printing raw triples ---")
# for s, p, o in g:
# 	print((s, p, o))

# # For each foaf:Person in the store, print out their mbox property's value.
# print("--- printing mboxes ---")
# for person in g.subjects(RDF.type, FOAF.Person):
# 	for mbox in g.objects(person, FOAF.mbox):
# 		print(mbox)

# # Bind the FOAF namespace to a prefix for more readable output
# g.bind("foaf", FOAF)

# # print all the data in the Notation3 format
# print("--- printing mboxes ---")



# print(g.serialize(format='xml').decode("utf-8"))

g.serialize(destination='knowledge-graph.xml', format="xml")
g.close()
