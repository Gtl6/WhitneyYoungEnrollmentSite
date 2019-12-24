from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from enroller import settings
from . import views

urlpatterns = [
    url(r'^$', views.redLogin, name='redLogin'),
    url(r'^mainPage/$', views.mainPage, name='main'),
    url(r'^mainSurveyPage/$', views.mainSurveyPage, name='mainSurvey'),
    url(r'^homeLanguageSurvey/$', views.homeLangSurvey, name='homeLanguageSurvey'),
    url(r'^raceAndEthnicitySurvey/$', views.raceAndEthnicitySurvey, name='raceAndEthnicitySurvey'),
    url(r'^mediaConsentForm/$', views.mediaConsentFormPage, name='mediaConsentForm'),
    url(r'^contactSurveyForm/$', views.contactSurveyPage, name='contactSurveyForm'),
    url(r'^previousSchoolSurveyPage/$', views.previousSchoolSurveyPage, name='previousSchoolSurvey'),
    url(r'^emergencyAndHealthSurvey/$', views.emergencyAndHealthInfoPage, name='emergencyAndHealthSurvey'),
    url(r'^registrationPage/$', views.registerPage, name='registrationPage'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^updateData/$', views.updateData, name='updateData'),
    url(r'^forgotPassword/$', views.forgotPassword, name='forgotPassword'),
    url(r'^sendResetEmail/$', views.sendResetEmail, name='sendResetEmail'),
    url(r'^validateResetToken/$', views.checkResetToken, name='validateResetToken'),
    url(r'^setNewPwd/$', views.setNewPwd, name='setNewPwd'),
    url(r'^admin/$', views.adminLoginPage, name='admin'),
    url(r'^adminLogin/$', views.loginAdmin, name='adminLogin'),
    url(r'^adminMain/$', views.adminMainPage, name='adminMain'),
    url(r'^addOneStudent/$', views.addOneStudentPage, name='addOneStudent'),
    url(r'^createTheKid/$', views.createSingleStudent, name='createTheKid'),
    url(r'^addMultipleStudents/$', views.addMultipleStudentsPage, name='addMultipleStudents'),
    url(r'^addThoseKids/$', views.addKidsTheseDays, name='addThoseKids'),
    url(r'^downloadDatabaseInfo/$', views.downloadDbInfo, name='downloadDatabaseInfo'),
    url(r'^dlDatabase/$', views.dlDatabase, name='dlDatabase'),
    url(r'^lockAccountOfSingleStudent/$', views.lockOneKid, name='lockAccountOfSingleStudent'),
    url(r'^checkForKid/$', views.checkForKid, name='checkForKid'),
    url(r'^lockOneKid/$', views.lockSingleDown, name='lockOneKid'),
    url(r'^unlockOneKid/$', views.unlockSingleDown, name='unlockOneKid'),
    url(r'^lockAllAccounts/$', views.lockAllAccounts, name='lockAllAccounts'),
    url(r'^lockAll/$', views.lockAll, name='lockAll'),
    url(r'^unlockAll/$', views.unlockAll, name='unlockAll'),
    url(r'^addAdmin/$', views.addAdminAccount, name='addAdmin'),
    url(r'^checkAdminInfo/$', views.checkAdminInfo, name='checkAdminInfo'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
