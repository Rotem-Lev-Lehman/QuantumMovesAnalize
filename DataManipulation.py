import sys
import csv
from dateutil.parser import parse
from datetime import datetime
import json
import MyModel
from pprint import pprint

csv.field_size_limit(sys.maxsize)  # used so the size limit exception will not pop up...

'''
def getTimeDiff(startTime, endTime):
    # return the time difference
    start = parse(startTime)
    end = parse(endTime)
    # diff = (end-start).total_seconds()
    diff = end - start  # the amount in between end and start in date format!
    return diff


def getInfoAboutTimeStamps(fileName):
    print 'getting information'
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        data = []
        for row in creader:
            c = json.loads(row[10])
            fin = c["finished_at"]
            start = c["started_at"]
            timeDiff = getTimeDiff(start, fin)
            data.append(timeDiff)
        return data
'''

def writeInfoAboutTimeStampsToCSV(data):
    print 'writing to csv'
    with open('timeStamps.csv', 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['time difference', 'in seconds'])
        for row in data:
            cwriter.writerow([row, row.total_seconds()])


def writeRowToENDOfCSV(fileName, row):
    with open(fileName, 'ab') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(row)


def getIPAndNumOfWorksANDMaxAmount(ip):
    print 'Now counting for each ip how much time it was used'
    ipAndNumOfWorks = []
    maxAmount = 0
    for curr in ip:
        amount = ip.count(curr)
        if (curr, amount) not in ipAndNumOfWorks:
            ipAndNumOfWorks.append((curr, amount))
            if amount > maxAmount:
                maxAmount = amount
    return ipAndNumOfWorks, maxAmount


def createAmountVec(ipAndNumOfWorks, maxAmount):
    print 'Now creating the amountVec'
    amountsVec = []
    for i in range(maxAmount + 1):
        if i > 0:
            num = 0
            for ip, count in ipAndNumOfWorks:
                if count == i:
                    num = num + 1
            amountsVec.append((i, num))
    return amountsVec


def writeEveryThingToCSV(ipAndNumOfWorks, amountsVec, totalNumOfPeople):
    print 'writing everything to csv'
    with open('amounts.csv', 'wb') as csvResult:
        cwriter = csv.writer(csvResult, delimiter=',')
        cwriter.writerow(['Work Amount', 'People Amount', 'Total num of people is: ' + str(totalNumOfPeople)])
        for i, amount in amountsVec:
            cwriter.writerow(['amount of people who made ' + str(i) + ' works', amount])
    with open('ipAndNumOfWorks.csv', 'wb') as csvResult:
        cwriter = csv.writer(csvResult, delimiter=',')
        cwriter.writerow(['IP', 'Num Of Works'])
        for ip, num in ipAndNumOfWorks:
            cwriter.writerow([ip, num])


def writeLeadersToCSV(leaders):
    print 'writing leaders to csv'
    with open('leaders.csv', 'wb') as csvLeaders:
        cswriter = csv.writer(csvLeaders, delimiter=',')
        cswriter.writerow(['IP', 'Num Of Works'])
        for currIP, currNum in leaders:
            cswriter.writerow([currIP, currNum])


def writeAllOfTheMergedDataToCSV(merged):
    # 0.ip,1.contributions, 2.duration, 3.score, 4.stars, 5.Exploitation rate, 6.levels amount, 7.sessionsAmount
    print 'writing merged data to csv'
    with open('mergedDataPerIPForAnalyzingGroups.csv', 'wb') as mergedFile:
        cswriter = csv.writer(mergedFile, delimiter=',')
        cswriter.writerow(['IP', 'Contributions', 'Duration', 'Score', 'Stars', 'Exploitation Rate', 'Levels amount', 'Sessions Amount'])
        for a, b, c, d, e, f, g, h in merged:
            cswriter.writerow([a, b, c, d, e, f, g, h])


