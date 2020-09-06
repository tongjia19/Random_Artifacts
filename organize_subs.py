import os


# target_dir = '/Volumes/TJs EXTERNAL/Videos/Foreign'
target_dir = '/Users/ttjiaa/Movies/movies'

remove_ext_list = [
  '.txt',
  '.exe'
]

sub_ext_list = [
  '.srt'
]

keep_srt_dict = {
  '2_Und': 'en',
  '2_Eng': 'en',
  '2_Engish': 'en',
  'English': 'en',
  '29_Chinese': 'zh'
}

media_ext_list = [
  '.mp4',
  '.mkv'
]


def split_dir(dirpath):
  head, tail = os.path.split(dirpath)
  return head, tail

def split_file_ext(filename):
  file_head, file_ext = os.path.splitext(filename)
  return file_head, file_ext

def is_valid_media_file(filename):
  _, file_ext = split_file_ext(filename)
  return file_ext in media_ext_list

def is_sub_file(filename):
  _, file_ext = split_file_ext(filename)
  return file_ext in sub_ext_list

def is_valid_sub_file(filename):
  file_head, _ = split_file_ext(filename)
  return is_sub_file(filename) and file_head in keep_srt_dict.keys()

def remove_garbage(dirpath, filename):
  _, file_ext = split_file_ext(filename)
  if file_ext in remove_ext_list:
    os.remove(os.path.join(dirpath, filename))

def clean_subs_stage_1(dirpath, filename):
  dir_head, dir_tail = split_dir(dirpath)
  if dir_tail == 'Subs':
    if is_valid_sub_file(filename):
      os.replace(os.path.join(dirpath, filename), os.path.join(dir_head, filename))
    else:
      os.remove(os.path.join(dirpath, filename))

def get_likely_media_file(filenames):
  for filename in filenames:
    if is_valid_media_file(filename):
      return filename

def get_likely_subs_files(filenames):
  subs = []
  for filename in filenames:
    if is_valid_sub_file(filename):
      file_head, _ = split_file_ext(filename)
      subs.append([filename, keep_srt_dict[file_head]])
  return subs

def clean_subs_stage_2(dirpath, dirnames, filenames):
  for dirname in dirnames:
    if dirname == 'Subs' and not os.listdir(os.path.join(dirpath, dirname)):
      os.rmdir(os.path.join(dirpath, dirname))

  likely_media_file = get_likely_media_file(filenames)
  likely_subs_files = get_likely_subs_files(filenames)

  if likely_media_file and likely_subs_files:
    media_file_name, _ = split_file_ext(likely_media_file)

    for sub_file_name, language in likely_subs_files:
      new_sub_file_name = media_file_name + '.' + language + '.srt'
      os.replace(os.path.join(dirpath, sub_file_name), os.path.join(dirpath, new_sub_file_name))

def clean_subs_stage_3(dirpath, dirnames, filenames):
  for filename in filenames:
    file_name_head, file_ext = split_file_ext(filename)
    if is_sub_file(filename) and file_name_head[-2:] not in keep_srt_dict.values():
      os.replace(os.path.join(dirpath, filename), os.path.join(dirpath, file_name_head + '.en' + file_ext))

for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
      remove_garbage(dirpath, filename)
      clean_subs_stage_1(dirpath, filename)

for dirpath, dirnames, filenames in os.walk(target_dir):
    clean_subs_stage_2(dirpath, dirnames, filenames)

for dirpath, dirnames, filenames in os.walk(target_dir):
    clean_subs_stage_3(dirpath, dirnames, filenames)
