def ten_maximum_seeders(data: list):

    max_index = []

    data = [int(e) for e in data]
    l = 0
    while l < 10 :
        nb = max(data)
        max_index.append(str(nb))
        data.remove(nb)
        l+=1
    
    return max_index

    

