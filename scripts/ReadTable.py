# Pass in a "file" object, not a filename string
# i.e. readTable(open('table.txt'))
# The returned dictionary has the following structure:
#   KEYS:   ENSEMBL ID
#   VALUES: Tuple of (Uniprot ID, Gene Name)

def readTable(f):
    dic = {}
    for line in f:
        if line[0] != '#':
            parts = line.strip().split()
            dic[parts[0]] = (parts[1],parts[2])
    return dic

# everything below this is just test code
d = readTable(open('in.txt'))
print len(d)
