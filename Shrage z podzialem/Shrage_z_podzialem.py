import queue
import sys

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
    flag=0
    prev_task = (int(0), int(0), int(sys.maxsize))
    #zainicjować prev task zeby nie weszlo do pierwszego if zeby q było duze
    while (not G_ready_queue.empty()) or (not N_not_ordered_queue.empty()):
        while flag==0 and not N_not_ordered_queue.empty():
            task = N_not_ordered_queue.get()[1]
            #print(task[0],task[1],task[2])
            #print("obecny =",task[2])
            #print("prev[0]", prev_task[0])
            #print("poprzedni =",prev_task[2])
            #print("task[0] = ",task[0])
            #print("task[1] = ",task[1])
            #print("task[2] = ",task[2])
            #print("t =",t)
            
            if task[0]<=t:
                G_ready_queue.put((-task[2], task))
                
            else:
                N_not_ordered_queue.put((task[0], task))
                flag=1
            if task[2] > prev_task[2]:
                    #pom = (t,task[0]-prev_task[0],prev_task[2])
                    ##G_ready_queue.put(-prev_task[2], (t,czas roboty ktoty pozostal,prev_task[2]))
                    G_ready_queue.put((-prev_task[2], (task[0],t-task[0],prev_task[2])))
                    ##G_ready_queue.put(-pom[2],)
                    t = task[0]
                    dMax = t
                    flag = 0
        if not G_ready_queue.empty():
            task = G_ready_queue.get()[1]
            prev_task= task
            start_time = max(t, task[0])
            t = start_time + task[1]
            dMax = max(dMax, t + task[2])
            flag=0
        else:
            task = N_not_ordered_queue.get()[1]
            t = task[0]
            N_not_ordered_queue.put((task[0], task))
            flag=0

    file.close()
    return dMax

path1 = 'SCHRAGE'
path2 = '.DAT'

for i in range(1,10):
    path= f'{path1}{i}{path2}'
    print(path)
    print(get_dMax(path))