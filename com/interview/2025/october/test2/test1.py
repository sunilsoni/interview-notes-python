from ast import literal_eval
import re

def StockPicker(arr):
    # parse input like "[10,12,4,5,9]"
    if isinstance(arr, str):
        try:
            prices = list(map(int, literal_eval(arr)))
        except Exception:
            prices = list(map(int, re.findall(r'-?\d+', arr)))
    else:
        prices = arr

    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        else:
            profit = price - min_price
            if profit > max_profit:
                max_profit = profit

    result = str(max_profit) if max_profit > 0 else "-1"

    # challenge token filter
    token = "p8xdf5atc6"
    token_set = set(token.lower())
    filtered = ''.join(ch for ch in result if ch.lower() not in token_set)
    return filtered if filtered else "EMPTY"

# keep this function call here
print(StockPicker(input()))
