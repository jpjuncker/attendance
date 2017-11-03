# Import all csv files matching name 'yymmdd-hhmmssplayerInfosMerged.csv'
# and populate a cross-raid attendance sheet from them.
# Also provide a means of updating without parsing the entire set of files again

import sys, string, csv, os, re
import pandas
import sqlite3 as sqlite
from datetime import datetime, time

dataReg = re.compile('playerInfosMerged.csv')

def main():
    RAIDFILENAMETAG = 'playerInfosMerged.csv'
    TABLEHEADER = []
    TABLEHEADER.append('Player')

#   List properly formatted files for read
    raidDate = []
    for f in os.listdir('./data'):
        raidDate.append(getRaidDate(f))
    raidDate = filter(None, raidDate)
#   print raidDate

    names = getUniqueNames(raidDate)

#   Scan each table for each player and save rows
    individualData = getIndividualData(names, raidDate)

#   Initialize SQLite DB
    buildDB()

#   Populate row info into multi-day table




#   Lists formatted files
def getRaidDate(s):
    if dataReg.search(s):
        return './data/'+s
    return


#   Lists unique player names from list of files
def getUniqueNames(l):
    namesList = []
    for f in l:
        namesList = namesList + getUniqueNamesH(f)
#   print len(namesList)
    namesList = set(namesList)
#   print len(namesList)
    return list(namesList)

#   Helper function, reads csv file and returns 'Name' column
def getUniqueNamesH(f):
    names = []
    with open(f, 'rb') as cf:
        r = csv.reader(cf)
        for row in r:
            names.append(row[0])
    names.pop(0)
    return names


def getIndividualData(names, files):
    data = []
    for n in names:
        player = []
        for f in files:
            with open(f, 'rb') as cf:
                r = csv.reader(cf)
                for row in r:
                    if n == row[0]:
                        player.append(row)
        data.append(player)
    print(data)



def readAttendance():
    return

#   Connect temporarily to datbase, create Attendance table if it does not exist
def buildDB():
    con = None
    try:
        sqlite.connect('./data/attendance.db')
        print con
        cur = con.cursor()
        cur.execute("SELECT SQLITE_VERSION()")
        data = cur.fetchone()
        print 'SQLite %s DB loaded' % data
        cur.execute("CREATE TABLE IF NOT EXISTS Attendance(Name TEXT, Race TEXT, Class TEXT, Guild TEXT)")
    except sqlite.Error, e:
        print 'Error: %s' % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    main()
