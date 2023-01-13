from itertools import groupby
from collections import namedtuple
import matplotlib.pyplot as plt

square_room =50

room = [['bed', 6, 2],
       ['wardrobe', 4, 3],
       ['table', 7, 1],
       ['chair', 2, 1],
       ['stone', 7, 1],
       ['sofa', 3, 3]]


max_columns = [14]
print('Таблиця#1 заданих меблів(розмір та кількість)')
print(f'{"="*max(max_columns)*5}')

print('The name is furniture     Square   Count')

print(f'{"="*max(max_columns)*5}')
for el in room:
    for col in el:
        print(f'{col:{max(max_columns)+1}}', end='')
    print()


newroom = []


def soffa(name, size, count):
       newroom.append(['2x' + name, size, 2])
       return count - 2


def anyvalidcomb(items, maxwt, val=0, wt=0):
    if not items:
        yield [], val, wt
    else:
        this, *items = items
        for n in range(this.number + 1):
            w = wt + n * this.weight
            if w > maxwt: break
            v = val + n * this.value
            this_comb = [this] * n
            for comb, value, weight in anyvalidcomb(items, maxwt, v, w):
                yield this_comb + comb, value, weight


def combo(roomsmall, a):
    maxwt = roomsmall[0][1]
    z = [1, roomsmall[0][0]]
    COMB, VAL, WT = range(3)
    Item = namedtuple('Items', 'name weight value number')
    smalr = [[i[0], i[1], i[1], i[2]] for i in roomsmall]
    items = [Item(*x) for x in smalr[1:]]
    bagged = max( anyvalidcomb(items, maxwt), key=lambda c: (c[VAL], -c[WT]))
    x = [[len(list(grp)), item.name] for item, grp in groupby(sorted(bagged[COMB]))]

    for i in x:
        n = 0
        for j in room:
            if i[1] == j[0]:
                p = i[0]
                while p > 0:
                    room[n][2] = room[n][2] - 1
                    p = p - 1
            n += 1
    if z[1] == 'bed' and a == 1:
        room[0][2]=room[0][2]-1
    e=0
    if z[1] == 'wardrobe' and a == 2:
        for i in room:
            if i[0] == 'wardrobe' and i[2]>0:
                room[e][2] = room[e][2] -1
            e +=1
    if z[1] == 'table' and a == 3:
        for i in room:
            if i[0] == 'table' and i[2]>0:
                room[e][2] = room[e][2] -1
            e +=1
    v = ''
    w = 0
    x.append(z)
    for i in x:
        v = v + ' ' + '-'. join([''. join([str(i[0]), 'x']), i[1]])
        w += i[0]
    newroom.append([v, roomsmall[0][1], w])


def combo2():
    for i in room:
        if i[0] == 'wardrobe' and i[2] > 0:
            l = []
            l.append(i)
            for j in room:
                e = 0
                if  j[0] == 'stone' and i[2] > j[2] and j[2]>0:
                    e=1
                    l.append(j)
            if e ==1:
                combo(l, 2)
        if i[0] == 'table' and i[2] > 0:
            j = []
            j.append(i)
            for q in room:
                e = 0
                if q[0] == 'stone' and i[1] >= q[1] and q[2]>0:
                    e=1
                    j.append(q)
                if e==1:
                    combo(j, 3)


def maybe():
    n=0
    v=0
    for i in room:
        if i[0]=='bed':
            v = i[1]
        if i[0] != 'bed' and i[1] <= v:
            n += i[2]
    return n


def start():
    b = 0
    for i in room:
        if i[0] == 'bed' and i[2] > 0:
                while b != 1:
                    combo(room, 1)
                    if room[0][2] <= 0:
                        b = 1
                    if maybe() <= 0:
                        b = 1
    combo2()
    q=0
    for i in room:
       if i[2] >= 2 and (i[0] != 'table' or i[0] != 'chair' or i[0] != 'sofa' ):

           room[q][2] = soffa(i[0], i[1], i[2])
       q+=1
    for i in room:
        if i[2]>0:
            k= i[2]
            while k>0:
                newroom.append(['1x-' + i[0], i[1], 1])
                k = k-1



def main():
    print(f'{"=" * max(max_columns) * 5}')

    x =[]
    y=[]
    s=0
    for row in room:
        s += row[1]*row[2]
        x.append(str( str(row[2])+'x ') + row[0])
        y.append(row[1]*row[2])
    s = square_room-s
    x.append('free space')
    y.append(s)
    plt.pie(y, labels=x, shadow=True, autopct='%1.1f%%', startangle=180)
    plt.title('Free space in the room without combining furniture')
    plt.show()

    start()
    max_columns2 = [28]
    print('')
    print('Таблиця#2 комбінованих меблів між собою (розмір та кількість)')
    print(f'{"=" * max(max_columns2) * 5}')
    print('The name is furniture                                  Square                       Count')
    print(f'{"=" * max(max_columns2) * 5}')
    for el in newroom:
        for col in el:
            print(f'{col:{max(max_columns2) + 1}}', end='')
        print()
    s2=0
    x=[]
    y=[]
    for i in newroom:
        s2 += i[1]
        x.append(i[0])
        y.append(i[1])
    s2 = square_room - s2
    x.append('free space')
    y.append(s2)
    plt.pie(y, labels=x, shadow=True, autopct='%1.1f%%', startangle=180)
    plt.title('Free space in the room for combining furniture')
    plt.show()
    print('')
    print(f'{"=" * 20 * 5}')
    print('Площа кімнати:', square_room )
    print('Вільне місце у кімнаті без комбінування меблів:', s)
    print('Вільне місце у кімнаті з комбінуванням меблів:', s2)
    print('Різниця:', s2-s)
    print(f'{"=" * 20 * 5}')

main()