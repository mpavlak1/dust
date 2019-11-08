#dust/src/extract/formreader.py

# Built-ins
import os

# Package
import __init__
from dust.src.utils.io import slurp
from dust.src.utils.filepaths import rem_filetype, as_filetype
from dust.src.extract.boxparse import split_bybox, remove_nonchar_noise
from dust.src.extract.tesseract import tesseractOCRsingle
from dust.src.extract.ghostscript import pdf_toimgs

def __read_formatfile__(filename, delim='\t', reformat=True):
    x = dict(map(lambda x: [x[0], eval(x[1])],
                 map(lambda x: x.strip().split(delim), slurp(filename))))
    if(reformat):
        #Format give as [x0, y0, x1, y1] needs to be refomatted to [x0, y0, x1-x0, y1-y0]
        #Box can be described as either top-left bottom-right corners or top-left with width and height
        for key in x.keys():
            x[key][2] -= x[key][0]
            x[key][3] -= x[key][1]
    return x


class FormExtractor():

    def __init__(self, templatefile, filename, threshold=0.75):
        self.templatefile = templatefile
        self.filename = filename
        self.__simthresh__ = threshold
        self.__dumpdir__ = os.path.join(rem_filetype(self.filename), '_img-dump')

    def __enter__(self):
        pdf_toimgs(self.filename)
        return self


class FormReader():

    def __init__(self, templatefile, filename, boxmap, extract_path = None, extact_filename = None, pdf_page = None, noisefilter_fn = None):
        self.templatefile = templatefile
        self.filename = filename
        self.data = {}

        self.__boxmap__ = boxmap
        self.__extract_path__ = extract_path
        self.__formextract_files__ = {}
        self.__noisefilter_fn__ = noisefilter_fn or remove_nonchar_noise
        
    def __splitfields__(self):
        split_bybox(self.filename, self.__extract_path__, boxs=self.__boxmap__.values(),
                    reference_imgfile = self.templatefile, noisefilter_fn = self.__noisefilter_fn__)

        box_legend = __read_formatfile__(os.path.join(self.__extract_path__, 'box_legend.txt'), reformat=False)
        for key in box_legend:
            self.__formextract_files__[tuple(box_legend[key])] = {'imgfile': key}
        for key in self.__boxmap__: 
            try:
                self.__formextract_files__[tuple(self.__boxmap__[key])]['var'] = key
            except KeyError:
                print([key])
                raise
                #If box for image but not in boxmap, error
                #Somehow there is an extra image file being parsed that was not defined explicitly

        self.__formextract_files__ = dict(map(lambda x: [x['var'],x['imgfile']],
                                          self.__formextract_files__.values()))

    def __parse_var__(self, imgfile):
        tesseractOCRsingle(imgfile, rem_filetype(imgfile), psm=11)
        return '\n'.join(slurp(as_filetype(imgfile, '.txt'))[:-1]).strip()

    def __ocrimgs__(self):
        for key in self.__formextract_files__:
            self.data[key] = self.__parse_var__(self.__formextract_files__[key])

    def __enter__(self):
        self.__splitfields__()
        self.__ocrimgs__()
        return self

    def __exit__(self, *args):
        self.__tofile__()
        self.__clean__()

    def __tofile__(self):
        pass

    def __clean__(self):
        '''Remove itermediary files'''
        for file in os.listdir(self.__extract_path__):
            try: os.remove(os.path.join(self.__extract_path__, file))
            except FileNotFoundError: pass
        os.rmdir(self.__extract_path__)




