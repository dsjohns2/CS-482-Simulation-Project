import csv
import matplotlib.pyplot as plt
import statistics as stat
with open("Travel_Times.csv") as f:
    data = csv.reader(f)
    travel_times = []
    header = None
    for line in data:
        if header is None:
            header = line
        else:
            travel_times.append(int(line[5]))
    print("Mean: {}".format(stat.mean(travel_times)))
    print("Median: {}".format(stat.median(travel_times)))
    print("Standard deviation: {}".format(stat.stdev(travel_times)))
    print("Variance: {}".format(stat.variance(travel_times)))
    shortest = min(travel_times)
    print("Min: {}".format(shortest))
    longest = max(travel_times)
    print("Max: {}".format(longest))
    width = (longest-shortest)//20
    x = list(range(shortest, longest, width))
    x_freq = [0 for i in x]
    for time in travel_times:
        for index, bucket in enumerate(x):
            if time < bucket + 20:
                x_freq[index] += 1
                break

    print(x_freq)
    print(x)
    plt.bar(x, x_freq, 50)
    plt.show()
