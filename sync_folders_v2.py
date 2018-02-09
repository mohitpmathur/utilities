'''
Author: Mohit Mathur

The script is used for the following purposes:
    - Consolidate multiple folders into one: Copy files from multiple folders
      into one single destination folder, skips copying duplicates, if different
      files have same name it renames one of them and copies
    - Synchronize 2 folders: Takes 2 folders as input and copies files into each
      other so that both have the exact same content
'''

import os
import shutil
import glob
from datetime import datetime


DEBUG = 0
INFORMATIONAL = 1
WARNING = 2
ERROR = 3

log_level = 1
print_screen = 0

def log_message(msg = "Sync Folders", level=1):    
    log_file = 'synchronize_folders.log'
    if level >= log_level:
        fhd = open(log_file, 'a')
        if msg == "SEP":
            # print separator
            fhd.write("-"*70 + "\n")
            if print_screen:
                print "-"*70 + "\n"
        elif msg == "NEWLINE":            
            fhd.write("\n")
            if print_screen:
                print "\n"
        else:
            fhd.write(msg + '\n')
            if print_screen:
                print msg
        fhd.close()


def consolidate(source, destination, sync, rename_snip):
    """
    This function is used to either:
        - consolidate multiple folders into 1 single folder. Any files that
            have the same name but different size, will be renamed before
            being copied to destination. Files with same name and same size
            will be skipped
        - synchronize the source and destination so destination has same
            folder structure as source. Any files with same name but different
            size will be renamed before copying. Files with same name and same
            size will be skipped

    Args:
    source (string): Source folder
    destination (string): Destination folder
    sync (int): sync = 1, synchronize folders
                sync = 1, consolidate folders
    rename_snip (str): string used to rename files with same name
                    but different size

    Returns:
    copied (list): list of destination files copied
    skipped (list): list of source files skipped
    renamed (list): list of dest files that have been renamed
                before being copied
    
    """
    log_message("Starting to consolidate folders...")
    log_message("Date: {}".format(datetime.now()))
    log_message("Source: {}".format(source))
    log_message("Destination: {}".format(destination))
    if sync:
        log_message("Task: Synchronize")
    else:
        log_message("Task: Consolidate")
    log_message("Rename Snippet: {}\n".format(rename_snip))
    skipped = []
    copied = []
    renamed = []
    for root, dirnames, filenames in os.walk(source):
        log_message("{} - {} - {}".format(root, dirnames, filenames), DEBUG)
        if sync == 1:
            if source == root:
                log_message("Root same as source: {}".format(root), DEBUG)
                # Do not create destination folder
                dest_path = destination            
            else:
                # Create destination folder
                sub_folder = root.replace(source, "").lstrip("\\")
                dest_path = os.path.join(destination, sub_folder)
                if not os.path.exists(dest_path):                    
                    os.makedirs(dest_path)
                    log_message("dest_path created", DEBUG)
        else:
            dest_path = destination
        log_message("\tdest_path: " + dest_path, DEBUG)
        for fname in filenames:
            # Check if this file exists in destination
            dest_file = os.path.join(dest_path, fname)
            source_file = os.path.join(root, fname)            
            log_message("\t\tdest_file: " + dest_file, DEBUG)
            log_message("\t\tsource_file: " + source_file, DEBUG)
            if os.path.exists(dest_file):
                log_message("\t\t\tdest_file exists", DEBUG)
                source_info = os.stat(source_file)
                dest_info = os.stat(dest_file)
                if source_info.st_size == dest_info.st_size:
                    log_message("\t\t\tdest_file same as source file. DUPLICATE. SKIP", DEBUG)
                    skipped.append(source_file)
                else:
                    log_message("\t\t\tdest_file size different from source_file. Try to Rename", DEBUG)
                    fcount = 0
                    renamed_file_name = os.path.join(dest_path, "{}*{}".format(rename_snip, fname))
                    log_message("\t\t\trenamed_file_name: {}".format(renamed_file_name), DEBUG)
                    renamed_files = glob.glob(renamed_file_name)
                    log_message("\t\t\tAll renamed files: {}".format(renamed_files), DEBUG)
                    same_file = False
                    for renamed_file in renamed_files:
                        if source_info.st_size == os.stat(renamed_file).st_size:
                            same_file = True
                            log_message("\t\t\tRenamed file with same size as source already exists. SKIP", DEBUG)
                            fcount += 1
                    fcount = len(renamed_files)
                    if fcount == 0 or same_file == False:
                        dest_file = os.path.join(dest_path, "{}_{}_{}".format(rename_snip, fcount+1, fname))
                        log_message("\t\t\tRENAMING and COPY dest_file: " + dest_file, DEBUG)
                        shutil.copy2(source_file, dest_file)
                        renamed.append(dest_file)
                    else:
                        skipped.append(source_file)
                        log_message("\t\t\tSKIPPED " + source_file, DEBUG)
            else:
                # copy file
                log_message("\t\t\tdest_file does not exist", DEBUG)
                shutil.copy2(source_file, dest_file)
                copied.append(dest_file)    
    log_message("\n\t\t ---- SUMMARY ---- \n")
    log_message("Copied: {}".format(len(copied)))
    for file_name in copied:
        log_message("\t{}".format(file_name))
    log_message("Copied After Renaming: {}".format(len(renamed)))
    for file_name in renamed:
        log_message("\t{}".format(file_name))
    log_message("Skipped: {}".format(len(skipped)))
    for file_name in skipped:
        log_message("\t{}".format(file_name))
    log_message("\nDate: {}".format(datetime.now()))
    log_message("Finished consolidating folders...")
    return copied, skipped, renamed


source = r"C:\Users\e1040624\Documents\Test\1"
destination = r"C:\Users\e1040624\Documents\Test\3"
rename_snip = "RENAMED"

log_message("NEWLINE")
log_message("SEP")
log_message("NEWLINE")

# if synchronizing source and destination
sync = 1

copied, skipped, renamed = consolidate(source, destination, sync, rename_snip)

log_message("SEP")
log_message("NEWLINE")