def removeLeadersByXPersentAndWriteEveryThingToCSV(ipAndNumOfWorks, amountsVec, persent):
    print 'removing leaders'
    sum0 = 0
    for i, num in amountsVec:
        sum0 = sum0 + num
    sum1 = sum0 / (100 - persent)  # only x% of people
    if persent == 0:
        sum1 = sum0
    sum2 = sum0 - sum1
    peopleWhoWereRemoved = []  # a vector that will contain the IP address of the people who were removed because they were in the best 10%
    while sum1 > 0:
        i, amount = amountsVec[len(amountsVec) - 1]
        if amount > 0:
            sum1 = sum1 - 1
            amountsVec[len(amountsVec) - 1] = (i, amount - 1)
            for currIP, currNum in ipAndNumOfWorks:
                if currNum == i:
                    if (currIP, currNum) not in peopleWhoWereRemoved:
                        peopleWhoWereRemoved.append((currIP, currNum))
            flag = 1
            while flag == 1:
                i2, amount2 = amountsVec[len(amountsVec) - 1]
                if amount2 == 0:
                    amountsVec.pop()
                else:
                    flag = 0
        else:
            amountsVec.pop()
    writeLeadersToCSV(peopleWhoWereRemoved)
    writeEveryThingToCSV(ipAndNumOfWorks, amountsVec, sum2)


def IPAndContributionsCount(fileName):
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        print 'Now getting the ip of each user who gave us information'
        ip = []
        for row in creader:
            ip.append(MyModel.getIPFromRow(row))
        ipAndNumOfWorks, maxAmount = getIPAndNumOfWorksANDMaxAmount(ip)
        amountsVec = createAmountVec(ipAndNumOfWorks, maxAmount)
        removeLeadersByXPersentAndWriteEveryThingToCSV(ipAndNumOfWorks, amountsVec, MyModel.getPercentOfLeadersWeWantToRemove())  # 10 percent

'''
def createFileWithOnlyReleventRows(fileName):
    # creates a file with the colomns after removing those who didn't contribute(have no marks in the value of the annotations colomn
    # returns the new file's name
    print 'Starting to create a file with only relevent rows'
    newFileName = 'Relevent_Rows_Only_From_' + fileName
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        for row in creader:
            # thats a bad json format, the fix of it is:
            goodRow = ''
            curr = row[11]
            for i in range(len(curr) - 1):
                if i > 0:
                    goodRow = goodRow + curr[i]
            c = json.loads(goodRow)
            val = c["value"]
            if val:
                writeRowToENDOfCSV(newFileName, row)
                # else:
                #	print 'bad row:'
                #	print row
        return newFileName
'''

def getIPAndTimeStamps(fileName, sessionTime):
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        print 'Now getting the ip of each user who gave us information'
        ipANDTimeStamps = []
        ip = []
        for row in creader:
            rowIP, start, fin = MyModel.getIPStartTimeAndFinTime(row)
            if rowIP not in ip:
                ip.append(rowIP)
            ipANDTimeStamps.append((rowIP, start, fin))
        # ipAndNumOfWorks,maxAmount = getIPAndNumOfWorksANDMaxAmount(ip)
        print 'Now sorting the data by ip,start time'
        ipANDTimeStamps.sort(key=lambda x: (x[0], x[1]))
        lastFinish = ipANDTimeStamps[0][2]
        sameSession = []
        # print 'IP:'
        # print ip
        # print 'ipANDTimeStamps:'
        # print ipANDTimeStamps
        print 'Now creating the sessions'
        for currIP in ip:
            flag = 0
            # flag2 = 0
            session = []
            for i, start, fin in ipANDTimeStamps:
                if str(i) == str(currIP):
                    if flag == 0:
                        lastFinish = fin
                        flag = 1
                        session.append((i, start, fin))
                        print session
                    else:
                        if (start - lastFinish).total_seconds() <= sessionTime:
                            session.append((i, start, fin))
                            lastFinish = fin
                        else:
                            # flag2 = 1
                            sameSession.append(session)
                            session = []
                            session.append((i, start, fin))
                            lastFinish = fin
            if session:
                sameSession.append(session)
                # print session
        return sameSession
        """print 'Printing sessions:'
        for session in sameSession:
            print '********************************************************************************************************************'
            print 'NEW SESSION!!!!'
            for i, start, fin in session:
                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                print 'ip = ' + i
                print 'start time = ' + str(start)
                print 'finish time = ' + str(fin)
                print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'END OF SESSION!!!!'
            print '********************************************************************************************************************'
        """


