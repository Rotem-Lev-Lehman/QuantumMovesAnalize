from dateutil.parser import parse

def getFilename():
    return 'QuantumMoves_180306.csv'

def getSessionsFilename():
    return 'sessions.csv'

def getAmountsFilename():
    return 'amounts.csv'

def getIpAndNumOfWorksFilename():
    return 'ipAndNumOfWorks.csv'

def getLeadersFilename():
    return 'leaders.csv'

def getInfoAboutRow(row):
    # the parameter is a row in a csv file (separated by ',')
    # returns all of the information about the domain in the given row

    # row[0] is the users ip
    # row[3] is the finish time for this contribution
    # row[4] is the score for this contribution
    # row[5] is the duration of time this contribution was done in
    ip = row[0]
    fin = row[3]
    score = row[4]
    duration = row[5]
    levelName = row[6]

    finSplit = fin.split(" ")
    date = finSplit[0]
    timezone = finSplit[2]

    f = parse(fin)
    durrInSec = duration * 10
    temp = date + " " + "00:00:" + str(durrInSec) + " " + timezone
    tempParsed = parse(temp)

    start = date + " " + str(f - tempParsed) + " " + timezone
    s = parse(start)
    return (ip, start, fin, duration, score, levelName)

def getIPFromRow(row):
    return row[0]

