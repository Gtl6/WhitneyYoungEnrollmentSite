import psycopg2
import hashlib
import ast
from datetime import datetime
from django.core.mail import send_mail

# NOTE! WHEN BUILDING ADD_STUDENTS FUNCTION, BE SURE TO ENTER EMPTY STRINGS IN UNUSED FIELDS, OR 0. ONLY NULL IN THE BOOLEANS.
# ALSO CHANGE THE DEBUG VAL WHEN YOU GO INTO IMPLEMENTATION
debug = False


# A basic function that connects to the local db
def connectToServer():
    try:
        conn = psycopg2.connect("dbname='enrolldb' user='Griftor05' host='wyenrollerinstance.cot5rtd7flb9.us-east-1.rds.amazonaws.com' password='Snorelax22'")
        if debug:
            print("Successfully connected to the db!")

        conn.autocommit = True
        return conn
    except:
        if debug:
            print("I couldn't connect to the db!")


# takes in a string and a list of strings, appends each item in the list to the string with a ', ' in between
# used for the csvDump() function to make a csv-esque string to be written to a file
# returns the items appended onto the string
def appendsy(stringer, listy):
    for i in listy:
        stringer += str(i) + ', '
    stringer += '<LEAVE EMPTY> ,'
    return stringer


# Simply grabs the student from the database based on their username
def grabStudentSurvey(username):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT * FROM enroller_student WHERE username='" + username + "';"
    cur.execute(pushStr)
    return cur.fetchall()[0]


# pulls in the index-th item from the 'survey' (provided list)
# returns whatever is in the database slot
def getSurvey(listy, index):
    returner = "ERROR IMPORTING FROM DB"
    for survey in listy:
        if (survey[0] == index):
            returner = survey
    return returner


# pulls in data for rendering a survey page, essentially builds the context for the page
def contextRenderEngine(dbName, username, nameAndRadioList):
    returner = []
    conn = connectToServer()
    cur = conn.cursor()

    # First you have to pull in the data from the student db, and fetch the survey based on that
    strOrigins = "SELECT " + dbName + "_id FROM enroller_student WHERE username='" + username + "';"
    cur.execute(strOrigins)
    student = cur.fetchall()
    id = student[0][0]

    # Then pull in data
    str1 = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME ='enroller_" + dbName + "';"
    str2 = "SELECT * FROM enroller_" + dbName + " WHERE id=" + str(id) + ";"
    cur.execute(str1)
    dbInfo = cur.fetchall()
    cur.execute(str2)
    dbValues = cur.fetchall()[0]

    # Also create a separate list with just the id keys in it
    i = 0
    idKeys = []
    for name in dbInfo:
        if '_id' in name[3]:
            idKeys.append(dbValues[i])
        i += 1

    # Three vars.
    idOffset = 0 # one to keep track of the position in the idKeys list
    i = 0 # one to keep track of position in the nameAndRadioList list
    listLen = len(nameAndRadioList)
    valsPulled = 2 # one to keep track of position in the pulled DB info

    # Looper to build context
    while i < listLen:
        doIt = True
        entry = []
        tag = nameAndRadioList[i]

        #Checks for each tag type. Refer to the templateLangGuide for an explanation of the tag types.

        if tag == '*a':
            entry.append('Address')
            entry.append(nameAndRadioList[i + 1])
            i += 1
            valsPulled -= 1

            str3 = "SELECT * FROM enroller_address WHERE id=" + str(idKeys[idOffset]) + ";"
            idOffset += 1
            cur.execute(str3)
            myAddress = cur.fetchall()[0]
            entry.append(myAddress[1])
            entry.append(myAddress[2])
            entry.append(myAddress[3])
            entry.append(myAddress[4])
            entry.append(myAddress[5])

            # Pull in data from address db, using the $tagOffset primary key, and the label of the next tag

        elif tag == '*n':
            entry.append('Number')
            i += 1
            entry.append(nameAndRadioList[i]) # Grabs the max len of the number
            entry.append(nameAndRadioList[i + 1]) # Grabs the name of the data item for the page
            i += 1

            entry.append(dbValues[valsPulled])

        elif tag == '*b':
            entry.append('Boolean')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            entry.append(dbValues[valsPulled])

        elif tag == '*c':
            entry.append('Country List')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            entry.append(dbValues[valsPulled])

        elif tag == '*d':
            entry.append('Date')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            myDate = str(dbValues[valsPulled])

            if myDate != 'None':
                myDate = myDate[5:7] + '/' + myDate[8:10] + '/' + myDate[0:4]

            entry.append(myDate)

        elif tag == '*g':
            entry.append('Guardian')
            entry.append(nameAndRadioList[i + 1])
            i += 1
            valsPulled -= 1

            str3 = "SELECT * FROM enroller_guardian WHERE id=" + str(idKeys[idOffset]) + ";"
            idOffset += 1
            cur.execute(str3)
            myGuardian = cur.fetchall()[0]
            entry.append(myGuardian[1])
            entry.append(myGuardian[2])
            entry.append(myGuardian[3])
            entry.append(myGuardian[4])
            entry.append(myGuardian[5])
            entry.append(myGuardian[6])

            # 6 - 10 is an address, pull first address from the Guardian, should be the only address available, in the last index
            homeAddress = myGuardian[len(myGuardian) - 1]
            str4 = "SELECT * FROM enroller_address where id=" + str(homeAddress) + ";"
            cur.execute(str4)
            homeAddress = cur.fetchall()[0]

            entry.append(homeAddress[1]) # 6
            entry.append(homeAddress[2]) # 7
            entry.append(homeAddress[3]) # 8
            entry.append(homeAddress[4]) # 9
            entry.append(homeAddress[5]) # 10

            # the rest are just from the Guardian survey, 13-18
            entry.append(myGuardian[7]) # 11
            entry.append(myGuardian[8]) # 12
            entry.append(myGuardian[9]) # 13
            entry.append(myGuardian[10]) # 14
            entry.append(myGuardian[11]) # 15
            entry.append(myGuardian[12]) # 16
            entry.append(myGuardian[13]) # 17

        elif tag == '*t':
            entry.append('Title')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            valsPulled -= 1

        elif tag == '*ut':
            entry.append('Underlined Title')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            valsPulled -= 1

        elif tag == '*v':
            entry.append('Verification Checkbox')
            entry.append(nameAndRadioList[i + 1])
            i += 1

            entry.append(dbValues[valsPulled])

        # Next one just checks if the thing is a radio list
        elif ((listLen - i) > 1) and (type(nameAndRadioList[i + 1]) == type([])):
            entry.append('Radio List')
            entry.append(nameAndRadioList[i])
            i += 1

            entry.append(nameAndRadioList[i])
            entry.append(dbValues[valsPulled])

        # Catch all is a String input
        else:
            # Have to check if it's a db name first though
            if(nameAndRadioList[i][0] != '#'):
                entry.append('String Input')
                entry.append(nameAndRadioList[i])

                entry.append(dbValues[valsPulled])
            else:
                doIt = False
                valsPulled -= 1

        if(doIt):
            returner.append(entry)
        i += 1
        valsPulled += 1


    return returner


