from Inc.Conf import TConf
ConfApp = TConf('Conf/App')

# esp8266 Plugin/App/Therm/__init__.py
from Inc.ConfDev import TConfDev
ConfDevTherm = TConfDev()
ConfDevTherm.Load('Conf/Dev', ConfApp)
