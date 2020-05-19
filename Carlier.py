import queue
import sys
from dataclasses import dataclass, field
from typing import Any

# klasa pomocnicza niezbędna do poprawnego umieszczenia w kolejce dwóch tasków o takiej samej wartości priorytetu
# nie pozwala kolejce na porównywania tasków w takiej sytuacji (gotowe rozwiąanie z internetu)
@dataclass(order=True)
class PrioritizedTask:  
    priority: int
    Task: Any=field(compare=False)

# klasa pomocnicza przechowująca permutację tasków wraz z ich czasami dostarczenia (punktami czasu) wg algorytmu schrage
# ułatwia obliczanie a, b i c
class Permutation(object):
    def __init__(self):
        self.Tasks = []
        self.DeliveryTimes = []

    def AddTask(self, task, deliveryTime):  # dodaje task i jego czas dostarczenia (punkt w którym je dostarczymy)
        self.Tasks.append(task)
        self.DeliveryTimes.append(deliveryTime)


class Task(object):
    def __init__(self, id, r, p, q):
        self.id = id
        self.r = r
        self.p = p
        self.q = q
    def __repr__(self):
        return str(self.id) + ':\t' + str(self.r) + '\t' + str(self.p) + '\t' + str(self.q) + '\n'

# schrage jak ostatnio zwraca dmax czyli najpóźnieszy czas dostarczenia (do określenia UB górnej granicy rozwiązania)
# tylko zwraca dodatkowo permutację tasków z czasami dostarczenia (w obiekcie Permutation) i dmax czyli wartość funkcji celu 
def schrage(tasksList):
    N_not_ordered_queue = queue.PriorityQueue()
    G_ready_queue = queue.PriorityQueue()
    Result_Permutation = Permutation()
    for task in tasksList:
        N_not_ordered_queue.put(PrioritizedTask(task.r, task))

    t=0
    dMax=0
    flag=0
    while (not G_ready_queue.empty()) or (not N_not_ordered_queue.empty()):
        while not N_not_ordered_queue.empty():
            task = N_not_ordered_queue.get().Task
            if task.r<=t:
                G_ready_queue.put(PrioritizedTask(-task.q, task))
            else:
                N_not_ordered_queue.put(PrioritizedTask(task.r, task))
                break
        if not G_ready_queue.empty():
            task = G_ready_queue.get().Task
            Result_Permutation.AddTask(
                task=task, 
                deliveryTime=max(t, task.r)+task.p+task.q
                )
            t = max(t, task.r) + task.p
            dMax = max(dMax, t + task.q)
        else:
            task = N_not_ordered_queue.get().Task
            t = task.r
            N_not_ordered_queue.put(PrioritizedTask(task.r, task))
    return dMax, Result_Permutation

# preschrage jak ostatnio zwraca dmax czyli najpóźnieszy czas dostarczenia (do określenia LB dolnej granicy rozwiązania)
def preschrage(tasksList):
    N_not_ordered_queue = queue.PriorityQueue()
    G_ready_queue = queue.PriorityQueue()
    for task in tasksList:
        N_not_ordered_queue.put(PrioritizedTask(task.r, task))

    t=0
    dMax=0
    prev_task = Task(int(0), int(0), int(0), int(sys.maxsize))
    #zainicjować prev task zeby nie weszlo do pierwszego if zeby q było duze
    while (not G_ready_queue.empty()) or (not N_not_ordered_queue.empty()):
        while not N_not_ordered_queue.empty():
            task = N_not_ordered_queue.get().Task
            if task.r<=t:
                G_ready_queue.put(PrioritizedTask(-task.q, task))
                if task.q > prev_task.q:
                    p = t - task.r
                    t = task.r
                    dMax = t
                    if p > 0:
                        G_ready_queue.put(PrioritizedTask(-prev_task.q, Task(int(0),prev_task.r,p,prev_task.q)))
                    break;
            else:
                N_not_ordered_queue.put(PrioritizedTask(task.r, task))
                break
        if not G_ready_queue.empty():
            task = G_ready_queue.get().Task
            start_time = max(t, task.r)
            t = start_time + task.p
            dMax = max(dMax, t + task.q)
            prev_task = task
        else:
            task = N_not_ordered_queue.get().Task
            t = task.r
            N_not_ordered_queue.put(PrioritizedTask(task.r, task))
    return dMax

