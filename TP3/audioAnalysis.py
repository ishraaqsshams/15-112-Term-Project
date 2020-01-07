# initial code inspired my from https://tinyurl.com/t4sluy5 
# user HYRY
# What I watched to understand audio analysis - https://www.youtube.com/watch?v=RHmTgapLu4s&t=19s
# https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python
import numpy as np
import soundfile as sf
import time
import wave

# returns the sound file data
def getData(song):
    sfdata, sfrate = sf.read(song)
    return sfdata


# returns a list of times in milliseconds where the energy at that time is greater than
# the average energies of the last 20 chunks - 
# inspired by previous 15-112 term project
# Pulse - Devansh Kukreja
# https://www.youtube.com/watch?v=QLwTMGOUm10
# additionally some code modified from https://www.programcreek.com/python/example/93227/scipy.io.wavfile.read
# which analyzes the sound energy from a wavfile
def getTimes(song, chunk = 2048 * 4):
    wav = wave.Wave_read(song)
    rate = wav.getframerate()
    data = getData(song)
    #holds average of the powers of the last 20 chunks
    avgList = []
    # returns the times when it is considered a beat
    timeList = []
    i = 0
    # goes through all the chunks in the song
    while True:
        power = 20*np.log10(np.abs(np.fft.rfft(data[chunk * i: chunk * (1 + i), 0])))
        freq = np.linspace(0, rate/2.0, len(power))
        if (chunk * (i + 1)) > len(data):
            break
        avg = abs(sum(power) / len(power))
        # compares the power of current chunk to the last 20
        if i > 19:
            if avg > sum(avgList) / len(avgList):
                # chunk * i / rate = time in seconds
                timeS = chunk * i / rate
                timeMS = timeS * 1000
                timeList.append(timeMS)
            avgList.pop(0)
        avgList.append(avg)
        i += 1  
    wav.close()
    return timeList