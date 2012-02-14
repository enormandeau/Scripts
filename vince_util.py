## Eric Normandeau
## 2010-02-18

# Script to modify format of the first line of a file
# For Vincent Bourret


#############################
## Format first line of file

INPUT_FILE = r"C:\Python26\_projects\vincent_bourret\SMC_text.txt"
OUTPUT_FILE = r"C:\Python26\_projects\vincent_bourret\_output_SMC_text.txt"

data = open(INPUT_FILE).readlines()
line_in = data[0].split("\t")
line_out = ""
temp = ""

for i in line_in:
    if i == "" or i == "\n":
        line_out += "\t" + temp
    else:
        temp = i
        line_out += "\t" + temp

line_out = line_out[1:] + "\n"
data[0] = line_out

with open(OUTPUT_FILE, "w") as f:
    for line in data:
        f.write(line)

