from django.db import models


class Student(models.Model):
    # Text field to allow for registration
    activationcode = models.CharField(max_length=10)
    # Account locked, checks whether the user can sign in or not
    accountLocked = models.BooleanField(default=False)
    # ID at school
    schoolId = models.CharField(max_length=8)
    # Reset val, whenever someone loses their password, they will be given a randomly generated tag
    # If the tag provided matches with their given tag, they can enter it in order to reset their password
    resetVal = models.CharField(max_length=10)
    # Text field to hold email name
    username = models.CharField(max_length=200)
    # Text field to take in password
    # Password should be hashed on retrieval
    password = models.CharField(max_length=1000)
    # Each of the surveys
    mainsurvey = models.ForeignKey('mainsurvey', on_delete=models.CASCADE)
    raceandethnicitysurvey = models.ForeignKey('raceandethnicitysurvey', on_delete=models.CASCADE)
    mediaconsentform = models.ForeignKey('mediaconsentform', on_delete=models.CASCADE)
    contactsurvey = models.ForeignKey('contactsurvey', on_delete=models.CASCADE)
    previousschoolsurvey = models.ForeignKey('previousschoolsurvey', on_delete=models.CASCADE)
    emergencyandhealthinfo = models.ForeignKey('emergencyandhealthinfo', on_delete=models.CASCADE)
    homelanguagesurvey = models.ForeignKey('homelanguagesurvey', on_delete=models.CASCADE)

    def __unicode__(self):
        return Address + self.pk


class HomeLanguageSurvey(models.Model):
    # Survey finished? Boolean
    surveyCompleted = models.BooleanField()
    # Language the survey was taken in
    # Drop down list that generates the page
    surveyLanguage = models.CharField(max_length=20, blank=True)
    # Is a language other than English spoken in your home?
    # No, yes with a text entry next to the yes
    homeLanguageOtherThanEnglishSpoken = models.NullBooleanField()
    # If a language other than English is spoken in your home, what is it?
    # Text box
    homeLanguageOtherThanEnglish = models.CharField(max_length=100, blank=True)
    # Does the student speak another language other than English?
    # No, yes with a text entry again
    studentSpeaksLanguageOtherThanEnglish = models.NullBooleanField()
    # If the student speaks a language other than english, what is it
    # Text box
    studentOtherLanguage = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return Address + self.pk


class MainSurvey(models.Model):
    # Survey finished? Boolean
    surveyCompleted = models.BooleanField()
    # Text field, nums only restriction
    studentID = models.CharField(max_length=8, blank=True)
    # Text field
    lastName = models.CharField(max_length=20, blank=True)
    # Text field
    firstName = models.CharField(max_length=20, blank=True)
    # Text field
    middleName = models.CharField(max_length=20, blank=True)
    # Used to denote jr, sr, etc.
    # Should be used with a radio buttons
    generation = models.CharField(max_length=20, blank=True)
    # Emphasize this should be gender on birth cert
    # Use radio buttons
    gender = models.CharField(max_length=50, blank=True)
    # Number selection list from 7 to 12
    entryGrade = models.CharField(max_length=2, blank=True)
    # Boolean as to whether the student has a birth certificate on record
    # Should be a radio list, side by side, ( ) yes ( ) no
    birthCertOnFile = models.NullBooleanField()
    # Birth Verification Type, either 'passport' or 'birth certificate'
    # But it'll probably be a dropdown list of options
    birthVer = models.CharField(max_length=100, blank=True)
    # Birth Country, dropdown list
    birthCountry = models.CharField(max_length=50, blank=True)
    # Birth State, dropdown list
    birthDate = models.DateField(null=True, blank=True)
    # Birth City, text field
    birthCity = models.CharField(max_length=100, blank=True)
    # Date of first enrollment in any US School
    # Should be a date field
    firstUSEnrollDate = models.DateField(null=True, blank=True)
    # Full years complete school in US
    # Should be a text box, num restriction
    numYearsUSSchooling = models.CharField(max_length=2, blank=True)
    # Date first entered US
    dateEnteredUS = models.DateField(null=True, blank=True)
    # Student has refugee status
    # Boolean ( ) yes ( ) no
    refugeeStatus = models.NullBooleanField()
    # Country of refugee
    # Drop down list of items
    refugeeCountry = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return Address + self.pk


class RaceAndEthnicitySurvey(models.Model):
    # Survey done? Boolean
    surveyCompleted = models.BooleanField()
    # Race
    # Should be a drop down list
    race = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return Address + self.pk


class MediaConsentForm(models.Model):
    # Survey done? Boolean
    surveyCompleted = models.BooleanField()
    # Boolean, represented by the consent form layout
    consentToMedia = models.NullBooleanField(blank=True)

    def __unicode__(self):
        return Address + self.pk


class ContactSurvey(models.Model):
    # Boolin finished?
    surveyCompleted = models.BooleanField()
    # An address for the physical address
    physicalAddress = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='physical', blank=True)
    # Second will be mailing address if different from physical address
    mailingAddressChanged = models.BooleanField(default=False)
    mailingAddress = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='mail', blank=True)
    # General phone number
    # Phone number input box
    homePhoneNumber = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return Address + self.pk


