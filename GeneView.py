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

def generateLollipop( gene, genes ):
    command = ["./lollipops","-labels"]
    command.append("-o="+outFolder"/images/"+gene+".svg")
    command.append(gene)
    for mutation in genes[gene]:
        edit = mutation.replace("\xe2\x80\x8f","")
        command.append(edit)
    call(command)

def generateHTML( gene ):
    html = open(outFolder + "/pages/"+gene+".html",'w')
    html.write('<html>')
    html.write('  <head>')
    html.write('    <title>' + gene + '</title>')
    html.write('    <link rel="stylesheet" type="text/css" href="GeneView_style.css">')
    html.write('  </head>')
    html.write('  <body>')
    html.write('    <h1>' + gene + '</h1><br><br>')
    html.write('    <img class="lollipop" src="../images/' + gene + '.svg" alt="lollipop gene view of ' + gene + '"><br><br>')
    html.write('    <h2>Other Information</h2>')
    html.write('    <p>')
    html.write('      <a href="http://google.com">Dummy Link</a>')
    html.write('    </p>')
    html.write('  </body>')
    html.write('</html>')

def generateIndexHTML( genes ):
    html = open(outFolder + "/index.html",'w')
    html.write('<html>')
    html.write('  <head>')
    html.write('    <title>GeneView</title>')
    html.write('    <link rel="stylesheet" type="text/css" href="GeneView_style.css">')
    html.write('  </head>')
    html.write('</html>')

import sys
import os
from subprocess import call
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of arguments. Correct usage:"
        print "GeneView.py <vcf_file>"
        sys.exit()
    outFolder = "output"
    genesAndMutations = parseMutationList(open(sys.argv[1],'r')) # parse VCF and return dict, where dict[geneName] = [list of mutationName@freq]
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
        os.makedirs(outFolder + "/images")
        os.makedirs(outFolder +"/pages")
    if not os.path.exists(outFolder + "/images"): # create images folder if it doesn't exist
        os.makedirs(outFolder + "/images")
    if not os.path.exists(outFolder + "/pages"): # create pages folder if it doesn't exist
        os.makedirs(outFolder + "/pages")
    for gene in genesAndMutations: # generate a lollipop image and HTML page for each gene
        generateLollipop(gene,genesAndMutations)
        generateHTML(gene)
    generateIndexHTML(genesAndMutations) # generate index.html