import sys
import logging
import struct
import os
from pandas import Series, DataFrame, ExcelWriter
import pandas as pd
import datetime
from CORE.stdfparser import parser

class tt(parser): 
    
    def take(self, typsub):
        self.log.info('===========  start of Record %s =======' % str(self.Rec_Dict[typsub]))
        if 'Sdr' in str(self.Rec_Dict[typsub]):
            for i in self.data['SITE_NUM']:
                self.Active_site.append(i)
                self.PTR_dict[i]={}
                self.FTR_dict[i]={}
            self.Head=self.data['HEAD_NUM']            
            
        elif 'Pmr' in str(self.Rec_Dict[typsub]):
            
            type=["Pin Index","Channel Type","Channel Name","Physical Pin Name","Logical Pin Name","Head Num","Site Num"]
            
            self.PMR_nd[self.data['PMR_INDX']]={}
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.PMR_nd[self.data['PMR_INDX']][i]=str(self.data[i])
        elif 'Ptr' in str(self.Rec_Dict[typsub]):
            self.PTR_dict[self.data['SITE_NUM']][str(self.data['TEST_NUM'])+':'+self.data['TEST_TXT']]=self.data['RESULT']
            
            #if self.data['TEST_NUM']==1 and self.data['HEAD_NUM']==self.Head and self.data['SITE_NUM']==self.Active_site[0]:
                #self.Part_num+=1 
                #for i in self.Active_site:
                    #self.PTR_nd[(self.Part_num,i)]={}
            #self.PTR_nd[(self.Part_num,self.data['SITE_NUM'])][str(self.data['TEST_NUM'])+':'+self.data['TEST_TXT']]=self.data['RESULT']
        elif 'Ftr' in str(self.Rec_Dict[typsub]):
            self.FTR_dict[self.data['SITE_NUM']][str(self.data['TEST_NUM'])+':'+self.data['TEST_TXT']]=self.data['TEST_FLG']
            #for i in self.Active_site:
                #self.FTR_nd[(self.Part_num,i)]={}
            #self.FTR_nd[(self.Part_num,self.data['SITE_NUM'])][str(self.data['TEST_NUM'])+':'+self.data['TEST_TXT']]=self.data['TEST_FLG']        
        elif 'Prr' in str(self.Rec_Dict[typsub]):
            self.PTR_nd[int(self.data['PART_ID'],10)]=self.PTR_dict[self.data['SITE_NUM']]
            self.FTR_nd[int(self.data['PART_ID'],10)]=self.FTR_dict[self.data['SITE_NUM']]
            
            self.PTR_nd[int(self.data['PART_ID'],10)]['HARD_BIN']=self.data['HARD_BIN']
            self.PTR_nd[int(self.data['PART_ID'],10)]['SOFT_BIN']=self.data['SOFT_BIN']
            self.PTR_dict[self.data['SITE_NUM']]={}

            self.FTR_nd[int(self.data['PART_ID'],10)]['HARD_BIN']=self.data['HARD_BIN']
            self.FTR_nd[int(self.data['PART_ID'],10)]['SOFT_BIN']=self.data['SOFT_BIN']
            self.FTR_dict[self.data['SITE_NUM']]={}
                        
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
            DataFrame(self.FTR_nd).transpose().to_excel(writer, sheet_name='FTR') 
        
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
    do('D:\Test_results_validating\CB\CB-0412\ESP-CB#7_fail_io_verify-0---PICCOLO-0-uttc505-20160411213329.std.gz')
    # pool = ThreadPool(multiprocessing.cpu_count())
    # pool.map(do,stdf_list)
    # pool.close()

    # file='D:\ESP-ESP1551021CP000_QA_R1-P4BX26.00#C---PICCOLO-73592-UTTC504-20160121215001.std'
    # do(file)

if __name__ == '__main__':
    start=datetime.datetime.now()
    print 'Starting time:',start
    main()
    print 'Job Done!'
    end=datetime.datetime.now()
    print 'Endting time:',end
    print 'Time taken: ',end-start
