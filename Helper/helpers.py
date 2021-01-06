import inspect
from sqlalchemy.inspection import inspect

def divide_chunks(lst, nbr_of_itms):  
    for i in range(0, len(lst), nbr_of_itms):
        yield lst[i:i + nbr_of_itms] 





def object_as_dict(obj):

   

    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}




def remove_dupe_dicts(l):
    return [dict(t) for t in {tuple(d.items()) for d in l }]