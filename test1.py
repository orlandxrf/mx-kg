import rdflib

g = rdflib.Graph()
has_border_with = rdflib.URIRef('http://www.example.org/has_border_with')
located_in = rdflib.URIRef('http://www.example.org/located_in')

germany = rdflib.URIRef('http://www.example.org/country1')
france = rdflib.URIRef('http://www.example.org/country2')
china = rdflib.URIRef('http://www.example.org/country3')
mongolia = rdflib.URIRef('http://www.example.org/country4')

europa = rdflib.URIRef('http://www.example.org/part1')
asia = rdflib.URIRef('http://www.example.org/part2')

g.add((germany,has_border_with,france))
g.add((china,has_border_with,mongolia))
g.add((germany,located_in,europa))
g.add((france,located_in,europa))
g.add((china,located_in,asia))
g.add((mongolia,located_in,asia))

print ( g.serialize(format="xml") )