# generates a csv file based off of the local data table
# creates a csv file local to where the script is
# Actually I don't want to use this function
# But it took so long to write, I'm keeping it until final rollout
'''
def csvDump():

    conn = connectToServer()
    cur = conn.cursor()
    cur.execute("SELECT * from enroller_student")
    students = cur.fetchall()
    cur.execute("SELECT * from enroller_address")
    addresses = cur.fetchall()
    cur.execute("SELECT * from enroller_contactsurvey")
    contactSurveys = cur.fetchall()
    cur.execute("SELECT * from enroller_emergencyandhealthinfo")
    emergencyAndHealthSurveys = cur.fetchall()
    cur.execute("SELECT * from enroller_guardian")
    guardians = cur.fetchall()
    cur.execute("SELECT * from enroller_homelanguagesurvey")
    homeLanguageSurveys = cur.fetchall()
    cur.execute("SELECT * from enroller_mainsurvey")
    mainSurveys = cur.fetchall()
    cur.execute("SELECT * from enroller_mediaconsentform")
    mediaConsentForms = cur.fetchall()
    cur.execute("SELECT * from enroller_previousschoolsurvey")
    previousSchoolSurveys = cur.fetchall()
    cur.execute("SELECT * from enroller_raceandethnicitysurvey")
    raceAndEthnicitySurvey = cur.fetchall()

    finalReport = []

    # The layout of the model to be converted to csv will be
    # Line 1: The names of the columns
    # For each survey, there is a seperate row of data
    # To add a survey, insert a break ('', ) followed by the data names
    # To add a new data entry, stick it in the form where it's found, and make sure the function that pulls the data pulls the correct value for the correct column. Otherwise everything will be very ugly.
    # If the data doesn't make it obvious what the survey is, include a comment (write polite code, if you please)
    line1 = ['Student Name', 'Student ID Number',
             '', 'Main Survey Finished', 'Generation', 'Gender', 'Entry Grade', 'Birth Certificate on File',
             'Birth Verification Type', 'Birth Country', 'Birth Date', 'Birth City', 'First US Enrollment date',
             'Number of years of US schooling', 'Date Entered US', 'Refugee Status', 'Refugee Country',
             '', 'Home Language Survey Finished', 'Survey Language', 'Home language other than English spoken',
             'Home language other than English', 'Student Speaks language other than English', 'Student other language',
             '', 'Race and ethnicity survey finished', 'race',
             '', 'Media consent form finished', 'Consented to recording?',
             '', 'Contact survey completed?', 'Student Home Phone #', 'Physical Address Street # and Name',
             'Physical Address Apartment #', 'Physical Address City', 'Physical Address State', 'Physical Address Zipcode',
             'Mailing Address Street # and Name', 'Mailing Address Apartment #', 'Mailing Address City',
             'Mailing Address State', 'Mailing Address Zipcode',
             '', 'Previous school survey complete', 'School transferred From', 'Old School Street Address',
             'Old School City', 'Old School State', 'Old School Zip Code', 'Student in Good standing at old school',
             'Last public school attended', 'Special Ed services', 'Enroller guardian name',
             'Enroller guardian relationship', 'Enroller guardian signed', 'Date form filled out',
             '', 'Emergency and health info survey complete', 'Living arrangement',
             'Order of Protection or No Contact Order', 'Guardian 1 name', 'Guardian 1 relationship',
             'Guardian 1 lives with student', 'Guardian 1 gets student\'s mail', 'Guardian 1 emergency contact',
             'Guardian 1 pickup permission', 'Guardian 1 home phone #', 'Guardian 1 cell phone #',
             'Guardian 1 email address', 'Guardian 1 name of employer', 'Guardian 1 Work Phone #',
             'Guardian 1 Communication Language', 'Guardian 2 name', 'Guardian 2 relationship',
             'Guardian 2 lives with student', 'Guardian 2 gets student\'s mail', 'Guardian 2 emergency contact',
             'Guardian 2 pickup permission', 'Guardian 2 home phone #', 'Guardian 2 cell phone #',
             'Guardian 2 email address', 'Guardian 2 name of employer', 'Guardian 2 Work Phone #',
             'Guardian 2 Communication Language', 'Doctor Name', 'Doctor Phone #', 'Student Health Insurance',
             'Illinois Medical Card ID', 'Guardian member of Armed Forces', 'Guardian expecting to be deployed',
             'Information certified', 'Date form was filled out',
             ]

    line1 = str(line1)
    line1 = line1[1:len(line1) - 1]

    finalReport.append(line1)

    # For each of the lines after that, start with the student, and build it out from there
    for myStudent in students:
        nextLine = ""
        myMain = getSurvey(mainSurveys, myStudent[7])
        myHomeLang = getSurvey(homeLanguageSurveys, myStudent[6])
        myRaceAndEthnicity = getSurvey(raceAndEthnicitySurvey, myStudent[10])
        myMediaConsentForm = getSurvey(mediaConsentForms, myStudent[8])
        myContactSurvey = getSurvey(contactSurveys, myStudent[4])
        myPreviousSchoolSurvey = getSurvey(previousSchoolSurveys, myStudent[9])
        myEmergencyAndHealthInfoSurvey = getSurvey(emergencyAndHealthSurveys, myStudent[5])

        # Now for each of those surveys, pull each data item, and stick it into the item
        firstName = myMain[4]
        middleName = myMain[5]
        lastName = myMain[3]
        myID = myMain[2]

        name = firstName + ' ' + middleName + ' ' + lastName
        nextLine = name + ', '
        nextLine = nextLine + myID + ', ,'

        # Main survey

        mainFin = myMain[1]
        generation = myMain[6]
        gender = myMain[7]
        entryGrade = myMain[8]
        birthCertOnFile = myMain[9]
        birthVerType = myMain[10]
        birthCountry = myMain[11]
        birthDate = myMain[12]
        birthCity = myMain[13]
        firstUSEnrollDate = myMain[14]
        numOfYearsUSSchooling = myMain[15]
        dateEnteredUSA = myMain[16]
        refugeeStatus = myMain[17]
        countryFromWhichStudentIsRefugee = myMain[18]

        mainSurveyForLine = [mainFin, generation, gender, entryGrade, birthCertOnFile, birthVerType, birthCountry,
                             birthDate, birthCity, firstUSEnrollDate, numOfYearsUSSchooling, dateEnteredUSA, refugeeStatus,
                             countryFromWhichStudentIsRefugee]

        nextLine = appendsy(nextLine, mainSurveyForLine)

        # Home language survey

        homeLangSurveyFin = myHomeLang[1]
        homeLangSurveyLang = myHomeLang[2]
        homeLangOtherThanEnglishSpoken = myHomeLang[3]
        homeLangOtherThanEnglish = myHomeLang[4]
        studentSpeaksLanguageOtherThanEnglish = myHomeLang[5]
        studentOtherLanguage = myHomeLang[6]

        homeLangSurveyForLine = [homeLangSurveyFin, homeLangSurveyLang, homeLangOtherThanEnglishSpoken,
                                 homeLangOtherThanEnglish, studentSpeaksLanguageOtherThanEnglish, studentOtherLanguage]

        nextLine = appendsy(nextLine, homeLangSurveyForLine)

        # Race and ethnicity

        raceAndEthnicitySurveyFinished = myRaceAndEthnicity[1]
        race = myRaceAndEthnicity[2]

        raceAndEthnicitySurveyForLine = [raceAndEthnicitySurveyFinished, race]

        nextLine = appendsy(nextLine, raceAndEthnicitySurveyForLine)

        # Media consent form

        mediaConsentFin = myMediaConsentForm[1]
        mediaConsentGiven = myMediaConsentForm[2]

        mediaConsentForLine = [mediaConsentFin, mediaConsentGiven]

        nextLine = appendsy(nextLine, mediaConsentForLine)

        # Contact Survey

        contactSurveyCompleted = myContactSurvey[1]
        contactSurveyHomePhone = myContactSurvey[2]

        # Pull in contact surveys
        myContactPhysicalAddress = getSurvey(addresses, myContactSurvey[4])
        myContactMailingAddress = getSurvey(addresses, myContactSurvey[3])

        physicalStreet = myContactPhysicalAddress[1]
        physicalApartment = myContactPhysicalAddress[2]
        physicalCity = myContactPhysicalAddress[3]
        physicalState = myContactPhysicalAddress[4]
        physicalZipCode = myContactPhysicalAddress[5]

        mailingStreet = myContactMailingAddress[1]
        mailingApartment = myContactMailingAddress[2]
        mailingCity = myContactMailingAddress[3]
        mailingState = myContactMailingAddress[4]
        mailingZipCode = myContactMailingAddress[5]

        contactSurveyForLine = (
        contactSurveyCompleted, contactSurveyHomePhone, physicalStreet, physicalApartment, physicalCity, physicalState,
        physicalZipCode, mailingStreet, mailingState, mailingApartment, mailingCity, mailingState, mailingZipCode)

        nextLine = appendsy(nextLine, contactSurveyForLine)

        # Previous school survey

        schoolSurveyFin = myPreviousSchoolSurvey[1]
        schoolTransferringFrom = myPreviousSchoolSurvey[2]
        studentInGoodStanding = myPreviousSchoolSurvey[3]
        lastPublicSchool = myPreviousSchoolSurvey[4]
        specialEdServices = myPreviousSchoolSurvey[5]
        enrollerGuardianName = myPreviousSchoolSurvey[6]
        enrollerGuardianRelationship = myPreviousSchoolSurvey[7]
        enrollerGuardianSigned = myPreviousSchoolSurvey[8]
        enrollmentDate = myPreviousSchoolSurvey[9]

        # Grab the previous school's address

        oldSchoolAddress = getSurvey(addresses, myPreviousSchoolSurvey[10])
        oldSchoolStreet = oldSchoolAddress[1]
        oldSchoolCity = oldSchoolAddress[3]
        oldSchoolState = oldSchoolAddress[4]
        oldSchoolZipCode = oldSchoolAddress[5]

        oldSchoolInfoForLine = [schoolSurveyFin, schoolTransferringFrom, oldSchoolStreet, oldSchoolCity, oldSchoolState,
                                oldSchoolZipCode, studentInGoodStanding, lastPublicSchool, specialEdServices,
                                enrollerGuardianName, enrollerGuardianRelationship, enrollerGuardianSigned, enrollmentDate]

        nextLine = appendsy(nextLine, oldSchoolInfoForLine)

        # Emergency Health Survey
        emergencyHealthFin = myEmergencyAndHealthInfoSurvey[1]
        confBox1 = myEmergencyAndHealthInfoSurvey[2]
        confBox2 = myEmergencyAndHealthInfoSurvey[3]

        # Pull up guardians
        guardian1 = getSurvey(guardians, myEmergencyAndHealthInfoSurvey[12])
        guardian2 = getSurvey(guardians, myEmergencyAndHealthInfoSurvey[13])

        guardianName = guardian1[1]
        guardianRelationship = guardian1[2]
        guardianLivesWith = guardian1[3]
        guardianGetsMailings = guardian1[4]
        guardianEmergency = guardian1[5]
        guardianPermissionToPickup = guardian1[6]
        guardianHomePhoneNumber = guardian1[7]
        guardianCellPhoneNumber = guardian1[8]
        guardianEmailAddress = guardian1[9]
        guardianNameofEmployer = guardian1[10]
        guardianWorkPhoneNumber = guardian1[11]
        guardianWorkCommunicationLang = guardian1[12]
        guardian2Name = guardian2[1]
        guardian2Relationship = guardian2[2]
        guardian2LivesWith = guardian2[3]
        guardian2GetsMailings = guardian2[4]
        guardian2Emergency = guardian2[5]
        guardian2PermissionToPickup = guardian2[6]
        guardian2HomePhoneNumber = guardian2[7]
        guardian2CellPhoneNumber = guardian2[8]
        guardian2EmailAddress = guardian2[9]
        guardian2NameofEmployer = guardian2[10]
        guardian2WorkPhoneNumber = guardian2[11]
        guardian2WorkCommunicationLang = guardian2[12]

        # Other info
        doctorName = myEmergencyAndHealthInfoSurvey[4]
        doctorPhoneNumber = myEmergencyAndHealthInfoSurvey[5]
        studentHealthInsurance = myEmergencyAndHealthInfoSurvey[6]
        illinoisMedicalCardID = myEmergencyAndHealthInfoSurvey[7]
        guardianArmedForces = myEmergencyAndHealthInfoSurvey[8]
        guardianExpectingDeployment = myEmergencyAndHealthInfoSurvey[9]
        infoCertified = myEmergencyAndHealthInfoSurvey[10]
        dateFormFilledOut = myEmergencyAndHealthInfoSurvey[11]

        emergencyHealthForLine = [emergencyHealthFin, confBox1, confBox2, guardianName, guardianRelationship,
                                  guardianLivesWith, guardianGetsMailings, guardianEmergency, guardianPermissionToPickup,
                                  guardianHomePhoneNumber, guardianCellPhoneNumber, guardianEmailAddress,
                                  guardianNameofEmployer, guardianWorkPhoneNumber, guardianWorkCommunicationLang,
                                  guardian2Name, guardian2Relationship, guardian2LivesWith, guardian2GetsMailings,
                                  guardian2Emergency, guardian2PermissionToPickup, guardian2HomePhoneNumber,
                                  guardian2CellPhoneNumber, guardian2EmailAddress, guardian2NameofEmployer,
                                  guardian2WorkPhoneNumber, guardian2WorkCommunicationLang, doctorName, doctorPhoneNumber,
                                  studentHealthInsurance, illinoisMedicalCardID, guardianArmedForces,
                                  guardianExpectingDeployment, infoCertified, dateFormFilledOut]

        nextLine = appendsy(nextLine, emergencyHealthForLine)

        # Putting the line into the final doc
        finalReport.append(nextLine)

    return finalReport
'''

