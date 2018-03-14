a = [2,4,6,7,8]
num = 0
avg = 0
for x in a:
    num += 1
    avg = avg *(num-1)/num+x/num
    print(avg)