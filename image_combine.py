"""
Usage: python image_combine imageA(left) imageB(right)

"""
__author__ = 'Meldonization'

# Might need to change these if AppSo writer rules altered
spacing = 8 # the spacing in pix
finwidth = 800 # final image file width in pix

# Might need to change as your needs
finsize = 130 # final image maximum size in kb
wmoffset = 80 # bottom offset for the watermark of the combined image
sc = (0, 0, 0) # separation color if combining images: black - (0,0,0) 

try: 
    from PIL import Image
except:
    sys.exit("Please run `sudo easy_install pip && \
          pip install pillow` first...")
import os, sys, base64, StringIO


def watermark(im, mark, position):
    """Adds a watermark to an image."""
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)
    
def saveimg(filename, img):
    """Save image by file name[fn]
         - jpeg only and there is a file size limit 
    """
    quality = 100 # initial jpeg quality, no need to change.
    while True:
        img.save(filename, 'jpeg', quality = quality)
        if (os.stat(filename).st_size / 1024. <= finsize):
            break
        quality -= 1
    return True

Nargs = len(sys.argv)

if (Nargs <= 1 or Nargs > 3): 
    print "\nIncorrect number of arguments..\n"
    print "Usage: python image_combine.py imageA(to-be-watermarked) "
    print "       python image_combine.py \
        imageA(to-be-combined-at-left) imageB(right)"
    sys.exit("\n> Please drag img file to terminal..\n")


# Please ignore this encoded watermark file..
wmfile = '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\
oIAAAAASUVORK5CYII='

wmimg = Image.open(StringIO.StringIO(base64.b64decode(wmfile)))    
    
if (Nargs == 2):
    # Watermark the input image and save it.
    print "\n>>> Watermarking the target img...\n"
    img = Image.open(str(sys.argv[1]),'r')
    width, height = img.size
    finalh = int(finwidth * 1.0 / width * height)
    img = img.resize((finwidth, finalh))
    boxwm = (finwidth - wmimg.width, finalh - wmimg.height - wmoffset)
    img = watermark(img, wmimg, boxwm)
    fileout = os.path.split(str(sys.argv[1]))[0] + '/watermarked.jpg'
    saveimg(fileout, img)
     
if (Nargs == 3):
    print "\n>>> Combining and watermarking the target imgs...\n"
    img1 = Image.open(str(sys.argv[1]),'r')
    img2 = Image.open(str(sys.argv[2]),'r')
    fileout = os.path.split(str(sys.argv[1]))[0] + '/combined.jpg'
    width, height = img1.size
    singlew = finwidth / 2 - spacing / 2
    singleh = int(singlew * 1.0 / width * height)
    img1 = img1.resize((singlew, singleh))
    img2 = img2.resize((singlew, singleh))
    out = Image.new('RGBA', (finwidth, singleh), sc)
    box1 = (0, 0)
    box2 = (singlew + spacing, 0)
    boxwm = (singlew - wmimg.width, singleh - wmimg.height - wmoffset)
    out.paste(img1, box1)
    img2 = watermark(img2, wmimg, boxwm)
    out.paste(img2, box2)
    saveimg(fileout, out)

print "Image saved to " + fileout + "\n"
