import csv
import matplotlib.pyplot as plt
import statistics as stat
import sys
from scipy.stats import chisquare

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
    csv_files = sys.argv[1:]
    for num, csv_file in enumerate(csv_files):
        f = open(csv_file)
        sim_csv = csv.reader(f)
        sim_data = [float(line[0]) for line in sim_csv]
        f.close()
        shortest = int(min(travel_times))
        longest = int(max(travel_times))
        # Adjust this to change frequency buckets for chi-square
        width = ((longest-shortest)//5)
        x = list(range(shortest, longest, width))
        uber_freq = [0 for i in x]
        sim_freq = [0 for i in x]

        for time in travel_times:
            for index, bucket in enumerate(x):
                if time < bucket + width:
                    uber_freq[index] += 1
                    break
        for time in sim_data:
            for index, bucket in enumerate(x):
                if time < bucket + width:
                    sim_freq[index] += 1
                    break
        print(csv_file, end=": ")
        print("Mean: {}".format(stat.mean(sim_data)))
        print("Median: {}".format(stat.median(sim_data)))
        print("Standard deviation: {}".format(stat.stdev(sim_data)))
        print("Variance: {}".format(stat.variance(sim_data)))
        print("Bucket length: {}".format(len(x)))
        print(str(chisquare(sim_freq, f_exp=uber_freq).statistic))
        print("")

        # Uncomment to plot
        # plt.bar(x, uber_freq, 50)
        # plt.xlabel("Time (seconds)")
        # plt.ylabel("Riders")
        # plt.figure(2)
        # plt.bar(x, sim_freq, 50)
        # plt.show()
