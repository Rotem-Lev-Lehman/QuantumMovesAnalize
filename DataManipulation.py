import sys
import csv
from dateutil.parser import parse
from datetime import datetime
import json
from pprint import pprint

csv.field_size_limit(sys.maxsize)  # used so the size limit exception will not pop up...


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
            # row[0] is the users ip, we will save that data so we can manipulate it now
            ip.append(row[0])
        ipAndNumOfWorks, maxAmount = getIPAndNumOfWorksANDMaxAmount(ip)
        amountsVec = createAmountVec(ipAndNumOfWorks, maxAmount)
        removeLeadersByXPersentAndWriteEveryThingToCSV(ipAndNumOfWorks, amountsVec, 10)  # 10 persent


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


def getIPAndTimeStamps(fileName, sessionTime):
    with open(fileName, 'rb') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        a = creader.next()  # get rid of the first row (instructions...)
        print 'Now getting the ip of each user who gave us information'
        ipANDTimeStamps = []
        ip = []
        for row in creader:
            # row[0] is the users ip, we will save that data so we can manipulate it now
            if row[0] not in ip:
                ip.append(row[0])
            fin = row[3]  # hit_createdAt
            start = row[7]  # session_createdAt
            f = parse(fin)
            s = parse(start)
            ipANDTimeStamps.append((row[3], s, f))
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


def startAnalyzing():
    print 'Starting to analize the data from "All_EtchACellData_WithoutNames.csv"'
    fileName = 'QuantumMoves_180306.csv'
    # fileName = 'Relevent_Rows_Only_From_All_EtchACellData_WithoutNames.csv'
    # newFileName = createFileWithOnlyReleventRows(fileName)
    # newFileName = 'Relevent_Rows_Only_From_All_EtchACellData_WithoutNames.csv'
    IPAndContributionsCount(fileName)


# print 'TimeStamps handlling'
# data = getInfoAboutTimeStamps(newFileName)
# writeInfoAboutTimeStampsToCSV(data)

def sessionsSplit():
    print 'Starting to split the data from "QuantumMoves_180306.csv" to sessions'
    fileName = 'QuantumMoves_180306.csv'
    sessions = getIPAndTimeStamps(fileName, 1800)  # 30 minutes, 60 seconds per minutes
    print 'Writing sessions into csv file'
    with open('sessions.csv', 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['Session ID', 'IP', 'Start time', 'End time'])
        sid = 0
        for s in sessions:
            for ip, start, fin in s:
                cwriter.writerow([sid, ip, start, fin])
            sid = sid + 1
    with open('sessionsInfo.csv', 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['Session ID', 'IP', 'Number of works in session'])
        sid = 0
        for s in sessions:
            cwriter.writerow([sid, s[0][0], len(s)])
            sid = sid + 1
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
    with open('sessionsPerIP.csv', 'wb') as csvfile:
        cwriter = csv.writer(csvfile, delimiter=',')
        cwriter.writerow(['IP', 'Number of sessions'])
        for s in sessionsPerIP:
            cwriter.writerow([s[0], s[1]])


print 'Starting program'
# sessionsSplit()
# startAnalyzing()
# print parse('2016-05-07 21:03:42.338 UTC') - parse('2016-05-07 01:30:48.119 UTC')
x = '2016-05-07 11:04:35.399 UTC'
date = x.split(" ")[0]
timezone = x.split(" ")[2]
y = 0.4893827
xp = parse(x)
ym = y * 10  # look at : 'from datetime import timedelta'
yms = date + " " + "00:00:" + str(ym) + " " + timezone
yparsed = parse(yms)
print str(yparsed)
print str(xp)
print str(xp - yparsed)
print 'done'


















