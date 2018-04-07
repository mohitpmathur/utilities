@echo off

echo ### Backing up Sunaina
ROBOCOPY C:\Users\Mohit\Documents\Sunaina F:\Sunaina /e /LOG+:logs\Sunaina_backuplog.txt /NP

echo ### Backing up Mooney
ROBOCOPY C:\Users\Mohit\Desktop\Mooney F:\Sunaina\Mooney /e /LOG+:logs\Sunaina_backuplog.txt /NP

echo ### Backing up Mohit
ROBOCOPY C:\Users\Mohit\Documents\Mohit F:\Mohit /e  /XF *.ova /XF *.iso /XD temp /XD data /XD input /XD submissions /LOG+:logs\Mohit_backuplog.txt /NP

echo ### Backing up Music
ROBOCOPY C:\Users\Mohit\Music\Hindi F:\Music\Hindi /e /LOG+:logs\Music_backuplog.txt /NP

echo ### Backing up Pictures
ROBOCOPY C:\Users\Mohit\Pictures F:\Pictures /e /LOG+:logs\Pictures_backuplog.txt /NP

echo ### Backing up Phone Pictures
ROBOCOPY C:\Users\Mohit\Documents\Phone_Pics_Backup F:\Pictures /e /LOG+:logs\Pictures_backuplog.txt /NP

