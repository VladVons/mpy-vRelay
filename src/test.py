#!/usr/bin/env python3

import os, time
from Inc.DB.Dbl import TDbl, TDblFields

dbl1 = TDbl()
File = 'Products.dbl'
if (os.path.isfile(File)):
    dbl1.Open(File)

    dbl2 = TDbl()
    dbl2.Create(File + '_', dbl1.Fields)

    dbl1.RecGo(1000)
    for RecNo in dbl1:
        #lt = time.localtime(dbl1.GetField('Created'))
        #DateTime = '%d-%02d-%02d %02d:%02d:%02d' % (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])
        #print(RecNo, dbl1.GetField('Name'), DateTime, dbl1.GetField('Value'))

        dbl2.RecAdd()
        dbl2.SetRec(dbl1.Buf)
    print(dbl2.GetSize())
    dbl2.Close()
else:
    Fields = TDblFields()
    Fields.Add('Name', 's', 5)
    Fields.Add('Created', 'f')
    Fields.Add('Value', 'f')

    dbl1.Create(File, Fields)
    for Idx in range(60*24):
        dbl1.RecAdd()
        dbl1.SetField('Name', 'Monitor_%s' % Idx)
        dbl1.SetField('Created', time.time())
        dbl1.SetField('Value', 100.14 + Idx)
dbl1.Close()
