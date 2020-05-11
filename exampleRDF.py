from rdflib.namespace import FOAF, RDF
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace



bob = URIRef("http://example.org/people/Bob")
linda = BNode()  # a GUID is generated

amlo = URIRef("http://example.org/people/López_Obrador")
bety = URIRef("http://example.org/people/Beatriz_Müller")
merry = URIRef("http://example.org/status/esta_casado_con")

name = Literal('Bob')  # passing a string
# age = Literal(24)  # passing a python int
# height = Literal(76.5)  # passing a python float

g = Graph()

g.bind("foaf", FOAF)

# g.add((bob, RDF.type, FOAF.Person))
# g.add((bob, FOAF.name, name))
# g.add((bob, FOAF.knows, linda))
# g.add((linda, RDF.type, FOAF.Person))
# g.add((linda, FOAF.name, Literal("Linda")))

g.add((amlo, RDF.type, FOAF.Person))
g.add((amlo, FOAF.name, Literal('López_Obrador')))
g.add((amlo, merry, bety))
g.add((bety, RDF.type, FOAF.Person))
g.add((bety, FOAF.name, Literal('Beatriz_Müller')))

print(g.serialize(format="xml").decode("utf-8"))
