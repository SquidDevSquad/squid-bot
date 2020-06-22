def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


# TODO Mor: add tests
def remove_sub_list(lst, sub_lst):
    return [elem for elem in lst if elem not in sub_lst]


def find_by_id(id_val, lst):
    return next((elem for elem in lst if elem.id == id_val), False)


def contains_duplicates(lst):
    return not len(lst) == len(set(lst))
