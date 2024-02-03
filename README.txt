General description of the algorithm


The algorithm for Splitter 3 was created specifically for automatic photometric data separation from the TESS space telescope. This software can be used to split light curves of periodic variable stars into separate extrema (minima and maxima) for further analysis.
Moreover, Splitter also can be used to process data not only
from the TESS space telescope (as it was intended) but for other sources of observations such
as Kepler, K2, AAVSO, etc


The stages of the algorithm are the following:

1. The data extraction (Julian dates and magnitudes only) from a text file.
2. Smoothing the data in a specific way to reduce noise. Details are provided below in
Section 3. It is important to note that smoothed data is used only to find the edges
of each interval. Further processing requires original data.
3. Calculation of the first derivative for smoothed data.
4. Smoothing the first derivative to remove false positives.
5. Calculation of the second derivative.
6. Determination of all points where the second derivative equals zero. More specifically,
search for specific points where the second derivative for two consecutive points has
different signs. The first point of this pair is the right edge for an interval and the next
point corresponds to the left edge for the next interval.
7. Searching for the large gaps in the observations. We consider a gap as a large one if
time difference between two consecutive data points is larger than 25% of the period.
8. Creation of the list with edges of all intervals.
9. Several essential verifications.
(a) First: whether the interval has a sufficient amount of points for approximation
(at least 10), and its width is at least 10% and at most 100% of the star’s period.
(b) Second: whether each interval contains an extremum within its edges.
(c) Third: whether the star is eclipsing binary and if yes then if the minima contain
out-of-eclipse parts.