from lsst.ip.isr import IsrTask

class DecamIsrTask(IsrTask):
    def convertIntToFloat(self, exp):
        """No conversion necessary."""
        return exp
