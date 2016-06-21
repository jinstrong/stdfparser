import sys
import logging
import os
import sys
from pandas import DataFrame, ExcelWriter, concat
import pandas as pd


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from stdf_parser import Parser


class TT(Parser):
    """
    this is an inherited instance which overwrites some functions in original parse class:

    self.take:
        this function takes the parsed data and save all info to nested dicts;
    self.dump:
        this function further processed the dicts, transform to DataFrames, and dump files to excels;

    """

    def take(self, typsub):
        if 'Sdr' in str(self.Rec_Dict[typsub]):
            for i in self.data['SITE_NUM']:
                self.Active_site.append(i)
                self.PFTR_dict[i] = {}

            self.Head = self.data['HEAD_NUM']
            for i, j in self.Rec_Dict[typsub].fieldMap:
                self.test_info['info'][str(self.Rec_Dict[typsub]) + ':' + i] = str(self.data[i])

        elif 'Pmr' in str(self.Rec_Dict[typsub]):

            self.PMR_nd[self.data['PMR_INDX']] = {}
            for i, j in self.Rec_Dict[typsub].fieldMap:
                self.PMR_nd[self.data['PMR_INDX']][i] = str(self.data[i])
        elif 'Ptr' in str(self.Rec_Dict[typsub]):
            if self.data['SITE_NUM'] not in self.PFTR_dict.keys():
                self.PFTR_dict[self.data['SITE_NUM']] = {}
                print ('Site: ', self.data['SITE_NUM'], ' is not originally an active site', self.File_Name)
            self.PFTR_dict[self.data['SITE_NUM']][
                str(self.data['TEST_NUM']).zfill(3) + ':' + self.data['TEST_TXT']] = float(self.data['RESULT'])
            if self.spec_sum_set == 0:
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3) + ':' + self.data['TEST_TXT']] = {}
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3) + ':' + self.data['TEST_TXT']]['LO_LIMIT'] = \
                    self.data['LO_LIMIT']
                self.spec_summ[str(self.data['TEST_NUM']).zfill(3) + ':' + self.data['TEST_TXT']]['HI_LIMIT'] = \
                    self.data['HI_LIMIT']

        elif 'Ftr' in str(self.Rec_Dict[typsub]):
            self.PFTR_dict[self.data['SITE_NUM']][
                str(self.data['TEST_NUM']).zfill(3) + ':' + self.data['TEST_TXT']] = float(
                int(self.data['TEST_FLG'], 16))

        elif 'Prr' in str(self.Rec_Dict[typsub]):
            self.spec_sum_set = 1
            self.PFTR_nd[int(self.data['PART_ID'], 10)] = self.PFTR_dict[self.data['SITE_NUM']]

            self.PFTR_nd[int(self.data['PART_ID'], 10)]['000:HARD_BIN'] = self.data['HARD_BIN']
            self.PFTR_nd[int(self.data['PART_ID'], 10)]['000:SOFT_BIN'] = self.data['SOFT_BIN']
            self.PFTR_nd[int(self.data['PART_ID'], 10)]['000:SITE_NUM'] = self.data['SITE_NUM']
            self.PFTR_nd[int(self.data['PART_ID'], 10)]['000:TEST_T'] = self.data['TEST_T']
            self.PFTR_dict[self.data['SITE_NUM']] = {}
        else:
            for i, j in self.Rec_Dict[typsub].fieldMap:
                self.test_info['info'][str(self.Rec_Dict[typsub]) + ':' + i] = str(self.data[i])

    def dump(self):
        chip_id_full = '999:chip_id_full'
        data = DataFrame(self.PFTR_nd).transpose()
        keys = data.keys()
        key_hard_bin = ''.join(filter(lambda s: 'HARD_BIN' in s, keys))
        key_site_num = ''.join(filter(lambda s: 'SITE_NUM' in s, keys))
        key_soft_bin = ''.join(filter(lambda s: 'SOFT_BIN' in s, keys))
        key_efuse_burned = ''.join(filter(lambda s: 'efuse_burned' in s, keys))
        key_chip_id_part0 = ''.join(filter(lambda s: 'chip_id_part0' in s, keys))
        key_chip_id_part1 = ''.join(filter(lambda s: 'chip_id_part1' in s, keys))

        for i in data[key_soft_bin].unique():
            self.test_yield[i] = {}
            # basename = os.path.basename(self.Path_name)
            # name_front = basename.find('_') + 1
            # name_end = basename.find('---') - 12
            # name = basename[name_front:name_end]
            # self.test_yield[i][name] = {}
            # for j in data[key_site_num].unique():
            #     self.test_yield[i][name][j] = data[(data[key_site_num] == j) & (data[key_soft_bin] == i)][
            #         key_hard_bin].count()
            #     self.test_yield[i][name]['total'] = data[(data[key_soft_bin] == i)][key_hard_bin].count()
            #     self.test_yield[i][name]['yield'] = '{0:.2%}'.format(
            #         self.test_yield[i][name]['total'] / float(data[key_hard_bin].count()))
            # df_1 = DataFrame(self.test_yield).transpose()
            # dfs = [pd.DataFrame([x for x in df_1[col]], index=df_1.index) for col in df_1.columns]
            # df2 = pd.concat(dfs, axis=1, keys=df_1.columns)
            # df2.columns.names = ['test', 'info']
            # df2.index.names = ['soft_bin']

            for j in data[key_site_num].unique():
                self.test_yield[i][j] = data[(data[key_site_num] == j) & (data[key_soft_bin] == i)][
                    key_hard_bin].count()
                self.test_yield[i]['total'] = data[(data[key_soft_bin] == i)][key_hard_bin].count()
                self.test_yield[i]['yield'] = '{0:.2%}'.format(
                    self.test_yield[i]['total'] / float(data[key_hard_bin].count()))
        df_1 = DataFrame(self.test_yield).transpose()

        data[chip_id_full] = data[key_chip_id_part0] + data[key_chip_id_part1] * 10000000
        data_id = data[(data[key_hard_bin] == 1) & (data[key_efuse_burned] == 0)][chip_id_full]
        if data_id[data_id.duplicated() == True].count() > 0:
            raise (self.Path_name + 'is with duplicated chip id')
            with open(self.Path_name + 'duplicated.txt', w) as duplicated_txt:
                duplicated_txt.write(self.Path_name + 'is with duplicated chip id')
        with ExcelWriter(self.Path_name) as writer:
            DataFrame(self.test_info).to_excel(writer, sheet_name='Related')
            DataFrame(self.PMR_nd).transpose().to_excel(writer, sheet_name='PMR')
            DataFrame(self.PFTR_nd).transpose().to_excel(writer, sheet_name='PTR_FTR')
            DataFrame(
                data[(data[key_hard_bin] == 1) & (data[key_efuse_burned] == 0)]).describe().transpose().combine_first(
                DataFrame(self.spec_summ).transpose()).to_excel(writer, sheet_name='summary_spec')
            df_1.to_excel(writer, sheet_name='yield')

    def setup(self):
        pass

    def cleanup(self):
        pass

    def file_setup(self):
        pass

    def file_cleanup(self):
        pass


def do(file):
    # dummy comment, to test hg auth settings
    log = logging.getLogger('test')
    lvl = logging.INFO
    logging.basicConfig(level=lvl)
    x = TT()
    x.Rec_Set = []  #
    x.Rec_Nset = []

    x.parse(file)


def main():
    # file = sys.argv[1]
    file = 'D:\ESP8266EX-XM_P4BX24.00#E_ESP1551023DE000\ESP-ESP1551023DE000_FT-P4BX24.00#E---ESP8266EX-XM-10515-UTTC504-20160219232627.std.gz'
    do(file)


if __name__ == '__main__':
    main()
