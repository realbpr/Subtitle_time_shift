import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os

root = tk.Tk()  # creates main window
root.withdraw()  # hide window until called for

srt_path = filedialog.askopenfilename()  # prompt window for choosing file path of srt file
srt = Path(srt_path)


filename = os.path.basename(str(srt))
newname = filename[:-4] + "_FIXED"

shift = float(input("Enter desired time shift (seconds): "))  # user inputs desired time shift

oldSub = open(srt, 'r', encoding='UTF8')

new_sub = str(srt.resolve().parent) + r"\\" + newname + ".srt"  # complete file path and name of new_sub.txt which we will create
newSub = open(new_sub, 'w', encoding='UTF8')

oldLines = oldSub.readlines()  # sets up array of lines of old subtitle file
newLines = oldLines.copy()


# converts string of time in format XX:XX:XX,XXX (hours:minutes:seconds,milliseconds) into the number of seconds
def convert_sec(HrTime):
    msec = float(HrTime[9:12])  # reads milliseconds str section, converts to float to be added
    sec = float(HrTime[6:8])
    mins = float(HrTime[3:5])
    hrs = float(HrTime[0:2])
    return msec/1000 + sec + mins*60 + hrs*3600


# Converts a (float) sum of seconds into str of format XX:XX:XX,XXX (hours:minutes:seconds,milliseconds)
def convert_Hrs(SecTime):
    # Want Hrs = "XX:XX:XX,XXX " space at the end is necessary to have 12th element in str
    msec = int((SecTime % 1)*1000)  # takes remainder of dividng by 1 to get remainder fraction of second, then turns into integer by x1000 to convert into milliseconds
    msec_str = str(msec)
    
    if msec < 100:  # all if statements in here ensure strings begin with zero if needed (ex. 02 not 2 if is <10) since must take up 2 spaces (and 3 spaces for milliseconds)
        if msec < 10:
            msec_str = "00"+str(msec)

    sec = int(SecTime % 60 - SecTime % 1)  # isolates seconds modulus of 60 and subtracts milliseconds to get just seconds (under 60)
    sec_str = str(sec)
    if sec < 10:
        sec_str = "0" + str(sec)

    mins = int((SecTime % 3600 - SecTime % 60)/60)
    mins_str = str(mins)
    if mins < 10:
        mins_str = "0" + str(mins)

    hours = int((SecTime - SecTime % 3600)/3600)
    hours_str = str(hours)
    if hours < 10:
        hours_str = "0" + str(hours)

    Hrs = hours_str + ":" + mins_str + ":" + sec_str + "," + msec_str
    return Hrs


# Shift time for all lines
for n in range(len(oldLines)):
    if "-->" in oldLines[n]:
        oldStart = oldLines[n][0:12]
        oldEnd = oldLines[n][17:29]  # identifies original start time and end time of given line

        oldStart_sec = convert_sec(oldStart)
        oldEnd_sec = convert_sec(oldEnd)  # converts to seconds

        newStart_sec = oldStart_sec + shift
        newEnd_sec = oldEnd_sec + shift  # shifts start and end times

        newStart = convert_Hrs(newStart_sec)
        newEnd = convert_Hrs(newEnd_sec)  # converts back to XX:XX:XX.XXX format

        newLines[n] = newStart + " --> " + newEnd + "\n"  # writes new lines with shifted times


for k in range(len(newLines)):  # updates new_sub.txt
    newSub.write(newLines[k])


# closes file to stop writing, can now change txt to srt
oldSub.close()
newSub.close()
