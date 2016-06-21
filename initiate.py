"""
This file is the entrance to start the integrated processing tool for ATE related data in a folder

"""
# from __future__ import absolute_import
import os
import sys
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import pandas as pd
import numpy as np
import argparse

import logging

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from stdf_core.test import TT


def set_affinity_on_worker():
    """When a new worker process is created, the affinity is set to all CPUs"""
    print("I'm the process %d " % os.getpid())


def get_yield(excel_file):
    """
    This function parse an excel file, extracts yield sheet info as a dataframe

    :param excel_file:
    :return:
    """
    with pd.ExcelFile(excel_file) as xls:
        data = pd.read_excel(xls, 'yield', index_col=[0]).transpose()
    return data


def get_dict(excel_file):
    """
    This function parse an excel file, extracts yield sheet info and converts data into nested dict


    :param excel_file:
    :return:
    """
    new_dict = get_yield(excel_file).to_dict()
    my_dict = {}
    basename = os.path.basename(excel_file)
    name_front = basename.find('_') + 1
    name_end = basename.find('---') - 12
    time_front = excel_file.rfind('-')
    dot_position = excel_file.find('.std')
    time = excel_file[time_front:dot_position]
    name = basename[name_front:name_end]+time

    for key0, value0 in new_dict.iteritems():
        my_dict[key0] = {}
        my_dict[key0][name] = {}
        for key1, value1 in value0.iteritems():
            #         print key,key1,value1
            my_dict[key0][name][key1] = value1
        #     print my_dict
    return my_dict


def merge(a, b, path=None):
    """
    this function merges 2 nested dicts and return the merged one

    :param a:
    :param b:
    :param path:
    :return:
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def extract_yield_new(folder):
    """
    this function iterates the parsed excel files and generate test & yield info to excel files;

    :param folder:
    :return: dict of test info
    """

    dump_excel = os.path.join(folder, 'yield_all.xlsx')
    std_excel = list(filter(lambda s: s.endswith('std.gz.xlsx'), os.listdir(folder)))
    std_excel_path = list(map(lambda s: os.path.join(folder, s), std_excel))
    list_dict = list(map(lambda s: get_dict(s), std_excel_path))
    new_dict = reduce(merge, list_dict)
    df = pd.DataFrame.from_dict(new_dict).transpose()
    df = df.replace(np.nan, {column: {} for column in df.columns})
    dfs = [pd.DataFrame([x for x in df[col]], index=df.index) for col in df.columns]
    df1 = pd.concat(dfs, axis=1, keys=df.columns)
    df1.columns.names = ['test', 'info']
    df1.index.names = ['soft_bin']

    ft_r0_keys = filter(lambda (s1, s2): 'FT_R' not in s1 and 'QA' not in s1, df1.keys())
    ft_total = df1[ft_r0_keys].sum(level='info', axis=1)['total'].sum()
    non_qa_keys = filter(lambda (s1, s2): 'QA' not in s1, df1.keys())
    ft_pass = df1[non_qa_keys].sum(level='info', axis=1)['total'][1]

    summary = {}
    summary['Device Name'] = folder.split('\\')[-1].split('_')[0]
    summary['Lot Nbr'] = folder.split('\\')[-1].split('_')[1]
    summary['MES Lot ID'] = folder.split('\\')[-1].split('_')[2]

    summary['ft_total'] = ft_total
    summary['ft_pass'] = ft_pass
    summary['ft_yield'] = '{0:.2%}'.format(ft_pass / ft_total)

    summ = pd.DataFrame(summary.items(), columns=['info', 'data']).transpose()
    with pd.ExcelWriter(dump_excel) as writer:
        df1.to_excel(writer, sheet_name='yield', startrow=4, startcol=0)
        summ.to_excel(writer, sheet_name='yield', startrow=0, startcol=0)
    return summary


def single(process_file):
    """
    this function is an instance of class TT to initiate parse of a single std.gz file;
    :param process_file:
    :return:
    """
    if os.path.exists(process_file + ".xlsx") == 1:
        return 1
    # cmd = 'c:\\anaconda2\python.exe CORE/test.py ' + file
    # os.system(cmd)
    # dummy comment, to test hg auth settings
    log = logging.getLogger('test')
    lvl = logging.INFO
    logging.basicConfig(level=lvl)
    x = TT()
    x.Rec_Set = []  #
    x.Rec_Nset = []
    try:
        x.parse(process_file)
    except KeyError:
        print (process_file, 'failed crc check')


class Scheduler:
    """

    this is a class to load parameters from cmd line arguments with argparse
    self.digest:
        this function scans the folder and gets the lists of files to be processed
    self.launch:
        this function actually starts the test

    """

    def __init__(self, conf):
        # pdb.set_trace()
        self._argument = conf
        self.stdf_list = []
        self.digest()
        print ('processing folder', self._argument.source)

    def digest(self):
        file_list = list(map(lambda s: os.path.join(self._argument.source, s), os.listdir(self._argument.source)))
        self.stdf_list = list(filter(lambda s: s.endswith('std.gz') or s.endswith('std'), file_list))

    def launch(self):

        pool = ThreadPool(multiprocessing.cpu_count(), set_affinity_on_worker())
        pool.map(single, self.stdf_list)
        pool.close()
        extract_yield_new(self._argument.source)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Modularized Anlaysis Pipelining System, Anlaysis Made Simple yet Powerful.')
    parser.add_argument("-i", "--source", dest="source", default='', help="path to source data")  # metavar="FILE")
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

    # parser.add_argument("-e", "--file-type", dest="file_type", default='',help="file type (extension) filter")


    # schedule = Scheduler(dict([ tuple(x.rstrip(' ').split(' ')) if len(x.rstrip(' ').split(' '))>1 else tuple(x.rstrip(' ').split(' ')+['']) for x in re.split('-*',' '.join(sys.argv))[1:] ]))
    Scheduler(parser.parse_args()).launch()

    sys.exit(0)
