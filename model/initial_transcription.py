class iRNAP(object):
    """
    Describes an RNAP undergoing initial transcription.
    """

    def __init__(self,
            rna_length=2,
            pre_translocated=True,
            post_translocated=False,
            paused=False,
            backtracked=False,
            iplus1_site=2,
            RNADNA_duplex_length=2,
            scrunched_DNA_size=0,
            free_5prime_RNA_length=0,
            max_duplex_length=10):

        # Simplified overall description of RNAP state during initial transcription
        self.RNA_length = rna_length
        self.pre_translocated = pre_translocated
        self.post_translocated = post_translocated
        self.paused = paused
        self.backtracked = backtracked
        self.iplus1_site = iplus1_site
        self.RNADNA_duplex_length = RNADNA_duplex_length
        self.scrunched_DNA_size = scrunched_DNA_size
        self.free_5prime_RNA_length = free_5prime_RNA_length
        self.__max_duplex_length = max_duplex_length

        self.SanityCheck()

    def __repr__(self):

        strs = 'RNA-len:\t{0}\nDuplex-len:\t{1}\nScrunched-size:\t{2}\niplus1_pos:\t{3}\n\n'
        strs = strs.format(self.RNA_length, self.RNADNA_duplex_length,
                self.scrunched_DNA_size, self.iplus1_site)
        if self.post_translocated:
            strs += 'Is POST-translocated\n'
        if self.pre_translocated:
            strs += 'Is PRE-translocated\n'
        if self.paused:
            strs += 'Is paused\n'
        if self.backtracked:
            strs += 'Is backtracked\n'

        return strs

    def SanityCheck(self):
        """
        Internal consistency-checking of states. Must be called after each update of state.
        """

        if self.backtracked:
            assert self.pre_translocated is False
            assert self.post_translocated is False
            assert self.paused is False

        if self.paused:
            assert self.pre_translocated is False
            assert self.post_translocated is False
            assert self.backtracked is False

        if self.post_translocated:
            assert self.pre_translocated is False
            assert self.backtracked is False
            assert self.paused is False

        if self.pre_translocated:
            assert self.post_translocated is False
            assert self.backtracked is False
            assert self.paused is False

        assert self.RNA_length >= self.RNADNA_duplex_length

        assert self.scrunched_DNA_size < self.RNA_length

        assert self.free_5prime_RNA_length < self.RNA_length

        if self.free_5prime_RNA_length > 0:
            assert self.free_5prime_RNA_length == self.RNA_length - self.RNADNA_duplex_length

        if self.RNADNA_duplex_length > self.__max_duplex_length:
            assert self.free_5prime_RNA_length > 0

    def GetActiveSiteDinucleotide(self, its):
        """
        Assumes an its on the form "AT(...)"" where AT are the +1 and +2 positions
        in the transcribed region.
        """
        return its[self.iplus1_site-1] + its[self.iplus1_site]

    def GetActiveSiteNucleotide(self, its):
        return self.get_active_site_dinucleotide(its)[-1]

    def ReverseTranslocate(self):
        self.SanityCheck()

        if self.pre_translocated:
            print('Was already pre-translocated!')
            1/0
        else:
            self.pre_translocated = True
            self.post_translocated = False

        self.SanityCheck()

    def Translocate(self):
        self.SanityCheck()

        if self.post_translocated:
            print('Was already translocated!')
            1/0
        else:
            self.pre_translocated = False
            self.post_translocated = True

        self.SanityCheck()

    def Pause(self):
        self.SanityCheck()
        if self.paused:
            print('Was already paused!')
            1/0
        else:
            if self.pre_translocated:
                self.paused = True
                self.pre_translocated = False
            else:
                print('Must be pre-translocated to pause!')
                1/0

        self.SanityCheck()

    def CanBackTrack(self):
        self.SanityCheck()
        return self.paused or self.backtracked

    def Backtrack(self):
        """
        Backtrack either from a paused state, or backtrack even further from an
        already backtracked state
        """
        self.SanityCheck()
        if self.CanBackTrack():

            if self.paused:
                self.paused = False
                self.backtracked = True

            self.iplus1_site -= 1
            self.scrunched_DNA_size -= 1
            # duplex length decreases by 1 if duplex is not full length
            if self.RNADNA_duplex_length <= self.__max_duplex_length:
                self.RNADNA_duplex_length -= 1

            # free 5' end reduced by one if it exists
            if self.free_5prime_RNA_length > 0:
                self.free_5prime_RNA_length -= 1
        else:
            print('Was not in a state from which to backtrack!')
            1/0

        self.SanityCheck()

    def CanGrow(self):
        excluded_from_growing = self.pre_translocated and self.backtracked and self.paused
        if excluded_from_growing and self.post_translocated:
            return False
        else:
            return True

    def GrowRNA(self):
        self.SanityCheck()
        if self.CanGrow():
            self.iplus1_site += 1
            self.RNA_length += 1
            self.scrunched_DNA_size += 1

            # increase duplex length until RNA reaches length 10
            if self.RNA_length <= self.__max_duplex_length:
                self.RNADNA_duplex_length = self.RNA_length

            # when reaching a full duplex, start growing a free 5' end
            if self.RNADNA_duplex_length == self.__max_duplex_length:
                self.free_5prime_RNA_length += 1
        else:
            print('Must be post-translocated to grow RNA!')
            1/0

        self.SanityCheck()

if __name__ == '__main__':

    myRNAP = iRNAP()
    myRNAP.GrowRNA()
    myRNAP.Translocate()
    myRNAP.ReverseTranslocate()
    myRNAP.Pause()
    myRNAP.Backtrack()

    print(myRNAP)

