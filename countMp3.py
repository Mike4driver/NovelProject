# from mutagen.wavpack import WavPack
import os
import wave
import contextlib
import math
import sys


def getNovelLength(dirName):
    novelFileList = os.listdir(dirName)

    novelFileList = [dirName + '\\' + novelFile for novelFile in novelFileList]

    totalLength = 0
    for novelFile in novelFileList:
        with contextlib.closing(wave.open(novelFile,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            totalLength += duration/60

    print(f"This novel is {math.ceil(totalLength)} minutes or {math.ceil(totalLength/60)} hours")

if __name__== "__main__":
    dirName = sys.argv[1]
    getNovelLength(dirName)