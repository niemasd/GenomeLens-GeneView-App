# Pass in a "file" object, not a filename string
# i.e. readTable(open('HUMAN_9606_idmapping.dat'))
# The returned dictionary has the following structure:
#   KEYS:   ENSEMBL ID or REFSEQ ID
#   VALUES: Tuple of (Uniprot ID, Gene Name)


def parseDAT(f):
    genes = {} # genes[key] = [RefSeq,Ensembl_TRS,UniProtKB-AC,gene_name]
    for line in f:
        if 'RefSeq' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'','']
            genes[parts[0]][0].append(parts[2])
        elif 'ChiTaRS\t' in line or 'GeneWiki\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'','']
            genes[parts[0]][3] = parts[2]
        elif 'Ensembl_TRS\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'','']
            genes[parts[0]][1].append(parts[2])
        #elif 'UniProtKB-AC\t' in line:
        elif 'UniProtKB-ID\t' in line:
            parts = line.strip().split('\t')
            if parts[0] not in genes:
                genes[parts[0]] = [[],[],'','']
            genes[parts[0]][2] = parts[2]
            #print "UNIPROT: " + parts[2]
    dic = {}
    for key in genes:
        refseq,ensembl,uniprot,genename = genes[key]
        for r in refseq:
            dic[r] = (uniprot,genename)
        for e in ensembl:
            dic[e] = (uniprot,genename)
        #dic[parts[1]] = parts[2]
        #dic[parts[0]] = parts[2]
    return dic

#d = parseDAT(open('../HUMAN_9606_idmapping.dat'))
#for k in d.keys():
#    print "KEY: " + k
#    #print "VALUE: " + d.get(k)
#    print "VALUE: " + d[k]
#    print
##print d.keys()
##print len(d)
