import re, string, csv, sys
import pandas
from datetime import datetime, time

def main():
    PLAYERINFOS, BOSSKILLS, JOIN, LEAVE, LOOT = 'PlayerInfos', 'BossKills', 'Join', 'Leave', 'Loot'
    PLAYERINFOS_WIDTH = 6
    JOINDATA_WIDTH = 6
    LEAVEDATA_WIDTH = 2
    LOOTDATA_WIDTH = 15 # 2 extra cols for nested tags
    FILEBASE = sys.argv[-1]
    if sys.argv == 'tabulate.py':
        print 'File input required'
        quit()
    BASEFILE = FILEBASE
    LBFILE = 'LB%s'%FILEBASE
    fAddLineBreaks(BASEFILE, LBFILE)
    f = open(LBFILE, 'r')
    rawtext = f.read()
    f.close()
    splittext = splitText(rawtext)
    playerInfos = getTable(splittext, PLAYERINFOS)
    bossKills = getTable(splittext, BOSSKILLS)
    joinData = getTable(splittext, JOIN)
    leaveData = getTable(splittext, LEAVE)
    lootData = getTable(splittext, LOOT)
    playerInfos = pandas.DataFrame(tabulateByKeys(playerInfos, PLAYERINFOS_WIDTH))
    playerInfos.columns = ['Name', 'Race', 'Guild', 'Sex', 'Class', 'Level']
    bossKills = pandas.DataFrame(tabulateBossKills(bossKills))
    joinData = pandas.DataFrame(tabulateByKeys(joinData, JOINDATA_WIDTH))
    joinData.columns = ['Name', 'Race', 'Class', 'Sex', 'Level', 'Join']
    leaveData = pandas.DataFrame(tabulateByKeys(leaveData, LEAVEDATA_WIDTH))
    leaveData.columns = ['Name', 'Leave']
    lootData = pandas.DataFrame(tabulateByKeys(lootData, LOOTDATA_WIDTH))
    playerInfosMerged = playerInfos.merge(joinData, on=['Name','Class','Level','Sex','Race'])
    playerInfosMerged = playerInfosMerged.merge(leaveData, on='Name')
    playerInfosMerged['Duration'] = getDuration(playerInfosMerged['Join'], playerInfosMerged['Leave'])
    filedate = getFileNameDate(joinData.Join)
#   tfp = 'bossKills.csv'
#   tfn = '%s%s'%(filedate, tfp)
#   bossKills.to_csv(tfn, sep=',', index=False)
    tfp = 'playerInfosMerged.csv'
    tfn = '%s%s'%(filedate, tfp)
    playerInfosMerged.to_csv(tfn, sep=',', index=False)

def sec2hms(s):
    nhours = s/3600
    s -= (3600*nhours)
    nmin = s/60
    s -= (60*nmin)
    hms = time(hour=nhours, minute=nmin, second=s)
    return time.strftime(hms, '%X')

def getDuration(join, leave):
    duration = []
    for i in range(len(join)):
        t_join = join[i]
        t_leave = leave[i]
        t_join = datetime.strptime(t_join, '%m/%d/%y %H:%M:%S')
        t_leave = datetime.strptime(t_leave, '%m/%d/%y %H:%M:%S')
        t_duration = t_leave - t_join
        t_duration = sec2hms(t_duration.seconds)
        duration.append(t_duration)
    return duration

def getFileNameDate(raw):
    a = raw[0]
    d = '%s%s%s-%s%s%s'%(a[6:8],a[:2],a[3:5],a[9:11],a[12:14],a[15:])
    return d

def fAddLineBreaks(source, dest):
    f = open(source, 'r')
    plaintext = f.read()
    plaintext = plaintext.replace('</race><sex>', '</race><guild>N/A</guild><sex>')
    plaintext = plaintext.replace("><", ">\n<")
    f.close()
    g = open(dest, 'w')
    g.write(plaintext)
    g.close()

def splitText(rawtext):
    lines = string.split(rawtext, '\n')
    for i in lines:
        re.sub('\n', '', i)
    return lines

def getTable(split, table):
    reg = re.compile(table)
    tdata = []
    record = False
    for i in split:
        if record:
            tdata.append(i)
        if reg.search(i) != None:
            record = not record
    return tdata[0:len(tdata)-1]

def purgeTags(raw):
    pattern = '</.*>'
    pattern2 = '<.*>'
    for i in range(0, len(raw)):
        raw[i] = re.sub(pattern, '', raw[i])
        raw[i] = re.sub(pattern2, '', raw[i])
    return raw

def tabulateBossKills(raw): # 3 dimensions?
    return

def tabulateByKeys(raw, width):
    tab = []
    rowcount = 0
    tagless = purgeTags(raw)
    nrow = len(tagless)
    nrow = int(nrow/(width+2))
    for i in range(nrow):
        row = []
        for j in range(2,width+2):
            val = (i*(2+width))+j-1
            row.append(tagless[val])
        tab.append(row)
    return tab

if __name__ == '__main__':
    main()
