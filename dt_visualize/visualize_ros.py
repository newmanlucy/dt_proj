#!/usr/bin/env python

from visualize_node import NodeVisualizer
from graphviz import Digraph
from sys import argv

class ROSVisualizer():
    def __init__(self, robot_name, name, filenames, outfile, colorscheme):
        g = Digraph(name)
        g.attr(splines='ortho')
        g.attr(overlap='false')
        g.attr(fontname='helvetica')
        g.attr(fontsize='24.0')
        g.attr('node',fontname='mono')
        g.attr('node', pad="3")
        g.attr(nodesep="1")
        g.attr(ranksep="1")
        for f in filenames:
            cname = "cluster_" + f
            node = NodeVisualizer(robot_name, cname, f, colorscheme)
            node.visualize(g)
        g.render(outfile, view=True)

        print(g.source)

if __name__ == '__main__':
    files = argv[1].split(':')
    ROSVisualizer("robot_name", 
        "ROSViz",
        files,
        "out.gv",
        "brbg4")