# check to see if a student is A) already in the database, and B) has already registered
# returns a list where the first bool tells A), the second bool tells B)
def validateRegToken(token):
    conn = connectToServer()
    cur = conn.cursor()
    cur.execute("SELECT * from enroller_student;")
    profs = cur.fetchall()
    found = False
    alreadyRegistered = False
    for usr in profs:
        if usr[1] == token:
            found = True
            if usr[2] != '':
                alreadyRegistered = True

    return [found, alreadyRegistered]


# Hashes a password using the username and password in combination
def superHash(pwd, usrn):
    for timz in range(0, 100000):
        usrn = hashlib.md5(usrn.encode('UTF-8')).hexdigest()
        pwd = hashlib.md5((pwd + usrn).encode('UTF-8')).hexdigest()
    return pwd


# Add the student's username and password (hashed, salted, and peppered, of course) to the database
def registerStudent(usrn, pwd, token):
    # For super security do a hash with a salt and pepper based on the username and password
    pwd = superHash(pwd, usrn)

    con = connectToServer()
    curs = con.cursor()
    cmd = 'UPDATE enroller_student SET username= \'%s\', password=\'%s\' WHERE "activationcode"=\'%s\';' %(usrn, pwd, token)
    curs.execute(cmd)
    curs.execute('COMMIT;')


