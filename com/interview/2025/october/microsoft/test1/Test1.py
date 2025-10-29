from collections import deque, defaultdict  # import deque for fast queue and defaultdict for easy dict of lists
from typing import Dict, Iterable, List, Hashable, Tuple  # import types for clear function signatures
import random  # import random for generating large test graphs reproducibly


def topo_order(deps: Dict[Hashable, Iterable[Hashable]]) -> List[Hashable]:
    """
    Return one valid topological order for the given dependency map.
    'deps' maps job -> iterable of prerequisite jobs.
    Raises ValueError if a cycle exists.
    """
    # Build a set of all jobs we know about (keys + any that appear only as prerequisites)
    all_jobs = set(deps.keys())  # start with jobs that have explicit entries
    for job, pres in deps.items():  # loop over each job and its prerequisites
        for p in pres:              # loop over each prerequisite for that job
            all_jobs.add(p)         # add prerequisite to the set so no node is missed

    # Create graph edges: prereq -> job (because prereq must run before job)
    graph = defaultdict(list)  # adjacency list from a job to jobs that depend on it
    indeg = {j: 0 for j in all_jobs}  # in-degree count for each job (how many prerequisites remain)

    for job, pres in deps.items():  # go through each job and its prerequisites again to build edges
        for p in pres:              # for each prerequisite
            graph[p].append(job)    # add edge from prerequisite to the job
            indeg[job] = indeg.get(job, 0) + 1  # increase in-degree for the job because it waits on p

    print(indeg)
    # Initialize queue with all jobs that have no prerequisites (in-degree 0)
    q = deque(j for j in all_jobs if indeg.get(j, 0) == 0)  # start nodes can run now
    order = []  # this list will store the final schedule

    # Process the queue until empty
    while q:                                   # continue while there are runnable jobs
        cur = q.popleft()                      # take one job that is ready
        order.append(cur)                      # append it to the schedule
        for nxt in graph[cur]:                 # for every job that depends on the finished job
            indeg[nxt] -= 1                    # we have satisfied one prerequisite for 'nxt'
            if indeg[nxt] == 0:                # if 'nxt' has no more prerequisites
                q.append(nxt)                  # then it can run; push it to the queue

    # After processing, if we did not schedule all jobs, there is a cycle
    if len(order) != len(all_jobs):            # compare scheduled count with total jobs
        # Collect nodes with remaining in-degree to hint at the cycle
        stuck = [j for j, d in indeg.items() if d > 0]  # nodes not resolved
        raise ValueError(f"Cycle detected; unresolved jobs: {stuck}")  # raise clear error

    return order  # return the valid order if all went well


def is_valid_order(deps: Dict[Hashable, Iterable[Hashable]], order: List[Hashable]) -> Tuple[bool, str]:
    """
    Check if 'order' respects all dependencies in 'deps'.
    Returns (ok, message). Message explains the first problem if any.
    """
    # Create a position map: where each job appears in the order
    pos = {job: i for i, job in enumerate(order)}  # helps us compare order positions quickly

    # Make sure all jobs mentioned anywhere are present in the order
    all_jobs = set(deps.keys())                    # begin with jobs that have entries
    for js in deps.values():                       # add any job that appears only as a prerequisite
        for p in js:
            all_jobs.add(p)

    if set(order) != all_jobs:                     # order must contain exactly all jobs
        missing = all_jobs - set(order)            # jobs not listed
        extra = set(order) - all_jobs              # jobs not known
        return False, f"Order mismatch. Missing: {sorted(missing)}, Extra: {sorted(extra)}"  # explain issue

    # Verify every dependency: each prerequisite must come before the job
    for job, pres in deps.items():                 # check each job and its prerequisites
        for p in pres:                             # go through each prerequisite
            if pos[p] > pos[job]:                  # if prerequisite comes after the job, order is invalid
                return False, f"Dependency broken: {p} should come before {job}"  # explain the violation

    return True, "OK"                              # if all checks pass, return OK


# --------- Test helpers below (simple main-based testing, no unittest) ---------

