def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


def add_to_list(lst, list_to_add):
    lst.extend(list_to_add)


# TODO Mor: add tests
def find_by_id(id_val, lst):
    return next((elem for elem in lst if elem.id == id_val), False)


def contains_duplicates(lst):
    return not len(lst) == len(set(lst))
