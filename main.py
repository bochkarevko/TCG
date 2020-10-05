import argparse
from graphviz import Graph
from itertools import combinations 
import subprocess
import numpy as np
import logging

def get_data(N:int=10):
    cmd = ["./get_top.sh", str(N)]
    subprocess.Popen(cmd).wait()
    cmd = ["./all_files.sh", str(N)]
    subprocess.Popen(cmd).wait()

def parse(N:int=10):
    contributors_list = []
    with open(f"data/contributors_{N}.txt", "r") as file:
        for line in file:
            contributors_list.append(line.strip())
    return contributors_list

def plot_graph(contributors):
    g = Graph(f'Top {len(contributors)} contributors', filename='graph.gv', engine='neato')
    g.attr(rankdir='LR')

    pairs = list(combinations(contributors, 2))
    counts = np.zeros(len(pairs), dtype=int)
    for i, (contributor1, contributor2) in enumerate(pairs):
        cmd = ["comm", "-123", "--total", f"data/{contributor1}.txt", f"data/{contributor2}.txt"]
        shared_changed = subprocess.run(cmd, stdout=subprocess.PIPE)
        count = int(shared_changed.stdout.decode('utf-8').split()[2])
        counts[i] = count

    top_25 = np.percentile(counts, 75)
    logging.debug(f"N contributions for top 25%: {top_25}")

    lens = (np.max(counts) - counts + np.min(counts)) / np.max(counts) * 10 # some edge gets 0 length - not good
    for i, (contributor1, contributor2) in enumerate(pairs):
        if counts[i] > 0:
            if counts[i] > top_25:
                color = 'red'
            else:
                color = 'black'
            g.edge(contributor1, contributor2, len=str(lens[i]), 
                   label=str(counts[i]), color=color)

    logging.debug(g.source)
    g.view()

def plot_graph_nx(contributors):
    G = nx.Graph()
    labels = {}
    for contributor in contributors:
        G.add_node(contributor)
        labels[contributor] = contributor
 
    pairs = list(combinations(contributors, 2))
    for contributor1, contributor2 in pairs:
        cmd = ["comm", "-123", "--total", f"data/{contributor1}.txt", f"data/{contributor2}.txt"]
        shared_changed = subprocess.run(cmd, stdout=subprocess.PIPE)
        count = int(shared_changed.stdout.decode('utf-8').split()[2])
        if count > 0:
            G.add_edge(contributor1, contributor2, weight=count)

    pos = nx.circular_layout(G) # spring_layout
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=750)
    
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    nx.draw_networkx_edges(G, pos, width=5)

    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis('off')
    plt.title(f"Top {len(contributors)} contributors")
    plt.savefig(f"Top_{len(contributors)}.png") 
    plt.show() 
 
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10,
                        help="How many contributors to get")
    parser.add_argument("--verbose", help="debug log level",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    get_data(args.number)
    contributors_list = parse(args.number)
    plot_graph(contributors_list)
