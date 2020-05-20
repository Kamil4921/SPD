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

            int result = CountPunishment(tasks, tasksCount);
            Console.WriteLine(result);
        }

        public static int BitConfigurator(int n, int p, int b)
        {
            int mask = 1 << p;
            return (n & ~mask) | ((b << p) & mask);
        }

        public static int CountPunishment(List<Task> tasks, int taskCount)                                           // Liczy karę dla obecnego porzadku w liscie
        {
            List<int> resultList = new List<int>();
            List<int> maxValueList = new List<int>();
            List<int> placeOfOne = new List<int>();
            int minValue, maxValue, confBit;
            string confBitBin, binValue, reversedString;
            int count = 0;

            resultList.Add(Math.Max(tasks[0].executionTime - tasks[0].deadline, 0) * tasks[0].punishment);

            for (int i = 1; i < ((int)Math.Pow(2,taskCount)); i++)
            {
                binValue = Convert.ToString(i, 2);
                for(int j = 0;j< binValue.Length; j++)
                {
                    confBit = BitConfigurator(i, j, 0);
                    confBitBin = Convert.ToString(confBit, 2);
                    var tmp = binValue.ToArray().Reverse();
                    reversedString = "";
                    foreach(var bin in tmp)
                    {
                        reversedString += bin;
                    }
                    var reveredStringArr = reversedString.ToArray();
                    
                    for(int k = 0; k < reveredStringArr.Length; k++)
                    {
                        if(reveredStringArr[k] == '1')
                        {
                            placeOfOne.Add(k);
                        }
                    }
                    if(binValue != confBitBin)
                    {
                        for(int l = 0; l < placeOfOne.Count; l++)
                        {
                            count += tasks[placeOfOne[l]].executionTime;
                        }
                        maxValue = Math.Max(count - tasks[j].deadline, 0) * tasks[j].punishment + resultList[confBit];
                        maxValueList.Add(maxValue);
                    }
                    count = 0;
                    placeOfOne.Clear();
                }
                minValue = maxValueList.Min();
                resultList.Add(minValue);
                maxValueList.Clear();
            }
            return resultList.Last();
        }
    }

    class Task
    {
        public int Id { get; }
        public int executionTime { get; }
        public int punishment { get; }
        public int deadline { get; }

        public Task(int iD, int executionTime, int punishment, int deadline)
        {
            Id = iD;
            this.executionTime = executionTime;
            this.punishment = punishment;
            this.deadline = deadline;
        }
    }
}
