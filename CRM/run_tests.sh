#! /bin/bash

echo "**********Testing CRM**********"
echo Testing Account_management
echo "********************************"
python3 CRM/manage.py test Account_management

echo "********************************"
echo Testing CRM_core
echo "********************************"
python3 CRM/manage.py test CRM_core

echo "********************************"
echo Testing Exercises_checker
echo "********************************"
python3 CRM/manage.py test Exercises_checker


echo "********************************"
echo Testing Files_organizer
echo "********************************"
python3 CRM/manage.py test Files_organizer

echo "********************************"
echo Testing Meetings_calendar
echo "********************************"
python3 CRM/manage.py test Meetings_calendar

echo "********************************"
echo Testing Payments_system
echo "********************************"
python3 CRM/manage.py test Payments_system

echo "********************************"
echo Testing System_administration
echo "********************************"
python3 CRM/manage.py test System_administration






