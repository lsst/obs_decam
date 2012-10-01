from lsst.pipe.tasks.register import ParseTask

def parseExtname(md):
    side, ccd = "X", 0
    if not md.exists("EXTNAME"):
        return side, ccd
    extname = md.get("EXTNAME").strip()
    if extname[0] in "NS":
        side = extname[0]
    ccd = int(extname[1:])
    return side, ccd

class DecamParseTask(ParseTask):
    def translate_side(self, md):
        side, ccd = parseExtname(md)
        return side

    def translate_ccd(self, md):
        side, ccd = parseExtname(md)
        return ccd

    def translate_object(self, md):
        obj = None
        if md.exists("OBJECT"):
            obj = md.get("OBJECT").strip()
        if obj is None or len(obj) == 0 and md.exists("OBSTYPE"):
            obj = md.get("OBSTYPE").strip()
        if obj is None or len(obj) == 0:
            return "UNKNOWN"
        return obj
