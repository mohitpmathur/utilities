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


def log_message(msg = "Sync Folders"):
    log_file = 'synchronize_folders.log'
    fhd = open(log_file, 'a')
    if msg == "SEP":
        # print separator
        fhd.write("-"*70 + "\n")
    elif msg == "NEWLINE":
        fhd.write("\n")
    else:
        fhd.write(msg + '\n')
    fhd.close()


def consolidate(source, destination, rename_snip):
    log_message("Starting to consolidate folders...")
    log_message("Date: {}".format(datetime.now()))
    log_message("Source: {}".format(source))
    log_message("Destination: {}".format(destination))
    log_message("Rename Snippet: {}".format(rename_snip))
    skipped = []
    copied = []
    renamed = []
    for root, dirnames, filenames in os.walk(source):
        #print "{} - {} - {}".format(root, dirnames, filenames)
        for fname in filenames:
            #print "\t", fname
            # Check if this file exists in destination
            dest_file = os.path.join(destination, fname)
            source_file = os.path.join(root, fname)            
            #print "\t\tdest_file:", dest_file
            if os.path.exists(dest_file):
                source_info = os.stat(source_file)
                dest_info = os.stat(dest_file)
                if source_info.st_size == dest_info.st_size:
                    #print "\t\tDUPLICATE. SKIP"
                    skipped.append(source_file)
                else:
                    #print "\t\tRENAME"
                    fcount = 0
                    renamed_files = glob.glob(os.path.join(destination, "{}*{}".format(rename_snip, fname)))
                    #print "\t\tAll renamed files:", renamed_files
                    same_file = False
                    for renamed_file in renamed_files:
                        #print "\t\trenamed_file:",renamed_file
                        if source_info.st_size == os.stat(renamed_file).st_size:
                            same_file = True
                            #print "\t\tsame"
                            fcount += 1
                    #print "\t\tSAME_FILE:", same_file
                    fcount = len(renamed_files)
                    if fcount == 0 or same_file == False:
                        dest_file = os.path.join(destination, "{}_{}_{}".format(rename_snip, fcount+1, fname))
                        shutil.copy2(source_file, dest_file)
                        renamed.append(source_file)
                    else:
                        skipped.append(source_file)
            else:
                # copy file
                #print "\t\tCOPY"
                shutil.copy2(source_file, dest_file)
                copied.append(source_file)    
    log_message("\n\t\t ---- SUMMARY ---- \n")
    log_message("Copied: {}".format(len(copied)))
    for file_name in copied:
        #print "\t", file_name
        log_message("\t{}".format(file_name))
    log_message("Copied After Renaming: {}".format(len(renamed)))
    for file_name in renamed:
        #print "\t", file_name
        log_message("\t{}".format(file_name))
    log_message("Skipped: {}".format(len(skipped)))
    for file_name in skipped:
        #print "\t", file_name
        log_message("\t{}".format(file_name))
    log_message("\nDate: {}".format(datetime.now()))
    log_message("Finished consolidating folders...")
    return copied, skipped, renamed


source = r"C:\Users\Mohit\Documents\Phone_Pics_Backup\iPhone Backup\Orig"
destination = r"C:\Users\Mohit\Documents\Phone_Pics_Backup\iPhone Backup\Consolidated"
rename_snip = "RENAMED"

log_message("NEWLINE")
log_message("SEP")
log_message("NEWLINE")

copied, skipped, renamed = consolidate(source, destination, rename_snip)

log_message("SEP")
log_message("NEWLINE")

