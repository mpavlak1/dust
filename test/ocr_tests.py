# /dust/test/ocr_test.py

### Test module for entire pipeline from raw imgfile to text output document

## Built-ins
import os
import re
import unittest

## Package
import __init__
from dust.src.extract.boxparse import split_bybox, remove_nonchar_noise
from dust.src.extract.formreader import __read_formatfile__, FormReader
from dust.src.extract.images import monochrome
from dust.src.extract.tesseract import tesseractOCRsingle
from dust.src.extract.ghostscript import pdf_toimgs
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
                   'In file {}\nExpected: \'123 45 6789\', found {}'.format(sampfile, text.replace('-',' '))


class TestW2FormReader(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestW2FormReader, self).__init__(*args, **kwargs)

        self.w2dir = os.path.abspath('./test_files/w2_forms')
        self.ref2019 = os.path.join(self.w2dir, 'w2_reference_2019.png')
        self.sam2009_001 = os.path.join(self.w2dir, 'w2_sample_2019_001.png')
        
        self.dump = os.path.join(self.w2dir,'dump')
        os.makedirs(self.dump, exist_ok=True)
        self.clean_dumpdir()

        self.w2boxes = __read_formatfile__(os.path.join(self.w2dir, 'w2_format.txt'))

    def test_one(self):
        return True
        assert 1 == 0
        raise Exception('BREAK')
        
    def test_readform(self):

        self.clean_dumpdir()
        fr = FormReader(self.ref2019, self.sam2009_001, self.w2boxes, extract_path = self.dump)
        fr.__enter__()

        expected = {'SSN': '555-12-3456', 'EIN': '12-9876543', 'employee_address_line':
                    'Widgets and Things Inc.\n\n\n\n123 Fake Street\n\n\n\nFakecity, MS 54321',
                    'control_number': 'Z9Y8',
                    'first_name': 'Jane A.', 'last_name': 'Doe', 'suffix': 'Jr',
                    'employeer_address_line': '123 Main Street\n\n\n\nSometowne, MS 54321',
                    'wages': '56,789.12', 'federal_income_tax_withheld': '4,321.98',
                    'social_security_wages': '60,000.00', 'social_security_tax_withheld': '3,120',
                    'medicare_wages': '60,000.00', 'medicare_tax_withheld': '789.45',
                    'social_security_tips': '', 'allocated_tips': '',
                    'dependent_care_benefits': '', 'nonqualified_plans': ''}

        for key in expected.keys():
            assert key in fr.data
            assert fr.data[key] == expected[key], \
                   'For var: {}, Expected: {}, Found: {}'.format(key, expected[key], fr.data[key])
            
    def clean_dumpdir(self):
        for file in os.listdir(self.dump):
            os.remove(os.path.join(self.dump, file))

unittest.main()
##suite = unittest.TestSuite()
##suite.addTest(TestW2FormReader("test_one"))
##runner = unittest.TextTestRunner()
##runner.run(suite)


