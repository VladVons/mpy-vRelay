'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.08
License:     GNU, see LICENSE for more details
Description:.
'''

# python Sort dictionary of dictionaries by value
#SortD({'a1': {'Key': 1, 'Val': 111}, 'a2':{'Key': 2, 'Val': 222}})
def SortDD(aObj: dict, aName: str) -> list: 
    return sorted(aObj.items(), key = lambda k: k[1][aName])

# python Sort list of dictionaries by value
#SortL([{'Key': '/b1', 'Val': 21}, {'Key': '/a1', 'Val': 11}], 'Key')
def SortLD(aObj: list, aName: str) -> list: 
    return sorted(aObj, key = lambda k: k[aName])

#[{'Alias': 'dht22-a', 'Pin': 22, 'Type': 'Sen_dht22'}]
#def FindAD(aArr: list, aAlias: str)->dict:
#    if (aArr):
#        return next(Item for Item in aArr if Item['Alias'] == aAlias)