# checks the login data against the server's data, returns a pair of bools
# bools[0] is whether the username is in the db
# bools[1] is whether the password is in the db with that username, defaults to false if no username
def checkLoginData(username, password, type):
    conn = connectToServer()
    cur = conn.cursor()
    if type =='admin':
        getStr = "SELECT * from enroller_admin"
        usnNum = 1
        pwdNum = 2
    elif type == 'normal':
        getStr = "SELECT * from enroller_student"
        usnNum = 2
        pwdNum = 3
    else:
        raise Exception('Expected \'type\' var to be either \'normal\' or \'admin\', got \'' + type + '\'')

    cur.execute(getStr)
    profs = cur.fetchall()
    found = False
    passwordMatch = False
    locked = False

    for usr in profs:
        if usr[usnNum] == username.strip():
            found = True
            if usr[pwdNum] == password.strip():
                passwordMatch = True
            else:
                passwordMatch = False
            if type == 'normal':
                locked = usr[-3]

    returner = [found, passwordMatch, locked]
    return returner


# This should deal with colons, escape chars, and anything else that could throw our shit for a loop
def scrubber(myData):
    for key, data in myData.items():
        if len(data) == 1:
            data = data[0]
            if "'" in data:
                myData[key] = [data.replace("'", "''")]
            elif "\\" in data:
                myData[key] = [data.replace("\\", "\\\\")]

    return myData


# Checks to see if a survey is complete, based on the data provided
# Really just checks to see if the length is appropriate
def checkDone(data, db, usn):
    conn = connectToServer()
    cur = conn.cursor()

    # These numbers are the general lengths the surveys should be to be complete
    # It is technically possible to go over these without filling out certain boxes
    # But that's a negligible test case for right now
    checkDict = {'mainsurvey':14, 'contactsurvey':6, 'homelanguagesurvey':3, 'emergencyandhealthinfo':45,
                 'mediaconsentform':1, 'previousschoolsurvey':10, 'raceandethnicitysurvey':1}
    posDict = {'mainsurvey':7 , 'contactsurvey':4, 'homelanguagesurvey': 6, 'emergencyandhealthinfo': 5,
                 'mediaconsentform': 8, 'previousschoolsurvey': 9, 'raceandethnicitysurvey': 10}

    actualData = {}
    for name, answer in data.items():
        if answer != [''] and name != 'csrfmiddlewaretoken':
            actualData[name] = answer

    # First gotta pull the id number of the survey we want
    studentSurvey = grabStudentSurvey(usn)
    idNum = studentSurvey[posDict[db]]

    tf = False
    if len(actualData) > checkDict[db] or len(actualData) == checkDict[db]:
        tf = True

    pushStr = "UPDATE enroller_" + db + " SET \"surveyCompleted\"=" + str(tf) + " WHERE id='" + str(idNum) + "';"
    cur.execute(pushStr)
    conn.commit()

# Check to see if the address in the contactSurvey has been changed
def checkContactChanged(data, db, usn):
    if(db == 'contactSurvey'):
        conn = connectToServer()
        cur = conn.cursor()

        # get the data already in the db
        student = grabStudentSurvey(usn)
        surveyId = student[4]

        pushStr = "SELECT \"mailingAddress_id\" FROM enroller_contactsurvey WHERE id=" + str(surveyId) + ";"
        cur.execute(pushStr)
        contactMailingAddress = cur.fetchall()[0][0]

        pushStr = "SELECT * FROM enroller_address WHERE id=" + str(contactMailingAddress) + ";"
        cur.execute(pushStr)
        myAddress = cur.fetchall()[0]

        # Now grab the info you collected from the page itself
        addressNameList = ['nameNumber', 'apartmentNo', 'city', 'state', 'zipCode']
        collectedInfo = []

        for name in addressNameList:
            name = 'Student\'s mailing address_' + name
            collectedInfo.append(data[name][0])

        collectedInfo = ['cupidshuffle'] + collectedInfo

        matchup = True
        for num in range(1, 6):
            if myAddress[num] != collectedInfo[num]:
                matchup = False

        if not matchup:
            pushStr = "UPDATE enroller_contactSurvey SET \"mailingAddressChanged\"=TRUE WHERE id=" + str(surveyId) + ";"
            cur.execute(pushStr)
            conn.commit()


