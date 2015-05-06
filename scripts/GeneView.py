# parse text file (contains gene name + mutation)
colorPat = "ff0000" # red
colorNonPat = "00ccff" # light blue

def parseMutationList( geneDict ):
    out = {}
    for geneID in geneDict:
        #parts = line.strip().split()
        #geneID = parts[0]
        #mutation = parts[1]
        #mafs = parts[2]
        #svt = parts[3]
        
        #EXAMPLE: R248Q#7f3333@131
        entry = mutation
        if svt == 'True':
            entry += colorPat
        else:
            entry += colorNonPat
        if mafs != "NA":
            m = mafs.split('/')
            sum = float(m[0]) + float(m[1]) + float(m[2]) #not sure how to use MAF entry, ?/?/?
            entry += '@'
            entry += str(int(sum*100))
        
        if geneID in out:
            out[geneID].append(entry)
        else:
            out[geneID] = [entry]
    return out

def generateLollipop( gene ):
    command = ["./lollipops","-labels"]
    #command.append("-o="+outFolder+"/"+gene.name+".svg")
    #command.append(gene.name)
    command.append("-o="+outFolder+"/"+gene.uniprotID+".svg")
    command.append("-U="+gene.uniprotID)
    for mutation in gene.AAChanges:
        # aaChange#color@size
        # if in patient
        if gene.inPat[mutation]:
            color = colorPat
        else:
            color = colorNonPat
        arg = mutation + "#" + color
        if gene.mafs[mutation] is not None:
            size = int(float(gene.mafs[mutation][2])*100)
            # bring up to at least one
            if size == 0:
                size = 1
            arg += "@" + str(size)
        #edit = mutation.replace("\xe2\x80\x8f","")
        command.append(arg)
    print(" ".join(command))
#    call(command)

def generateHTML( gene ):
    html = open(outFolder + "/pages/"+gene+".html",'w')
    html.write('<html>\n')
    html.write('  <head>\n')
    html.write('    <title>' + gene + '</title>\n')
    html.write('    <link rel="stylesheet" type="text/css" href="../GeneView_style.css">\n')
    html.write('  </head>\n')
    html.write('  <body>\n')
    html.write('    <h1>' + gene + '</h1><br><br>\n')
    html.write('    <img class="lollipop" src="../images/' + gene + '.svg" alt="lollipop gene view of ' + gene + '"><br><br>\n')
    html.write('    <h2>Other Information</h2>\n')
    html.write('    <p>\n')
    html.write('      <a href="http://www.ncbi.nlm.nih.gov/gene/?term='+gene+'">GenBank</a><br>\n')
    html.write('      <a href="http://www.genecards.org/cgi-bin/carddisp.pl?gene='+gene+'">GeneCards</a><br>\n')
    html.write('      <a href="http://www.ncbi.nlm.nih.gov/omim/?term='+gene+'">OMIM</a><br>\n')
    html.write('      <a href="https://en.wikipedia.org/wiki/'+gene+'">Wikipedia</a><br>\n')
    html.write('    </p>\n')
    html.write('  </body>\n')
    html.write('</html>')

def generateIndexHTML( genes ):
    html = open(outFolder + "/index.html",'w')
    html.write('<html>\n')
    html.write('  <center>\n')
    html.write('    <head>\n')
    html.write('      <title>GeneView</title>\n')
    html.write('      <link rel="stylesheet" type="text/css" href="GeneView_style.css">\n')
    html.write('    </head>\n')
    html.write('    <body>\n')
    html.write('      <h1>GeneView</h1><br>\n')
    html.write('      <u>List of Genes:</u><br>\n')
    for gene in sorted(genes.keys()):
        html.write('      <a href="pages/'+gene+'.html">'+gene+'</a><br>\n')
    html.write('    </body>\n')
    html.write('  </center>\n')
    html.write('</html>')

## Pass in a "file" object, not a filename string
## i.e. readUniprotEnsemblTable(open('table.txt'))
## The returned dictionary has the following structure:
##   KEYS:   ENSEMBL ID
##   VALUES: Tuple of (Uniprot ID, Gene Name)
#def readUniprotEnsemblTable(f):
#    dic = {}
#    for line in f:
#        if line[0] != '#':
#            parts = line.strip().split()
#            dic[parts[0]] = (parts[1],parts[2])
#    return dic


import sys
import os
import glob
import shutil
from subprocess import call
from importVCF import importVCF
#from ReadTable import readTable
from ParseDAT import parseDAT


# sample usage:
#   python GeneView.py ../../../Dropbox/GenomeLens/SVT/candidates_CH_SVT_Final_v2.vcf ../esp_dl/ESP6500SI-V2-SSA137.GRCh38-liftover.chrAll.snps_indels.vcf ESP exampleOut ../inputs/UNIPROT_REFSEQ_ENSEMBLE.tab
#   python GeneView.py ../svt_gatk_candidate_mut/candidates_CH_SVT_Final_v2.vcf ../esp_dl/ESP6500SI-V2-SSA137.GRCh38-liftover.chrAll.snps_indels.vcf ESP ../exampleOut
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print "ERROR: Incorrect number of arguments. Correct usage:"
        print "GeneView.py <pat_vcf_file> <ref_vcf_file> <ref_type [ESP]> <username_aka_output> <uniprot_refseq_ensemblID_table>"
        sys.exit()
    outFolder = sys.argv[4]
    #genesAndMutations = parseMutationList(open(sys.argv[1],'r')) # parse VCF and return dict, where dict[geneName] = [list of mutationName@freq]
    #genesAndMutations = parseMutationList(importVCF(sys.argv[2], sys.argv[3], sys.argv[1]))
    #uniprotDict = readTable(open('db/UNIPROT_REFSEQ_ENSEMBLE.tab'))
    #global uniprotDict
    #uniprotDict = readTable(open(sys.argv[5]))
    uniprotDict = parseDAT(open(sys.argv[5]))
    #uniprotDict = readUniprotEnsemblTable(sys.argv[5])
    genes = importVCF(sys.argv[2], sys.argv[3], sys.argv[1], uniprotDict)
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
        #os.makedirs(outFolder + "/images")
        #os.makedirs(outFolder +"/pages")
    #if not os.path.exists(outFolder + "/images"): # create images folder if it doesn't exist
        #os.makedirs(outFolder + "/images")
    #if not os.path.exists(outFolder + "/pages"): # create pages folder if it doesn't exist
        #os.makedirs(outFolder + "/pages")
    #for css in glob.glob("*.css"): # copy all CSS files to output folder
        #shutil.copy(css,outFolder)
    #for gene in genesAndMutations: # generate a lollipop image and HTML page for each gene
    for gene in genes.keys():
        # gene is a uniprotID. Make sure it actually is one, since
        # some were added as dummy values
        if uniprotDict.get(gene) is None:
            #continue
            print "NOT IN uniprotDic " + gene
        #generateLollipop(gene,genesAndMutations) # add in to generate lollipops
        generateLollipop(genes[gene]) # add in to generate lollipops
        #generateHTML(gene)
    #generateIndexHTML(genesAndMutations) # generate index.html
