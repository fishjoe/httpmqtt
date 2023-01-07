#  Author : Fishjoe
"""
This file update the existing files on MCU from the folder on your PC. You need to setup your project
folder on your pc as an http server. (ender the project folder in terminal and type: "python3 -m http.server")

"""




import network
import os
import sys
import urequests as requests
# from stats import StatsResult, stats
import time
import datetime

# ...........
import datetime


if "ESP32" in sys.implementation._machine:
    OFFSET = datetime.datetime(2000, 1, 1, 0, 0)
else:
    OFFSET = datetime.datetime(1970, 1, 1, 0, 0)

# offsets of other boards are not tested and missing

class FileNotExistsError(OSError):
    pass


class StatsResult:
    """
    Stats result of a file or directory.
    """
    def __init__(self, file):
        self.mode, *_, self.size, self.atime, self.mtime, self.ctime = os.stat(file)            
        self.file = file

    @property
    def is_directory(self) -> bool:
        return bool(self.mode >> 14 & 1)

    @property
    def is_file(self) -> bool:
        return bool(self.mode >> 15 & 1)

    @property
    def dt_atime(self):
        return OFFSET + datetime.timedelta(seconds=self.atime)
    
    @property
    def dt_mtime(self):
        return OFFSET + datetime.timedelta(seconds=self.mtime)
    
    @property
    def dt_ctime(self):
        return OFFSET + datetime.timedelta(seconds=self.ctime)


def stats(file: str) -> StatsResult:
    """
    Stats result of a file or directory.
    """
    try:
        return StatsResult(file)
        
    except OSError as error:
        if error.args[0] == 2:
            raise FileNotExistsError(f"{file} does not exist.")
        else:
            raise
        

def stats_parse_back(stat_obj):  # I try not touch code from third party. result: rtc
    mtime = str(stat_obj.dt_mtime)
    import re
    delim = re.compile("[- :]")
#     dttp = (int(yyyy),int(mm),int(dd),int(hh),int(mm),int(ss),0,0)
    dttp = [int(i) for i in delim.split(mtime)]+[0,0]
    struc_time = time.mktime(dttp)
    # print("line 84", struc_time)
    return struc_time


def date_and_time_string(t = time.localtime(), title_date="", title_time="", sep_date_n_time="", sep_date="", sep_time=""):
    tm = ""
    # print(str(t))
    for i in t[:6]:
        if len(str(i)) == 1:
            se = "0" + str(i)
        else:
            se = str(i)
        tm += se
    date_and_time_string = title_date + sep_date + tm[:4] + sep_date + tm[4:6] + tm[6:8] + sep_date_n_time + \
                           title_time + tm[8:10] + sep_time + tm[10:12] + sep_time + tm[12:14]
    # print(date_and_time_string)
    return date_and_time_string


def getURL(server, file):
    server = server if server[-1] == "/" else server+"/"
    return server + file
    


def get_mod_info_on(server, file): # and test for server status.
    URL = getURL(server, file)
    # print(URL)
    try:
        # print("line 119: timing")
        r = requests.head(URL)
        url_time = r.headers['Last-Modified']
        # print("line 122", url_time)
    except:
        url_time = "Thu, 01 Jan 1970 00:00:00 GMT"
    return url_time


def update(server, file):
    URL = getURL(server, file)
    # print(URL)
    resp = requests.get(URL)
    with open(file, "w") as file:
        file.write(resp.content)
        # print("Suceed")


def parse_requested_time(url_time):
    ulist = url_time.split(",")[1].strip().split(" ")
    yyyy = ulist[2]
    dd = "0" + str(ulist[0]) if len(ulist[0]) == 1 else str(ulist[0])
    m = 1+["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(ulist[1])
    mm = str(m) if m > 9 else "0" + str(m)
    hhmmss = ""
    for t in ulist[3].split(":"):
        tt = "0" + t if len(t) == 1 else t
        hhmmss = hhmmss + tt
    timeobj = time.mktime((int(yyyy), m, int(dd), int(hhmmss[:2]),  int(hhmmss[2:4]), int(hhmmss[4:]), 0, 0))
    timeobj = timeobj + (3600 * 13)
    thistime = time.localtime(timeobj)
    # # print(thistime)
    # print("\r.", end="", sep="")
    return timeobj, thistime

def is_not_folder(fileInfo):
    return fileInfo[1] == 32768
    
 
if __name__ == "__main__":
    
    # TODO Does not responde if http server fails.
    server = "http://192.168.1.212:8000"    
    
    try:
        requests.head(server)
        # print("line 159: 1 . server working")
    except OSError:
        # print("line 161: 1n . server not readay")
        sys.exit()
    
    for ft in os.ilistdir():
        # print(f"line 165, 2 . {ft[0]} being examed")
        if is_not_folder(ft):
            f = ft[0]
            url_time = get_mod_info_on(server, f)
            # print(f"line 169: 3, {url_time} received")
            objtime, _ = parse_requested_time(url_time)
            # print("line 171:",objtime)
            sta = stats(f)
            localmtime=stats_parse_back(sta)
            # print("line 171:",localmtime)
            
            # # print(f, " : ", objtime, localmtime)
            if objtime > localmtime:
                print(f"line 178: {f} updated")
                update(server, f)
            else:
                print(f"line 181: {f} not updated")
                pass
  