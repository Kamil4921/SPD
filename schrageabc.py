import queue

def get_dMax(path):
    file = open(path, "r")
    n = int(file.readline())

    N_not_ordered_queue = queue.PriorityQueue()
    G_ready_queue = queue.PriorityQueue()
    U_done_list = []

    for i in range(n):
        bufor = file.readline()
        space = bufor.split(" ")
        RPQ = (int(space[0]), int(space[1]), int(space[2]))
        N_not_ordered_queue.put((RPQ[0], RPQ))

    t=0
    dMax = 0
    flag=0
    while (not G_ready_queue.empty()) or (not N_not_ordered_queue.empty()):
        while flag==0 and not N_not_ordered_queue.empty():
            task = N_not_ordered_queue.get()[1]
            if task[0]<=t:
                G_ready_queue.put((-task[2], task))
            else:
                N_not_ordered_queue.put((task[0], task))
                flag=1
        if not G_ready_queue.empty():
            task = G_ready_queue.get()[1]
            t = max(t, task[0]) + task[1]
            dMax = max(dMax, t + task[2])
            flag=0
            U_done_list.append(task)
        else:
            task = N_not_ordered_queue.get()[1]
            t = task[0]
            N_not_ordered_queue.put((task[0], task))
            flag=0
    i=0
    indexa = 0
    indexb = 0
    indexc = 0
    for i, v in enumerate(U_done_list):
        x=1
        #print (i, v)
    aMaxi=0
    aMaxiq = 0
    bMaxi = 0
    bMaxiq = 0
    cMaxi=0
    cMaxiq = 0

    for k in range (0,i+1):
        #print(k)
        bMaxi=(max(bMaxi,U_done_list[k][0])+U_done_list[k][1])
        bMaxiq=bMaxi+U_done_list[k][2]
        if bMaxiq==dMax:
            #print(U_done_list[k][0] , U_done_list[k][1], bMaxiq,k)
            b=U_done_list[k]
            indexb=k

    kk=indexb
    while (kk>0):
        aMaxi=0
        print(aMaxi,kk)
        for p in range(0, kk):
            aMaxi = (max(aMaxi, U_done_list[p][0]) + U_done_list[p][1])
            #aMaxiq = aMaxi + U_done_list[k][2]
        print(aMaxi,U_done_list[kk][0])
        if (aMaxi>U_done_list[kk][0]):
             kk-=1
            #print('obnizylem')
        else:
            indexa=kk
            break
    kk=indexb
    while kk>=indexa:
        print('kk',kk)
        if U_done_list[kk][2]<U_done_list[indexb][2]:
            indexc=kk
            break
        else:
            kk-=1

    print(indexa, indexc,indexb)
    file.close()
    return dMax

if __name__ == '__main__':
    dMax = 0
    a=[0,0,0]
    b=[0,0,0]
    c=[0,0,0]
    path1 = 'SCHRAGE'
    path2 = '.DAT'

    for i in range(11,12):
        path= f'{path1}{i}{path2}'
        print(path)
        print(get_dMax(path))