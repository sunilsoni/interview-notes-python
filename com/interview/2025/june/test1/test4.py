import os                                   # for directory traversal
import json                                 # for JSON loading
import pandas as pd                         # for DataFrame
import time                                 # for simple timing
###Design a function that reads a directory of JSON files with inconsistent nested structures and dynamically flattens them into a normalized Pandas DataFrame, adding missing columns as needed.

def flatten_dict(d, parent_key='', sep='_'):
    """
    Recursively flattens a nested dict.
    d: input dict
    parent_key: prefix for keys (used in recursion)
    sep: separator between parent and child keys
    """
    items = {}                                # store flattened key→value
    for k, v in d.items():                    # iterate each key, value
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            # if value is a dict, recurse into it
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            # otherwise, store the value directly
            items[new_key] = v
    return items

def flatten_json_dir(directory):
    """
    Reads all .json files in 'directory', flattens each, and returns a DataFrame.
    """
    records = []                              # list of flattened dicts
    for fname in os.listdir(directory):
        if not fname.lower().endswith('.json'):
            continue                          # skip non-JSON files
        path = os.path.join(directory, fname) # full file path
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)               # parse JSON
        if isinstance(data, dict):
            flat = flatten_dict(data)         # flatten top-level dict
        else:
            # non-dict JSON (e.g. list or single value)
            flat = {'value': data}
        records.append(flat)                  # collect for DataFrame
    # build DataFrame; pandas unions columns and fills missing with NaN
    df = pd.DataFrame(records)
    return df

def main():
    """
    Runs test cases in a simple manner and prints PASS/FAIL.
    """
    # 1) Small test
    test_dir = 'test_small'
    os.makedirs(test_dir, exist_ok=True)
    # file1.json → has keys a and b.c
    with open(os.path.join(test_dir, 'file1.json'), 'w') as f:
        json.dump({'a': 1, 'b': {'c': 2}}, f)
    # file2.json → has keys a and b.d
    with open(os.path.join(test_dir, 'file2.json'), 'w') as f:
        json.dump({'a': 3, 'b': {'d': 4}}, f)

    df_small = flatten_json_dir(test_dir)
    # expected columns: {'a','b_c','b_d'}, 2 rows
    ok_small = set(df_small.columns) == {'a','b_c','b_d'} and df_small.shape[0] == 2
    print('Small test:', 'PASS' if ok_small else 'FAIL')

    # 2) Large test (performance and count)
    test_dir2 = 'test_large'
    os.makedirs(test_dir2, exist_ok=True)
    N = 1000
    for i in range(N):
        # each file has {"i": i}
        with open(os.path.join(test_dir2, f'{i}.json'), 'w') as f:
            json.dump({'i': i}, f)
    start = time.time()
    df_large = flatten_json_dir(test_dir2)
    duration = time.time() - start
    ok_large = df_large.shape == (N, 1)       # N rows, 1 column
    # require it to finish under, say, 2 seconds
    ok_perf = duration < 2.0
    print('Large count test:', 'PASS' if ok_large else 'FAIL')
    print('Large perf test:', 'PASS' if ok_perf else f'FAIL ({duration:.2f}s)')

if __name__ == '__main__':
    main()