# This function is the bane of my existence
# 'Simply' pushes data from the page to the given database
def pushDataToDb(dbName, username, data, namesAndRadioLists):
    conn = connectToServer()
    cur = conn.cursor()
    addressNameList = ['nameNumber', 'apartmentNo', 'city', 'state', 'zipCode']
    addressDBNameList = ['streetNumberAndName', 'apartmentNo', 'city', 'state', 'zipCode']
    guardianNameList = ['name', 'relationship', 'checks', 'address', 'homePhone', 'cellPhone',
                        'email', 'employer', 'workPhone', 'commLang']
    checksNameList = ['livesWith', 'getsMailings', 'emergency', 'permissionToPickup']
    guardianDBNameList = {'name': 'name', 'relationship': 'relationship', 'homePhone':'homePhoneNumber',
                          'cellPhone':'cellPhoneNumber', 'email':'emailAddress', 'employer':'nameOfEmployer',
                          'workPhone':'workPhoneNumber', 'commLang':'communicationLanguage'}
    namesAndRadioLists = ast.literal_eval(namesAndRadioLists)

    # First you have to pull in the data from the student db, and fetch the survey based on that
    strOrigins = "SELECT " + dbName + "_id FROM enroller_student WHERE username='" + username + "';"
    cur.execute(strOrigins)
    student = cur.fetchall()
    id = student[0][0]

    # Then pull in data
    str1 = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME ='enroller_" + dbName + "';"
    str2 = "SELECT * FROM enroller_" + dbName + " WHERE id=" + str(id) + ";"
    cur.execute(str1)
    dbInfo = cur.fetchall()
    cur.execute(str2)
    dbValues = cur.fetchall()[0]

    # Also create a separate list with just the id keys in it
    i = 0
    idKeys = []
    for name in dbInfo:
        if '_id' in name[3]:
            idKeys.append(dbValues[i])
        i += 1

    # Three vars.
    idOffset = 0  # one to keep track of the position in the idKeys list
    i = 0  # one to keep track of position in the nameAndRadioList list
    listLen = len(namesAndRadioLists)
    valsPulled = 2  # one to keep track of position in the pulled DB info

    # Create a dictionary of my data
    myData = {}
    for key in data.keys():
        myData[key] = data.getlist(key)

    # Don't forget to scrub your data! I don't deal with dirty data.
    myData = scrubber(myData)

    # Check to see if the survey is now complete
    checkDone(myData, dbName, username)
    # And check to see if the contactsurvey address has changed
    checkContactChanged(myData, dbName, username)

    # And now the actual submitting part
    while i < listLen:
        item = namesAndRadioLists[i]

        if item == '*a':
            i += 1

            #Get the name of the address
            nameOfAddress = namesAndRadioLists[i]

            #Get the correct table entry
            myAddressId = idKeys[idOffset]
            idOffset += 1
            i += 1

            # use a for list with the list of items for an address list
            for j in range(0, len(addressNameList)):
                # First get the name of the dictEntry
                entryName = nameOfAddress + '_' + addressNameList[j]

                # Then grab the item from the dictionary
                dataItem = myData.get(entryName)

                if dataItem is not None:
                    # Then build your string to push it to the db
                    pushStr = "UPDATE enroller_address SET \"" + addressDBNameList[j] + "\" = '" + dataItem[0] + "' WHERE \"id\" = " + str(myAddressId) + ";"

                    # Then push it, I guess
                    cur.execute(pushStr)
                    conn.commit()

        elif item == '*b' or item == '*c':
            i += 1
            nameOfItem = namesAndRadioLists[i]
            dataItem = myData.get(nameOfItem)
            i += 1
            dataColumn = namesAndRadioLists[i]

            if dataItem is not None:
                pushStr = "UPDATE enroller_" + dbName + " SET \"" + dataColumn[1:] + "\" = '" + dataItem[0] + "' WHERE id=" + str(id) + ";"

                cur.execute(pushStr)
                conn.commit()

        elif item == '*d':
            i += 1
            nameOfItem = namesAndRadioLists[i] + '_date'
            dataItem = myData.get(nameOfItem)
            dataItem = dataItem[0]
            i += 1
            dataColumn = namesAndRadioLists[i]

            if dataItem == '' or dataItem == 'None' or dataItem == 'null':
                pushStr = "UPDATE enroller_" + dbName + " SET \"" + dataColumn[1:] + "\" = NULL WHERE id=" + str(id) + ";"
            else:
                pushStr = "UPDATE enroller_" + dbName + " SET \"" + dataColumn[1:] + "\" = '" + dataItem + "' WHERE id=" + str(id) + ";"

            cur.execute(pushStr)
            conn.commit()

        elif item == '*g':
            i += 1

            # Get the name of the guardian
            nameOfGuardian = namesAndRadioLists[i]

            # Get the correct table entry
            myGuardianId = idKeys[idOffset]
            idOffset += 1
            i += 1

            # Then get the address that's referred to in the Guardian entry
            getStr = "SELECT * FROM enroller_guardian WHERE id=" + str(myGuardianId) + ";"

            cur.execute(getStr)
            currentGuardian = cur.fetchall()[0]

            homeAddressID = currentGuardian[len(currentGuardian) - 1]

            j = 0

            # Okay, we have the ids of the surveys we want to push through, and highly disorganized data
            while j < len(guardianNameList):
                nameOfThing = nameOfGuardian + '_' + guardianNameList[j]

                dataItem = myData.get(nameOfThing)

                # now that I have the piece of data, I have 3 options.
                # If it's a piece of guardian data, push it to guardian
                # if it's a piece of address data, push it to address
                # if it's a list, pull the data out, and push it to the guardian database

                if guardianNameList[j] == 'address':
                    for h in range(0, len(addressNameList)):
                        # First get the name of the dictEntry
                        entryName = nameOfGuardian + '_' + addressNameList[h]

                        # Then grab the item from the dictionary
                        dataItem = myData.get(entryName)

                        if dataItem is not None:
                            # Then build your string to push it to the db
                            pushStr = "UPDATE enroller_address SET \"" + addressDBNameList[h] + "\" = '" + dataItem[
                                0] + "' WHERE \"id\" = " + str(homeAddressID) + ";"

                            # Then push it, I guess
                            cur.execute(pushStr)
                            conn.commit()

                elif guardianNameList[j] == 'checks':
                    for checkListName in checksNameList:
                        # if the name is in the list
                        if dataItem is not None:
                            tf = checkListName in dataItem
                        else:
                            tf = False


                        pushStr = "UPDATE enroller_guardian SET \"" + checkListName + "\" = '" + str(tf) + \
                                      "' WHERE \"id\" = " + str(myGuardianId) + ";"

                        cur.execute(pushStr)
                        conn.commit()

                else:
                    nameInDb = guardianDBNameList.get(guardianNameList[j])

                    if dataItem is not None:
                        pushStr = "UPDATE enroller_guardian SET \"" + nameInDb + "\" = '" + dataItem[0] + \
                                      "' WHERE \"id\" = " + str(myGuardianId) + ";"

                        cur.execute(pushStr)
                        conn.commit()


                j += 1

        elif item == '*n':
            i += 2 # Can safely skip the maxlength attribute of the number
            toEnter = myData.get(namesAndRadioLists[i])
            i += 1
            nameInDb = namesAndRadioLists[i][1:]

            if toEnter is not None:
                toEnter = toEnter[0]

                pushStr = "UPDATE enroller_" + dbName + " SET \"" + nameInDb + "\" = '" + toEnter + \
                          "' WHERE \"id\" = " + str(id) + ";"

                cur.execute(pushStr)
                conn.commit()

        elif item == '*v':
            i += 1
            nameOfItem = namesAndRadioLists[i]
            dataItem = myData.get(nameOfItem + '_checkBox')
            i += 1
            dataColumn = namesAndRadioLists[i]

            if dataItem is not None:
                pushStr = "UPDATE enroller_" + dbName + " SET \"" \
                          + dataColumn[1:] + "\" = TRUE WHERE id=" + str(id) + ";"

                cur.execute(pushStr)
                conn.commit()
            else:
                pushStr = "UPDATE enroller_" + dbName + " SET \"" \
                          + dataColumn[1:] + "\" = FALSE WHERE id=" + str(id) + ";"

                cur.execute(pushStr)
                conn.commit()

        # Could be in a radio list
        elif i < listLen - 1 and type(namesAndRadioLists[i + 1]) == type([]):
                toEnter = myData.get(namesAndRadioLists[i] + "_radioList")
                i += 2
                nameInDb = namesAndRadioLists[i][1:]

                if toEnter is not None:
                    toEnter = toEnter[0]

                    pushStr = "UPDATE enroller_" + dbName + " SET \"" + nameInDb + "\" = '" + toEnter + \
                          "' WHERE \"id\" = " + str(id) + ";"

                    cur.execute(pushStr)
                    conn.commit()

        # Otherwise, it's a text box
        else:
            i += 1

            nameInDb = namesAndRadioLists[i][1:]

            toEnter = myData.get(item)

            if toEnter is not None:
                toEnter = toEnter[0]

                pushStr = "UPDATE enroller_" + dbName + " SET \"" + nameInDb + "\" = '" + toEnter + \
                          "' WHERE \"id\" = " + str(id) + ";"

                cur.execute(pushStr)
                conn.commit()

        i += 1


