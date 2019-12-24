from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render
from enroller.serverWorking import *
from django.shortcuts import redirect
import csv


# Generates the context for a page from the database information already on the student
def makeContext(dbName, username, nameAndRadioList, surveyName):
    info = contextRenderEngine(dbName, username, nameAndRadioList)
    c = {'name':surveyName, 'info':info}
    return c


def registerPage(request):
    return render(request, 'enroller/Main Site Pages/registerPage.html')


def redLogin(request):
    return redirect('/login')


def mainPage(request):
    if 'username' in request.COOKIES:

        completionDict = checkSurveyCompletion(request.COOKIES.get('username'))
        context = {}

        fins = 0

        for name, tf in completionDict.items():
            if tf:
                color = 'green'
                fins += 1
            else:
                color = 'red'

            context[name + "Color"] = color

        if fins == 7: # If all surveys are finished
            return render(request, 'enroller/Main Site Pages/allSurveysFinished.html')

        return render(request, 'enroller/Main Site Pages/mainPage.html', context=context)
    else:
        return redirect('/login')


def mainSurveyPage(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        genders = ['Male', 'Female']
        birthCertificationType = ['Birth Certificate', 'Passport']
        namesAndRadioEntries = ['*n',
                                '8',
                                'Student ID',
                                '#studentID',
                                'Last Name',
                                '#lastName',
                                'First Name',
                                '#firstName',
                                'Middle Name',
                                '#middleName',
                                'Generation (jr, etc.)',
                                '#generation',
                                'Gender on birth certificate', genders,
                                '#gender',
                                'Entry Grade (between 7 and 12)',
                                '#entryGrade',
                                '*b',
                                'Birth Certificate on File?',
                                '#birthCertOnFile',
                                'Birth Certification Type', birthCertificationType,
                                '#birthVer',
                                '*c',
                                'Country of Birth',
                                '#birthCountry',
                                '*d',
                                'Birth Date',
                                '#birthDate',
                                'City of Birth',
                                '#birthCity',
                                '*d',
                                'Date of First Enrollment in a US School',
                                '#firstUSEnrollDate',
                                'Number of Years of US Schooling',
                                '#numYearsUSSchooling',
                                '*d',
                                'Date entered US (if applicable, if not leave blank)',
                                '#dateEnteredUS',
                                '*b',
                                'Student has refugee status?',
                                '#refugeeStatus',
                                '*c',
                                'Refugee Country (if applicable, if not leave blank)',
                                '#refugeeCountry',
                                ]
        nameOfSurvey = 'Main Survey'
        dbName = 'mainsurvey'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def homeLangSurvey(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        namesAndRadioEntries = ['Student\'s First Language',
                                '#surveyLanguage',
                                '*b',
                                'Is a language other than English spoken at home?',
                                '#homeLanguageOtherThanEnglishSpoken',
                                'What other language, if any, is spoken at home?',
                                '#homeLanguageOtherThanEnglish',
                                '*b',
                                'Does the student primarily speak a language other than English?',
                                '#studentSpeaksLanguageOtherThanEnglish',
                                'If so, what language?',
                                '#studentOtherLanguage',
                                ]
        nameOfSurvey = 'Home Language Survey'
        dbName = 'homelanguagesurvey'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def raceAndEthnicitySurvey(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        races = ['American Indian', 'Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Mixed Race', 'Native Hawaiian or Other Pacific Islander', 'White']
        namesAndRadioEntries = ['What race do you most closely identify with?', races,
                                '#race',
                                ]
        nameOfSurvey = 'Race and Ethnicity Survey'
        dbName = 'raceandethnicitysurvey'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def mediaConsentFormPage(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        namesAndRadioEntries = \
        [
            '*b',
            "I do hereby consent to have my student photographed, video taped, audio taped, or interviewed by the Board of Education of the City of Chicago (the 'Board') or the news media when school is in session or when my child is under the supervision of the Board. I understand in the course of the above described activites that the Board might like to celebrate my child's accomplishments and work. Therefor, I further consent for the Board's release of information on my child's name, academic/non-academic awards and information concerning my child's participation in school-sponsored activities, organizations, and athletics. I also consent to the Board's use of my child's name, photograph or likeness, voice or creative work(s) on the Internet or on a CD or any other electronic/digital media or print media. As the child's parent or legal guardian, I agree to release and hold harmless the Board, its members, trustees, agents, officers, contractors, volunteers, and employees from and against any and all claims, demands, actions, complaints, suits or other forms of liability that shall arise out of or by reason of, or be caused by the use of my child's name, photograph or likeness, voice or creative work(s), on television, radio, or motion pictures, or in the print medium, or on the Internet or ay other electronic/digital medium. It is further understood and I do agree that no monies or other consideration in any form, including reimbursement for any expenses by me or my child, will become due to me, my child, our heirs, agents, or assigns at any time because of my child's participation in any of the above activities or the above-described use of my child's name, photograph or likeness, voice or creative work(s). I understand that I may cancel my consent by providing written notice to the principle.",
            '#consentToMedia',
        ]
        nameOfSurvey = 'Media Consent Survey'
        dbName = 'mediaconsentform'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def contactSurveyPage(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        namesAndRadioEntries = ['Home Phone Number',
                                '#homePhoneNumber',
                                '*a',
                                'Student\'s mailing address',
                                '#mailingaddress_id',
                                '*a',
                                'Student\'s physical address (if different from above)',
                                '#physicaladdress_id',
                                ]
        nameOfSurvey = 'Contact Survey'
        dbName = 'contactsurvey'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def previousSchoolSurveyPage(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        namesAndRadioEntries = ['School Transferring From',
                                '#schoolTransferringFrom',
                                '*a',
                                'Address of Previous School',
                                '#oldschooladdress_id',
                                '*b',
                                'Is the Student in good standing?',
                                '#studentInGoodStanding',
                                'Last Chicago Public, Charter, or Contract School Attended',
                                '#lastPublicSchool',
                                '*b',
                                'Is the student receiving any type of Special Education Services?',
                                '#specialEdServices',
                                'Name of guardian enrolling student',
                                '#enrollerGuardianName',
                                'Relationship of enrolling guardian to student',
                                '#enrollerGuardianRelationship',
                                '*v',
                                'Verify that all information is correct, then check the box below.',
                                '#enrollerGuardianSigned',
                                ]
        nameOfSurvey = 'Previous School Survey'
        dbName = 'previousschoolsurvey'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def emergencyAndHealthInfoPage(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
        confidential1 = ['awaiting foster care placement', 'in a car/park/other public place', 'doubled-up' ' in a hotel/motel', 'in a shelter', 'in transitional housing', 'none of the above']
        insuranceOptions = ['Illinois Medical Card', 'No Insurance', 'Private/Employer Health Insurance']
        namesAndRadioEntries = ['Select one of the below options only if (1) it reflects your child\'s current living situation; OR (2) it reflects your living situation if you are a youth not living with a Parent or Guardian. (Your answer will help school staff with enrollment and may enable the student to receieve additional services.)', confidential1,
                                '#confidentialInfoBox1',
                                '*b',
                                'Is there a current Order of Protection or No Contact Order which concerns this student?',
                                '#confidentialInfoBox2',
                                '*g',
                                'Guardian Contact Information',
                                '#guardian1_id',
                                '*g',
                                'Second Guardian Contact Information',
                                '#guardian2_id',
                                '*g',
                                'Neighbor who can be contacted in an emergency and has permission to pick up student',
                                '#neighbor_id',
                                '*t',
                                'Medical information',
                                'Family Doctor Name',
                                '#doctorName',
                                '*a',
                                'Doctor\'s Office Address',
                                '#doctorAddress_id',
                                'Family Doctor Phone Number',
                                '#doctorPhoneNumber',
                                'Student Health Insurance', insuranceOptions,
                                '#studentHealthInsurance',
                                '*n',
                                '9',
                                'Illinois Medical ID # (9-digit number located on back of card)',
                                '#illinoisMedicalCardID',
                                ]
        nameOfSurvey = 'Emergency And Health Info'
        dbName = 'emergencyandhealthinfo'

        c = makeContext(dbName, username, namesAndRadioEntries, nameOfSurvey)
        a = render(request, 'enroller/Main Site Pages/surveyTemplate.html', context=c)
        a.set_cookie('NamesAndRadioLists', namesAndRadioEntries, max_age=7200)
        a.set_cookie('surveyName', dbName, max_age=7200)
        return a
    else:
        return redirect('/login')


def register(request):
    username = request.POST.get("uName", "").lower()
    password = request.POST.get("psw", "")
    confirmPassword = request.POST.get("pswConf", "")
    registrationToken = request.POST.get("reg", "")
    bools = validateRegToken(registrationToken)

    # Also add in the case where the email is already in the database

    if password == username:
        con = Context ({'errorMessage':'You cannot put a password that is the same as your username'})
    elif password != confirmPassword:
        con = Context ({'errorMessage':'Your passwords don\'t match!'})
    elif not '@' in username:
        con = Context ({'errorMessage':'You must enter a valid email address'})
    elif usnExists(username):
        con = Context ({'errorMessage':'That username has already been used!'})
    elif len(password) < 7:
        con = Context ({'errorMessage':'Enter a password that is at least 7 characters long'})
    elif bools[0] and bools[1]:
        # Returns the page "You already registered!"
        con = Context({'errorMessage':'Your registration token has already been used. Contact your administrator if you believe this is a mistake.'})
    elif bools[0] and not bools[1]:
        # Returns the page "You successfully registered!"
        registerStudent(username, password, registrationToken)
        a = redirect('/mainPage')
        a.set_cookie('username', username, max_age=7200)
        return a
    else:
        # Returns the page "Your code couldn't be found. Contact your administrator if you think this is a mistake."
        con = Context({'errorMessage':'Your registration token couldn\'t be validated. Contact your administrator if you believe this is a mistake.'})

    return render(request, 'enroller/Main Site Pages/registerPage.html', con)


def login(request):
    username = request.POST.get("uname", "").lower()
    password = request.POST.get("psw", "")

    print(username)

    if username == '' and password == '':
        a = render(request, 'enroller/Main Site Pages/loginPage.html')
    else:
        password = superHash(password, username)
        bools = checkLoginData(username, password, 'normal')
        if bools[0] and not bools[1]:
            con = Context ({'errorMessage':'That username or password was not found.'})
            a = render(request, 'enroller/Main Site Pages/loginPage.html', con)
        elif not bools[0]:
            con = Context({'errorMessage':'Your username was not found. Are you sure you have registered?'})
            a = render(request, 'enroller/Main Site Pages/loginPage.html', con)
        elif bools[0] and bools[1] and bools[2]:
            con = Context({'errorMessage':'Your account has been locked. Contact your administrator if you believe this is a mistake.'})
            a = render(request, 'enroller/Main Site Pages/loginPage.html', con)
        elif bools[0] and bools[1]:
            a = redirect('/mainPage')
            a.set_cookie('username', username, max_age=7200)
    return a


def updateData(request):
    data = request.POST
    nRL = request.COOKIES.get('NamesAndRadioLists')
    username = request.COOKIES.get('username')
    dbName = request.COOKIES.get('surveyName')
    pushDataToDb(dbName, username, data, nRL)
    return redirect('/mainPage')


def forgotPassword(request):
    return render(request, 'enroller/Main Site Pages/forgotPasswordPage.html')


def sendResetEmail(request):
    email = request.POST.get('uName').lower()

    worked = sendPwdResetEmail(email)

    if worked:
        a = render(request, 'enroller/Main Site Pages/resetPasswordPageConf.html')
        a.set_cookie('username', email, max_age=7200)
        return a
    else:
        context = {'errorMessage':'That username wasn\'t found in our database.'}
        return render(request, 'enroller/Main Site Pages/forgotPasswordPage.html', context=context)


def checkResetToken(request):
    token = request.POST.get('token')

    worked = checkTokenWithDb(token)

    if worked:
        return render(request, 'enroller/Main Site Pages/resetPasswordPageActual.html')
    else:
        context = {'errorMessage':'That token was not found in our database. Did you copy it correctly?'}
        return render(request, 'enroller/Main Site Pages/resetPasswordPageConf.html', context=context)


def setNewPwd(request):
    pwd = request.POST.get('newPwd')
    usn = request.COOKIES.get('username').lower()

    setNewPasswordInDb(pwd, usn)

    return render(request, 'enroller/Main Site Pages/successfulReset.html')


# So yeah, I'm gonna write my own admin view. Cause you know, why not, eh?
def adminLoginPage(request):
    return render(request, 'enroller/adminPages/adminLoginPage.html')


def loginAdmin(request):
    username = request.POST.get("uname", "")
    password = request.POST.get("psw", "")
    if username == '' and password == '':
        a = render(request, 'enroller/adminPages/adminLoginPage.html')
    else:
        password = superHash(password, username)
        bools = checkLoginData(username, password, 'admin')
        if bools[0] and not bools[1]:
            con = Context({'errorMessage':'That username or password was not found.'})
            a = render(request, 'enroller/adminPages/adminLoginPage.html', con)
        elif not bools[0]:
            con = Context ({'errorMessage':'Your username was not found. Are you sure you have registered?'})
            a = render(request, 'enroller/adminPages/adminLoginPage.html', con)
        elif bools[0] and bools[1]:
            a = redirect('/adminMain')
            a.set_cookie('adminUsername', superHash(password, username), max_age=7200)
    return a


def adminMainPage(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/adminMainPage.html')
    else:
        return redirect('/adminLogin')


def addOneStudentPage(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/addNewStudentPage.html')
    else:
        return redirect('/adminLogin')


def createSingleStudent(request):
    if request.POST.get("aptnumber") == "":
        addon = ''
    else:
        addon = ' #'

    registToken = createStudent(request.POST.get("id", ""), request.POST.get("division", ""),
                                request.POST.get("fullname", ""), request.POST.get("gender", ""),
                                request.POST.get("grade", ""), request.POST.get("race", ""),
                                request.POST.get("streetnameandnumber", "") + addon + request.POST.get("aptnumber", ""),
                                request.POST.get("city", ""), request.POST.get("state", ""),
                                request.POST.get("zipcode", ""), request.POST.get("parentname", ""),
                                request.POST.get("relationshiptostudent", ""), request.POST.get("phonenumber", ""))
    con = Context({'token':registToken})
    return render(request, 'enroller/Main Site Pages/studentBeenCreated.html', con)


def addMultipleStudentsPage(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/addMultipleStudents.html')
    else:
        return redirect('/adminLogin')


def addKidsTheseDays(request):
    wellLemmeSee = request.FILES.get('theFile').read()

    kidTokens = addLoadsOfKids(wellLemmeSee)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="StudentNamesAndActivationCodes.csv"'

    writer = csv.writer(response)
    for kid in kidTokens:
        writer.writerow([kid[0], kid[1]])

    return response


def downloadDbInfo(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/DatabaseDump.html')
    else:
        return redirect('/adminLogin')


def dlDatabase(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EnrollmentDatabase.csv"'

    myCSV = createMyCSV()
    print(myCSV)

    writer = csv.writer(response)
    for survey in myCSV:
        writer.writerow([survey[0]])
        for entry in survey[1]:
            writer.writerow(entry)
        writer.writerow([])
        writer.writerow([])

    return response


def lockOneKid(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/lockUnlockPages.html')
    else:
        return redirect('/adminLogin')


def checkForKid(request):
    if 'adminUsername' in request.COOKIES:
        theId = request.POST.get('idNum')
        student = findKid(theId)

        if student != 'sorryButNope':
            c = {'kidName':student}
            a = render(request, 'enroller/adminPages/showKidGotten.html', context=c)
            a.set_cookie('kidId', theId, max_age=7200)
            return a
        else:
            c = {'errorMessage':'Sorry, I couldn\'t find that student in the database. Did you get the id correct?'}
            return render(request, 'enroller/adminPages/lockUnlockPages.html', context=c)
    else:
        return redirect('/adminLogin')


def lockSingleDown(request):
    if 'adminUsername' in request.COOKIES:
        theId = request.COOKIES.get('kidId')
        lockOneKidAccount(theId, 'TRUE')

        return redirect('/adminMain')
    else:
        return redirect('/adminLogin')


def unlockSingleDown(request):
    if 'adminUsername' in request.COOKIES:
        theId = request.COOKIES.get('kidId')
        lockOneKidAccount(theId, 'FALSE')

        return redirect('/adminMain')
    else:
        return redirect('/adminLogin')


def lockAllAccounts(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/lockAllAccounts.html')
    else:
        return redirect('/adminLogin')


def lockAll(request):
    if 'adminUsername' in request.COOKIES:
        lockAllUserAccounts("TRUE")

        return redirect('/adminMain')
    else:
        return redirect('/adminLogin')


def unlockAll(request):
    if 'adminUsername' in request.COOKIES:
        lockAllUserAccounts("FALSE")

        return redirect('/adminMain')
    else:
        return redirect('/adminLogin')


def addAdminAccount(request):
    if 'adminUsername' in request.COOKIES:
        return render(request, 'enroller/adminPages/addNewAdmin.html')
    else:
        return redirect('/adminLogin')


def checkAdminInfo(request):
    if 'adminUsername' in request.COOKIES:
        usn = request.POST.get('usn')
        pwd = request.POST.get('pwd')
        pwdConf = request.POST.get('pwdConf')
        email = request.POST.get('email')

        if len(usn) < 5:
            c = {'errorMessage':'Please use a username that is at least 5 characters long.'}
            return render(request, 'enroller/adminPages/addNewAdmin.html', context=c)
        elif len(pwd) < 7:
            c = {'errorMessage':'Please use a password that is at least 7 characters long.'}
            return render(request, 'enroller/adminPages/addNewAdmin.html', context=c)
        elif pwd != pwdConf:
            c = {'errorMessage':'Your passwords don\'t match!'}
            return render(request, 'enroller/adminPages/addNewAdmin.html', context=c)
        else:
            createAnAdmin(usn, pwd, email)
            return render(request, 'enroller/adminPages/AdminConfirmed.html')

        return render(request, 'enroller/adminPages/addNewAdmin.html')
    else:
        return redirect('/adminLogin')
