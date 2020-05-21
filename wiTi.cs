using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace Algorytm_PD_dla_wiTi
{
    class wiTi
    {
        static void Main(string[] args)
        {
            string path = @"C:\Users\kamil\Downloads\dane1.txt";

            var lines = File.ReadAllLines(path).ToArray();                                                      // wczytanie danych 

            List<Task> tasks = new List<Task>();                                                                // inicjacja kolejki tasków 

            int tasksCount = int.Parse(lines[0].Split(' ')[0]);                                                 // wczytanie liczby zadań

            for(int i= 1; i <= tasksCount; i++)
            {
                tasks.Add(new Task(i, int.Parse(lines[i].Split(' ')[0]),                                        // dadanie taskow do listy
                int.Parse(lines[i].Split(' ')[1]), int.Parse(lines[i].Split(' ')[2])));                         
            }

            int result = CountPunishment(tasks, tasksCount);                                                    // wywołanie funkcji liczącej karę
            Console.WriteLine(result);
        }

        public static int BitConfigurator(int n, int p, int b)                                                  // konfiguruje które zadanie/ zadania wykonujemy 
        {
            int mask = 1 << p;
            return (n & ~mask) | ((b << p) & mask);
        }

        public static int CountPunishment(List<Task> tasks, int taskCount)                      // Liczy karę dla obecnego porzadku w liscie
        {
            List<int> resultList = new List<int>();                                             // Lista naszych wyników 
            List<int> maxValueList = new List<int>();                                           // Lista do przechowywania wartosći maksymalnej z danej iteracji
            List<int> placeOfOne = new List<int>();                                             // Lista przechowywująca na którym miejscu znajduje się 1 czyli jakie zadania wykonujemy
            int minValue, maxValue, confBit;                                                    
            string confBitBin, binValue, reversedString;
            int count = 0;

            resultList.Add(Math.Max(tasks[0].executionTime -                                    //Dodanie do listy kary za pierwsze nasze zadanie
                                    tasks[0].deadline, 0) * tasks[0].punishment);               // (czas wykonania - oczekiwany czas zakonczenia)*kara

            for (int i = 1; i < ((int)Math.Pow(2,taskCount)); i++)                              // Główna pętla iteruje 2^ilość tasków -1 razy dlatego zaczynamy od 1, tyle mamy podproblemów do zbadania
            {
                binValue = Convert.ToString(i, 2);                                              // zamiana tego jaki podproblem rozpatrujemy do wartosci binarnej 
                for(int j = 0;j< binValue.Length; j++)                                          // petla w kórej sprawdzamy nasze podproblemy 
                {
                    confBit = BitConfigurator(i, j, 0);                                         // konfiguracja bitu dla konkretnego zadania
                    confBitBin = Convert.ToString(confBit, 2);                                  // zamiana tego bitu do wartosci binarnej
                    var tmp = binValue.ToArray().Reverse();                                     // zmienna pomocnicza do przechowywania odwróconej wartosic binValue
                    reversedString = "";
                    foreach(var bin in tmp)                                                     // tu odwracamy wyjaśnienie cały ten foreach jako całość bym traktował w sumie razem nawewt z tmp
                    {
                        reversedString += bin;                                                  // odwrócenie wartści z binvalue żebyśmy czytali zadania od lewej np dla zadania 2 bitowo wynosito "10" 
                                                                                                // ale czytamy od lewj wiec zeby nie wyszło ze robimy zadanie  pierwsze to odwracamy do "01"
                    
                    }
                    var reveredStringArr = reversedString.ToArray();                            // zamiana stringa do tablicy przechowującej każdy znak
                    
                    for(int k = 0; k < reveredStringArr.Length; k++)                            // w tej petli sprawdzamy na któym miejscu stoi 1 czyli oznaczenie ze konkretny task jest rozpatrywany
                    {
                        if(reveredStringArr[k] == '1')                                          // Sprawdzenie kazdego miejsca w poszukiwaniu 1
                        {
                            placeOfOne.Add(k);                                                  // jeśli znaleźliśmy to dodajemy do tablicy miejsce na którym się znajduje
                        }
                    }
                    if(binValue != confBitBin)                                                  // sprawdzamy czy nasze zadanie jest równe aktualnemu robimy to zeby tylko raz liczyć karę dla konkretnego podproblemu
                    {
                        for(int l = 0; l < placeOfOne.Count; l++)
                        {
                            count += tasks[placeOfOne[l]].executionTime;                        // sumowanie czasów wykonania tasków jakie 
                        }
                        maxValue = Math.Max(count - tasks[j].deadline, 0) *                     // liczymy naszą karę dla danego podproblemu
                            tasks[j].punishment + resultList[confBit];                          // wartośc maksymalna z (czasy wykonania tasków-dedline danego taska zero w przypadku gdy nie 
                                                                                                // ma spóźnienia tego taska)* kara + kara poprzedniego podproblemu
                        maxValueList.Add(maxValue);                                             // dodanie wyliczonej wartosci do listy
                    }
                    count = 0;                                                                  // zerujemy naszą zmienna do liczenia czasu wykonania zadan
                    placeOfOne.Clear();                                                         // Czyszczenie listy gdzie znajduje się 1 żeby przy następnym podproblemie nie przeszkadało
                }
                minValue = maxValueList.Min();
                resultList.Add(minValue);                                                       // na liste rezulatatów dodajemy wartośc najmenijszej kary z danego podproblemu
                maxValueList.Clear();                                                           // Czyścimy liste wartosci maksymalnych dla danego podproblemu
            }
            return resultList.Last();                                                           // Zwraca ostatnia wartośc na liście rezultatów czyli z problemu z samymi 1
        }
    }

    class Task
    {
        public int Id { get; }                                                              // Przechwuje Id taska
        public int executionTime { get; }                                                   // czas wykonania 
        public int punishment { get; }                                                      // kara za spóźnienie
        public int deadline { get; }                                                        // rządany termin zakończenia

        public Task(int iD, int executionTime, int punishment, int deadline)                // konstruktor taska 
        {
            this.Id = iD;
            this.executionTime = executionTime;
            this.punishment = punishment;
            this.deadline = deadline;
        }
    }
}
