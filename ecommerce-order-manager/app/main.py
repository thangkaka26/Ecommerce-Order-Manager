import sys
sys.dont_write_bytecode = True
import os
CUR_DIR = os.path.dirname(__file__)
sys.path.append(CUR_DIR)

from ui import gui
gui.ExecuteEcommerce()