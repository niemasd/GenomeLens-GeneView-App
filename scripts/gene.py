
class Gene:
    # ctor
    def __init__(self, name, ensembl, refSeq, uniprot, aaChange, mafs, inPat):
        ## gene name, as given by snpeff
        # gene name, as given by uniprotID. This is the key
        self.name = name

        # ensembl transcript ID, as given by snpeff
        self.ensemblID = ensembl

        # refseq ID, as given by ESP6500
        self.refSeq = refSeq

        # uniprot ID, as translated from snpeff
        self.uniprotID = uniprot

        # list of amino acid changes
        self.AAChanges = [aaChange]

        # key: aaChange
        # value: list of MAFs
        self.mafs = {}
        self.mafs[aaChange] = mafs

        # key: aaChange
        # value: boolean (present in patient?)
        self.inPat = {}
        self.inPat[aaChange] = inPat

    # print format is: <gene> <aa change> <maf/maf/maf> <in patient>
    def __str__(self):
        retVal = ""
        for aa in self.AAChanges:
            maf = "NA"
            if self.mafs[aa] is not None:
                maf = "/".join(self.mafs[aa])

            retVal += "{} {} {} {} {} {}\n".format(self.name,
                                             ensemblID,
                                             uniprotID,
                                             aa,
                                             maf,
                                             self.inPat[aa])
        #retVal = retVal.rstrip() # remove trailing newline
        return retVal

    # update or add AA, MAF, inPat
    def addAAmaf(self, aaChange, maf, inPat):
        # if in patient
        if inPat:
            # if updating inPat field in existing entry
            if aaChange in self.AAChanges:
                self.inPat[aaChange] = inPat
            # if adding inPat field (non existing entry)
            else:
                self.AAChanges.append(aaChange)
                self.mafs[aaChange] = None
                self.inPat[aaChange] = inPat
        # otherwise, just add a new entry
        else:
            self.AAChanges.append(aaChange)
            self.mafs[aaChange] = maf
            self.inPat[aaChange] = inPat

    # return if this patient has a mutation in this gene at all
    def anyInPat(self):
        return any(self.inPat.values())

    # update geneName based on SnpEff data
    def addGeneName(self, geneName):
        # don't have a name yet
        if len(self.name) == 0:
            # the string passed in isn't empty
            if len(geneName) != 0:
                self.name = geneName
            # if the passed in string is empty, don't do anything
        # else, have a name already. Sanity check- is it the same?
        else:
            if self.name != geneName:
                print ("ERROR: " + str(self.name) + " does not match " + str(geneName) + ". Taking SnpEff's " + str(geneName) + ".")
                self.name = geneName
