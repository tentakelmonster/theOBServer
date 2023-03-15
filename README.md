# theOBServer
LPR tool support yeay

version = 1.1

how to use:

0a. make sure you have python installed

0b. python needs to be in your systems PATH variable (command line needs to be able to run python)

0c. you'll also need the Tk module for python -> `python -m pip install tk`

0d. for easiest use, set up OBServer.py and paths.json right next to the text files

0e. check if the file names in the json match the ones in the folder and no file is missing

0f. missing files will be created automatically

1. execute the python script, for example by running runOBServer.sh (I hope this actually works)

1a. alternativly, open command line and type 'python OBServer.py'

2. on startup, the script resets life totals to 20 and reads the last entries of the name files.

3. enter all names in the corresponding entry slots and press 'set' (the files are only updated on 'set' and 'reset all')

4. the life totals save on each increment, decrement or any other form of changing the values in the entry.

4a. for best results, only enter integers in these

4b. there's hot keys for incrementing and decrementing life totals. these don't work when you're entering something. click anywhere to refocus on the frame (hotkeys work again)

and that's it :D
