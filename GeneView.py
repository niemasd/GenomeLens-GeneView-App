# Takes VCF file and returns dictionary. Keys = Gene Names; Values = list of <mutation_name>@<number(freq?)>
def parseVCF( file ):
    first = True
    out = {}
    for line in file:
        # ignore first line
        if first:
            first = False
        else:
            stripped = line.strip()
            #do stuff to actually find gene ID and mutation
            mutationID = "TEST_MUT@100" #change 100 to actual frequency
            geneID = "TEST_GENE"
            if geneID in out:
                out[geneID].append(mutationID)
            else:
                out[geneID] = [mutationID]
    return out

import sys
from subprocess import call
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of arguments. Correct usage:"
        print "GeneView.py <vcf_file>"
        sys.exit()
    genesAndMutations = parseVCF(open(sys.argv[1],'r')) # parse VCF and return dict, where dict[geneName] = [list of mutationName@freq]
    if not os.path.exists("images"): # create images folder if it doesn't exist
        os.makedirs("images")
    for gene in genesAndMutations: # for every gene:
        command = ["./lollipops","-labels"]
        command.append("-o=images/"+gene+".svg")
        command.append(gene)
        command.append(genesAndMutations[gene])
        call(command)