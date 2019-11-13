#/dust/src/utils/lookup.py

# Pacakage
import __init__

def mask(bits):         return ~-(1<<bits)
def zerobit(mask, x):   return mask^(1<<x)
def zerobits(mask, xs): return mask^sum(map(__shift__, xs))
def shield(num):        return 1<<(~-num)
def __shift__(x):       return 1<<x

class BinaryLookupTable():

    def __init__(self, truthtable = None, default = False):
        self.count = 0
        self.__mn__ = 0

        if(truthtable):
            assert all(map(lambda x: isinstance(x, int), truthtable.keys()))
            size = max(truthtable)

            self.__mn__ = zerobits(mask(size+1), filter(lambda x: not truthtable.get(x, not default),
                                                      truthtable.keys()))
            self.count = size            

    def set(self, index, boolean = True):
        self.__mn__ = self.__mn__&zerobit(mask(self.count), index) | 1<<(index*int(boolean))
        self.count = self.count + max(0, index-self.count)

    def get(self, index):
        return (self.__mn__&shield(-~index))>>index

    def __len__(self): return -~self.count
##    def __repr__(self): return hex(self.__mn__)


##def benchmark(niter = 10):    
##    tt = dict(zip(range(10), map(lambda x: x%2==0, range(10))))
##    b = BinaryLookupTable(tt)
##    z = dict(zip(range(1000000), map(lambda x: x%2==0, range(1000000))))
##
##    import time
##    from numpy import random
##    rands = [random.randint(1, 1000000) for _ in range(10000000)]
##
##    def test0(tbl):
##        start = time.time()
##
##        for r in rands:
##            tbl.get(r)
##        
##        end = time.time()
##        #print('Total time elapsed: {} (seconds)'.format(end-start))
##        return end-start
##        
##    print('Test for Binary Lookup Table\n')
##
##    tt_runs = [test0(tt) for _ in range(niter)]
##
##    print('Average time elapsed: {} (seconds)'.format(sum(tt_runs)/niter))
##    print('Minmim run time: {} (seconds)'.format(min(tt_runs)))
##    print('Maximum run time: {} (seconds)'.format(max(tt_runs)))
##
##    print('\nTest for built-in dictionary\n')
##
##    z_runs = [test0(z) for _ in range(niter)]
##    print('Average time elapsed: {} (seconds)'.format(sum(z_runs)/niter))
##    print('Minmim run time: {} (seconds)'.format(min(z_runs)))
##    print('Maximum run time: {} (seconds)\n'.format(max(z_runs)))
##
##
##    print('Average differential: {}'.format( sum(z_runs)/niter - sum(tt_runs)/niter))
##    print('Minimum differential: {}'.format(min(z_runs)-max(tt_runs)))
##    print('Maximum differential: {}'.format(max(z_runs)-min(tt_runs)))

