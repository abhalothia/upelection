myData = []
head = ['district','block_name','village_name','total_cand', 'seat_res', 'electors', 'tv', 'rejected', 'tvv', 'turnout']
head = head + ['cand1', 'f_hus1', 'age1', 'sex1', 'mob1', 'edu1', 'v1', 'canr1', 'tv1', 'tvv1']

next_c = ['cand', 'f_hus', 'age', 'sex', 'mob', 'edu', 'v', 'canr', 'tv', 'tvv', 'deposit']

for i in range(2,30):
    for s in next_c:
        head.append(s + str(i))
myData.append(head)

print(myData)