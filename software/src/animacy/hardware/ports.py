"""
Animacy

Hardware ports.

Copyright (c) 2026 Sparky Bobo
"""

import board

class IOPort:
    """IOPort definition."""

    def __init__(self, name:str, pin:board.Pin) -> None:
        """Initialize IOPort."""
        self.name = name
        self.pin = pin
        pass

class SerialPort:
    """Serial definition."""

    def __init__(self, name:str, txpin:board.Pin, rxpin:board.Pin, baudrate=int, timeout=float) -> None:
        """Initialize SerialPort."""
        self.name = name
        self.txpin = txpin
        self.rxpin = rxpin
        self.baudrate = baudrate
        self.timeout = timeout
        pass    

class I2CPort:
    """Serial definition."""

    def __init__(self, name:str, cpin:board.Pin, dpin:board.Pin) -> None:
        """Initialize SerialPort."""
        self.name = name
        self.cpin = cpin
        self.dpin = dpin
        pass    

class Ports:
    """Port definition."""
    io0  = IOPort("gpio0", board.GP0)
    io1  = IOPort("gpio1", board.GP1)
    io2  = IOPort("gpio2", board.GP2)
    io3  = IOPort("gpio3", board.GP3)
    io4  = IOPort("gpio3", board.GP4)
    io5  = IOPort("gpio3", board.GP5)
    io6  = IOPort("gpio3", board.GP6)
    io7  = IOPort("gpio3", board.GP7)
    io8  = IOPort("gpio3", board.GP8)
    io9  = IOPort("gpio3", board.GP9)
    io10 = IOPort("gpio3", board.GP10)
    io11 = IOPort("gpio3", board.GP11)
    io12 = IOPort("gpio3", board.GP12)
    io13 = IOPort("gpio3", board.GP13)
    io14 = IOPort("gpio3", board.GP14)
    io15 = IOPort("gpio3", board.GP15)
    io = [ io0, io1, io2, io3, io4, io5, io6, io7, io8, io9, io10, io11, io12, io13, io14, io15 ]
    # Every board has a MIDI UART
    midi = SerialPort("midi", board.GP16, board.GP17, baudrate=31250, timeout=0.001)      
    # Every board has 1 accessory i2c port
    i2c = I2CPort("is2", board.GP19, board.GP18)
    # Every board has 1 diagnostic i2c port
    diag = I2CPort("diag", board.GP21, board.GP20)          
    # Every board has a built-in status and Neopixel port
    led = IOPort("led", board.GP22)
    status = IOPort("status" ,board.LED)
