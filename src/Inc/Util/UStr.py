'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''


def SplitPad(aCnt: int, aStr: str, aDelim: str) -> list:
    R = aStr.split(aDelim, aCnt - 1)
    for i in range(aCnt - len(R)):
        R.append('')
    return R


def ConvertTo(aData):
    if ( (aData) and (type(aData).__name__ in ['str', 'unicode']) ):
        if (aData[0] == '"') and (aData[-1] == '"'):
            aData = aData[1:-1]
        elif (aData.lower() in ['true', 'false']):
            aData = bool(aData)
        elif (aData.isdigit()):
            aData = int(aData)
        elif (IsFloat(aData)):
            aData = ToFloat(aData)
        elif (IsArr(aData)):
            aData = json.loads(aData)
    return aData


class TDictRepl:
    def __init__(self, aDict: dict = {}):
        self.Dict = aDict

    def Parse(self, aStr: str) -> str:
        import re as re

        if (self.Dict):
            #r = re.compile(r'(\$\w+)\b')
            r = re.compile(r'(\$[a-zA-Z0-9]+)')
            while True:
                m = r.search(aStr)
                if (m):
                    Find = m.group(0)
                    Repl = self.Dict.get(Find, '-x-')
                    aStr = aStr.replace(Find, Repl)
                else:
                    break

        self.Dict = {}
        return aStr