class PreviousSchoolSurvey(models.Model):
    # Bools for dayz
    surveyCompleted = models.BooleanField()
    # School transferred from
    # Char field
    schoolTransferringFrom = models.CharField(max_length=100, blank=True)

    # Put in an address for the old school
    oldSchoolAddress = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True)

    # Is the student in good standing?
    # should be a yes / no
    studentInGoodStanding = models.NullBooleanField(blank=True)
    # Last Chicago, Public, Charter, or Contract School attended
    # Text field
    lastPublicSchool = models.CharField(max_length=100, blank=True)
    # Is the student receiving any type of Special Education services?
    # Boolean
    specialEdServices = models.BooleanField(blank=True)
    # Student enrolled by (Print name of Parent)
    # Text field
    enrollerGuardianName = models.CharField(max_length=200, blank=True)
    # What is that person's relationship to the student
    # Choice list
    enrollerGuardianRelationship = models.CharField(max_length=100, blank=True)
    # Signature of parent
    # Should be a check box next to a legal disclaimer
    enrollerGuardianSigned = models.NullBooleanField(blank=True)
    # Date of enrollment
    # Should be a date box
    enrollmentDate = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return Address + self.pk


class EmergencyAndHealthInfo(models.Model):
    # you should know this by now fam
    # Boolean
    surveyCompleted = models.BooleanField()
    # Where the kid lives, see form under Confidential Information Box 1 for description
    # Radio list
    confidentialInfoBox1 = models.CharField(max_length=100, blank=True)
    # Order of Protection or No Contact order protection, see Confidential Info Box 2 for description
    # yes no box
    confidentialInfoBox2 = models.NullBooleanField()

    # Make 2 Guardians here
    guardian1 = models.ForeignKey('Guardian', on_delete=models.CASCADE, related_name='guardian1', blank=True, null=True)
    guardian2 = models.ForeignKey('Guardian', on_delete=models.CASCADE, related_name='guardian2', blank=True, null=True)
    neighbor = models.ForeignKey('Guardian', on_delete=models.CASCADE, related_name='neighbor', blank=True, null=True)

    # Make 1 Guardian that isn't an immediate close relative
    # Family Doctor Name
    # Text field
    doctorName = models.CharField(max_length=100, blank=True)

    # Family doctor address
    doctorAddress = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, default='1')

    # Doctor Phone Number
    # Phone # input
    doctorPhoneNumber = models.CharField(max_length=11, blank=True)
    # Student health insurance
    # Radio list
    studentHealthInsurance = models.CharField(max_length=100, blank=True)
    # Student medical ID # (if applicable)
    # Text entry, num restriction
    illinoisMedicalCardID = models.CharField(max_length=9, blank=True)
    # Guardian a member of the armed forces?
    # yes no
    guardianArmedForces = models.NullBooleanField()
    # Guardian expecting to be deployed to active duty (if above is true)
    # yes or no
    guardianExpectingDeployment = models.NullBooleanField()
    # Certify that above is correct (all everything)
    # Single checkbox
    informationCertification = models.NullBooleanField()
    # Date form was filled out
    # Date input
    dateFormFilledOut = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return Address + self.pk


class Guardian(models.Model):
    # Guardian 1 Stuffs
    # Name
    # Text field
    name = models.CharField(max_length=100, blank=True)
    # Relationship to student
    # Text field
    relationship = models.CharField(max_length=20, blank=True)
    # Check all that apply, check form for all options
    # Each of these will be a Bool because no lists in SQL?
    # Either way, use check box list
    livesWith = models.NullBooleanField()
    getsMailings = models.NullBooleanField()
    emergency = models.NullBooleanField()
    permissionToPickup = models.NullBooleanField()

    # Stick in an address here
    homeAddress = models.ForeignKey('Address', related_name='homeAddress', on_delete=models.CASCADE, blank=True, default='1')

    # Home phone number, if diff from student
    # Phone # input
    homePhoneNumber = models.CharField(max_length=100, blank=True)
    # Cell phone number
    # Phone # input
    cellPhoneNumber = models.CharField(max_length=100, blank=True)
    # Email address
    # Text field
    emailAddress = models.CharField(max_length=200, blank=True)
    # Name of employer
    # Text field
    nameOfEmployer = models.CharField(max_length=100, blank=True)

    # Work phone number
    # Phone number input
    workPhoneNumber = models.CharField(max_length=100, blank=True)
    # Language preferred for communication (i.e. phone calls)
    # Dropdown list
    communicationLanguage = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return Address + self.pk


class Address(models.Model):
    # Street number and name
    streetNumberAndName = models.CharField(max_length=200, blank=True)
    # Apartment number
    apartmentNo = models.CharField(max_length=4, blank=True)
    # City
    city = models.CharField(max_length=200, blank=True)
    # State
    # Use the dropdown lists for this
    state = models.CharField(max_length=2, blank=True)
    # Zip Code
    zipCode = models.CharField(max_length=5, blank=True)

    def __unicode__(self):
        return Address + self.pk


class Admin(models.Model):
    # Username
    username = models.CharField(max_length=200, blank=False)
    # Password
    pwd = models.CharField(max_length=200, blank=False)
    # Email
    email = models.CharField(max_length=200, blank=True)