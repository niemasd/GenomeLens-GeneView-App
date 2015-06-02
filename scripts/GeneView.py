# parse text file (contains gene name + mutation)
colorPat = "ff0000" # red
colorNonPat = "00ccff" # light blue

def generateLollipop( gene ):
    command = ["./lollipops","-w=7000"]
    uniprotID = gene.uniprotID
    uniprotID = uniprotID.replace("_HUMAN", "") # not sure if need this
    #command.append("-o="+outFolder+"/"+uniprotID+".svg")
    command.append("-o="+outFolder+"/"+gene.name+ "_" + uniprotID + ".svg")
    command.append("-U="+uniprotID)
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
    print("Processing " + gene.name)
    print(" ".join(command))
    call(command)
    print("\n")

import sys
import os
import glob
import shutil
from subprocess import call
from importVCF import importVCF
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
    uniprotDict = parseDAT(open(sys.argv[5]))
    genes = importVCF(sys.argv[2], sys.argv[3], sys.argv[1], uniprotDict)
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    for gene in genes.keys():
        # gene is a uniprotID. Make sure it actually is one, since
        # some were added as dummy values
        #if gene not in uniprotDict.values(): # originally had 'is None:' at the end
        #    #print "NOT IN uniprotDic " + gene
        #    continue
        generateLollipop(genes[gene])
    # create uniprots.txt file (for views.py)
    uniprotsFile = open(outFolder + "/uniprots.txt",'w')
    for file in glob.glob(outFolder + "/*.svg"):
        if '/' in file:
            sp = file.split('/')
        elif '\\' in file:
            sp = file.split('\\')
        uniprotsFile.write(sp[len(sp)-1].split('.')[0] + '\n')
    uniprotsFile.close()
