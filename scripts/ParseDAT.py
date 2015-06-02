# Pass in a "file" object, not a filename string
# i.e. readTable(open('HUMAN_9606_idmapping.dat'))
# The returned dictionary has the following structure:
#   KEYS:   ENSEMBL ID or REFSEQ ID
#   VALUES: Tuple of (Uniprot ID, Gene Name)


def parseDAT(f):
    genes = {} # genes[uniprot] = [RefSeq,Ensembl_TRS,gene_name]
    for line in f:
        if 'RefSeq' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][0].append(parts[2])
        elif 'ChiTaRS\t' in line or 'GeneWiki\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][2] = parts[2]
        elif 'Ensembl_TRS\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'']
            genes[parts[0]][1].append(parts[2])
    dic = {}
    for uniprot in genes:
        refseq,ensembl,genename = genes[uniprot]
        ##for now, only do entries with both uniprot and genename
        #if genename == '':
        #    continue
        if '-' in uniprot:
            uniprot = uniprot.split('-')[0]
        for r in refseq:
            dic[r] = (uniprot,genename)
        for e in ensembl:
            dic[e] = (uniprot,genename)
        #dic[parts[1]] = parts[2]
        #dic[parts[0]] = parts[2]
    return dic

#d = parseDAT(open('../../input/HUMAN_9606_idmapping.dat'))
#for k in d.keys():
#    print "KEY: " + k
#    #print "VALUE: " + d.get(k)
#    print "VALUE: " + d[k][0] + ", " + d[k][1]
#    print
##print d.keys()
##print len(d)
