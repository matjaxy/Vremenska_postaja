import os
from alchemy_interface import *
#os.remove('/home/pi/m/measures.db')

# create tables
Base.metadata.create_all(engine)
