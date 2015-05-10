# TODO update importContextVCF to store ensembl/Uniprot IDs as keys instead of gene names
# TODO update lollipops call
# TODO read in excel for patient
# TODO implement ExAC formatting
# TODO for efficiency, consider writing all ref genes as python objs (use cPickle lib), then read as needed for patient. or, read in pat first, then only create the objs as needed. or, pre generate all ref genes with all ref data as lollipop svgs, then just deal with editing svgs on the fly
# TODO fix MAF output formatting
# TODO fix flow of data from reading in vcf files to creating lollipop plots. Right now, reading in vcf files creates a giant string of information, then creating lollipop plots parses that string. This may be better with just passing a dictionary of Gene objs. However, it also depends on how the patient specific data is being stored internally (vcf? sqlite db?)

import vcf
import re # regex
import sys
from gene import Gene

def importContextVCF(fileName, contextSrc, uniprotDict):
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
            currGeneSet = record.INFO[infoGeneName] # gene names
            maf = record.INFO[infoMAF] # minor allele freqs
            for entry in prot:
                if isESP:
                    if ")" in entry: # parsing issue. Silent mutations rep by "=", which is parsed incorrectly. In this case, there's no ending ")", so skip (ie don't add)
                        ## entry ex: NM_014339.5:p.(N292S)
                        ##pDot = entry.partition(":")[2] # result ex p.(N292S)
                        ##endParen = pDot.partition("(")[2] # result ex N292S)
                        ##trimmed = endParen.partition(")")[0] # result ex N292S
    
                        ## entry ex: NM_014339.5:p.(N292S)
                        ##tr = aaRegexSt.sub("", entry) # result ex p.(N292S)
                        ##trimmed = aaRegexEnd.sub("", tr) # result ex N292S)
                        ##aaChange.append(trimmed)
                        #aaChange.append(aaRegexEnd.sub("", aaRegexSt.sub("", entry))) # one liner

                        ## entry ex: NM_014339.5:p.(N292S)
                        # split around ":".
                        # First part is RefSeq ID, second part is amino acid change
                        sp = entry.split(":")
                        refSeq = sp[0]
                        pDot = sp[1] # result ex p.(N292S)
                        endParen = pDot.partition("(")[2] # result ex N292S)
                        aa = endParen.partition(")")[0] # result ex N292S
                        #aa = sp[1]

                        # translate from refSeq to uniprot
                        #uniprotID = uniprotDict[refSeq]
                        uniprotID = uniprotDict.get(refSeq)
                        if uniprotID is None:
                            # FIXME try with refSeq or skip?
                            uniprotID = refSeq
                        #else:
                        #    print "NOT NONE " + uniprotID
                        
                        #if uniprotID == "": # no uniprot or refseq
                        if len(uniprotID) == 0: # no uniprot or refseq
                            uniprotID = currGeneSet[0] # try with gene name or skip? FIXME
                        #else:
                        #    print "NOT LEN == 0 " + uniprotID
                            #print "CHANGED " + entry
                        #print "\"" + uniprotID  + "\""
                        # store
                        #if currGene in geneDict:
                        #maf = record.INFO[infoMAF] # minor allele freqs
                        if uniprotID in geneDict:
                            # add this aa to this gene's records, default inPat=F
                            #geneDict[currGene].addAAmaf(currAA, maf, False)
                            geneDict[uniprotID].addAAmaf(aa, maf, False)
                        else:
                            # add new gene to dict, default inPat to False
                            #geneDict[currGene] = Gene(currGene, "", refSeq, uniprotID, currAA, maf, False)
                            geneDict[uniprotID] = Gene(uniprotID, "", refSeq, uniprotID, aa, maf, False)
    
            #currGeneSet = record.INFO[infoGeneName] # gene names
            #maf = record.INFO[infoMAF] # minor allele freqs
            #
            ## store this entry
            #for currGene in currGeneSet:
            #    for currAA in aaChange:
            #        if currGene in geneDict:
            #            # add this aa to this gene's records, default inPat=F
            #            geneDict[currGene].addAAmaf(currAA, maf, False)
            #        else:
            #            # add new gene to dict, default inPat to False
            #            geneDict[currGene] = Gene(currGene, currAA, maf, False)
    
    return geneDict

