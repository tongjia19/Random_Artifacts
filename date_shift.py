import os
from datetime import datetime, timedelta


def mom(path):
    for filename in os.listdir(path):
        #if ('.jpg' or '.mp4') and ('IMAG' or 'VIDE') in filename:
        if 'VIDE' in filename:
            date_string = filename[:17]
            dt = datetime.strptime(date_string, '%y-%m-%d-%H-%M-%S')
            dt -= timedelta(hours=24)
            latter = filename[17:]
            print date_string
            print dt
            print dt.strftime('%y-%m-%d-%H-%M-%S')
            print ''
            os.rename(
                path + filename,
                (
                    path +
                    dt.strftime('%y-%m-%d-%H-%M-%S') +
                    latter
                )
            )
        continue


def tj(path):
    for filename in os.listdir(path):
        #if ('.jpg' or '.mp4') and ('IMG' or 'VID_') in filename:
        if 'VID_' in filename:
            date_string = filename[:14]
            dt = datetime.strptime(date_string, '%y-%m-%d-%H-%M')
            dt += timedelta(hours=12)
            latter = filename[14:]
            print date_string
            print dt
            print dt.strftime('%y-%m-%d-%H-%M')
            print ''
            os.rename(
                path + filename,
                (
                    path +
                    dt.strftime('%y-%m-%d-%H-%M') +
                    latter
                )
            )
        continue

mom("/Volumes/TJ's EXTERNAL/Photos/2016.05.03/")
#tj("/Volumes/TJ's EXTERNAL/Photos/2016.05.03/")