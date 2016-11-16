import sys

#Opens the files
infile = open(sys.argv[1], 'r')
outfile_name = sys.argv[1].split('.')
outname = outfile_name[0]+"_trimmed.csv"
print outname
outfile = open(outname, 'w')
interval = int(sys.argv[2])

#Handles the headers of the files
for line in infile:
    if line.strip() == "Date,Time,ms,LEVEL,TEMPERATURE":
        outfile.write(line)
        break

counter = 0
for line in infile:
    if counter == 0:
        line_list = line.strip().split(',')
        initial_val = float(line_list[3])
        line_list[3] = 0.0
        line_to_write = ''
        for num in range(5):
            if num < 4:
                line_to_write += str(line_list[num])+','
            else:
                line_to_write += str(line_list[num])+'\n'
        outfile.write(line_to_write)
    elif counter % int(interval) == 0:
        line_list = line.strip().split(',')
        line_list[3] = float(line_list[3]) - initial_val
        line_to_write = ''
        for num in range(5):
            if num < 4:
                line_to_write += str(line_list[num])+','
            else:
                line_to_write += str(line_list[num])+'\n'
        outfile.write(line_to_write)
    counter += 1
