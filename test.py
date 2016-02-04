import sys
import logging
import struct
import os
from multiprocessing.dummy import Pool as ThreadPool

from stdfparser import parser

file_name=''
file_dump=['' for i in xrange(10000000)]
line_num=0

class tt(parser):

    def take(self, typsub):


        self.strr[self.lin_num]='Star of Record: '+str(self.Rec_Dict[typsub])
        self.lin_num+=1
        for i,j in self.Rec_Dict[typsub].fieldMap:

            self.strr[self.lin_num]=str(self.Rec_Dict[typsub])+' '+str(i)+' '+str(self.data[i])
       
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
    do(sys.argv[1])
    # print sys.argv[1:]
    # for file in sys.argv[1:]:
    #     print file
    # pool = ThreadPool(1)
    # pool.map(do,sys.argv[1:])
    # pool.close()

if __name__ == '__main__':
    main()
    print 'Job Done!'
