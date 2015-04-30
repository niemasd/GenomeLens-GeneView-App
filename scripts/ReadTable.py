# Pass in a "file" object, not a filename string
# i.e. readTable(open('table.txt'))
# The returned dictionary has the following structure:
#   KEYS:   ENSEMBL ID or REFSEQ ID
#   VALUES: Uniprot ID
#
# ORIGINAL TABLE FORMAT:
#1. UniProtKB-AC
#2. UniProtKB-ID
#3. GeneID (EntrezGene)
#4. RefSeq
#5. GI
#6. PDB
#7. GO
#8. UniRef100
#9. UniRef90
#10. UniRef50
#11. UniParc
#12. PIR
#13. NCBI-taxon
#14. MIM
#15. UniGene
#16. PubMed
#17. EMBL
#18. EMBL-CDS
#19. Ensembl
#20. Ensembl_TRS
#21. Ensembl_PRO
#22. Additional PubMed
#
# OUR TABLE FORMAT:
#1. UniProtKB-AC
#2. RefSeq
#3. Ensembl_TRS

def readTable(f):
    dic = {}
    for line in f:
        parts = line.split('\t')
        for ensembl in parts[2].split('; '):
            dic[ensembl] = parts[0]
        for refseq in parts[1].split('; '):
            dic[refseq] = parts[0]
    return dic

d = readTable(open('db/UNIPROT_REFSEQ_ENSEMBLE.tab'))
print len(d)
