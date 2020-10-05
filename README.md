# TCG - Top (Git) Contributors Graph
Builds a weighted graph representing top git contributors in a project. (Internship task)

## Tecnhnologies
* Python 3
* NumPy
* graphviz (as a python lib)
* Various Unix utilities

## Usage
To build TopN git contributors graph of a repo, clone this repo inside the repo you want to work with and launch `main.py`.
```
$ cd /your_repo/
$ git clone *this_repo*
$ cd /TCG/
$ python main.py [-n N_contributors] [--verbose]
```
As a result, a graph will be shown. This graph will be saved as .gv and .pdf in the /TCG/ folder.

## How it works
1. Top N contributors list is retrieved from `git log` and saved to `/data/contributors_N.txt`;
2. For each contributor from the list a list of all files changed by this contributor is retrived and saved to `/data/contributor_name.txt`;
3. For every possible pair of contributors files changed by both contributors are counted (using `comm`);
4. Graph is built with contributors as nodes and edges' length inversely proportional to the number of "shared" files from step 3. Edges representing links above 75th percentile are colored red.

![Alt text](/screenshot.png?raw=true "Top 10 contributors to React")

## Problems
* Python is redundant here, but it was faster/easier to do it this way;
* Graph becomes incomprehensible even with n~30. `graphviz` graphs have rank attributes for nodes and other things that might help prettify the graph;
* Solution should be lazier. If data for top 50 was already retrieved, then on the next run the data should be re-used, not re-downloaded. If data was retrieved for top 30, then only data for 31-50th contributors should be retrived on `-n 50` launch. (Of course, then an additional flag --force-redownload should be introduced);
* Possible problem with the React repo: "Dan" and "Dan Abramov" are probably one person. Maybe close nodes with similar names should be merged;
