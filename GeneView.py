# parse text file (contains gene name + mutation)
def parseMutationList( file ):
    out = {}
    for line in file:
        parts = line.strip().split()
        geneID = parts[0]
        mutation = parts[1]
        if geneID in out:
            out[geneID].append(mutation)
        else:
            out[geneID] = [mutation]
    return out

import sys
import os
from subprocess import call
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of arguments. Correct usage:"
        print "GeneView.py <vcf_file>"
        sys.exit()
    genesAndMutations = parseMutationList(open(sys.argv[1],'r')) # parse VCF and return dict, where dict[geneName] = [list of mutationName@freq]
    if not os.path.exists("images"): # create images folder if it doesn't exist
        os.makedirs("images")
    for gene in genesAndMutations: # for every gene:
        command = ["./lollipops","-labels"]
        command.append("-o=images/"+gene+".svg")
        command.append(gene)
        for mutation in genesAndMutations[gene]:
            edit = mutation.replace("\xe2\x80\x8f","")
            command.append(edit)
        print command
        #call(command)