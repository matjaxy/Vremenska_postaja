import time
import os
os.remove('./measures.db')
time.sleep(5)
os.system("init_db.py")
