def divide_chunks(lst, nbr_of_itms):  
    for i in range(0, len(lst), nbr_of_itms):
        yield lst[i:i + nbr_of_itms] 
       
        