def make_large_dag(n_nodes: int = 2000, edges_per_node: int = 3, seed: int = 42) -> Dict[str, List[str]]:
    """
    Create a reproducible large DAG for stress testing.
    Nodes are 'J0'...'J{n_nodes-1}'.
    Each node i depends on up to 'edges_per_node' random nodes from [0, i-1], which keeps it acyclic.
    """
    random.seed(seed)                              # fix seed for repeatability
    deps: Dict[str, List[str]] = {}               # dependency map to return
    nodes = [f"J{i}" for i in range(n_nodes)]      # list of node labels

    deps[nodes[0]] = []                            # first node has no prerequisites
    for i in range(1, n_nodes):                    # for each remaining node
        # Choose k previous nodes as prerequisites (k may be less than edges_per_node near the start)
        k = min(edges_per_node, i)                 # cannot choose more prerequisites than available previous nodes
        pres = random.sample(nodes[:i], k=k)       # sample k unique prerequisites from earlier nodes
        deps[nodes[i]] = pres                      # set the prerequisite list
    return deps                                    # return the generated dependency map


def run_tests() -> None:
    """
    Run a set of tests and print PASS/FAIL for each.
    Also prints one valid order for visibility.
    """
    tests = []                                      # list to hold all test cases

    # --- Test 1: Example from prompt ---
    deps1 = {                                      # define the dependencies exactly as described
        "A": ["B", "C"],                           # A depends on B and C
        "B": ["C"],                                 # B depends on C
        "C": ["D"],                                 # C depends on D
        "D": [],                                    # D has no dependencies
        "E": []                                     # E has no dependencies
    }
    tests.append(("Prompt example", deps1))         # add this test

    # --- Test 2: Multiple independent chains ---
    deps2 = {                                      # a mix of separate chains and free nodes
        "M": ["N"],                                 # M after N
        "N": [],                                    # N free
        "X": ["Y", "Z"],                            # X after Y and Z
        "Y": [],                                    # Y free
        "Z": [],                                    # Z free
        "K": []                                     # K free
    }
    tests.append(("Independent chains", deps2))     # add the second test

    # --- Test 3: Self dependency (should raise) ---
    deps3 = {"A": ["A"]}                            # A depends on itself -> cycle
    tests.append(("Self dependency (cycle)", deps3))# add the third test

    # --- Test 4: Simple 2-node cycle (should raise) ---
    deps4 = {"A": ["B"], "B": ["A"]}                # two node cycle
    tests.append(("Two-node cycle", deps4))         # add the fourth test

    # --- Test 5: Large DAG stress test ---
    deps5 = make_large_dag(n_nodes=5000, edges_per_node=3, seed=7)  # build a decent sized DAG
    tests.append(("Large DAG 5k nodes", deps5))     # add the stress test

    # Run all tests one by one
    for idx, (name, deps) in enumerate(tests, start=1):  # enumerate tests with numbers starting at 1
        try:
            print(deps)
            order = topo_order(deps)                # try to compute a topological order
            ok, msg = is_valid_order(deps, order)   # validate the produced order
            status = "PASS" if ok else "FAIL"       # decide pass/fail based on validation
            print(f"[{idx}] {name}: {status}")      # print the test result line
            if not ok:
                print(f"    Reason: {msg}")         # if failed, explain why
            else:
                # Print the first few items to show the schedule without flooding the console
                preview = ", ".join(map(str, order[:10]))  # prepare a small preview of the order
                print(f"    Sample order (first 10): {preview}")  # show part of the order
                print(f"    Total jobs scheduled: {len(order)}")  # show total count for confidence
        except ValueError as e:                      # catch cycle errors from topo_order
            # Expected for the two cycle tests, unexpected otherwise
            expected_cycle = "cycle" in name.lower() # check if the test name implies a cycle
            status = "PASS" if expected_cycle else "FAIL"  # pass if we expected a cycle
            print(f"[{idx}] {name}: {status}")      # print the result
            print(f"    Message: {str(e)}")         # show the error message for clarity


# Simple entry point (no unittest)
if __name__ == "__main__":                           # run only when executed as a script
    run_tests()                                      # call the test runner
