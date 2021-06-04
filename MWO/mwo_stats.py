#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
'''
MWO Stats retrieval scrapper

Requirements:
- python3
- selenium python module
- Firefox browser
- geckodriver from Mozilla
- a desire to see math on your stats

Usage:
$ mwo_stats.py

This will write out your stats along with some additional calculated stuff to mwo_stats.csv

You can then open that in your spreadsheet application of choice and see all the pretty data

'''

import os
import pprint

from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

BASE_URL = "https://mwomercs.com/"
PROF_URL = BASE_URL + "profile"
STATS_URL = PROF_URL + "/stats"
MECH_DATA = STATS_URL + "?type=mech"
WEAP_DATA = STATS_URL + "?type=weapon"
MAPS_DATA = STATS_URL + "?type=map"
MODE_DATA = STATS_URL + "?type=mode"
MECH_NAME = {
    'SPARKY':'GRF-1E',
    'UZIEL UZL-3S(S)':'UZL-3SS',
    'SKOKOMISH':'ZEU-SK',
    'CENTURION CN9-A(NCIX)':'CN9-ANCIX',
    'BLOOD ADDER':'COU-BA',
    'BELIAL':'UZL-BE',
    'CATAPHRACT CTF-3L(L)':'CTF-3LL',
    'NIGHT GYR NTG-PRIME(S)':'NTG-PRIMES',
    'COUGAR COU-PRIME(S)':'COU-PRIMES',
    'K-9':'UM-K9',
    'BOILER':'SNV-BR',
    'SUPERNOVA SNV-1(S)':'SNV-1S',
    'MEAN BABY':'ANH-MB',
    'ANNIHILATOR ANH-2A(S)':'ANH-2AS',
    'BLACKJACK BJ-2(L)':'BJ-2L',
    'DEATHSTRIKE':'MCII-DS',
    'MAD CAT MK II MCII-1(S)':'MCII-1S',
    'PIRATES\' BANE':'LCT-PB',
    'KNOCKOUT':'MAL-KO',
    'PANTHER PNT-10K(R)':'PNT-10KR',
    'HELLBRINGER HBR-F(L)':'HBR-FL',
    'JADE KITE':'NTG-JK',
}

def login_to_mwo(ffox):
    '''
    Prompt for username / passwd
    Open the selenium-driven browser
    Log in
    Return the browser object
    '''
    print("Enter user email: ", end='')
    email = input()

    passwd = getpass("Enter user password: ")

    ffox.get(PROF_URL)

    login_link = ffox.find_element_by_link_text('LOGIN')
    login_link.click()

    email_input = ffox.find_element_by_id('email')
    email_input.send_keys(email)

    psswd_input = ffox.find_element_by_id('password')
    psswd_input.send_keys(passwd)
    psswd_input.submit()

    try:
        alert = ffox.find_element_by_class_name('alert alert-error').text.strip()
        if 'Invalid email/password' in alert:
            print("Invalid email/password entered, please try again.")
            login_to_mwo(ffox)
    except NoSuchElementException:
        print("Logged in!")

def get_mechbays(ffox):
    '''
    Retrieve the profile page
    Iterate over mechBay classed tags and return the dictionary of owned my_mechs
    '''
    ffox.get(PROF_URL)
    mech_bays = ffox.find_elements_by_class_name('mechBay')
    mech_bay = {}
    for bay in mech_bays:
        try:
            mech_bay[bay.text.strip()] += 1
        except KeyError:
            mech_bay[bay.text.strip()] = 1

    return mech_bay

def get_stat_data(url, ffox):
    '''
    Retrieve the specific stats page
    Find the table of stats and store each row as a dictionary entry under the first column
    Return the dictionary of stats
    '''
    ffox.get(url)
    my_stats = {}
    stat_list = [x.text.strip() for x in ffox.find_elements_by_xpath('//thead/tr/th')]
    for obj in ffox.find_elements_by_xpath('//tbody/tr'):
        idx = 0
        obj_name = ''
        for stat in obj.find_elements_by_tag_name('td'):
            if idx == 0:
                obj_name = stat.text.strip()
                my_stats[obj_name] = {}
            else:
                my_stats[obj_name][stat_list[idx]] = stat.text.strip()
            idx += 1

    return my_stats

def get_owner_data(mechbays, stats):
    """Check stats entries against mechbay contents to see if you currently own the mech"""
    for mech in stats.keys():
        bay = mech
        if mech in MECH_NAME.keys():
            bay = MECH_NAME[mech]

        bay = bay.split(' ')[-1] # Get the end of the mech name
        stats[mech]['Owned'] = bool(bay in mechbays.keys())

    return stats

def main():
    '''
    Main processing
    '''
    # Set up the log location for the geckodriver so we can delete it later
    geckolog = "/tmp/geckodriver.log"

    # Set up the webdriver instance here so we can close it no matter what happens
    browser = webdriver.Firefox(log_path=geckolog)
    try:
        # Prompt the user for email/password and log in
        login_to_mwo(browser)
        # Retrieve mechbays (owned mechs)
        my_mechs = get_mechbays(browser)
        # Retrieve all available mech stats
        my_mech_stats = get_stat_data(MECH_DATA, browser)
        # Update mech data with 'current' ownership
        my_mech_stats = get_owner_data(my_mechs, my_mech_stats)
        # Retrieve all available weapon stats
        my_weap_stats = get_stat_data(WEAP_DATA, browser)
        # Retrieve game map stats
        my_maps_stats = get_stat_data(MAPS_DATA, browser)
        # Retrieve game mode stats
        my_mode_stats = get_stat_data(MODE_DATA, browser)
    finally:
        browser.close()
        os.unlink(geckolog)

    pprint.pprint(my_mechs)
    pprint.pprint(my_mech_stats)
    pprint.pprint(my_weap_stats)
    pprint.pprint(my_maps_stats)
    pprint.pprint(my_mode_stats)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborting...")
