# WellPlotter
An application for plotting monitor well data files from Solinst Leveloggers

WellPlotter is an application built with Node.js, express, python, bootstrap, html5, and d3. WellPlotter enables users to take raw csv files from Solinst Leveloggers and quickly plot the data to analyze. This process is done in multiple stages:

First users must upload a set of data from a barometric pressure logger as well as one or more monitor well data files.

To create the graphs, WellPlotter first barometrically corrects each well data file using the data points from the barometer. It matches data points based on date and time so that the barometric correction is input resilient. Next it reduces the number of data points by a factor of 5 (there is typically too much data to produce a clear graph). While reducing the number of points, WellPlotter also changes the "Level" reading from the leveloggers to a net change reading to show the fluctuations in water levels in each monitor well. Once the final data file has been prepared d3 is used to plot the resulting datasets from the input monitor wells. 

[Example](images/wellplot.png)

If you have any questions, comments, contributions, or concerns please let us know by submitting an issue, a pull request, or by sending a message.
