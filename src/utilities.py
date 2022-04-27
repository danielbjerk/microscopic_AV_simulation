import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def make_cross(centre, radius=5, kerf=2, with_ramp=True, ramp_len=100):
    centre = np.array(centre)
    centres_of_sides = [
        centre + np.array([radius, 0]),
        centre + np.array([0, radius]),
        centre + np.array([-radius, 0]),
        centre + np.array([0, -radius]),
    ]
    
    corners_in = [
        centres_of_sides[0] + np.array([0, kerf]),
        centres_of_sides[1] + np.array([-kerf, 0]),
        centres_of_sides[2] + np.array([0, -kerf]),
        centres_of_sides[3] + np.array([kerf, 0])
    ]
    corners_out = [
        centres_of_sides[0] + np.array([0, -kerf]),
        centres_of_sides[1] + np.array([kerf, 0]),
        centres_of_sides[2] + np.array([0, kerf]),
        centres_of_sides[3] + np.array([-kerf, 0])
    ]

    roads = []

    num_sides = len(centres_of_sides)
    for i in range(num_sides):
        start = list(corners_in[i])
        end_right = list(corners_out[(i + 1) % num_sides])
        end_straight = list(corners_out[(i + 2) % num_sides])
        end_left = list(corners_out[(i + 3) % num_sides])
        
        roads.append([end_right, start])
        roads.append([end_straight, start])
        roads.append([end_left, start])

    if with_ramp:
        off_ramps = [
        [list(corners_in[0]), list(corners_in[0] + np.array([ramp_len, 0]))],
        [list(corners_in[1]), list(corners_in[1] + np.array([0, ramp_len]))],
        [list(corners_in[2]), list(corners_in[2] + np.array([-ramp_len, 0]))],
        [list(corners_in[3]), list(corners_in[3] + np.array([0, -ramp_len]))]
        ]

        on_ramps = [
        [list(corners_out[0] + np.array([ramp_len, 0])), list(corners_out[0])],
        [list(corners_out[1] + np.array([0, ramp_len])), list(corners_out[1])],
        [list(corners_out[2] + np.array([-ramp_len, 0])), list(corners_out[2])],
        [list(corners_out[3] + np.array([0, -ramp_len])), list(corners_out[3])]
        ]
        roads = on_ramps + off_ramps + roads
    return roads


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
    plt.ylim(200, -200)
    plt.show()


if __name__=="__main__":
    roads = [
    # Inn til krysset
    [[-5, -5], [-200, -5]],
    [[-200, 5], [-5, 5]],

    [[5, 5], [200, 5]],
    [[200, -5], [5, -5]],

    [[5, -5], [5, -200]],    
    [[-5, -200], [-5, -5]], 

    [[-5, 5], [-5, 200]],
    [[5, 200], [5, 5]]
    ]
    cross= make_cross((0,0))
    roads = cross

    print("Initialized roads:")
    [print(f"{r},") for r in roads]

    plot_roads(roads)

    nodes = [i for i in range(len(roads) + 1)]
    edges = all_road_connections(roads)
    sources, sinks = sources_and_sinks(nodes, edges)
    print(all_valid_routes(nodes, sources, sinks, edges))
    