def startAnalyzingAmountsGraphData():
    print 'Starting to analize the amounts graph data from the model'
    fileName = MyModel.getFilename()
    IPAndContributionsCount(fileName)


def sessionsSplit():
    print 'Starting to split the data from our model to sessions'
    fileName = MyModel.getFilename()
    sessions = getIPAndTimeStamps(fileName, MyModel.getSizeOfSessionInSeconds())  # 30 minutes, 60 seconds per minutes
    print 'Writing sessions into csv file'
    with open(MyModel.getSessionsFilename(), 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['Session ID', 'IP', 'Start time', 'End time'])
        sid = 0
        for s in sessions:
            for ip, start, fin in s:
                cwriter.writerow([sid, ip, start, fin])
            sid = sid + 1
    print 'writing the sessions info file'
    with open('sessionsInfo.csv', 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['Session ID', 'IP', 'Number of works in session'])
        sid = 0
        for s in sessions:
            cwriter.writerow([sid, s[0][0], len(s)])
            sid = sid + 1
    print 'calculating the sessions per ip vector'
    sessionsPerIP = []
    for s in sessions:
        flag = 0
        for i in range(len(sessionsPerIP)):
            if s[0][0] == sessionsPerIP[i][0]:
                sessionsPerIP[i][1] = str(int(sessionsPerIP[i][1]) + 1)
                flag = 1
        if flag == 0:
            sessionsPerIP.append([s[0][0], '1'])
    print 'writing the file sessions per ip: '
    with open(MyModel.getSessionsPerIPFilename(), 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['IP', 'Number of sessions'])
        for s in sessionsPerIP:
            cwriter.writerow([s[0], s[1]])

