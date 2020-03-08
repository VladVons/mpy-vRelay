'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.08
License:     GNU, see LICENSE for more details
Description:.
'''

# python Sort dictionary of dictionaries by value
def SortD(aObj: dict, aName: str) -> list: 
    return sorted(aObj.items(), key = lambda k: k[1][aName])


def SortL(aObj: list, aName: str) -> list: 
    return sorted(aObj, key = lambda k: k[aName])