# extract gene name and amino acid change and ensembl ID.
# Return as a list [gene name, aa change, ensmblID]
# ex: 'NON_SYNONYMOUS_CODING(MODERATE|MISSENSE|gCc/gTc|A325V|347|MKNK1|protein_coding|CODING|ENST00000341183|11|1)'
# ex: 'EXON(MODIFIER|||||MKNK1|retained_intron|CODING|ENST00000532897|5|1)'
def parseEff(effEntry, geneNameIdx, aaIdx, ensemblIdx):
    noEffect = (effEntry.partition("(")[2]).partition(")")[0].strip()
    effTok = noEffect.split("|")
    geneName = effTok[geneNameIdx]
    aaChange = effTok[aaIdx]
    ensemblID = effTok[ensemblIdx]
    if geneName == "" or aaChange == "" or ensemblID == "":
        return None
    else:
        return [geneName, aaChange, ensemblID]

# read in the patient VCF file. Parse the EFF entry for gene name and amino
# acid change.
# Edits the passed geneDict (add or update)
def importPatientVCF(fileName, geneDict, uniprotDict):
    vcf_reader = vcf.Reader(open(fileName, 'r'))

    # find index of AA change based on SnpEff header
    # should be:
    # Predicted effects for this variant.Format: 'Effect ( Effect_Impact | Functional_Class | Codon_Change | Amino_Acid_Change| Amino_Acid_length | Gene_Name | Transcript_BioType | Gene_Coding | Transcript_ID | Exon_Rank  | Genotype_Number [ | ERRORS | WARNINGS ] )'
    headerStr = ((vcf_reader.infos['EFF'].desc).partition("(")[2]).partition(")")[0].strip()
    headerTok = headerStr.split("|") # just the stuff in the (), split by |
    aaIdx = -1
    geneNameIdx = -1
    ensemblIdx = -1
    for tok in headerTok:
        if "Amino_Acid_Change" in tok:
            aaIdx = headerTok.index(tok)
        elif "Gene_Name" in tok:
            geneNameIdx = headerTok.index(tok)
        elif "Transcript_ID" in tok:
            ensemblIdx = headerTok.index(tok)
    if aaIdx == -1:
        print "ERROR: Couldn't find Amino_Acid_Change in EFF header"
        return -1
    if geneNameIdx == -1:
        print "ERROR: Couldn't find Gene_Name in EFF header"
        return -1
    if ensemblIdx == -1:
        print "ERROR: Couldn't find Transcript_ID in EFF header"
        return -1
    
    # iterate over lines in vcf file
    for record in vcf_reader:
        #print record.INFO
        if 'EFF' in record.INFO:
            effEntries = record.INFO['EFF']
        else:
            continue
        for entry in effEntries:
            # geneAAlist = [gene name, aa change, ensmblID]
            geneAAlist = parseEff(entry, geneNameIdx, aaIdx, ensemblIdx)

            # no gene name or aa change in this entry. continue
            if geneAAlist is None:
                continue

            geneName = geneAAlist[0]
            aa = geneAAlist[1]
            ensemblID = geneAAlist[2]

            # get uniprotID
            #uniprotID = uniprotDict[geneAAlist[3]]
            uniprotID = uniprotDict.get(ensemblID)

            #print "UNCHANGED " + str(uniprotID)
            if uniprotID is None:
                # FIXME try with ensemblID? or skip?
                uniprotID = ensemblID

            if len(uniprotID) == 0:
                uniprotID = geneName # try with gene name to match context vcf or skip? FIXME

            #print "CHANGED " + uniprotID
            # if have stored this gene in geneDict
            #if geneAAlist[0] in geneDict: # store by gene name
            #if geneAAlist[2] in geneDict: # store by ensembl ID
            if uniprotID in geneDict: # store by uniprot ID
                #geneDict[geneAAlist[2]].addAAmaf(geneAAlist[1], None, True)
                geneDict[uniprotID].addAAmaf(aa, None, True)
            # else, make a new Gene obj
            else:
                #geneDict[geneAAlist[2]] = Gene(geneAAlist[0], geneAAlist[2], uniprotID, geneAAlist[1], None, True)
                #geneDict[uniprotID] = Gene(geneAAlist[0], geneAAlist[2], "", uniprotID, geneAAlist[1], None, True)
                geneDict[uniprotID] = Gene(uniprotID, ensemblID, "", uniprotID, aa, None, True)
 

def importVCF(refFile, refType, patFile, uniprotDict):
    geneDict = importContextVCF(refFile, refType, uniprotDict)
    importPatientVCF(patFile, geneDict, uniprotDict) # updates existing dict
    #return geneDict

    # filter results
    ret = {}
    for key in geneDict:
        # only keep the genes that the patient has
        if (geneDict[key]).anyInPat():
            #ret.append(str(geneDict[key]))
            ret[key] = geneDict[key]
    return ret
            
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
