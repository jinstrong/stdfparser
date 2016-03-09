import sys
import logging
import struct
import os
from pandas import Series, DataFrame, ExcelWriter
import pandas as pd

from stdfparser import parser

class tt(parser): 

    def take(self, typsub):
        if 'Sdr' in str(self.Rec_Dict[typsub]):
            for i in self.data['SITE_NUM']:
                self.Active_site.append(i)
            self.Head=self.data['HEAD_NUM']

        elif 'Pmr' in str(self.Rec_Dict[typsub]):
            self.PMR_num+=1
            type=["Pin Index","Channel Type","Channel Name","Physical Pin Name","Logical Pin Name","Head Num","Site Num"]
            
            self.PMR_nd[self.PMR_num]={}
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.PMR_nd[self.PMR_num][i]=str(self.data[i])
        elif 'Ptr' in str(self.Rec_Dict[typsub]):
            if self.data['TEST_NUM']==1 and self.data['HEAD_NUM']==self.Head and self.data['SITE_NUM']==self.Active_site[0]:
                self.PTR_num+=1 
                for i in self.Active_site:
                    self.PTR_nd[(self.PTR_num,i)]={}
            self.PTR_nd[(self.PTR_num,self.data['SITE_NUM'])][self.data['TEST_TXT']]=self.data['RESULT']
            
            #print DataFrame(self.PMR_nd)
            #print nd
            #print DataFrame(nd).keys
        #self.strr[self.lin_num]='Star of Record: '+str(self.Rec_Dict[typsub])
        #self.lin_num+=1
       

            # self.strr[self.lin_num]=str(self.Rec_Dict[typsub])+' '+str(i)+' '+str(self.data[i])
            # self.lin_num+=1
            #if 'Ptr' in str(self.Rec_Dict[typsub]):
                #b=2
    def dump(self): 
        with ExcelWriter(self.Path_name[:-4]+'.xlsx') as writer:
            DataFrame(self.PMR_nd).transpose().to_excel(writer, sheet_name='PMR')
            DataFrame(self.PTR_nd).transpose().to_excel(writer, sheet_name='PTR')    
        
        #with open(self.Path_name, 'w') as result:
            #for i in range(0, self.lin_num + 1):
                #a = str(self.strr[i])
                #result.write(a + '\n')
        #print "STDF Extract finish:",self.Path_name


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
    do('D:\PICCOLO_P4BX26.00#C_ESP1551021CP000\ESP-ESP1551021CP000_FT2-P4BX26.00#C---PICCOLO-73592-UTTC504-20160119172152.std.gz')
    # pool = ThreadPool(multiprocessing.cpu_count())
    # pool.map(do,stdf_list)
    # pool.close()

    # file='D:\ESP-ESP1551021CP000_QA_R1-P4BX26.00#C---PICCOLO-73592-UTTC504-20160121215001.std'
    # do(file)

if __name__ == '__main__':
    main()
    print 'Job Done!'
