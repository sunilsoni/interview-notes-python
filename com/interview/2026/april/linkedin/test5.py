import time
from collections import deque


# ==========================================
# 1. GRAPH GENERATOR: THE CELEBRITY TRAP
# ==========================================
def generate_celebrity_trap_network():
    print("Generating network with 1,000,000 users...")
    graph = {}
    edges = []  # We need a list of raw edges for Union-Find

    # Helper to add connections to both the graph and the edge list
    def add_connection(u, v):
        if u not in graph: graph[u] = []
        if v not in graph: graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
        edges.append((u, v))

    # Create the straight path: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
    add_connection(0, 1)
    add_connection(1, 2)
    add_connection(2, 3)
    add_connection(3, 4)
    add_connection(4, 5)
    add_connection(5, 6)

    # THE TRAP: Node 1 is a celebrity with 1 Million random followers.
    for i in range(10, 1000010):
        add_connection(1, i)

    print("Network generated successfully!\n")
    return graph, edges


# ==========================================
# 2. UNION-FIND CLASS
# ==========================================
class UnionFind:
    def __init__(self, size):
        self.parent = [i for i in range(size)]
        self.rank = [1] * size

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            elif self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1


# ==========================================
# 3. ALGORITHM IMPLEMENTATIONS
# ==========================================

def standard_bfs(graph, start_id, target_id):
    search_queue = deque([(start_id, 0)])
    visited = set([start_id])
    nodes_checked = 0

    while search_queue:
        current_id, current_distance = search_queue.popleft()
        nodes_checked += 1
        if current_id == target_id:
            return current_distance, nodes_checked

        for friend_id in graph.get(current_id, []):
            if friend_id not in visited:
                visited.add(friend_id)
                search_queue.append((friend_id, current_distance + 1))
    return -1, nodes_checked


def bidirectional_bfs(graph, start_id, target_id):
    start_queue = deque([start_id])
    target_queue = deque([target_id])
    start_visited = {start_id: 0}
    target_visited = {target_id: 0}
    nodes_checked = 0

    def expand_search_party(active_queue, active_visited, other_visited):
        nonlocal nodes_checked
        current_id = active_queue.popleft()
        current_distance = active_visited[current_id]
        nodes_checked += 1

        for friend_id in graph.get(current_id, []):
            if friend_id in other_visited:
                return current_distance + 1 + other_visited[friend_id]
            if friend_id not in active_visited:
                active_visited[friend_id] = current_distance + 1
                active_queue.append(friend_id)
        return -1

    while start_queue and target_queue:
        if len(start_queue) <= len(target_queue):
            result = expand_search_party(start_queue, start_visited, target_visited)
        else:
            result = expand_search_party(target_queue, target_visited, start_visited)
        if result != -1:
            return result, nodes_checked
    return -1, nodes_checked


def test_union_find(edges, max_nodes, start_id, target_id):
    uf = UnionFind(max_nodes)
    operations = 0

    # Union-Find MUST process all edges to build its groups
    for u, v in edges:
        uf.union(u, v)
        operations += 1

    # Once built, checking the connection is instant (1 operation)
    is_connected = (uf.find(start_id) == uf.find(target_id))
    operations += 1

    return is_connected, operations


# ==========================================
# 4. RUNNING THE BENCHMARK
# ==========================================
def main():
    graph, edges = generate_celebrity_trap_network()
    start_node = 0
    target_node = 6
    max_node_id = 1000015  # Buffer size for the Union-Find array

    # --- 1. Standard BFS ---
    start_time = time.perf_counter()
    std_result, std_ops = standard_bfs(graph, start_node, target_node)
    std_time = time.perf_counter() - start_time

    # --- 2. Bidirectional BFS ---
    start_time = time.perf_counter()
    bi_result, bi_ops = bidirectional_bfs(graph, start_node, target_node)
    bi_time = time.perf_counter() - start_time

    # --- 3. Union-Find ---
    start_time = time.perf_counter()
    uf_result, uf_ops = test_union_find(edges, max_node_id, start_node, target_node)
    uf_time = time.perf_counter() - start_time

    # --- RESULTS DASHBOARD ---
    print("==================================================")
    print("             PERFORMANCE DASHBOARD                ")
    print("==================================================")
    print(f"1. Standard BFS")
    print(f"   Result     : Path is {std_result} steps")
    print(f"   Operations : {std_ops:,} nodes checked")
    print(f"   Time       : {std_time:.6f} seconds")
    print("--------------------------------------------------")
    print(f"2. Bidirectional BFS")
    print(f"   Result     : Path is {bi_result} steps")
    print(f"   Operations : {bi_ops:,} nodes checked")
    print(f"   Time       : {bi_time:.6f} seconds")
    print("--------------------------------------------------")
    print(f"3. Union-Find")
    print(f"   Result     : Connected? {uf_result}")
    print(f"   Operations : {uf_ops:,} edges processed")
    print(f"   Time       : {uf_time:.6f} seconds")
    print("==================================================")
    print("                   ANALYSIS                       ")
    print("==================================================")
    print("- Winner for Pathfinding : Bidirectional BFS (Ignored the 1M trap).")
    print("- Loser for one-off search: Union-Find (Had to process all 1M followers).")


if __name__ == "__main__":
    main()