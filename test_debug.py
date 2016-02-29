import sys
import logging
import struct
import os


from stdfparser import parser

class tt(parser):

    def take(self, typsub):


        #self.strr[self.lin_num]='Star of Record: '+str(self.Rec_Dict[typsub])
        #self.lin_num+=1
        for i,j in self.Rec_Dict[typsub].fieldMap:

            #self.strr[self.lin_num]=str(self.Rec_Dict[typsub])+' '+str(i)+' '+str(self.data[i])
            #self.lin_num+=1

            b=2
    def dump(self):
        with open(self.Path_name, 'w') as result:
            for i in range(0, self.lin_num + 1):
                a = str(self.strr[i])
                result.write(a + '\n')
        print "STDF Extract finish:",self.Path_name


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
