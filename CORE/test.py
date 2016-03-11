import sys
import logging
import struct
import os
import datetime
from stdfparser import parser
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from pandas import Series, DataFrame, ExcelWriter
import datetime


class tt(parser):

    def take(self, typsub):
        if 'Sdr' in str(self.Rec_Dict[typsub]):
            for i in self.data['SITE_NUM']:
                self.Active_site.append(i)
                self.PFTR_dict[i]={}
               
            self.Head=self.data['HEAD_NUM']            
            
        elif 'Pmr' in str(self.Rec_Dict[typsub]):
            
            type=["Pin Index","Channel Type","Channel Name","Physical Pin Name","Logical Pin Name","Head Num","Site Num"]
            
            self.PMR_nd[self.data['PMR_INDX']]={}
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.PMR_nd[self.data['PMR_INDX']][i]=str(self.data[i])
        elif 'Ptr' in str(self.Rec_Dict[typsub]):
            self.PFTR_dict[self.data['SITE_NUM']][(self.data['TEST_NUM'],self.data['TEST_TXT'])]=self.data['RESULT']
            
        elif 'Ftr' in str(self.Rec_Dict[typsub]):
            self.PFTR_dict[self.data['SITE_NUM']][(self.data['TEST_NUM'],self.data['TEST_TXT'])]=self.data['TEST_FLG']
    
        elif 'Prr' in str(self.Rec_Dict[typsub]):
            self.PFTR_nd[int(self.data['PART_ID'],10)]=self.PFTR_dict[self.data['SITE_NUM']]
            
            self.PFTR_nd[int(self.data['PART_ID'],10)][(0,'HARD_BIN')]=self.data['HARD_BIN']
            self.PFTR_nd[int(self.data['PART_ID'],10)][(0,'SOFT_BIN')]=self.data['SOFT_BIN']
            self.PFTR_nd[int(self.data['PART_ID'],10)][(0,'SITE_NUM')]=self.data['SITE_NUM']
            self.PFTR_nd[int(self.data['PART_ID'],10)][(0,'TEST_T')]=self.data['TEST_T']
            self.PFTR_dict[self.data['SITE_NUM']]={}
                        
    def dump(self): 
        with ExcelWriter(self.Path_name[:-4]+'.xlsx') as writer:
            DataFrame(self.PMR_nd).transpose().to_excel(writer, sheet_name='PMR')
            DataFrame(self.PFTR_nd).transpose().to_excel(writer, sheet_name='PTR_NTR')
            # DataFrame(self.FTR_nd).transpose().to_excel(writer, sheet_name='FTR') 
        
    def setup(self): pass

    def cleanup(self): pass

    def file_setup(self): pass

    def file_cleanup(self): pass

def do(file):
    # dummy comment, to test hg auth settings
    log = logging.getLogger('test')
    lvl = logging.INFO
    logging.basicConfig(level=lvl)
    x = tt()
    x.Rec_Set = [] #
    x.Rec_Nset = []
  

    x.parse(file)

def main():
    file=sys.argv[1]
    print 'processing ongoing:',file
    do(file)
    print 'processing done:',file

if __name__ == '__main__':
    main()
