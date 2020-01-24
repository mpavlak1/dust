#dust/src/extract/formreader.py

# Built-ins
import os

# Package
import __init__
from dust.src.utils.io            import slurp
from dust.src.utils.filepaths     import rem_filetype, as_filetype
from dust.src.extract.images      import image_similarity, __imgarr__
from dust.src.extract.boxparse    import split_bybox, remove_nonchar_noise
from dust.src.extract.tesseract   import tesseractOCRsingle
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

    def __init__(self, templatefile, filename, threshold=0.75, pages=None):
        self.templatefile = templatefile
        self.filename = filename
        self.__simthresh__ = threshold
        self.__dumpdir__ = '{}{}'.format(rem_filetype(self.filename), '_img-dump')
        self.__imgfiles__ = []
        self.__pages__ = pages        

    def __enter__(self):
        pdf_toimgs(self.filename, img_format='jpeg', pages=self.__pages__)
        _basename = os.path.split(rem_filetype(self.filename))[1]
        for file in os.listdir(self.__dumpdir__):
            if(_basename in file):
                self.__imgfiles__.append(os.path.join(self.__dumpdir__, file))
        return self

    def __lazysearch__(self, thresh=0.70):
        #Return the first image that is atleast as similar as threshold
        
        template_arr = __imgarr__(self.templatefile)
        for file in self.__imgfiles__:
            img_arr = __imgarr__(file)
            _rate = image_similarity(img_arr, template_arr)
            if(_rate > thresh):
                return file
        raise StopIteration

    def __bestsearch__(self):
        #Score similarity of all images and return highest match

        match_rates = {}
        template_arr = __imgarr__(self.templatefile)
        for file in self.__imgfiles__:
            img_arr = __imgarr__(file)
            match_rates[file] = image_similarity(img_arr, template_arr)
        return max(match_rates, key = lambda x: match_rates[x])

    def match(self, mode='best', thresh=0.70):
        #From the converted list of files, find the images most similar to the tempate
        assert mode in self.match.modes, 'Invalid search mode ({}). Valid mode choices: {}'.format(mode,__search__.modes)
        return self.match.modes[mode].__call__(self) if 'best' else self.match.modes[mode].__call__(self, thresh=thresh)
    match.modes = {'lazy':__lazysearch__, 'best':__bestsearch__}

    def __exit__(self, *args):
        pass


class FormReader():

    def __init__(self, templatefile, filename, boxmap,
                 extract_path = None, extact_filename = None, pdf_page = None, noisefilter_fn = None):
        self.templatefile = templatefile
        self.filename = filename
        self.data = {}

        self.__boxmap__ = boxmap
        self.__extract_path__ = extract_path or '{}{}'.format(rem_filetype(self.filename), '_img-dump')
        self.__formextract_files__ = {}
        self.__noisefilter_fn__ = noisefilter_fn or remove_nonchar_noise

        assert isinstance(pdf_page,int) or not pdf_page
        self.__pages__ = [pdf_page]
        
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
##        print(rem_filetype(imgfile))
        tesseractOCRsingle(imgfile, rem_filetype(imgfile), psm=11)
        return '\n'.join(slurp(as_filetype(imgfile, '.txt'))[:-1]).strip()

    def __ocrimgs__(self):
        for key in self.__formextract_files__:
            self.data[key] = self.__parse_var__(self.__formextract_files__[key])

    def __enter__(self):

        if(self.filename[-4:] == '.pdf'):
            with FormExtractor(self.templatefile, self.filename, pages=self.__pages__) as fe:
                self.filename = fe.match()
        
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


