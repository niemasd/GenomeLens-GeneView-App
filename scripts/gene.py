
class Gene:
    # ctor
    def __init__(self, name, aaChange, mafs, inPat):
        self.name = name

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
            retVal += "{} {} {} {}\n".format(self.name,
                                             aa,
                                             maf,
                                             self.inPat[aa])
        retVal = retVal.rstrip() # remove trailing newline
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

