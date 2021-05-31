"""
TODO: This file should provide the functionality to write text into the Minecraft world using blocks.
(Think Hollywood sign). It's probably a pipe dream though...
"""

from enum import Enum

from ..http_utils.interfaceUtils import setBlock


class Axis(Enum):
    X_POS = 1
    X_NEG = -1
    Z_POS = 2
    Z_NEG = -2
    Y_POS = 3
    Y_NEG = -3


def writeMessage(msg, textAxis, viewAxis, x, y, z, blockType, size=5):
    """
    Function that takes a message and writes it in blocks (kinda like the hollywood sign).
    msg: The message to be written
    textAxis: the axis that the text will appear left to right
    viewAxis: the axis parallel to viewing the text to reading it properly
    x,y,z: the block of the top left corner of the first character in msg
    blockType: a string indicating the type of block used to spell the message
    size: the height of the characters in blocks default=5
    """
    print("Writing {} starting at {} {} {}".format(msg, x, y, z))
    if textAxis == Axis.Y_POS or textAxis == Axis.Y_NEG:
        print("Don't support this text axis right now.")
        return

    def writeCharacter(c, x, y, z):
        def writeC(x, y, z):
            pass

        def writeS():
            pass

        def write4():
            pass

        def write3():
            pass

        def write0():
            pass

        def writeSpace():
            pass

        if c == "C":
            writeC(x, y, z)
        elif c == "S":
            writeS()
        elif c == "4":
            write4()
        elif c == "3":
            write3()
        elif c == "0":
            write0()

    for c in msg:
        writeCharacter(c, x, y, z)
