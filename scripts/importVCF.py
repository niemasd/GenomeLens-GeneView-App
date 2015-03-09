# TODO read in excel for patient
# TODO implement ExAC formatting
# TODO for efficiency, consider writing all ref genes as python objs (use cPickle lib), then read as needed for patient. or, read in pat first, then only create the objs as needed. or, pre generate all ref genes with all ref data as lollipop svgs, then just deal with editing svgs on the fly

import vcf
import re # regex
import sys
from gene import Gene

def importContextVCF(fileName, contextSrc):
    #vcf_reader = vcf.Reader(open('esp_dl/ESP6500SI-V2-SSA137.GRCh38-liftover.chr22.snps_indels.vcf', 'r'))
    vcf_reader = vcf.Reader(open(fileName, 'r'))
    
    if contextSrc == "ESP":
        # regex for cleaning up aa changes
        # entry ex: NM_014339.5:p.(N292S)
        # result ex: N292S
        aaRegexSt = re.compile("^.*:p\.\(")
        aaRegexEnd = re.compile("\)$")
        infoProt = 'HGVS_PROTEIN_VAR'
        infoGeneName = 'GL'
        infoMAF = 'MAF'
        isESP = True
    
    # key: gene name
    # value: Gene obj
    geneDict = {}
    
    # iterate over all lines in vcf file
    for record in vcf_reader:
        prot = record.INFO[infoProt] # protein changes
    
        # if has some protein amino acid change entry
        if all(entry is not None for entry in prot):
            # reformat aaChange entry to be just <ref><pos><alt>
            aaChange = []
            for entry in prot:
                if isESP:
                    if ")" in entry: # parsing issue. Silent mutations rep by "=", which is parsed incorrectly. In this case, there's no ending ")", so skip (ie don't add)
                        # entry ex: NM_014339.5:p.(N292S)
                        #pDot = entry.partition(":")[2] # result ex p.(N292S)
                        #endParen = pDot.partition("(")[2] # result ex N292S)
                        #trimmed = endParen.partition(")")[0] # result ex N292S
    
                        # entry ex: NM_014339.5:p.(N292S)
                        #tr = aaRegexSt.sub("", entry) # result ex p.(N292S)
                        #trimmed = aaRegexEnd.sub("", tr) # result ex N292S)
                        #aaChange.append(trimmed)
                        aaChange.append(aaRegexEnd.sub("", aaRegexSt.sub("", entry))) # one liner
    
            currGeneSet = record.INFO[infoGeneName] # gene names
            maf = record.INFO[infoMAF] # minor allele freqs
            
            # store this entry
            for currGene in currGeneSet:
                for currAA in aaChange:
                    if currGene in geneDict:
                        # add this aa to this gene's records, default inPat=F
                        geneDict[currGene].addAAmaf(currAA, maf, False)
                    else:
                        # add new gene to dict, default inPat to False
                        geneDict[currGene] = Gene(currGene, currAA, maf, False)
    
    return geneDict

# extract gene name and amino acid change.
# Return as a tuple (gene name, aa change)
# ex: 'NON_SYNONYMOUS_CODING(MODERATE|MISSENSE|gCc/gTc|A325V|347|MKNK1|protein_coding|CODING|ENST00000341183|11|1)'
# ex: 'EXON(MODIFIER|||||MKNK1|retained_intron|CODING|ENST00000532897|5|1)'
def parseEff(effEntry, geneNameIdx, aaIdx):
    noEffect = (effEntry.partition("(")[2]).partition(")")[0].strip()
    effTok = noEffect.split("|")
    geneName = effTok[geneNameIdx]
    aaChange = effTok[aaIdx]
    if geneName == "" or aaChange == "":
        return None
    else:
        return (geneName, aaChange)

# read in the patient VCF file. Parse the EFF entry for gene name and amino
# acid change.
# Edits the passed geneDict (add or update)
def importPatientVCF(fileName, geneDict):
    vcf_reader = vcf.Reader(open(fileName, 'r'))

    # find index of AA change based on SnpEff header
    # should be:
    # Predicted effects for this variant.Format: 'Effect ( Effect_Impact | Functional_Class | Codon_Change | Amino_Acid_Change| Amino_Acid_length | Gene_Name | Transcript_BioType | Gene_Coding | Transcript_ID | Exon_Rank  | Genotype_Number [ | ERRORS | WARNINGS ] )'
    headerStr = ((vcf_reader.infos['EFF'].desc).partition("(")[2]).partition(")")[0].strip()
    headerTok = headerStr.split("|") # just the stuff in the (), split by |
    aaIdx = -1
    geneNameIdx = -1
    for tok in headerTok:
        if "Amino_Acid_Change" in tok:
            aaIdx = headerTok.index(tok)
        elif "Gene_Name" in tok:
            geneNameIdx = headerTok.index(tok)
    if aaIdx == -1:
        print "ERROR: Couldn't find Amino_Acid_Change in EFF header"
        return -1
    if geneNameIdx == -1:
        print "ERROR: Couldn't find Gene_Name in EFF header"
        return -1
    
    # iterate over lines in vcf file
    for record in vcf_reader:
        effEntries = record.INFO['EFF']
        for entry in effEntries:
            geneAAtup = parseEff(entry, geneNameIdx, aaIdx)

            # no gene name or aa change in this entry. continue
            if geneAAtup is None:
                continue
            # if have stored this gene in geneDict
            if geneAAtup[0] in geneDict:
                geneDict[geneAAtup[0]].addAAmaf(geneAAtup[1], None, True)
            # else, make a new Gene obj
            else:
                geneDict[geneAAtup[0]] = Gene(geneAAtup[0], geneAAtup[1], None, True)
 

# sample usage:
# python importVCF.py ../esp_dl/ESP6500SI-V2-SSA137.GRCh38-liftover.chr22.snps_indels.vcf ESP ../../../Dropbox/GenomeLens/SVT/candidates_CH_SVT_Final_v2.vcf | less
# python importVCF.py ../esp_dl/ESP6500SI-V2-SSA137.GRCh38-liftover.chrAll.snps_indels.vcf ESP ../svt_gatk_candidate_mut/candidates_CH_SVT_Final_v2.vcf
if __name__ == "__main__":
    if len(sys.argv) != 4 :
        print "ERROR: Incorrect number of arguments. Correct usage:"
        print sys.argv[0] + " <context vcf_file> [ESP|ExAC] <patient vcf_file>"
        sys.exit()

    geneDict = importContextVCF(sys.argv[1], sys.argv[2])
    importPatientVCF(sys.argv[3], geneDict) # updates existing dict
    # print
    for key in geneDict:
        # only print the genes that the patient has
        if (geneDict[key]).anyInPat():
            print geneDict[key]
