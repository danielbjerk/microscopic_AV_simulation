import matplotlib.pyplot as plt

def children_of_roads(roads):
    children = {}
    for i in range(len(roads)):
        children[i] = []
        end = roads[i][1]

        for j in range(len(roads)):
            if j == i:
                continue
            elif roads[j][0] == end:
                children[i].append(j)


# Tar liste av alle vei-segmentene og lager alle mulige router over dette kartet.
def route_generator(children, sources, sinks):
    if not sources or not sinks: return []
    for source in sources:
        for sink in sinks:
            pass
        


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

    children = children_of_roads(roads)
    print(route_generator(children, [0, 2, 6, 9, 11], [1, 3, 4, 8, 10, 12]))