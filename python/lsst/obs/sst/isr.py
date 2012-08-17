from lsst.ip.isr.isrTask import IsrTask

class SstIsrTask(IsrTask):
    def convertIntToFloat(self, exp):
        # Images are already float
        return exp

    def overscanCorrection(self, exp, amp):
        # There is no overscan
        return exp
