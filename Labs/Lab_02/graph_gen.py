import random

v = [10, 20, 30, 40, 50, 60, 70, 80, 90]

for j in v:
    thres = j
    tot = 0

    for i in range(10):
        cnt = 1
        while random.randint(1, 100) <= thres: cnt += 1
        tot += cnt

    print(j, end=' ')
    print("{:.15f}".format(tot / 10))
