
__author__  = "Joaquin"
__version__ = "5.3"
__update_time__ = "05-12-2018 14:21 UTC+01.00"
__all__ = ["Manipulator", "Surface", "Polygon"]

from .manipulator import Manipulator
from .structures import Surface 
from .polygon import Polygon	

print("Running SmoldynManipulator (version="+__version__+", last updated="+__update_time__+")\n")