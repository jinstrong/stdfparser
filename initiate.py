'''
This file is the entrance to start the integrated processing tool for ATE related data



'''

import os
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

import os
import sys
import pdb
# import reprlib
import importlib
#import psutil
import cProfile, pstats, io
import time
#from time import time, gmtime, strftime, localtime
import calendar
import datetime
import re
import argparse


def single(file):
	cmd='c:\\anaconda2\python.exe CORE/test.py '+file
	os.system(cmd)

class Scheduler:
    def __init__(self, conf):
        #pdb.set_trace()
        self._argument = conf
        self.stdf_list=[]
        self.digest()
    def digest(self):
        file_list=map(lambda s:os.path.join(self._argument.source,s),os.listdir(self._argument.source))
    	self.stdf_list=filter(lambda s:s.endswith('std.gz'),file_list)
       
    def launch(self):
        pool = ThreadPool(multiprocessing.cpu_count())
        pool.map(single,self.stdf_list)
        pool.close()

if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description='Modularized Anlaysis Pipelining System, Anlaysis Made Simple yet Powerful.')
    parser.add_argument("-i", "--source", dest="source", default='', help="path to source data")# metavar="FILE")
    # parser.add_argument("-o", "--target", dest="target", default='', help="output path")
    # parser.add_argument("-f", "--filter", dest="filter", default='',  help="process filter")
    # parser.add_argument("-r", "--record", dest="record", default='',  help="file to store the log")

    # parser.add_argument("-s", "--silent", dest="silent", default=False, action='store_true', help="skip unnecessary log printing")

    # parser.add_argument("-d", "--daemon", dest="daemon", default=False, action='store_true', help="run as daemon")

    # parser.add_argument("-p", "--project", dest="project", default='', help="project definition file")

    # parser.add_argument("-pf", "--profile", dest="profile", default=False, action='store_true', help="activate profiling")

    # parser.add_argument("-sl", "--system-limit", dest="system_limit", default='',help="cpu/mem usage limit")
    # parser.add_argument("-nl", "--number-limit", dest="number_limit", default='',help="number of file processed limit")

    # parser.add_argument("-rl", "--random-load", dest="random_load", default=False, action='store_true', help="Use disordered lister when loading data")

    #parser.add_argument("-e", "--file-type", dest="file_type", default='',help="file type (extension) filter")


    #schedule = Scheduler(dict([ tuple(x.rstrip(' ').split(' ')) if len(x.rstrip(' ').split(' '))>1 else tuple(x.rstrip(' ').split(' ')+['']) for x in re.split('-*',' '.join(sys.argv))[1:] ]))
    Scheduler(parser.parse_args()).launch()


    sys.exit(0)
