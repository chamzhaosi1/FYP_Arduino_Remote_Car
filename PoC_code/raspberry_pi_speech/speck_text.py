from num2words import num2words
from subprocess import call
import sys


cmd_beg= 'espeak '
cmd_end= ' | aplay /home/engineer/romo/raspberry_pi_speech/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/engineer/romo/raspberry_pi_speech/Text.wav ' # To store the voice file

# text = input("Enter the Text: ")
text = str(sys.argv[1])
print(text)

#Replacing ' ' with '_' to identify words in the text entered
text = text.replace(' ', '_')

#Calls the Espeak TTS Engine to read aloud a Text
call([cmd_beg+cmd_out+text+cmd_end], shell=True)