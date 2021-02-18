#!/usr/bin/micropython

class TThermos():
    def __init__(self, aHyster: int = 1):
        self.Hyster = aHyster
        self.State = False

    def Check(self, aBase, aValue):
        Hyster = abs(self.Hyster)

        if (aValue <= aBase - Hyster):
            self.State = self.Hyster > 0
        elif (aValue >= aBase + Hyster):
            self.State = self.Hyster < 0
        return self.State


Th = TThermos(-1)
while True:
    Cur = input('Cur: ')
    R = Th.Check(10, float(Cur))
    print('State', R)


'''
       if (aDif > 0):
            Result = (aValue < aBase) or (self.xDirection > 0 and aValue < aBase + aDif)
        else:
            Result = (aValue > aBase) or (self.xDirection < 0 and aValue > aBase + aDif)


hysteresis = 0.1

while True:
    time_since_s1_start = timenow - s1
    if time_since_s1_start < 0:
        time_since_s1_start = time_since_s1_start + 86400

    range_s1 = s2 - s1
    if range_s1 < 0:
       range_s1 = range_s1 + 86400

    if time_since_s1_start < range_s1:
        if (read_temp() < (temp_1 - hysteresis)):
            light_on()

        if (read_temp() > (temp_1 + hysteresis)):
            light_off()

    sleep(300)
'''