# funkcja wyznaczająca a, b i c danej permutacji
def getabc(cmax, perm):
    # znajdź b (jako pozycję w permutacji)
    # b: zadanie o czasie dostarczenia równym czasowi dostarczenia całej permutacji
    # iterujemy po wszystkich zadaniach żeby liczyło się ostatnie które spełnia wymagania 
    # (gdyby było ich kilka ważne jest najdalsze w permutacji)
    for i in range(len(perm.Tasks)):
        if perm.DeliveryTimes[i] == cmax:
            b = i

    # znajdź a (jako pozycję w permutacji)
    # a: zadanie które spełnia warunek:
    # czas dostarczenia permutacji = czas dostępności (r) zadania a 
    #                               + suma wszystkich czasów wykonań (p) zadań na pozycjach a-b 
    #                               + czas dostarczania/przewozu (q) zadania b
    for i in range(b+1):
        sumOfPinRangeJB = 0
        for j in range(i, b+1):
            sumOfPinRangeJB += perm.Tasks[j].p
        if cmax == perm.Tasks[i].r + sumOfPinRangeJB + perm.Tasks[b].q:
            a = i
            break   # break żeby liczyło się pierwsze zadanie które spełnia warunek (pozycja minimalna)

    # znajdź c (jako pozycję w permutacji, jeśli istnieje)
    # c: zadanie należące do przedziału <a;b> spełniające warunek:
    # czas dostarczania zadania c < czas dostarczania zadania b
    # !to jest porównanie czasów przewozu, nie punktów czasowych!
    # jeśli jest kilka potencjalnych c bierzemy najdalsze w permutacji
    c = None       # inicjujemy nullem żeby mieć informację gdy nie znajdzie się żadne c
    for i in range(a, b+1):
        if perm.Tasks[i].q < perm.Tasks[b].q:
            c = i

    return a, b, c

# funkcja wczytująca taski z pliku do listy
def readTasks(path):
    file = open(path, "r")
    n = int(file.readline())
    TasksList = []
    for i in range(n):
        RPQ = file.readline().split(" ")
        task = Task(i+1, int(RPQ[0]), int(RPQ[1]), int(RPQ[2]))
        TasksList.append(task)
    return TasksList

# funkcja carlier (zagnieżdżona/rekurencyjna)
def Carlier(tasksList, UB):
    U, Perm = schrage(tasksList)    # oblicz górną granicę funkcji celu dmax liczone schrage
    if U<UB:                        # warto cokolwiek liczyć jeśli górna granica jest mniejsza niż była
        a, b, c = getabc(U, Perm)   # wylicz zadania a,b,c
        if c is None:               # jeśli nie znaleziono zadania c to znaczy że schrage na zadaniach o podanych parametrach generuje optymalne rozwiązanie
            print("schrage wygenerował rozwiązanie optymalne: " + str(U))
            exit(0)

        Rprim = int(sys.maxsize)
        Qprim = int(sys.maxsize)
        Pprim = 0
        for i in range(c+1,b+1):
            Rprim = min(Rprim, Perm.Tasks[i].r) # r' = najmniejszy czas dostępu zadania z przedziału <c+1;b>
            Qprim = min(Qprim, Perm.Tasks[i].q) # q' = najmniejszy czas dostarczania zadania z przedziału <c+1;b>
            Pprim += Perm.Tasks[i].p            # p' = suma czasów wykonywania zadań z przedziału <c+1;b>
            
        TasksList = Perm.Tasks  # przepisanie tasków z permutacji do listy roboczej 

        # I węzeł: zmodyfikowane r
        oldR = Perm.Tasks[c].r  # zapamiętaj r zadania c żeby je potem przywrócić
        newR = max(oldR, Rprim+Pprim)   # nowe r to większa z wartości stare r lub r'+p'
        TasksList[c].r = newR           # modyfikuj parametr r zadania c
        LB = preschrage(TasksList)      # oblicz dolną granicę dmax wg preschrage
        if LB < UB:                     # jeśli dlna granica jest mniejsza niż górna to warto przeliczyć schrage dla tych parametrów
            Carlier(TasksList, UB)      # uruchamiamy carliera (który używa shrage na samympoczątku) ze zmodyfikowaną listą tasków 
        TasksList[c].r = oldR           # przywróć r
       
        # II węzeł: zmodyfikowane q
        oldQ = Perm.Tasks[c].q
        newQ = max(oldQ, Qprim+Pprim)   # nowe q to większa z wartości stare q lub q'+p'
        TasksList[c].q = newQ           # modyfikuj parametr q zadania c
        LB = preschrage(TasksList)      # oblicz dolną granicę dmax wg preschrage
        if LB < UB:                     # jeśli dlna granica jest mniejsza niż górna to warto przeliczyć schrage dla tych parametrów
            Carlier(TasksList, UB)      # uruchamiamy carliera (który używa shrage na samympoczątku) ze zmodyfikowaną listą tasków 
        TasksList[c].q = oldQ           # przywróć q



path = 'SCHRAGE10.DAT'
Carlier(tasksList=readTasks(path), 
        UB=int(sys.maxsize)) # początkowa wartość funkcji celu którą minimalizujemy jest maksymalna