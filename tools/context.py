import os
import sys

"""
provide 'tools/' directory with import context of the main project folder
"""

sys.path.insert(0, os.path.abspath('../flow-generator'))

from grid import Grid
from flow import Flow
import generator
import graphics
