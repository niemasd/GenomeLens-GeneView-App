# Pass in a "file" object, not a filename string
# i.e. readTable(open('HUMAN_9606_idmapping.dat'))
# The returned dictionary has the following structure:
#   KEYS:   ENSEMBL ID or REFSEQ ID
#   VALUES: Uniprot ID


def parseDAT(f):
    genes = {} # genes[gene] = [RefSeq,Ensembl_TRS,UniProtKB-AC]
    for line in f:
        if 'RefSeq' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][0].append(parts[2])
        elif 'Ensembl_TRS\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][1].append(parts[2])
        elif 'UniProtKB-AC\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][2] = parts[0]
    dic = {}
    for gene in genes:
        refseq,ensembl,uniprot = genes[gene]
        for r in refseq:
            dic[r] = uniprot
        for e in ensembl:
            dic[e] = uniprot
        #dic[parts[1]] = parts[2]
        #dic[parts[0]] = parts[2]
    return dic

d = parseDAT(open('../HUMAN_9606_idmapping.dat'))
for k in d.keys():
    print "KEY: " + k
    #print "VALUE: " + d.get(k)
    print "VALUE: " + d[k]
    print
#print d.keys()
#print len(d)
