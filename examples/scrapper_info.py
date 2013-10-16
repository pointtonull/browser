#!/usr/bin/python
# -*- coding: UTF-8 -*-

from functools import wraps
from scrapper import Scrapper
import fb
import pickle
import sys


def retry(func):
    @wraps(func)
    def decorated(*args):
        result = func(*args)
        while not result:
            print("Retrying..")
            result = func(*args, retry=True)
        return result
    return decorated


if __name__ == "__main__":
    scrapper = Scrapper()
    nodes = set()
    nodes_sets = [pickle.load(open(filename)) for filename in sys.argv[1:]]
    nodes_info_filename = "all_nodes_info.pickle"

    try:
        nodes_info = pickle.load(open(nodes_info_filename))
        processed = set(nodes_info.keys())
    except IOError:
        nodes_info = {}
        processed = set()

    for nodes_set in nodes_sets:
        for number, node in enumerate(nodes_set - processed):
            nodes_info[node] = scrapper.get_node_info(node)
            processed.add(node)
            try:
                print("%d / %d / %d  %s" % (len(processed), len(nodes_set), 
                    len(nodes_sets), nodes_info[node]["name"]))
            except:
                pass

            if not(number % 1000):
                nodes_info_file = open(nodes_info_filename, "w")
                pickle.dump(nodes_info, nodes_info_file)
                nodes_info_file.close()
                print("-------------------------------------------------- Flushed")

        nodes_info_file = open(nodes_info_filename, "w")
        pickle.dump(nodes_info, nodes_info_file)
        nodes_info_file.close()
        print("-------------------------------------------------- Flushed")
