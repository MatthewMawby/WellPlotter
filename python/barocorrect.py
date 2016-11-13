#####################################################################################
#-------------------------LEVELOGGER BAROMETRIC ADJUSTMENT--------------------------#
#--Written By: Matthew Mawby-----Date: 11 July 2016-----Version: 1.0.0--------------#
#-----------------------------------------------------------------------------------#
#####################################################################################
import datetime
import sys

#Opens the files
barofile = open(str(sys.argv[1]), 'r')
infile = open(sys.argv[2], 'r')
outfile = open(sys.argv[3], 'w')

#Handles the headers of the files
for line in infile:
    if line.strip() == "Date,Time,ms,LEVEL,TEMPERATURE":
        outfile.write(line)
        break

for line in barofile:
    if line.strip() == "Date,Time,ms,LEVEL,TEMPERATURE":
        break


#####################################################################################
#-----------------------------DATE AND TIME ADJUSTMENT------------------------------#
#--This block of code adjusts the files so that the first data point in the output--#
#--file is the first shared date and time between the two files---------------------#
#-----------------------------------------------------------------------------------#
#####################################################################################
baro_line = next(barofile)
well_line = next(infile)
baro_list = baro_line.strip().split(',')
well_list = well_line.strip().split(',')
baro_date = baro_list[0].split('/')
baro_time = baro_list[1].split(':')
well_date = well_list[0].split('/')
well_time = well_list[1].split(':')

date1 = datetime.datetime(int(baro_date[0]), int(baro_date[1]),
 int(baro_date[2]), int(baro_time[0]), int(baro_time[1]), int(baro_time[2]))
date2 = datetime.datetime(int(well_date[0]), int(well_date[1]),
 int(well_date[2]), int(well_time[0]), int(well_time[1]), int(well_time[2]))

if date1 == date2:
    taco = None

#trim the barologger file
elif date1 < date2:
    for line in barofile:
        baro_line = line
        baro_list = line.strip().split(',')
        baro_date = baro_list[0].split('/')
        baro_time = baro_list[1].split(':')
        date1 = datetime.datetime(int(baro_date[0]), int(baro_date[1]),
         int(baro_date[2]), int(baro_time[0]), int(baro_time[1]), int(baro_time[2]))
        if date1 == date2:
            break

#trim the well file
else:
    for line in infile:
        well_line = line
        well_list = line.strip().split(',')
        well_date = well_list[0].split('/')
        well_time = well_list[1].split(':')
        date2 = datetime.datetime(int(well_date[0]), int(well_date[1]),
         int(well_date[2]), int(well_time[0]), int(well_time[1]), int(well_time[2]))
        if date1 == date2:
            break

#Make the barometric adjustment and write the line
baro_line = baro_line.strip().split(',')
well_line = well_line.strip().split(',')
new_level = float(well_line[3])-float(baro_line[3])
well_line[3] = new_level
line_to_add = ''
for num in range(5):
    line_to_add = line_to_add + str(well_line[num])
    if num != 4:
        line_to_add = line_to_add + ','
line_to_add = line_to_add + '\n'
outfile.write(line_to_add)


#####################################################################################
#----------------------------MAIN BAROMETRIC ADJUSTMENT-----------------------------#
#--This block of code iterates through both files at once and ends when the---------#
#--shorter file ends so that barometric adjustments have been made on all shared----#
#--data points between the two files------------------------------------------------#
#####################################################################################
for well_line, baro_line in zip(infile, barofile):
    baro_line = baro_line.strip().split(',')
    well_line = well_line.strip().split(',')
    new_level = float(well_line[3])-float(baro_line[3])
    well_line[3] = new_level
    line_to_add = ''
    for num in range(5):
        line_to_add = line_to_add + str(well_line[num])
        if num != 4:
            line_to_add = line_to_add + ','
    line_to_add = line_to_add + '\n'
    outfile.write(line_to_add)