# This function will send out a password reset key
def sendPwdResetEmail(email):
    # First we need to check if the email actually exists in our db
    # Pull in db info
    conn = connectToServer()
    cur = conn.cursor()
    cur.execute("SELECT * from enroller_student WHERE \"username\"='" + email + "';")
    profs = cur.fetchall()
    if len(profs) == 0:
        return False
    else:
        # First need to generate a random activation key that isn't the same as anyone else's
        # Although fr, how likely is it we'll get any real collisions?
        # None if we just hash it, silly. Fine, I'll do a thing.
        hmm = "secretsAreNoFun" + str(datetime.now().time())
        token = superHash(email, hmm)[0:5]

        sub = 'Whitney Young Enrollment Password Reset Key'
        message = 'We recently received a request to change your Whitney Young Enrollment Password. If you requested' \
                  ' this change, enter your reset code below into the form to continue the reset process. \n\n' + token
        toEmails = [email]

        pushStr = "UPDATE enroller_student SET \"resetVal\"='" + token + "' WHERE \"username\"='" + email + "';"
        cur.execute(pushStr)
        conn.commit()

        send_mail(sub, message, 'wyregis@gmail.com', toEmails)

        return True


# Checks to see if the token is in the database
def checkTokenWithDb(token):
    conn = connectToServer()
    cur = conn.cursor()
    cur.execute("SELECT * from enroller_student WHERE \"resetVal\"='" + token + "';")
    profs = cur.fetchall()

    if len(profs) == 0 or token == '':
        return False
    else:
        # Then need to reset the field
        # Because otherwise hackers will do what they do best
        # Also need to make sure that the token entered isn't ''
        pushStr = "UPDATE enroller_student SET \"resetVal\"='' WHERE \"resetVal\"='" + token + "';"
        cur.execute(pushStr)
        conn.commit()
        return True


# Sets a new password in the database
def setNewPasswordInDb(pwd, usn):
    # For super security do a hash with a salt and pepper based on the username and password
    pwd = superHash(pwd, usn)

    conn = connectToServer()
    curs = conn.cursor()
    cmd = "UPDATE enroller_student SET password='" + pwd + "' WHERE username='" + usn + "';"
    curs.execute(cmd)
    conn.commit()


# Simply a helpfer function for my Create Student function, to make building lists easier
def nameCollapser(str1, listToAdd):
    for name in listToAdd:
        str1 += "\"" + name + "\", "

    return str1


