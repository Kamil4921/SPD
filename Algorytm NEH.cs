using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Algorytm_NEH
{
    class Program
    {
        static void Main()
        {
            string fileName = @"D:\Studia\SPD\Algorytm NEH\NEH9.DAT";
            var tasks = new List<Task>();
            var tasksQueue = new Queue<Task>();

            var lines = File.ReadLines(fileName).ToArray();

            int tasksCount = int.Parse(lines[0].Split(' ')[0]);     // wczytanie liczby zadań
            int machinesCount = int.Parse(lines[0].Split(' ')[1]);  // wczytanie liczby maszyn
            for(int i=1; i<tasksCount+1; i++)
            {
                var times = new List<int>();
                foreach(string time in lines[i].Split(' '))         // dzieli linię na czasy i dla każdego czasu
                {
                    if(time != "")
                    {
                        times.Add(int.Parse(time));                     // dodaje czas do listy rzutując go na int
                    }
                }
                tasks.Add(new Task(i, times.ToArray()));            // tworzy nowe zadanie o wczytanych czasach i dodaje do listy zadań
            }
            tasks.Sort();   // sortuje taski w liście malejąco wg priorytetu (sumy czasów na maszynach)
                            // default comparator przeciążony w klasie Task

            foreach(Task task in tasks)     // wrzuca taski do kolejki fifo 
            {
                tasksQueue.Enqueue(task);
                Console.WriteLine(task);
            }

            var OrderedTasks = new OrderedTasks(machinesCount); // tworzy pustą kolejność wykonywania
            int resultCmax = 0;                                 // inicjuje zmienną do przechowania wyniku
            while (tasksQueue.Count > 0)                        // dopóki są taski w kolejce 
            {                                                   // ściąga po kolei i wrzuca na optymalną pozycję
                resultCmax = OrderedTasks.AddTaskOptimallyGetCmax(tasksQueue.Dequeue());
            }
            Console.WriteLine(resultCmax);            
        }
    }
    class Task : IComparable
    {
        public int Id { get; }
        public int[] TimesOfOperations { get; }

        public int Priority { get; }

        public Task(int id, int[] times)
        {
            Id = id;
            TimesOfOperations = times;
            Priority = times.Sum();         // priorytet to suma czasów na wszystkich maszynach
        }
        public override string ToString()
        {
            string timesString = "";
            foreach(int time in TimesOfOperations)
            {
                timesString += time.ToString() + " ";
            }
            return $"Id: {Id}, Priority: {Priority}, Times: {timesString}";
        }
        public int CompareTo(object obj)        // Przeciążenie porównania dwóch tasków wg priorytetu
        {
            Task otherTask = obj as Task;
            return -Priority.CompareTo(otherTask.Priority); // '-' na początku bo chcemy kolejność nierosnącą
        }
    }
    
    class OrderedTasks  // klasa przechowująa taski w optymalnej wg neh kolejności
    {
        public int MachinesCount { get; set; }  // liczba maszyn
        public List<Task> Tasks { get; set; }   // lista tasków

        public OrderedTasks(int machinesCount)
        {
            MachinesCount = machinesCount;
            Tasks = new List<Task>();
        }
        public int AddTaskOptimallyGetCmax(Task task)   // sprawdza cmax dla każdego wstawienia elementu i wykonuje optymalne
        {
            var minCmax = int.MaxValue;     // maxvalue aby na pewno znalazł jakiś mniejszy cmax
            var optimalIndex = 0;           // inicjacja optymalnej pozycji - zawsze zmieniana ale musi być jakaś wartość początkowa
            foreach(int index in Enumerable.Range(0, Tasks.Count()+1))  // dla każdej pozycji
            {
                Tasks.Insert(index, task);                              // wstaw
                if(CountCmax() < minCmax)                               // przelicz i sprawdź czy cmax lepszy niż najmniejszy
                {
                    minCmax = CountCmax();                              // jeśli tak podmień min cmax 
                    optimalIndex = index;                               // i optymalną pozycję
                }
                Tasks.RemoveAt(index);                                  // cofnij wstawienie
            }
            Tasks.Insert(optimalIndex, task);                           // wstaw na optymalnej pozycji
            return minCmax;                                             // zwróć cmax
        }
        public int CountCmax()  // oblicza cmax dla obecnej kolejności tasków
        {
            int prevMaxTime;
            int i;
            var MaxTimesOnMachines = new int[MachinesCount];    // inicjuje tablicę maxymalnych czasów zakończenia wszystkich zadań na maszynie
            var newMaxTimesOnMachines = MaxTimesOnMachines;     // inicjuje tablicę pomocniczą - obie wypełniane 0
            foreach ( Task task in Tasks)
            {
                i = 0;
                prevMaxTime = 0;
                foreach (int maxTime in MaxTimesOnMachines) // updateuje każdy maxczas  
                {                              
                    newMaxTimesOnMachines[i] = Math.Max(
                        maxTime + task.TimesOfOperations[i],        // maxczas maszyny + czas taska na tej maszynie
                        prevMaxTime + task.TimesOfOperations[i]);   // maxczas poprzedniej maszyny + czas taska na tej maszynie
                    prevMaxTime = newMaxTimesOnMachines[i];
                    i++;
                }
                MaxTimesOnMachines = newMaxTimesOnMachines; // updateuj maxczasy dla dotychczasowych tasków
            }
            return MaxTimesOnMachines.Last();   // cmax jest równy maxczasowi ostatniej maszyny
        }
    }
}
