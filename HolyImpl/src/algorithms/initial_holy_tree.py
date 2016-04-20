from src.model.weight import Weight
from collections import deque
from sets import Set

def fast_initial_tree(graph, genus, source):
    """
    :param genus:
    :return: Predecessor pointer for initial holy tree.
    """
    pred = {source: None}
    dist = {}  # distance for each vertex
    visited = Set([source])  # keep track of which vertices we visited.
    # Initialize the distance values.
    dist[source] = Weight(homology=[0 for _ in range(2 * genus)])
    for v in graph.vertices:
        if v != source:
            dist[v] = Weight(length=float('inf'))
    # queue dictates which order we visit vertices.
    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        for v in u.neighbors.keys():
            # Add to the queue if has not been visited.
            # NOTE(lkhamsurenl): Each vertex will be added only once to the queue.
            if v not in visited:
                visited.add(v)
                queue.appendleft(v)
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
    return (pred, dist)

def bellman_ford_initial_tree(graph, genus, source):
    """
    :return: Predecessor pointer for initial holy tree.
    """
    # Keep track of the predecessor pointers for the SSSP rooted at the source. pred[source] = None.
    pred = {source: None}
    dist = {}  # distance for each Vertex
    # Initialize the distance values.
    dist[source] = Weight(homology=[0 for _ in range(2 * genus)])
    for v in graph.vertices:
        if v != source:
            dist[v] = Weight(length=float('inf'))
    # queue dictates which order we visit vertices.
    queue = deque()
    queue.appendleft(source)
    while len(queue) != 0:
        u = queue.pop()
        for v in u.neighbors.keys():
            # If tense, relax the dart.
            if dist[u] + u.neighbors[v].weight < dist[v]:
                dist[v] = dist[u] + u.neighbors[v].weight
                pred[v] = u
                queue.appendleft(v)
    return (pred, dist)
