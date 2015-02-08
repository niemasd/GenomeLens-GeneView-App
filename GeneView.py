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

def generateLollipop( gene ):
    command = ["./lollipops","-labels"]
    command.append("-o=images/"+gene+".svg")
    command.append(gene)
    for mutation in genesAndMutations[gene]:
        edit = mutation.replace("\xe2\x80\x8f","")
        command.append(edit)
    call(command)

def generateHTML( gene ):
    html = open("pages/"+gene+".html",'w')
    html.write("<html>")
    html.write("  <center>")
    html.write("    <h>"+gene+"</h><br>")
    html.write('    <img src="../images/'+gene+'.svg">')
    html.write("  </center>")
    html.write("</html>")

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
    if not os.path.exists("pages"): # create pages folder if it doesn't exist
        os.makedirs("pages")
    for gene in genesAndMutations: # generate a lollipop image and HTML page for each gene
        generateLollipop(gene)
        generateHTML(gene)
    #generate index