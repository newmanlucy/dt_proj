#!/usr/bin/env python

import yaml
import json
from os.path import splitext, basename
from graphviz import Digraph

DESCRIPTION = 'description'
PARAMETERS = 'parameters'
SUBSCRIPTIONS = 'subscriptions'
PUBLISHERS = 'publishers'
TOPIC = 'topic'

class NodeVisualizer():
    def __init__(self, robotname, name, file, colorscheme):
        self.robotname = robotname
        self.colorscheme = colorscheme
        self.name = name
        self.infilename = file
        self.basename = basename(splitext(self.infilename)[0])
        self.nodename = "/" + self.robotname + "/" + self.basename
        with open(file, 'r') as stream:
            try: 
                self.doc = yaml.load(stream)
            except:
                raise RuntimeError("invalid file")
        self.description = self.doc[DESCRIPTION]
        self.parameters = self.doc[PARAMETERS]
        self.subscriptions = self.doc[SUBSCRIPTIONS]
        self.publishers = self.doc[PUBLISHERS]

    @property
    def title(self):
        return self.basename.replace("_", " ").title()

    @property
    def outfilename(self):
        return splitext(self.infilename)[0] + ".gv"

    def format_pub_sub(self, string, out):
        prefix = "pub_" if out else "sub_"
        label = prefix + string
        name = self.nodename + "_" + label
        return label, name

    def format_topic(self, string):
        name = "/" + self.robotname + "/" + string[1:]
        return name

    def visualize(self, g):
        cname = "cluster_" + self.nodename[1:]
        c = Digraph(name=cname)

        c.attr(label=self.title)
#        c.attr(shape="oval")
        c.attr(labelfloat='yes')
        c.attr(labelfontcolor='grey18')
        c.attr(labelfontsize='24.0')
        c.attr(colorscheme=self.colorscheme)
#        c.attr(style='solid')
        c.attr(style='filled')
        c.attr(color='lightgrey')
        c.node_attr.update(style='filled',
            color='grey60', 
            fillcolor='lightsteelblue2')
        
        c.node(self.nodename, shape='oval', height="3", width="5")

        for pub in self.publishers:
            plabel, pname = self.format_pub_sub(pub, True)
            c.node(pname, 
                label=plabel, 
                shape='box', 
                style='filled,dotted', 
                fillcolor='lightsteelblue3')
            c.edge(self.nodename, pname, dir='none')
            topic = self.publishers[pub][TOPIC]
            tname = self.format_topic(topic)
            #print (tlabel, tname)
            pubnode = g.node(tname, 
                shape='box',
                style='filled',
                color='grey32',
                fillcolor='lightslategrey')
            g.edge(pname, tname)

        for sub in self.subscriptions:
            slabel, sname = self.format_pub_sub(sub, False)
            c.node(sname, 
                label=slabel,
                shape='box', 
                style='filled,dotted',
                fillcolor='lightsteelblue1')
            c.edge(sname, self.nodename, dir='none')
            topic = self.subscriptions[sub][TOPIC]
            tname = self.format_topic(topic)
            subnode = g.node(tname, 
                shape='box', 
                style='filled',
                color='grey32', 
                fillcolor='lightslategrey')
            g.edge(tname, sname)

        g.subgraph(c)
            

#        print(g.source)


    def __str__(self):
        return json.dumps(self.doc, indent=4, separators=(',',': '))

    def __repr__(self):
        print(self.__str__())


if __name__ == '__main__':
    nv = NodeVisualizer("testnode", "lane_filter_node.yaml", "brbg4")
    g = Digraph(name=nv.name)
    g.attr(splines='ortho')
    g.attr(overlap='false')
    nv.visualize(g)
    g.render(nv.outfilename, view=True)
