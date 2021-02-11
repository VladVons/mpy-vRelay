import json
#
from Inc.Http.MulUpload import TMulUpload
from Inc.Util import UStr, UFS


async def DoUrl(aParent, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
    LenData = int(aHead.get('content-length', '0'))
    if (LenData > 0):
        Ref = aHead.get('referer')
        if (Ref):
            Url, QueryR = UStr.SplitPad(2, Ref, '?')
            QueryR = aParent.ParseQuery(QueryR)
            Dir = QueryR.get('path', '')
            UFS.MkDir(Dir)
        else:
            Dir = ''

        R = await TMulUpload().Upload(aReader, aHead, Dir)
        R = json.dumps(R) + '\r\n'
        await aParent.Answer(aWriter, 200, 'txt', R)