def getIPAndLevelData(filename):
    print 'Starting to get ip and level data'
    with open(filename, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        print 'Now getting the ip, level and data of each user who gave us information'
        ipLevelAndData = []
        for row in creader:
            rowIP, startTime, finishTime, levelName, duration, score = MyModel.getInfoAboutRow(row)
            flag = 0

            stars = MyModel.getAmountOfStarsAchived(levelName, score)
            passedOneStar = False
            if (stars >= 1):
                passedOneStar = True

            for i in range(len(ipLevelAndData)):
                if(ipLevelAndData[i][0] == rowIP and ipLevelAndData[i][1] == levelName):
                    # update num of contributions
                    ipLevelAndData[i][2] = ipLevelAndData[i][2] + 1
                    # update total duration
                    ipLevelAndData[i][3] = ipLevelAndData[i][3] + duration
                    # update high score
                    if(ipLevelAndData[i][4] < score):
                        ipLevelAndData[i][4] = score
                    # update max stars
                    if (ipLevelAndData[i][5] < stars):
                        ipLevelAndData[i][5] = stars
                    # update exploited?
                    if(ipLevelAndData[i][8] == False):
                        if(ipLevelAndData[i][7] == True):
                            if(passedOneStar == True):
                                ipLevelAndData[i][8] = True
                            else:
                                if(ipLevelAndData[i][6] < finishTime):
                                    ipLevelAndData[i][8] = True
                        else:
                            if(passedOneStar == True):
                                if(ipLevelAndData[i][6] > finishTime):
                                    ipLevelAndData[i][8] = True
                                else:
                                    ipLevelAndData[i][7] = True
                                    ipLevelAndData[i][6] = finishTime
                            else:
                                if (ipLevelAndData[i][6] < finishTime):
                                    ipLevelAndData[i][6] = finishTime

                    flag = 1
                    break
            if(flag == 0):
                ipLevelAndData.append([rowIP, levelName, 1, duration, score, stars, finishTime, passedOneStar, False])
                # 0.ip, 1.levelName, 2.numOfContributions, 3.duration, 4.highestScore, 5.maxStars, 6.earliestFinishTimePassedOrLatestFinishTimeNotPassed, 7.passedOneStar, 8.exploited?
        return ipLevelAndData

def createAveragePerLevelForEachIP(ipLevelData):
    print 'now creating an average of all of the parameters needed'
    ipAveragePerLevelData = []
    for row in ipLevelData:
        flag = 0
        for i in range(len(ipAveragePerLevelData)):
            if(row[0] == ipAveragePerLevelData[i][0]):
                ipAveragePerLevelData[i][1] = ipAveragePerLevelData[i][1] + row[2]
                ipAveragePerLevelData[i][2] = ipAveragePerLevelData[i][2] + row[3]
                ipAveragePerLevelData[i][3] = ipAveragePerLevelData[i][3] + row[4]
                ipAveragePerLevelData[i][4] = ipAveragePerLevelData[i][4] + row[5]
                if(row[8] == True):
                    ipAveragePerLevelData[i][5] = ipAveragePerLevelData[i][5] + 1
                ipAveragePerLevelData[i][6] = ipAveragePerLevelData[i][6] + 1

                flag = 1
                break
        if(flag == 0):
            exploited = 0
            if(row[8] == True):
                exploited = 1
            ipAveragePerLevelData.append([row[0], float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(exploited), 1])
            #                              0.ip,1.contributions, 2.duration, 3.score, 4.stars, 5.exploited amount, 6.levels amount

    for i in range(len(ipAveragePerLevelData)):
        levelsAmount = float(ipAveragePerLevelData[i][6])
        for j in range(len(5)):  # going from 1 to 5 in the parameters given (all but ip and levels amount)
            ipAveragePerLevelData[i][j + 1] = float(float(ipAveragePerLevelData[i][j + 1]) / levelsAmount)

    return ipAveragePerLevelData


def getIPSessionsAmount(sessionsFileName):
    print 'Starting to get ip sessions amount'
    with open(sessionsFileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        ipAndSessionsAmount = []
        for row in creader:
            ip = row[0]
            amount = row[1]
            ipAndSessionsAmount.append((ip, amount))

        return ipAndSessionsAmount


def mergeSessionsAndRegularDataPerIP(ipAveragePerLevel, ipSessionsAmount):
    print 'now merging the ipAveragePerLevel with the ipSessionsAmount'
    merged = []

    print 'Now sorting the ipAveragePerLevel by ip'
    ipAveragePerLevel.sort(key=lambda x: (x[0]))
    #0.ip,1.contributions, 2.duration, 3.score, 4.stars, 5.exploited amount, 6.levels amount

    print 'Now sorting the ipSessionsAmount by ip'
    ipSessionsAmount.sort(key=lambda x: (x[0]))
    #0.ip, 1.amountOfSessions

    for i in range(len(ipAveragePerLevel)):
        if ipAveragePerLevel[i][0] != ipSessionsAmount[i][0]:
            print 'something is bad!!!'
        else:
            merged.append((ipAveragePerLevel[i][0], ipAveragePerLevel[i][1], ipAveragePerLevel[i][2], ipAveragePerLevel[i][3], ipAveragePerLevel[i][4], ipAveragePerLevel[i][5], ipAveragePerLevel[i][6], ipSessionsAmount[1]))
            #                           0.ip,1.contributions, 2.duration, 3.score, 4.stars, 5.exploited amount, 6.levels amount, 7.sessionsAmount

    return merged

def analizeGroupsOfUsers():
    print 'Starting to analize the data from our model to different groups of users'
    filename = MyModel.getFilename()
    sessionsFilename = MyModel.getSessionsPerIPFilename()
    ipLevelData = getIPAndLevelData(filename)  # done this
    ipAveragePerLevel = createAveragePerLevelForEachIP(ipLevelData)
    ipSessionsAmount = getIPSessionsAmount(sessionsFilename)
    merged = mergeSessionsAndRegularDataPerIP(ipAveragePerLevel, ipSessionsAmount)
    writeAllOfTheMergedDataToCSV(merged)


print 'Starting program'
sessionsSplit()
#startAnalyzingAmountsGraphData()
#analizeGroupsOfUsers()

print 'done'


















