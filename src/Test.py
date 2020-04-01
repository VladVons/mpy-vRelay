#!/usr/bin/micropython
#!/usr/bin/python3

import gc
import time


def Connect1():
    from machine import Pin, PWM
    import time

    print('hello')

    pwm = PWM(Pin(13))
    pwm.duty(999)
    time.sleep(1)
    pwm.duty(312)
    time.sleep(1)
    pwm.duty(0)


def Play():
    # https://github.com/dhylands/upy-rtttl
    from machine import Pin, PWM
    import time

    tempo = 5
    tones = {
        'c': 262,
        'd': 294,
        'e': 330,
        'f': 349,
        'g': 392,
        'a': 440,
        'b': 494,
        'C': 523,
        ' ': 0,
    }

    beeper = PWM(Pin(13, Pin.OUT), duty=512)
    #beeper = PWM(Pin(13, Pin.OUT), freq=440, duty=512)
    melody = 'cdefgabC'
    rhythm = [8, 8, 8, 8, 8, 8, 8, 8]

    for tone, length in zip(melody, rhythm):
        print(tone, length)
        beeper.freq(tones[tone])
        time.sleep(tempo/length)
    beeper.deinit()



from Inc.Conf import Conf
from App.Menu import TMenuApp
Menu = TMenuApp()
Menu.MMain('/Main')
