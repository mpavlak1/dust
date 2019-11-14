#/dust/src/utils/lookup.py

# Built-ins
from math import log2, ceil

# Pacakage
import __init__

### BinaryLookupTable and LookupTable are lighter weight look ups compared to the default
### python dictionary or other hashmap implementations
### There is a speed up 4x when using BinaryLookupTable over the python dictionary class
### The Generic LookupTable is slower at a factor between 4x to 9x, constant as N increases

### Primary purpose of the lookup tables is to reduce space complexity (with time improvement in
### the case of BinaryLookupTable and marginal slowdown in case of Generic Lookup Tables)
### with a pure python implementation with retaining most of the time complexity benifits of
### an hash-map. Both tables only support integers as key index and value result; to expand
### the lookup, a wrapper can be added around the table to store constants once rather than
### each appearance in the table.

### The BinaryTable can store only 2 potential results (True/False) while the Generic Lookup Table
### can store any arbitarty size of enumeration length -- however, the enumeration size will be
### expanded up to the nearest exponent of 2 to avoid costly multiplication of arbitrary size
### i.e: An enumeration set of 14 values will take up 16 bits (4 words) and have 2 unused bits
###      in each table entry.

def mask(bits):         return ~-(1<<bits)
def zerobit(mask, x):   return mask^(1<<x)
def zerobits(mask, xs): return mask^sum(map(__shift__, xs))
def shield(num):        return 1<<(~-num)
def __shift__(x):       return 1<<x

def zmask1 (bits, idx) : return (~-(1<<bits))^(0x1<<(idx))
def zmask2 (bits, idx) : return (~-(1<<bits))^(0x3<<(idx<<1))
def zmask4 (bits, idx) : return (~-(1<<bits))^(0xf<<(idx<<2))
def zmask8 (bits, idx) : return (~-(1<<bits))^(0xff<<(idx<<3))
def zmask16(bits, idx) : return (~-(1<<bits))^(0xffff<<(idx<<4))
def zmask32(bits, idx) : return (~-(1<<bits))^(0xffffffff<<(idx<<5))
def zmask64(bits, idx) : return (~-(1<<bits))^(0xffffffffffffffff<<(idx<<6))
def zmaski (bits,idx,i): return (~-(1<<bits))^((~-(1<<i))<<(idx<<(~-int(i).bit_length())))

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

class LookupTable():

    def __init__(self, enumsize):
        
        self.count = 0
        self.__mn__ = 0

        #enum size = number of unique elements to store
        # -> number of bits needed to store N enums objects = ceil(log2(N))
        self.valsize = ceil(log2(enumsize))
      
        msk = ~-(1<<self.valsize)
        shft = (~-int(self.valsize).bit_length())

        def zmask(bits, idx):
            try:
                return (~-(1<<bits))^(msk<<(idx<<shft))
            except ValueError:
                if(idx == 0): return 0
                else: raise
        self.zmask = zmask
        self.shft = shft

    def set(self, index, value):
        _d = max(0,index-self.count)
        self.count += (~-_d)
        bitcount = self.count << self.shft

        self.__mn__ = self.__mn__ & self.zmask(bitcount, index)
        
        try:
            self.__mn__ = self.__mn__ | value << ((~-index)<<self.shft)
        except ValueError:
            if(index == 0):
                self.__mn__ = self.__mn__ | value << 0
            else: raise
        self.count = -~self.count

    def get(self,index):
        try:
            return ~-(1<<self.valsize) & self.__mn__>>(~-index<<self.shft)
        except ValueError:
            if(index == 0):
                return ~-(1<<self.valsize) & (self.__mn__ << self.valsize)
            raise

