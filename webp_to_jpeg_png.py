import sys
import getopt
import os
import imghdr
from PIL import Image


def process(input_dir,formatt):
    files = sorted(os.listdir(input_dir))
    subdir = []
    for file in files:
        file_path = os.path.join(input_dir,file)
        if os.path.isfile(file_path):
            if file.endswith(".webp"):
                output_file_dir = '{} {}'.format(input_dir,formatt.upper())
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)
                
                out_file_path = os.path.join(output_file_dir, '{}{}'.format(file.split('.webp')[0], '.{}'.format(formatt)))
                im = Image.open(file_path).convert("RGB")
                im.save(out_file_path, format=formatt, subsampling=0, quality=100)
                print('{} --> {}'.format(file_path, out_file_path))

        elif os.path.isdir(file_path):
            print(file_path)
            subdir.append(file_path)

    return subdir

dirr = ''
formatt = ''
try:
    opts, args = getopt.getopt(
        sys.argv[1:], 'd:f:', ['dir=', 'format=']
    )
except getopt.GetoptError:
    print(sys.argv[0], ' -d < dir > -f < format >')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-d', '--dir'):
        dirr = arg
    elif opt in ('-f', '--format'):
        formatt = arg



subdir = process(dirr,formatt)
for s in subdir:
    process(s,formatt)
