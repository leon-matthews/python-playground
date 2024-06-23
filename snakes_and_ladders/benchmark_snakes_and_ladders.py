#!/usr/bin/env python3

import numpy
from matplotlib import pyplot
from pprint import pprint as pp


# Data - On mid-2009 MacBook Pro 13", 2.3GHz Intel Core 2 Duo, 8GB RAM, 500GB SSD
python36 = numpy.array([6.1, 6.2, 6.1, 6.0, 6.0, 6.1, 5.7, 6.1, 6.0, 6.1, 5.9]) * 1e3
python37 = numpy.array([6.8, 6.6, 6.6, 6.5, 6.6, 6.6, 6.5, 6.6, 6.6, 6.6, 6.6]) * 1e3
python38 = numpy.array([8.7, 8.7, 8.7, 8.8, 8.5, 8.8, 8.8, 8.6, 8.4, 8.8, 8.6]) * 1e3
python39 = numpy.array([8.3, 8.3, 8.5, 8.0, 8.8, 8.5, 8.6, 8.4, 8.5, 8.8, 8.1]) * 1e3

# Means
python36_mean = numpy.mean(python36)
python37_mean = numpy.mean(python37)
python38_mean = numpy.mean(python38)
python39_mean = numpy.mean(python39)

# Standard deviations
python36_std = numpy.std(python36)
python37_std = numpy.std(python37)
python38_std = numpy.std(python38)
python39_std = numpy.std(python39)

# Labels, etc...
labels = ('Python 3.6', 'Python 3.7', 'Python 3.8', 'Python 3.9')
x_pos = numpy.arange(len(labels))
centres = (python36_mean, python37_mean, python38_mean, python39_mean)
errors = (python36_std, python37_std, python38_std, python39_std)

# Build plot
figure, axes = pyplot.subplots()
axes.bar(x_pos, centres, yerr=errors, align='center', alpha=0.5, capsize=10, ecolor='black')
axes.set_ylabel("Games per second")
axes.set_xticks(x_pos)
axes.set_xticklabels(labels)
axes.set_title("Performance comparison of Snakes & Ladders")
axes.yaxis.grid(True)

# Show
# ~ pyplot.tight_layout()
pyplot.show()
