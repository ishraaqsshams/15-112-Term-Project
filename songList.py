import os

# inspired by the recursion pt.2 notes http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
# however eventually, did not use recursion

# returns a list of all the wav files in a directory
def getWavFiles(path):
    wavFiles = []
    for filename in os.listdir(path):
        newPath = path + '/' + filename
        if newPath.endswith('.wav'):
            wavFiles.append(newPath)
    return sorted(wavFiles)

# returns a list of all the wav files in a directory
def getMP3Files(path):
    mp3Files = []
    for filename in os.listdir(path):
        newPath = path + '/' + filename
        if newPath.endswith('.mp3'):
            mp3Files.append(newPath)
    return sorted(mp3Files)

# get song names from a mp3 or wav file
def getSongNameFromFile(file):
    start = file.count('/')
    startIndex = file.index('/', start) + 1
    endIndex = len(file) - 4 # file ends with either .mp3 or .wav
    return file[startIndex: endIndex]

# returns a list song names of a list of wav files
def getSongNames(wavFiles):
    songNames = []
    for wav in wavFiles:
        songNames.append(getSongNameFromFile(wav))
    return sorted(songNames)