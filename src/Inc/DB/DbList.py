'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.03.24
License:     GNU, see LICENSE for more details
Description:
    Db = TDbList(['red', 'green', 'blue'])
    Data = [[1,2,3], [10,20,30], [110,120,130]]
    Db.SetData(Data)

    print('GetSize', Db.GetSize())
    print('Data', Db.Data)
    print('Rec', Db.Rec)
    print('Json', str(Db))
    for Item in Db:
        print(Item.Rec.GetByName('red'),  Item.Rec[0])

    Db.Add()
    Db.Rec.SetByName('red', 11)
    Db.Flash()

    Db.Data.append([22,33,44])

    print('GetData', Db.GetData([0, 1]))
'''


import json


class TDbRec(list):
    def __init__(self, aHead: list):
        self.SetHead(aHead)

    def GetByName(self, aName: str) -> any:
        return self[self.Head[aName]]

    def SetByName(self, aName: str, aValue):
        self[self.Head[aName]] = aValue

    def Set(self, aList: list):
        self.clear()
        self.extend(aList)

    def SetHead(self, aFields: list):
        #self.Head = dict(zip(aFields, range(len(aFields))))
        self.Head = {Val: Idx for Idx, Val in enumerate(aFields)}


class TDbList():
    def __init__(self, aHead: list):
        self.Rec = TDbRec(aHead)
        self.Data = []
        self._RecNo = 0

    def __str__(self):
        return json.dumps({'data': self.Data, 'head': self.Rec.Head})

    def __iter__(self):
        return self

    def __next__(self):
        if (self._RecNo >= self.GetSize()):
            raise StopIteration
        else:
            self._RecInit()
            self._RecNo += 1
            return self

    def _RecInit(self):
        self.Rec.Set(self.Data[self._RecNo])

    def GetSize(self):
        return len(self.Data)

    def GetData(self, aFieldNo: list):
        #return [list(map(i.__getitem__, aFieldNo)) for i in self.Data]
        return [[D[i] for i in aFieldNo] for D in self.Data]

    def SetData(self, aList: list):
        self.Data = aList
        self.RecGo(0)

    def RecGo(self, aNo: int):
        self._RecNo = min(aNo, self.GetSize() - 1)
        self._RecInit()

    def Add(self):
        EmptyRec = [None for i in range(len(self.Rec.Head))]
        self.Data.append(EmptyRec)
        self.RecGo(self.GetSize())

    def Flash(self):
        self.Data[self._RecNo] = self.Rec
