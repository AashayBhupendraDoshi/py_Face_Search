import os
import pandas as pd

supported_image_formats = ['jpeg', 'jpg', 'jpe', 'jp2', 'png']
supported_video_formats = ['avi', 'mp4', 'mjpeg', 'mpng', 'h264']

def get_filelist_from_root(root_dir):
    # Check files in directory
    # Given a directory location check all files present in it
    # List returns complete address from / [linux Filesystem ROOT directory]
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        # Check if any files exist in root
        if len(files) == 0:
            pass
        else:
            for names in files:
                file_list += [os.path.join(root,names)]
        # Recursively Check Sub Directories
        # To speed up the task use loop instead of recursion
        
        
        
        #print(root, "consumes", end=" ")
        #print(sum(getsize(join(root, name)) for name in files), end=" ")
        #print("bytes in", len(files), "non-directory files")
    return file_list

def image_support(addr):
    if os.path.isfile(addr):
        if addr.split('.')[-1].lower() in supported_image_formats and len( os.path.split(addr)[-1].split('.') )<3:
            return 1
        else:
            return 0
    else:
        return -1

def video_support(addr):
    if os.path.isfile(addr):
        if addr.split('.')[-1].lower() in supported_video_formats and len( os.path.split(addr)[-1].split('.') )<3:
            return 1
        else:
            return 0
    else:
        return -1

def directory_check(addr):
    if os.path.isdir(addr) and len(os.listdir(addr))>0:
        return 1
    else:
        return 0

#def check_process_file(addr):
#    buff = os.path.split(addr)
#    pickle_file_name = buff[1] + ".pkl"
#    if os.path.isfile(os.join(addr,pickle_file_name)):
#        return 1
#    else:
#        return 0

def get_process_files(directory_address, task, media):
    # Return file name and last updated date of process file
    index_file = pd.read_pickle('./process_files/index_' + str(task) + "_" + str(media) + '.pkl')
    print(index_file)
    # If index file is blank return -1
    if index_file.empty:
        return -1,-1
    #buff = index_file['directory_address'].str.find(directory_address)
    buff = index_file[index_file['directory_address'] == directory_address]
    # Returns -1, -1 if file does not exist
    #if buff == -1:
    if buff.empty:
        return -1, -1
    else:
        #process_file = pd.read_pickle(buff['file_name'])
        return buff['file_name'].iloc[0], buff['last_updated'].iloc[0]