# Creates a single student given a few specific variables, as specified by the input data given by Mr Soto
def createStudent(id, name, gender, grade, race, address, city, state, zip, parentName, relationshipToStudent, parentPhoneNumber):
    conn = connectToServer()
    cur = conn.cursor()

    # Create an activation code for the student
    hmm = "secretsAreTheEnemyOfPassion" + str(datetime.now().time())
    token = superHash(id, hmm)[0:7]

    #Then make sure all the items are insertable
    nameList = name.split()
    firstName = nameList[0]
    lastName = nameList[1]
    apt = ""
    if race == "Black":
        race = "Black or African American"
    if race == "Hispanic":
        race = "Hispanic or Latino"
    if '#' in address:
        address = address.split(" #")
        apt = address[1]
        address = address[0]

    # First, need to create 7 (count em) addresses
    # Pull in the topmost id
    cur.execute("SELECT MAX(id) FROM enroller_address;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    addressIds = []
    for n in range(0, 6):
        pushStr = "INSERT INTO enroller_address (\"id\", \"streetNumberAndName\", \"apartmentNo\", \"city\", \"state\"," \
                    " \"zipCode\") VALUES ('" + str(topId + n) + "', '', '', '', '', '') RETURNING id;"
        cur.execute(pushStr)
        conn.commit()
        thisId = cur.fetchall()[0][0]
        addressIds.append(thisId)

    # Then one more because it needs to be included for the Student's pulled data
    # This one is used in the contact survey mailing address
    # Also a check will need to be instituted to see whether the address was changed
    pushStr = "INSERT INTO enroller_address (\"id\", \"streetNumberAndName\", \"apartmentNo\", \"city\", \"state\"," \
              " \"zipCode\") VALUES ('" + str(topId + 6) + "', '" + address + "', '"
    pushStr += apt + "', '" + str(city) + "', '" + str(state) + "', '"
    pushStr += str(zip) + "') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    thisId = cur.fetchall()[0][0]
    addressIds.append(thisId)

    cur.execute("SELECT MAX(id) FROM enroller_guardian;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    guardianIds = []
    # Then need to create 3 Guardians, which all need addresses from our list
    for n in range(0, 3):
        pushStr = "INSERT INTO enroller_guardian ("
        columns = ['id', 'name', 'relationship', 'livesWith', 'getsMailings', 'emergency', 'permissionToPickup',
                   'homePhoneNumber', 'cellPhoneNumber', 'emailAddress', 'nameOfEmployer', 'workPhoneNumber',
                   'communicationLanguage', 'homeAddress_id']
        pushStr = nameCollapser(pushStr, columns)[0:-2]
        pushStr += ") VALUES ('" + str(topId + n) + "', '', '', null, null, null, null, "
        pushStr += "'', '', '', '', '', '', '" + str(addressIds[n]) + "') RETURNING id;"
        cur.execute(pushStr)
        conn.commit()
        thisId = cur.fetchall()[0][0]
        guardianIds.append(thisId)
    # Then each of the surveys for the kid

    cur.execute("SELECT MAX(id) FROM enroller_emergencyandhealthinfo;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    #Start with Emergency and Health because it's going to be a pain in the ass
    pushStr = "INSERT INTO enroller_emergencyandhealthinfo ("
    columns = ['id', 'surveyCompleted', 'confidentialInfoBox1', 'confidentialInfoBox2', 'doctorName', 'doctorPhoneNumber',
                'studentHealthInsurance', 'illinoisMedicalCardID', 'guardianArmedForces', 'guardianExpectingDeployment',
                'informationCertification', 'dateFormFilledOut', 'guardian1_id', 'guardian2_id', 'neighbor_id',
                'doctorAddress_id']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '', null, '', '', '', '', null, null, null, null, '" + str(guardianIds[0]) + "', '" \
               + str(guardianIds[1]) + "', '" + str(guardianIds[2]) + "', '" + str(addressIds[3]) + "') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    emergencyAndHealthId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_contactsurvey;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # contactSurvey
    pushStr = "INSERT INTO enroller_contactsurvey ("
    columns = ['id', 'surveyCompleted', 'homePhoneNumber', 'mailingAddress_id', 'physicalAddress_id',
               'mailingAddressChanged']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '" + str(parentPhoneNumber) + "', '" + str(addressIds[6])
    pushStr += "', '" + str(addressIds[5]) + "', false) RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    contactSurveyId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_homelanguagesurvey;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # homeLanguageSurvey
    pushStr = "INSERT INTO enroller_homelanguagesurvey ("
    columns = ['id', 'surveyCompleted', 'surveyLanguage', 'homeLanguageOtherThanEnglishSpoken',
               'homeLanguageOtherThanEnglish', 'studentSpeaksLanguageOtherThanEnglish', 'studentOtherLanguage']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '', null, '', null, '') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    homeLanguageSurveyId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_mainsurvey;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # mainSurvey
    pushStr = "INSERT INTO enroller_mainsurvey ("
    columns = ['id', 'surveyCompleted', 'studentID', 'lastName', 'firstName', 'middleName', 'generation',
               'gender', 'entryGrade', 'birthCertOnFile', 'birthVer', 'birthCountry', 'birthDate', 'birthCity',
               'firstUSEnrollDate', 'numYearsUSSchooling', 'dateEnteredUS', 'refugeeStatus', 'refugeeCountry']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '" + str(id) + "', '" + str(lastName) + "', '" + str(firstName)
    pushStr += "', '', '', '" + str(gender) + "', '" + str(grade)
    pushStr += "', null, '', '', null, '', null, '', null, null, '') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    mainSurveyId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_mediaconsentform;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # mediaConsentForm
    pushStr = "INSERT INTO enroller_mediaconsentform ("
    columns = ['id', 'surveyCompleted', 'consentToMedia']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, null) RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    mediaConsentFormId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_previousschoolsurvey;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # previousSchoolSurvey
    pushStr = "INSERT INTO enroller_previousschoolsurvey ("
    columns = ['id', 'surveyCompleted', 'schoolTransferringFrom', 'studentInGoodStanding', 'lastPublicSchool',
               'specialEdServices', 'enrollerGuardianName', 'enrollerGuardianRelationship',
               'enrollerGuardianSigned', 'enrollmentDate', 'oldSchoolAddress_id']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '', null, '', false, '" + parentName + "', '" + relationshipToStudent
    pushStr += "', false, null, '" + str(addressIds[4]) + "') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    previousSchoolSurveyId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_raceandethnicitysurvey;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # raceAndEthnicitySurvey
    pushStr = "INSERT INTO enroller_raceandethnicitysurvey ("
    columns = ['id', 'surveyCompleted', 'race']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', false, '" + str(race) + "') RETURNING id;"

    cur.execute(pushStr)
    conn.commit()
    raceAndEthnicitySurveyId = cur.fetchall()[0][0]


    cur.execute("SELECT MAX(id) FROM enroller_student;")
    topId = cur.fetchall()[0][0]

    if type(topId) == type(None):
        topId = 0

    topId += 1

    # Then bind each of the surveys themselves to a student
    pushStr = "INSERT INTO enroller_student ("
    columns = ['id', 'activationcode', 'username', 'password', 'contactsurvey_id', 'emergencyandhealthinfo_id',
               'homelanguagesurvey_id', 'mainsurvey_id', 'mediaconsentform_id', 'previousschoolsurvey_id',
               'raceandethnicitysurvey_id', 'accountLocked', 'resetVal', 'schoolId']
    pushStr = nameCollapser(pushStr, columns)[0:-2]
    pushStr += ") VALUES ('" + str(topId) + "', '" + str(token) + "', '', '', '" + str(contactSurveyId) + "', '" + str(emergencyAndHealthId)
    pushStr += "', '" + str(homeLanguageSurveyId) + "', '" + str(mainSurveyId) + "', '" + str(mediaConsentFormId)
    pushStr += "', '" + str(previousSchoolSurveyId) + "', '" + str(raceAndEthnicitySurveyId) + "', false, '"
    pushStr +=  "', '" + str(id) + "');"

    cur.execute(pushStr)
    conn.commit()

    # And voila! Just like that, you've got yourself a student!
    # Just return the student's activation code, and we're golden

    return token


# Deletes a single student based on which entry they are in the database
def deleteStudent(dbStudentEntryID):
    # It's actually far easier to delete a student than to create one. Go figure. I'm going to enjoy running this one.
    # First gotta pull in all the survey IDs
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT * FROM enroller_student WHERE id='" + str(dbStudentEntryID) + "';"

    cur.execute(pushStr)
    studentSurvey = cur.fetchall()[0]

    contactSurveyID = studentSurvey[4]
    emergencyAndHealthID = studentSurvey[5]
    homeLangID = studentSurvey[6]
    mainSurveyID = studentSurvey[7]
    mediaConsentID = studentSurvey[8]
    previousSchoolID = studentSurvey[9]
    raceAndEthnicityID = studentSurvey[10]

    # Then just have to gather in the various addresses and guardians
    # Let's just take care of guardians first
    guardianIDs = []
    for n in range(1, 3):
        pushStr = "SELECT guardian" + str(n) + "_id FROM enroller_emergencyandhealthinfo WHERE id='"
        pushStr += str(emergencyAndHealthID) + "';"
        cur.execute(pushStr)
        guardianIDs.append(cur.fetchall()[0][0])

    pushStr = "SELECT neighbor_id FROM enroller_emergencyandhealthinfo WHERE id='"
    pushStr += str(emergencyAndHealthID) + "';"
    cur.execute(pushStr)
    guardianIDs.append(cur.fetchall()[0][0])

    # And now for the addresses
    addressIDs = []

    pushStr = "SELECT \"doctorAddress_id\" FROM enroller_emergencyandhealthinfo WHERE id='"
    pushStr += str(emergencyAndHealthID) + "';"
    cur.execute(pushStr)
    addressIDs.append(cur.fetchall()[0][0])

    pushStr = "SELECT \"mailingAddress_id\" FROM enroller_contactsurvey WHERE id='"
    pushStr += str(contactSurveyID) + "';"
    cur.execute(pushStr)
    addressIDs.append(cur.fetchall()[0][0])

    pushStr = "SELECT \"physicalAddress_id\" FROM enroller_contactsurvey WHERE id='"
    pushStr += str(contactSurveyID) + "';"
    cur.execute(pushStr)
    addressIDs.append(cur.fetchall()[0][0])

    pushStr = "SELECT \"oldSchoolAddress_id\" FROM enroller_previousschoolsurvey WHERE id='"
    pushStr += str(previousSchoolID) + "';"
    cur.execute(pushStr)
    addressIDs.append(cur.fetchall()[0][0])

    # Then pull the addresses from the guardians
    for x in guardianIDs:
        pushStr = "SELECT \"homeAddress_id\" FROM enroller_guardian WHERE id='"
        pushStr += str(x) + "';"
        cur.execute(pushStr)
        addressIDs.append(cur.fetchall()[0][0])

    # And then, just collapse inward. Let's do this.
    to_execute = []
    to_execute.append("DELETE FROM enroller_student WHERE id='" + str(dbStudentEntryID) + "';")
    to_execute.append("DELETE FROM enroller_contactsurvey WHERE id='" + str(contactSurveyID) + "';")
    to_execute.append("DELETE FROM enroller_emergencyandhealthinfo WHERE id='" + str(emergencyAndHealthID) + "';")
    to_execute.append("DELETE FROM enroller_homelanguagesurvey WHERE id='" + str(homeLangID) + "';")
    to_execute.append("DELETE FROM enroller_mainsurvey WHERE id='" + str(mainSurveyID) + "';")
    to_execute.append("DELETE FROM enroller_mediaconsentform WHERE id='" + str(mediaConsentID) + "';")
    to_execute.append("DELETE FROM enroller_previousschoolsurvey WHERE id='" + str(previousSchoolID) + "';")
    to_execute.append("DELETE FROM enroller_raceandethnicitysurvey WHERE id='" + str(raceAndEthnicityID) + "';")
    for x in guardianIDs:
        to_execute.append("DELETE FROM enroller_guardian WHERE id='" + str(x) + "';")
    for x in addressIDs:
        to_execute.append("DELETE FROM enroller_address WHERE id='" + str(x) + "';")

    for x in to_execute:
        cur.execute(x)
        conn.commit()


