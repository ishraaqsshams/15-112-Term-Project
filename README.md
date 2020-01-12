# 15-112-Term-Project

BEAT HAZARD
Readme File

Description: 
Beat Hazard is a two-dimensional space-shooting game where the player chooses a 
song to play, and based on it's beat, it spawns enemy ships and asteroids. The 
objective of the game is to stay alive for the duration of the song. The score 
is the percentage of the song completed. The player can move around with the arrow
keys and can shoot the enemies with mouse click. The player rotates based on the cursor 
position and aims in that direction when shooting.

To Run the game: run main.py. In order to play the song, in the song directory, 
you must download the song as both a wav file and as an mp3 file. The reason for
downloading it twice it that the mp3 file allows it to play in the background 
and the wav file allows audioAnalyis.py to analyze the music and return a list 
of times where a beat is present.

Libraries needed to be installed:
PyGame
Soundfile
Mutagen.mp3
NumPy
