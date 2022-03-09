import matplotlib.pyplot as plt
import networkx as nx

def all_road_connections(roads):
    # Tar liste av start-slutt-koordinat-tupler og finner alle veier som 
    # peker ut av en annen vei. 
    # Returnerer dette som en liste av [fra-vei-indeks, til-vei-indeks].

    #children = {}
    children = []
    for i in range(len(roads)):
        #children[i] = []
        end = roads[i][1]

        for j in range(len(roads)):
            if j == i:
                continue
            elif roads[j][0] == end:
                #children[i].append(j)
                children.append((i, j))
    return children

def sources_and_sinks(nodes, edges):
    sources = [n for n in nodes]
    sinks = [n for n in nodes]
    for (from_i, to_i) in edges:
        if from_i in sinks: sinks.remove(from_i)
        if to_i in sources: sources.remove(to_i)
    return sources, sinks


# Tar liste av alle vei-segmentene og lager alle mulige router over dette kartet.
def all_valid_routes(all_roads, sources, sinks, children):
    G = nx.DiGraph()
    G.add_nodes_from(all_roads)
    G.add_edges_from(children)
    valid_routes = []

    for source in sources:
        for sink in sinks:
            routes = nx.all_simple_paths(G, source, sink)
            if routes: valid_routes += list(routes)
    return valid_routes
        


def plot_roads(roads):
    fig, ax = plt.subplots()
    i = 0
    for [start, stop] in roads:
        xs = [start[0], stop[0]]
        ys = [start[1], stop[1]]
        ax.annotate("",  xy=stop, xytext=start,
            arrowprops=dict(arrowstyle="->"))
        ax.plot(xs, ys)
        #ax.arrow(start[0], start[1], stop[0] - start[0], stop[1] - start[1], width=1)
        ax.text(1/2*(stop[0] - start[0]) + start[0], 1/2*(stop[1] - start[1]) + start[1], str(i))
        i += 1
    plt.show()


if __name__=="__main__":
    roads = [
        [[300, 98], [160, 98]],     # 0
        [[160, 98], [0, 98]],       # 1
        [[0, 102], [160, 102]],     # 2
        [[160, 102], [300, 102]],   # 3
        [[180, 60], [0, 60]],       # 4
        [[220, 55], [180, 60]],     # 5
        [[300, 30], [220, 55]],     # 6
        [[180, 60], [160, 98]],     # 7
        [[158, 130], [300, 130]],   # 8
        [[0, 178], [155, 178]],     # 9
        [[155, 178], [300, 178]],   # 10
        [[300, 182], [155, 182]],   # 11
        [[155, 182], [0, 182]],     # 12
        [[160, 102], [158, 130]],   # 13
        [[158, 130], [155, 180]]    # 14
    ]

    plot_roads(roads)

    nodes = [i for i in range(14 + 1)]
    edges = all_road_connections(roads)
    sources, sinks = sources_and_sinks(nodes, edges)
    
    print(all_valid_routes(nodes, sources, sinks, edges))