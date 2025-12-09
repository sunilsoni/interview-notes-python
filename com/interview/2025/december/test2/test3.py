def add_to_list(item, lst=[]):
    lst.append(item)
    print(lst)

my_list = [1, 2, 3]
add_to_list(4)              # uses default list
add_to_list(5, my_list)     # uses your custom list
add_to_list(6)              # uses same default list as before
add_to_list(7, my_list)     # again uses your custom list
add_to_list(8)              # still uses same default list
