# Copyright (c) 2016 Tzutalin
# Create by TzuTaLin <tzu.ta.lin@gmail.com>

from PyQt4.QtGui import QImage
from base64 import b64encode, b64decode
from pascal_voc_io import PascalVocWriter
import os.path
import sys

class LabelFileError(Exception):
    pass

class LabelFile(object):
    # It might be changed as window creates
    suffix = '.lif'

    def __init__(self, filename=None):
        #self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)

    def savePascalVocFormat(self, filename, shapes, attrs,
                            imagePath, imageData, lineColor,
                            fillColor, databaseSrc=None):
        imgFolderPath = os.path.dirname(imagePath)
        imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFileName = os.path.basename(imagePath)
        imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]

        def format_shape(s):
            return dict(label=unicode(s.label),
                        line_color=s.line_color.getRgb()\
                                if s.line_color != lineColor else None,
                        fill_color=s.fill_color.getRgb()\
                                if s.fill_color != fillColor else None,
                        points=[(p.x(), p.y()) for p in s.points])

        # Read from file path because self.imageData might be empty if saving to
        # Pascal format
        image = QImage()
        image.load(imagePath)
        imageShape = [image.height(), image.width(), 1 if image.isGrayscale() else 3]
        writer = PascalVocWriter(imgFolderName, imgFileNameWithoutExt,\
                                 imageShape, localImgPath=imagePath)
        bSave = True #False
        for shape in shapes:
            fshape = format_shape(shape)
            
            attr = attrs[shape]
            points = fshape['points']
            label = fshape['label']
            pose = attr['pose']
            occluded = attr['occluded']
            truncated = attr['truncated']
            bndbox = LabelFile.convertPoints2BndBox(points)
            writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3],
                             label, pose, occluded, truncated)
            bSave = True

        if bSave:
            writer.save(targetFile = filename)
        return

    @staticmethod
    def isLabelFile(filename):
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == LabelFile.suffix

    @staticmethod
    def convertPoints2BndBox(points):
        xmin = sys.maxint
        ymin = sys.maxint
        xmax = -sys.maxint
        ymax = -sys.maxint
        for p in points:
            x = p[0]
            y = p[1]
            xmin = min(x,xmin)
            ymin = min(y,ymin)
            xmax = max(x,xmax)
            ymax = max(y,ymax)

        # Martin Kersner, 2015/11/12
        # 0-valued coordinates of BB caused an error while
        # training faster-rcnn object detector.
        if (xmin < 1):
            xmin = 1

        if (ymin < 1):
            ymin = 1

        return (int(xmin), int(ymin), int(xmax), int(ymax))
