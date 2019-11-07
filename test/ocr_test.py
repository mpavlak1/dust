# /dust/test/ocr_test.py

### Test module for entire pipeline from raw imgfile to text output document

## Built-ins
import os
import re
import unittest

## Package
import __init__
from dust.src.extract.boxparse import split_bybox, remove_nonchar_noise
from dust.src.extract.images import monochrome
from dust.src.extract.tesseract import tesseractOCRsingle
from dust.src.utils.io import slurp

## Additional Packages
import cv2

class TestW2Extract(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestW2Extract, self).__init__(*args, **kwargs)


        self.w2dir = os.path.abspath('./test_files/w2_forms')

        self.ref2019 = os.path.join(self.w2dir, 'w2_reference_2019.png')
        self.sam2019 = os.path.join(self.w2dir, 'w2_sample_2019.png')
        self.sam2017 = os.path.join(self.w2dir, 'w2_sample_2017.png')

        self.dump = os.path.join(self.w2dir,'dump')
        os.makedirs(self.dump, exist_ok=True)

        self.clean_dumpdir()

        self.w2_einbox = (646, 192, 526, 52)

        self.sampfiles = [self.sam2019, self.sam2017]

    def clean_dumpdir(self):
        for file in os.listdir(self.dump):
            os.remove(os.path.join(self.dump, file))


    def test_fullpipeline(self):

        for sampfile in self.sampfiles:

            self.clean_dumpdir()
            split_bybox(sampfile, self.dump, boxs=[self.w2_einbox],
                        reference_imgfile=self.ref2019)
            
            imgfile = os.path.join(self.dump, '0.png')

            assert os.path.exists(imgfile)
            img_arr = cv2.imread(imgfile,0)
            img_arr = remove_nonchar_noise(img_arr)
            
            cv2.imwrite(imgfile, img_arr)
            text_out = os.path.join(self.dump, 'text')
            tesseractOCRsingle(imgfile, text_out, psm=11)
            text_out+='.txt'

            assert os.path.exists(text_out)

            text = slurp(text_out)[0].strip()
        
            assert text.replace('-',' ') == '123 45 6789', \
                   'In file {}\nExpected: \'123 45 6789\', found {}'.format(sampfile, text.replace('-',''))


class TestOcrMethods(unittest.TestCase):
    pass


unittest.main()

