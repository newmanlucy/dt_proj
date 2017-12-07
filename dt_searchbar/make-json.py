#!/usr/bin/python

import os
from sys import argv
import json
import regex as re

def makeJSON(rootDir):
    jsonList = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            name, ext = os.path.splitext(fname)
            # only indexing markdown files
            if ext != ".md":
                continue
            file=os.path.join(dirName,fname)
            with open(file, 'r') as f:
                secName = None
                secID = None
                # assuming the following syntax for section name and ID:
                #   # [Title of Page] {#[section-ID] (options)} 
                pattern = re.compile("\#\s([^\n]+)[\s]+\{\#([\S]+)[^\n]*\}")
                for line in f:
                    match = pattern.match(line)
                    if match:
                        secName = match.groups()[0]
                        secID = match.groups()[1]
                        secURL = "http://purl.org/dth/" + secID
                        break
            # skip files with no ID
            if not secID:
                continue
            with open(file, 'r') as f:
                text=f.read().replace('\n', ' ')
                d={"id": secID, "title": secName, "body": text}                
                jsonList.append(d)
    ret = json.dumps(jsonList, indent=4, separators=(", ", ": "))
    print(ret)
    return ret

if __name__ == '__main__':
    makeJSON(argv[1])
