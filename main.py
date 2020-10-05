import argparse
from graphviz import Graph
from itertools import combinations 
import subprocess
import numpy as np
import logging

def get_data(N:int=10):
    logging.info(f"Getting top {N} contributors")
    cmd = ["./get_top.sh", str(N)]
    subprocess.Popen(cmd).wait()
    logging.info(f"Getting all files changed by top {N} contributors")
    cmd = ["./all_files.sh", str(N)]
    subprocess.Popen(cmd).wait()

def parse(N:int=10):
    contributors_list = []
    with open(f"data/contributors_{N}.txt", "r") as file:
        for line in file:
            contributors_list.append(line.strip())
    return contributors_list

def count_to_len(X:np.array, Max:int=10, Min:int=2):
    """interpolate lineary [min, max] -> [Max, 2] (min -> Max, max -> Min)"""
    return np.interp(X, (X.min(), X.max()), (Max, Min))

def plot_graph(contributors):
    logging.info(f"Preparing graph")
    g = Graph(f'Top {len(contributors)} contributors', 
              filename=f'graph_{len(contributors)}.gv', engine='neato')

    pairs = list(combinations(contributors, 2))
    counts = np.zeros(len(pairs), dtype=int)
    for i, (contributor1, contributor2) in enumerate(pairs):
        cmd = ["comm", "-123", "--total", 
            f"data/{contributor1}.txt", f"data/{contributor2}.txt"]
        shared_changed = subprocess.run(cmd, stdout=subprocess.PIPE)
        count = int(shared_changed.stdout.decode('utf-8').split()[2])
        counts[i] = count

    top_25 = np.percentile(counts[counts > 0], 75)
    bot_25 = np.percentile(counts[counts > 0], 25)
    logging.debug(f"N contributions for top 25%: {top_25}")
    logging.debug(f"N contributions for bot 25%: {bot_25}")

    lens = count_to_len(counts, Max=len(contributors))
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
 
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10,
                        help="How many contributors to get")
    parser.add_argument("--verbose", help="debug log level",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    if args.number > 60:
        logging.warning("N too large, sorry")
        exit()
    get_data(args.number)
    contributors_list = parse(args.number)
    plot_graph(contributors_list)
