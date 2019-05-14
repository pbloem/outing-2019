# Uses python2

import data
import rdflib as rdf
import random, math, requests, time

import roslib #; roslib.load_manifest('sr_example')
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, String

rospy.init_node('turtlebot_controller', anonymous=True)

def move(dist, angle):

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    message = Twist()
    message.linear.x = dist
    message.angular.z = angle

    pub.publish(message)

SAYSERVER = '127.0.0.1'
NAME = 'eswc'
# STARTING_NODE = rdf.URIRef('http://www.aifb.uni-karlsruhe.de/Publikationen/viewPublikationOWL/id647instance')
STARTING_NODE = rdf.URIRef('https://w3id.org/scholarlydata/person/ilaria-tiddi')

def say(inp):
    print(inp)
    requests.get('http://{}/?say="{}"'.format(SAYSERVER, inp))

class Inv():
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return 'inverse of {}'.format(str(self.m))

def s(node):
    pref = 'inverse of ' if type(node) == Inv else ''

    if type(node) == rdf.Literal:
        return str(node)

    url = str(node)

    return pref + url.split('/')[-1].split('#')[-1]

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
pos = (0.0, 0.0)

while True:

    props, cands = retrieve(node, graph)

    sub, pred, obj = random.choice(props)

    say('now at node {}'.format(s(node)))
    say('{} has property {} with value {}'.format(s(sub), s(pred), s(obj)))

    fr, prop, to = random.choice(cands)

    say('moving over relation {}'.format( s(prop) ))

    node = to

    # compute new position
    oldpos = pos
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))

    a = pos[0] - oldpos[0]
    b = pos[1] - oldpos[1]

    dist = math.sqrt(a*a + b*b)
    angle = math.atan(b/a)

    print('new pos ({:.2}, {:.2}), rotate {:.2}, move {:.2}'.format(pos[0], pos[1], angle, dist))

    move(dist, angle)

    input('...')




