import vcf
import sys
import re

#p = "s||||||s".split("|")
#for s in p:
#    print s == ""
#str1 = "str"
#print str1 == "str"
#print len(sys.argv)
vcfFile = open(sys.argv[1],'r')
vcf_reader = vcf.Reader(vcfFile)
#print vcf_reader.formats
print vcf_reader.infos
for rec in vcf_reader:
    if "EFF" in rec.INFO:
        #print str(rec) + "\t" + str(rec.INFO["EFF"])
        print str(rec) + "\t" + str(rec.INFO)
#print vcf_reader.infos['EFF'].desc
#print re.search("\(.*\)", vcf_reader.infos['EFF'].desc).group()
#print re.sub("(\()(.*)(\))", "\2", vcf_reader.infos['EFF'].desc)
#headerStr = ((vcf_reader.infos['EFF'].desc).partition("(")[2]).partition(")")[0].strip()
#print headerStr
#headerTok = headerStr.split("|")
#for tok in headerTok:
#    if "Amino_Acid_Change" in tok:
#        print tok.strip()
#        print headerTok.index(tok)
#    if False:
#        idx = headerTok.index(tok)
#
#print idx
##for record in vcf_reader:
##    print record.INFO['EFF']
#    #print record.INFO['GL']
#    print record.INFO['HGVS_PROTEIN_VAR']
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#record = vcf_reader.next()
#print record.INFO['EFF']
#print "\n"
#








# from splitMultRow.py before I deleted it
## tool to split comma separated values over multiple rows.
## example:
##   "GTF2A1L,STON1-GTF2A1L x y" ==> "GTF2A1L x y
##                                    STON1-GTF2A1L x y"
## Reads from stdin, prints to stdout
## Input is expected to be space delimited values (3 cols)
## where the first column is comma separated. No error checking is done
## on input (TODO)
#
#import sys
#if __name__ == "__main__":
#  file = open(sys.argv[1],'r') # TODO read from stdin instead
#  for line in file:
#    print(line)
#
#  file.close()