# Adds all kids from an imported CSV file in a very specific format
def addLoadsOfKids(myFile):
    f = myFile.split(b'\n')

    students = []

    for line in f:
        students.append(line)

    kidTokens = []
    students = students[:-1]

    for kid in students:
        myStudentList = kid.split(b",")
        regStu = []
        for thing in myStudentList:
            regStu.append(thing.decode("utf-8"))
        # Have to add the student, from this list of items related to the student
        # Figure out the kid's name, first
        idNum = regStu[0]
        name = regStu[2][1:-1] + " " + regStu[1][1:]
        gender = regStu[3]
        entryGrade = regStu[4]
        race = regStu[5]
        addressStreeNameAndNum = regStu[6]
        city = regStu[7]
        state = regStu[8]
        zip = regStu[9]
        parentName = regStu[10]
        relationship = regStu[11]
        pn = regStu[12][:-2]

        kidId = createStudent(idNum, name, gender, entryGrade, race, addressStreeNameAndNum, city, state, zip,
                              parentName, relationship, pn)
        kidList = [name, kidId]
        kidTokens.append(kidList)

    return kidTokens


# Pulls all information from the database table
def createMyCSV():
    conn = connectToServer()
    cur = conn.cursor()

    allSurveys = ['student', 'mainsurvey', 'emergencyandhealthinfo', 'contactsurvey', 'homelanguagesurvey',
                    'raceandethnicitysurvey', 'previousschoolsurvey', 'mediaconsentform', 'guardian', 'address']
    pulledSurveys = []

    for n in allSurveys:
        pushStr = "SELECT * FROM enroller_" + n + ";"
        cur.execute(pushStr)
        pulledSurveys.append([n, cur.fetchall()])

    return pulledSurveys


# Returns the full name of a kid searched up by their id number
def findKid(idNum):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT mainsurvey_id FROM enroller_student WHERE \"schoolId\"='" + str(idNum) + "';"
    cur.execute(pushStr)

    kid = cur.fetchall()

    if kid == []:
        return "sorryButNope"

    else:
        kid = kid[0][0]
        pushStr = "SELECT * FROM enroller_mainsurvey WHERE id='" + str(kid) + "';"
        cur.execute(pushStr)

        kid = cur.fetchall()[0]
        fName = kid[4]
        lName = kid[3]
        mInitial = kid[5]

        fullName = fName + " " + mInitial + " " + lName

        if fullName == "  ":
            fullName = '<name not given>'

        return fullName


# idNum is the id number of the kid, lock is a string boolean, either 'TRUE' or 'FALSE',
# depending on whether you want to lock (true) or unlock(false) the kid's account
def lockOneKidAccount(idNum, lock):
    conn = connectToServer()
    cur = conn.cursor()
    pushStr = "UPDATE enroller_student SET \"accountLocked\"=" + lock + " WHERE \"schoolId\"='"  + idNum + "';"
    cur.execute(pushStr)
    conn.commit()


# Locks all the accounts in the db at once
# Again, if you want to lock them, lock should be "TRUE", else, "FALSE"
def lockAllUserAccounts(lock):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT \"schoolId\" FROM enroller_student;"
    cur.execute(pushStr)
    idList = cur.fetchall()

    for n in idList:
        lockOneKidAccount(n[0], lock)


def usnExists(username):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT * FROM enroller_student WHERE username='" + username + "';"
    cur.execute(pushStr)
    myList = cur.fetchall()

    if len(myList) == 0:
        return False
    else:
        return True


# Return completion stats on all the different surveys
def checkSurveyCompletion(username):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT * FROM enroller_student WHERE username='" + username + "';"
    cur.execute(pushStr)
    student = cur.fetchall()[0]

    surveys = {'contactsurvey':4, 'emergencyandhealthinfo':5, 'homelanguagesurvey':6, 'mainsurvey':7,
               'mediaconsentform':8, 'previousschoolsurvey':9, 'raceandethnicitysurvey':10}
    fetched = {}
    for name, num in surveys.items():
        pushStr = "SELECT * FROM enroller_" + name + " WHERE id='" + str(student[num]) + "';"
        cur.execute(pushStr)
        fetched[name] = cur.fetchall()[0][1]

    return fetched


def createAnAdmin(usn, pwd, email):
    conn = connectToServer()
    cur = conn.cursor()

    pushStr = "SELECT MAX(id) FROM enroller_admin;"
    cur.execute(pushStr)
    maxId = cur.fetchall()[0][0]

    if type(maxId) == type(None):
        maxId = 0

    maxId += 1

    pwd = superHash(pwd, usn)
    pushStr = "INSERT INTO enroller_admin (id, username, pwd, email) VALUES ('" + str(maxId) + "', '" + usn + "', '"
    pushStr += pwd + "', '" + email + "');"
    cur.execute(pushStr)
    conn.commit()


def createEmptyStudent():
    newId = createStudent('DEFAULT', 'DEFAULT, DEFAULT', 'DEFAULT', '9', 'DEFAULT', 'DEFAULT',
                          'DEFAULT', 'IL', 'DEFAU', 'DEFAULT', 'DEFAULT', 'DEFAULT')
    print(newId)