import argparse
from itertools import combinations 
import matplotlib.pyplot as plt
import networkx as nx
import subprocess

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
    args = parser.parse_args()
    get_data(args.number)
    contributors_list = parse(args.number)
    plot_graph(contributors_list)
