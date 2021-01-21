''' 

Since habit data is stored onto a local
machine, an abs path provided by the user
of this software is required. A location 
to store this path is also required,
which is why their is a  constant exists 
below.

'''
import os.path

HAB_TRACE_FPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "trace.txt")
