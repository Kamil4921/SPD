import queue

def get_dMax(path):
    file = open(path, "r")
    n = int(file.readline())

    N_not_ordered_queue = queue.PriorityQueue()
    G_ready_queue = queue.PriorityQueue()

    for i in range(n):
        bufor = file.readline()
        space = bufor.split(" ")
        RPQ = (int(space[0]), int(space[1]), int(space[2]))
        N_not_ordered_queue.put((RPQ[0], RPQ))
        #print(N_not_ordered_queue)

    t=0
    dMax=0
    prev_task = (int(0), int(0), int(sys.maxsize))
    #zainicjować prev task zeby nie weszlo do pierwszego if zeby q było duze
    while (not G_ready_queue.empty()) or (not N_not_ordered_queue.empty()):
        while not N_not_ordered_queue.empty():
            task = N_not_ordered_queue.get()[1]
            if task[0]<=t:
                G_ready_queue.put((-task[2], task))
                if task[2] > prev_task[2]:
                    p = t - task[0]
                    t = task[0]
                    dMax = t
                    if p > 0:
                        G_ready_queue.put((-prev_task[2], (prev_task[0],p,prev_task[2])))
                    break;
            else:
                N_not_ordered_queue.put((task[0], task))
                break
        if not G_ready_queue.empty():
            task = G_ready_queue.get()[1]
            start_time = max(t, task[0])
            t = start_time + task[1]
            dMax = max(dMax, t + task[2])
            prev_task = task
        else:
            task = N_not_ordered_queue.get()[1]
            t = task[0]
            N_not_ordered_queue.put((task[0], task))

    file.close()
    return dMax

path1 = 'SCHRAGE'
path2 = '.DAT'

for i in range(1,10):
    path= f'{path1}{i}{path2}'
    print(path)
    print(get_dMax(path))