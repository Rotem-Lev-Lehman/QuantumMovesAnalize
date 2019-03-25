from dateutil.parser import parse


def getMainPath():
    return 'C:\Users\Rotem\Desktop\quantum moves\Quantum moves 1\QuantumMovesData_180306\\'


def getResultsFolder():
    return getMainPath() + 'results\\'


def getFilename():
    return getMainPath() + 'QuantumMoves_180306.csv'


def getSizeOfSessionInSeconds():
    return 1800


def getPercentOfLeadersWeWantToRemove():
    return 10


def getGroupsFileName():
    return getResultsFolder() + 'mergedDataPerIPForAnalyzingGroups.csv'


def getKMeansFileName():
    return getResultsFolder() + 'kmeansGroupsDevision.csv'


def getSessionsFilename():
    return getResultsFolder() + 'sessions.csv'


def getSessionsPerIPFilename():
    return getResultsFolder() + 'sessionsPerIP.csv'


def getAmountsFilename():
    return getResultsFolder() + 'amounts.csv'


def getIpAndNumOfWorksFilename():
    return getResultsFolder() + 'ipAndNumOfWorks.csv'


def getLeadersFilename():
    return getResultsFolder() + 'leaders.csv'


def getDate(row):
    strDate = row[3]
    date = parse(strDate)
    return date


def getInfoAboutRow(row):
    # the parameter is a row in a csv file (separated by ',')
    # returns all of the information about the domain in the given row

    # row[0] is the users ip
    # row[3] is the finish time for this contribution
    # row[4] is the score for this contribution
    # row[5] is the duration of time this contribution was done in
    # row[6] is the level name for this contribution

    ip = row[3]
    fin = row[3]
    score = float(row[4])
    duration = float(row[5])
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

    return (ip, s, f, levelName, duration, score)


def getIPFromRow(row):
    return row[3]


def getIPStartTimeAndFinTime(row):
    # row[3] is the finish time for this contribution
    ip = row[3]
    fin = row[3]
    duration = float(row[5])

    finSplit = fin.split(" ")
    date = finSplit[0]
    timezone = finSplit[2]

    f = parse(fin)
    durrInSec = duration * 10
    temp = date + " " + "00:00:" + str(durrInSec) + " " + timezone
    tempParsed = parse(temp)

    start = date + " " + str(f - tempParsed) + " " + timezone
    s = parse(start)
    return (ip, s, f)


def getAmountOfStarsFromScoreAndRanges(score, oneStarsMin, twoStarsMin, threeStarsMin):
    if score < oneStarsMin:
        return 0
    if score < twoStarsMin:
        return 1
    if score < threeStarsMin:
        return 2
    return 3


def getAmountOfStarsAchived(levelName, score):
    if levelName == 'Easiest Transport':
        return getAmountOfStarsFromScoreAndRanges(score, 0.3, 0.6, 0.95)
    if levelName == 'Easiest Transport 2':
        return getAmountOfStarsFromScoreAndRanges(score, 0.15, 0.6, 0.9)
    if levelName in ['Easiest Transport 3', 'Transport Move 3', 'Easiest Transport 4', 'Transport', 'Transport Move 1', 'Transport_Curved', 'Bring Home Water Wider', 'Bring Home Water Time', 'Bring Home Water Soft Spiked', 'Bring Home Water Mirror', 'Bring Home Water Mirror w static pit', 'Pour the Water 1', 'There And Back Again Improved', 'Bring to and from Static']:
        return getAmountOfStarsFromScoreAndRanges(score, 0.3, 0.6, 0.9)
    if levelName == 'First time tunneling':
        return getAmountOfStarsFromScoreAndRanges(score, 0.25, 0.6, 0.9)
    if levelName == 'Bring Home Water Simple':
        return getAmountOfStarsFromScoreAndRanges(score, 0.3, 0.7, 0.9)
    if levelName == 'Bring Home Water Simple OtherSide Improved':
        return getAmountOfStarsFromScoreAndRanges(score, 0.5, 0.7, 0.9)
    if levelName == 'Bring Home Water':
        return getAmountOfStarsFromScoreAndRanges(score, 0.2, 0.6, 0.95)
    if levelName in ['Bring Home and Transport', 'Bring Home Double Dynamic and actual Static']:
        return getAmountOfStarsFromScoreAndRanges(score, 0.6, 0.8, 0.95)
    if levelName == 'Transport_ShakeIt_Excited':
        return getAmountOfStarsFromScoreAndRanges(score, 0.8, 0.9, 0.98)
