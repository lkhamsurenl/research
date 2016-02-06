from src.model.dart import Dart
from src.model.vertex import Vertex
from src.model.weight import Weight
from collections import deque
from src.model.g1 import G1


def initial_tree(graph, source):
    """
    :return: Predecessor pointer for initial holy tree.
    """
    pred = {source: None}
    dist = {}  # distance for each Vertex
    visited = {}  # keep track of which vertices we visited.
    # Initialize the distance values.
    dist[source] = Weight(homology=[0, 0])
    for v in graph.vertices:
        if v != source:
            dist[v] = Weight(length=float('inf'))
    # queue dictates which order we visit vertices.
    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        visited[u] = 1
        for v in u.neighbors.keys():
            # Add to the queue if has not been visited.
            if v not in visited:
                queue.appendleft(v)
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
    return (pred, dist)


def update_weights(graph, source, pred, new_dist):
    """
    Given a source and new_dist with updated distance for source, propagate the distance through the graph.
    :param graph:
    :param source:
    :param new_dist:
    :return:
    """
    q = deque()
    q.appendleft(source)
    while len(q) != 0:
        u = q.pop()
        for v in u.neighbors.keys():
            # print("{0} -> {1}; pred[{1}] = {2}".format(u, v, pred[v]))
            if pred[v] != None and pred[v] == u:
                new_dist[v] = new_dist[u] + u.neighbors[v].weight
                q.appendleft(v)


def report(pred, dist):
    for u in pred.keys():
        pu = pred[u] if pred[u] != None else "None"
        dpu = dist[pred[u]] if pred[u] != None and dist[pred[u]] != None else "None"
        du = dist[u] if dist[u] != None else "None"
        print("{0} -> {1}, dist[{0}] = {2}, dist[{1}] = {3}".format(pu, u, dpu, du))


def move_across_dart(graph, s1, s2, pred, dist):
    """
    Perform moving from s1 -> s2. Assume s1 and s2 are valid vertices in graph and connected by an edge.
    :param graph:
    :param s1: Source vertex.
    :param s2: Destination vertex.
    :return:
    """
    lambd = 0.0
    while lambd < 1.0:
        # new_dist keeps track of distances, as source move from s1 -> s2.
        new_dist = {}

        lambd += 0.1
        # Find vertices with slack decreasing
        new_dist[s1] = Weight(lambd, dist[s1].homology, dist[s1].leafmost)
        update_weights(graph, s1, pred, new_dist)

        new_dist[s2] = Weight(1.0 - lambd, dist[s2].homology, dist[s2].leafmost)
        update_weights(graph, s2, pred, new_dist)

        # for u in new_dist:
        #     print("new_dist({}) = {}; dist = {}".format(u, new_dist[u], dist[u]))

        # For each edges, relax if necessary
        active = {}  # keep track of the active edges.
        for u in graph.vertices:
            for v in u.neighbors.keys():
                # If tense, relax the dart.
                if new_dist[u] + u.neighbors[v].weight < new_dist[v]:
                    active[u.neighbors[v]] = new_dist[u] + u.neighbors[v].weight - new_dist[v]
                    # new_dist[v] = new_dist[u] + u.neighbors[v].weight
                    # pred[v] = u
                    # print("{} -> {} pivots in. {}".format(u, v, u.neighbors[v].weight))
                    # report(pred, dist)
                    # print("new distances:")
                    # report(pred, new_dist)
                    # print("-------------------------------")

        ##############################
        # Do pivot on dart with minimum slack.
        minimum_slack = Weight(length=float('inf'))
        min_dart = None
        for d in active.keys():
            if minimum_slack > active[d]:
                min_dart = d
                minimum_slack = active[d]

        if min_dart != None:
            new_dist[min_dart.head] = new_dist[min_dart.tail] + min_dart.weight
            pred[min_dart.head] = min_dart.tail
            if min_dart.tail == s2:
                pred[min_dart.tail] = None
            print("{} -> {} pivots in. {}".format(min_dart.tail, min_dart.head, min_dart.weight))
            report(pred, dist)
            print("new distances:")
            report(pred, new_dist)
            print("-------------------------------")
        ###############################

        dist = new_dist

    # Done with the process, let's print out the new distances
    print("done with {0} -> {1}. New root is {1}".format(s1, s2))
    report(pred, dist)


def move_around_face(graph, vertices):
    """
    Move around the vertices in face in order, return all the SSSP for each vertex in vertices.
    :param graph: Graph to find MSSP
    :param vertices: face vertices given in order
    :return: All the shortest path distances for each vertex in the vertices list.
    """
    s1 = vertices[0]  # first source vertex
    (pred, dist) = initial_tree(graph, s1)
    print("---Initial tree---")
    report(pred, dist)
    print("----------------------")

    i = 1  # Root will be moving from vertices[i-1] to vertices[i]
    while i < len(vertices):
        s2 = vertices[1]
        # Source will move from s1 -> s2, updating pred and dist dictionaries.
        move_across_dart(graph, s1, s2, pred, dist)
        # Advance the pointer
        i += 1
        s1 = s2


def main():
    """
    Main function to get all the MSSP distances as move around the face.
    :return:
    """
    g1 = G1()
    vertices = []
    vertices.append(g1.get_vertex((1, 1)))
    vertices.append(g1.get_vertex((0, 1)))
    vertices.append(g1.get_vertex((0, 0)))
    vertices.append(g1.get_vertex((1, 0)))
    move_around_face(g1, vertices)


def debug():
    g1 = G1()
    vertices = []
    vertices.append(g1.get_vertex((1, 1)))
    vertices.append(g1.get_vertex((0, 1)))
    move_around_face(g1, vertices)


debug()