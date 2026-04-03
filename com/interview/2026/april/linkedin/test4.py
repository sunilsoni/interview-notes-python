import time
from collections import deque


# ==========================================
# 1. GRAPH GENERATOR: THE CELEBRITY TRAP
# ==========================================
def generate_celebrity_trap_network():
    print("Generating network with 1,000,000 users...")
    graph = {}

    # Create the straight path: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
    # You are 0. The Target is 6.
    graph[0] = [1]
    graph[1] = [0, 2]
    graph[2] = [1, 3]
    graph[3] = [2, 4]
    graph[4] = [3, 5]
    graph[5] = [4, 6]
    graph[6] = [5]

    # THE TRAP: Node 1 is a celebrity with 1 Million random followers.
    # We add 1,000,000 dummy nodes connected ONLY to Node 1.
    for i in range(10, 1000010):
        graph[1].append(i)
        graph[i] = [1]

    print("Network generated successfully!\n")
    return graph


# ==========================================
# 2. STANDARD BFS ALGORITHM
# ==========================================
def standard_bfs(graph, start_id, target_id):
    if start_id not in graph or target_id not in graph: return -1
    if start_id == target_id: return 0

    search_queue = deque([(start_id, 0)])
    visited = set([start_id])
    nodes_checked = 0  # Counter to prove how much work it does

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


# ==========================================
# 3. BIDIRECTIONAL BFS ALGORITHM
# ==========================================
def bidirectional_bfs(graph, start_id, target_id):
    if start_id not in graph or target_id not in graph: return -1
    if start_id == target_id: return 0

    start_queue = deque([start_id])
    target_queue = deque([target_id])

    start_visited = {start_id: 0}
    target_visited = {target_id: 0}

    nodes_checked = 0  # Counter to prove how much work it does

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
        # THE OPTIMIZATION: Always expand the smaller line
        if len(start_queue) <= len(target_queue):
            result = expand_search_party(start_queue, start_visited, target_visited)
        else:
            result = expand_search_party(target_queue, target_visited, start_visited)

        if result != -1:
            return result, nodes_checked

    return -1, nodes_checked


# ==========================================
# 4. MAIN BENCHMARK TESTER
# ==========================================
def main():
    # 1. Build the data
    graph = generate_celebrity_trap_network()
    start_node = 0
    target_node = 6

    # 2. Test Standard BFS
    print("--- RUNNING STANDARD BFS ---")
    start_time = time.perf_counter()
    std_distance, std_nodes = standard_bfs(graph, start_node, target_node)
    end_time = time.perf_counter()
    std_time_taken = end_time - start_time

    print(f"Distance Found : {std_distance} steps")
    print(f"Nodes Checked  : {std_nodes:,} nodes")
    print(f"Time Taken     : {std_time_taken:.6f} seconds\n")

    # 3. Test Bidirectional BFS
    print("--- RUNNING BIDIRECTIONAL BFS ---")
    start_time = time.perf_counter()
    bi_distance, bi_nodes = bidirectional_bfs(graph, start_node, target_node)
    end_time = time.perf_counter()
    bi_time_taken = end_time - start_time

    print(f"Distance Found : {bi_distance} steps")
    print(f"Nodes Checked  : {bi_nodes:,} nodes")
    print(f"Time Taken     : {bi_time_taken:.6f} seconds\n")

    # 4. Final Comparison
    print("==========================================")
    print("               FINAL RESULTS              ")
    print("==========================================")
    if bi_time_taken > 0:
        speed_multiplier = std_time_taken / bi_time_taken
        print(f"Bidirectional was {speed_multiplier:,.0f}x FASTER.")
        print(f"It checked {std_nodes - bi_nodes:,} FEWER nodes.")
    print("==========================================")


if __name__ == "__main__":
    main()