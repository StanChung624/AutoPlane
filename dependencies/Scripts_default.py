# -----------------------------------------------------------------------------#
# default scripts __init__ and luancher
# -----------------------------------------------------------------------------#
from .TimeControl import TimeControl
from time import time
import json
class Scripts_default:

    def __init__(self):
        self.INFO = None
        pass

    def run(self, INFO:dict={}, start_when=False):
        if self.INFO is not None:
            INFO = self.INFO
        self.luancher(INFO, start_when)

    def luancher(self, INFO, start_when):
        # INFO checked
        self.INFO = INFO
        self.check_data()

        # wait until given start_when
        if start_when:
            TimeControl.start_when(start_when)

        # timer - start
        tic = time()
        self.start()        
        elapse = time() - tic
        print("elapse time: ", elapse, ' (sec.)')

    def dump_required_info(self):
        with open('REQUIRED_INFO.txt', mode='w', encoding='big5') as f:
            json.dump(self.REQUIRED_INFO,f,ensure_ascii=False)

    def read_info(self):
        with open('REQUIRED_INFO.txt', mode='r', encoding='big5') as f:
            self.INFO = json.load(f)
        
        for key in self.INFO:
            print(key,'\t',self.INFO[key])
