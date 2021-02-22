from Inc.Conf import Conf
from Inc.ApiParse import QueryToDict
from Inc.Util.UHrd import Reset


async def DoUrl(aParent, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
    LenData = int(aHead.get('content-length', '0'))
    if (LenData > 0):
        R = 'about to reboot'

        Data = await aReader.read(LenData)
        Query = QueryToDict(Data.decode('utf-8'))
        Conf['STA_ESSID'] = Query.get('_STA_ESSID')
        Conf['STA_Paswd'] = Query.get('_STA_Paswd')
        Conf.Save()

        Reset()
    else:
        R = 'No data'

    await aParent.Answer(aWriter, 200, 'txt', R)
