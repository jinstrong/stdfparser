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
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.test_info['info'][str(self.Rec_Dict[typsub])+':'+i]=str(self.data[i])

        elif 'Pmr' in str(self.Rec_Dict[typsub]):

            type=["Pin Index","Channel Type","Channel Name","Physical Pin Name","Logical Pin Name","Head Num","Site Num"]

            self.PMR_nd[self.data['PMR_INDX']]={}
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.PMR_nd[self.data['PMR_INDX']][i]=str(self.data[i])
        elif 'Ptr' in str(self.Rec_Dict[typsub]):
            if self.data['SITE_NUM'] not in self.PFTR_dict.keys():
                self.PFTR_dict[self.data['SITE_NUM']]={}
                print 'Site: ',self.data['SITE_NUM'],' is not originally an active site',self.File_Name
            self.PFTR_dict[self.data['SITE_NUM']][str(self.data['TEST_NUM']).zfill(3)+':'+self.data['TEST_TXT']]=float(self.data['RESULT'])
            if self.spec_sum_set==0:
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3)+':'+self.data['TEST_TXT']]={}
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3)+':'+self.data['TEST_TXT']]['LO_LIMIT']=self.data['LO_LIMIT']
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3)+':'+self.data['TEST_TXT']]['HI_LIMIT']=self.data['HI_LIMIT']

        elif 'Ftr' in str(self.Rec_Dict[typsub]):
            self.PFTR_dict[self.data['SITE_NUM']][str(self.data['TEST_NUM']).zfill(3)+':'+self.data['TEST_TXT']]=float(int(self.data['TEST_FLG'],16))

        elif 'Prr' in str(self.Rec_Dict[typsub]):
            self.spec_sum_set=1
            self.PFTR_nd[int(self.data['PART_ID'],10)]=self.PFTR_dict[self.data['SITE_NUM']]

            self.PFTR_nd[int(self.data['PART_ID'],10)][('000:HARD_BIN')]=self.data['HARD_BIN']
            self.PFTR_nd[int(self.data['PART_ID'],10)][('000:SOFT_BIN')]=self.data['SOFT_BIN']
            self.PFTR_nd[int(self.data['PART_ID'],10)][('000:SITE_NUM')]=self.data['SITE_NUM']
            self.PFTR_nd[int(self.data['PART_ID'],10)][('000:TEST_T')]=self.data['TEST_T']
            self.PFTR_dict[self.data['SITE_NUM']]={}
        else:
            for i,j in self.Rec_Dict[typsub].fieldMap:
                self.test_info['info'][str(self.Rec_Dict[typsub])+':'+i]=str(self.data[i])

    def dump(self):
        chip_id_full = '999:chip_id_full'
        data = DataFrame(self.PFTR_nd).transpose()
        key_HARD_BIN = ''.join(filter(lambda s: 'HARD_BIN' in s, data.keys()))
        key_efuse_burned = ''.join(filter(lambda s: 'efuse_burned' in s, data.keys()))
        key_chip_id_part0 = ''.join(filter(lambda s: 'chip_id_part0' in s, data.keys()))
        key_chip_id_part1 = ''.join(filter(lambda s: 'chip_id_part1' in s, data.keys()))

        if key_chip_id_part0 is not '':
            data[chip_id_full] = data[key_chip_id_part0] + data[key_chip_id_part1] * 10000000
            data_id = data[(data[key_HARD_BIN] == 1) & (data[key_efuse_burned] == 0)][chip_id_full]
            if data_id[data_id.duplicated() == True].count() > 0:
                print self.Path_name + 'is with duplicated chip id'
                with open(self.Path_name + 'duplicated.txt', w) as duplicated_txt:
                    duplicated_txt.write(self.Path_name + 'is with duplicated chip id')
        with ExcelWriter(self.Path_name) as writer:
            DataFrame(self.test_info).to_excel(writer, sheet_name='Related')
            DataFrame(self.PMR_nd).transpose().to_excel(writer, sheet_name='PMR')
            DataFrame(self.PFTR_nd).transpose().to_excel(writer, sheet_name='PTR_FTR')
            if key_efuse_burned is not '':

                DataFrame(data[(data[key_HARD_BIN] == 1) & (data[key_efuse_burned] == 0)]).describe().transpose().combine_first(
                    DataFrame(self.spec_summ).transpose()).to_excel(writer, sheet_name='summary_spec')
            else:
                DataFrame(data[(data[key_HARD_BIN] == 1)]).describe().transpose().combine_first(
                    DataFrame(self.spec_summ).transpose()).to_excel(writer, sheet_name='summary_spec')
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
    file = 'D:\Test_results_validating\CB\CB-0412\ESP-CB#7_fail_io_verify-0---PICCOLO-0-uttc505-20160411213329.std.gz'

    do(file)

if __name__ == '__main__':
    main()
