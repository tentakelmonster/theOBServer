# theOBServer
LPR tool support yeay

version = 1.0

how to use:

0a. make sure you have python installed

0b. python needs to be in your systems PATH variable (command line needs to be able to run python)

0c. you'll also need the Tk module for python -> `pip install tk`

0d. for easiest use, set up OBServer.py and paths.json right next to the text files

0e. check if the file names in the json match the ones in the folder and no file is missing

0f. missing files will be created automatically

1. execute the python script, for example by running runOBServer.sh (I hope this actually works)

1a. alternativly, open command line and type 'python OBServer.py'

2. on startup, the script sets all files to an initial state (all labels are empty, life totals are 20)

3. enter all names in the corresponding entry slots and press 'set' (these are only updated on 'set', 'reset' and initial startup)

4. the life totals save on each increment, decrement or changing of the values in the entry

4a. for best results, only enter integers in these

and that's it :D

