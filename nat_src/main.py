import sys
from class_data import Data
from class_nostr_format import Usr
import parse
from errors import error_and_exit

# Initial settings
sys.dont_write_bytecode = True # Avoid generating a '.pyc'-file (Note: Not working lol, still creates a folder).

data = Data() # Making an instance of the Data-class.
user = Usr() # Making an instance of the usr-class.
error_code = parse.parse_and_store(data, user) # Parsing an storing input files (paths and contents) from Substack export
if (error_code != 0): # Upon error, exit program
	error_and_exit(error_code)
