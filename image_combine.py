"""
Usage: python image_combine imageA(left) imageB(right)

"""
__author__ = 'Meldonization'

# Please change `watermarkfile` location once for all!!
wmfile = "/Users/xxxxxx/Desktop/appso-mark_right.png" 

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
    sys.exit("Please run ` pip install pillow ` first...")
import os, sys


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

try: 
    wmimg = Image.open(wmfile,'r')
except:
    sys.exit("\nPlease edit var `wmfile` in this python script first.\n")

if (Nargs <= 1 or Nargs > 3): 
    print "\nIncorrect number of arguments..\n"
    print "Usage: python image_combine.py imageA(to-be-watermarked) "
    print "       python image_combine.py imageA(to-be-combined-at-left) imageB(right)"
    sys.exit("\n> Please drag img file to terminal..\n")
    
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
