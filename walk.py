import data
import rdflib as rdf
import random
import pyttsx3

engine = pyttsx3.init()

NAME = 'aifb'
STARTING_NODE = rdf.URIRef('http://www.aifb.uni-karlsruhe.de/Publikationen/viewPublikationOWL/id647instance')

def say(inp):
    engine.say(inp)
    engine.runAndWait()

class Inv():
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return 'inverse of {}'.format(str(self.m))

def s(node):

    if type(node) == rdf.Literal:
        return str(node)

    url = str(node)

    return url.split('/')[-1]

def retrieve(node, graph):
    """
    Executes a random walk step

    :param node:
    :return:
    """

    # collect properties (neighboring literals)
    properties = []
    for s, p, o in graph.triples( (node, None, None) ):
        if type(o) == rdf.Literal:
            properties.append((s, p, o))

    # collect next step candidates (neighboring non-literals)
    candidates = []
    for s, p, o in graph.triples( (node, None, None) ):
        if type(o) != rdf.Literal:
            candidates.append((s, p, o))

    for s, p, o in graph.triples((None, None, node)):
        candidates.append((o, Inv(p), s))

    return properties, candidates

graph = data.load(NAME)

node = STARTING_NODE

while True:

    props, cands = retrieve(node, graph)

    sub, pred, obj = random.choice(props)

    say('now at node {}'.format(s(node)))
    say('{} has property {} with value {}'.format(s(sub), s(pred), s(obj)))

    fr, prop, to = random.choice(cands)

    say('moving over property {}'.format( s(prop) ))

    input('...')




