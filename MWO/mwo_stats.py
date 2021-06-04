#!/usr/bin/env python3
"""
MWO Stats retrieval/scraper

Requirements:
- python3
- selenium python module
- Firefox browser
- geckodriver from Mozilla
  - make sure this is in your PATH
  - make sure to get the correct version for your Firefox browser version
- a desire to see math on your stats

Usage:
$ mwo_stats.py

This will write out your stats along with some additional calculated stuff to mwo_stats.csv

You can then open that in your spreadsheet application of choice and see all the pretty data
"""
import os
import sys
import argparse
import pprint

from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import ProtocolError

BASE_URL = "https://mwomercs.com/"
PROF_URL = BASE_URL + "profile"
STATS_URL = PROF_URL + "/stats"
MECH_DATA = STATS_URL + "?type=mech"
WEAP_DATA = STATS_URL + "?type=weapon"
MAPS_DATA = STATS_URL + "?type=map"
MODE_DATA = STATS_URL + "?type=mode"

# mech list
MECH_NAME = {
    "SPARKY": "GRF-1E",
    "ARES": "GRF-AR",
    "GRIFFIN GRF-5M(L)": "GRF-5ML",
    "MJÖLNIR": "GHR-MJ",
    "FIRESTORM": "FS-FS",
    "ROMEO 5000": "FLE-5K",
    "GHILLIE": "ENF-GH",
    "DIRE WOLF DWF-W(C)": "DWF-WC",
    "ULTRAVIOLET": "DWF-UV",
    "GRAND DRAGON DRG-1G(S)": "DRG-1GS",
    "CATAPULT CPLT-C2(S)": "CPLT-C2S",
    "CATAPULT CPLT-A1(C)": "CPLT-A1C",
    "SLEIPNIR": "CP-SP",
    "BROADSIDE": "COR-BR",
    "COMMANDO COM-1D(C)": "COM-1DC",
    "CICADA CDA-2A(C)": "CDA-2AC",
    "HIGH ROLLER": "BSW-HR",
    "SIREN": "BNC-SR",
    "KRAKEN": "AS7-KR",
    "ARCTIC CHEETAH ACH-PRIME(C)": "ACH-PRIMEC",
    "UZIEL UZL-3S(S)": "UZL-3SS",
    "UZIEL UZL-3P(C)": "UZL-3PC",
    "BELIAL": "UZL-BE",
    "SKOKOMISH": "ZEU-SK",
    "CENTURION CN9-A(NCIX)": "CN9-ANCIX",
    "CATAPHRACT CTF-3L(L)": "CTF-3LL",
    "BLOOD ADDER": "COU-BA",
    "COUGAR COU-PRIME(S)": "COU-PRIMES",
    "K-9": "UM-K9",
    "STREET CLEANER": "UM-SC",
    "URBANMECH UM-R68(L)": "UM-R68L",
    "SNOWBALL": "UM-SB",
    "BOILER": "SNV-BR",
    "SUPERNOVA SNV-1(S)": "SNV-1S",
    "MEAN BABY": "ANH-MB",
    "ANNIHILATOR ANH-2A(S)": "ANH-2AS",
    "BLACKJACK BJ-2(L)": "BJ-2L",
    "DEATHSTRIKE": "MCII-DS",
    "MAD CAT MK II MCII-1(S)": "MCII-1S",
    "PIRATES' BANE": "LCT-PB",
    "KNOCKOUT": "MAL-KO",
    "MAULER MAL-MX90(C)": "MAL-MX90C",
    "KATANA KAT": "PNT-KK",
    "PANTHER PNT-10K(R)": "PNT-10KR",
    "HELLBRINGER HBR-F(L)": "HBR-FL",
    "HELLBRINGER HBR-F(C)": "HBR-FC",
    "JADE KITE": "NTG-JK",
    "NIGHT GYR NTG-PRIME(S)": "NTG-PRIMES",
    "NIGHT GYR NTG-H(L)": "NTG-HL",
    "MAUL": "WHM-IIC-ML",
    "WOLFHOUND WLF-1(C)": "WLF-1C",
    "GRINNER": "WLF-GR",
    "QUARANTINE": "WVR-Q",
    "BLUDGEON": "WHM-IIC-BL",
    "NANUQ": "WHK-NQ",
    "RIVAL": "VGL-RV",
    "VAPOR EAGLE VGL-1(S)": "VGL-1S",
    "VINDICATOR VND-1AA(C)": "VND-1AAC",
    "THUNDERBOLT TDR-10SE(S)": "TDR-10SES",
    "TIMBER WOLF TBR-C(C)": "TBR-CC",
    "MISERY": "STK-M",
    "VANGUARD": "SNS-VN",
    "SHADOW CAT SHC-PRIME(C)": "SHC-PRIMEC",
    "MISHIPESHU": "SHC-MISH",
    "STORMCROW SCR-PRIME(S)": "SCR-PRIMES",
    "STORMCROW SCR-PRIME(C)": "SCR-PRIMEC",
    "HUGINN": "RVN-H",
    "POWERHOUSE": "RGH-PH",
    "LEGEND-KILLER": "RFL-LK",
    "DAO BREAKER": "RFL-DB",
    "RIFLEMAN RFL-8D(L)": "RFL-8DL",
    "PHOENIX HAWK PXH-2(C)": "PHX-2C",
    "FIREBALL": "PHX-FB",
    "PIRANHA PIR-1(S)": "PIR-1S",
    "OSIRIS OSR-3D(S)": "OSR-3DS",
    "ORION IIC ON1-IIC-A(C)": "ON1-IIC-AC",
    "SKÖLL": "ON1-IIC-SK",
    "EBON DRAGOON": "MLX-ED",
    "REVENANT": "MDD-RV",
    "BANDIT": "MDD-BD",
    "MARAUDER IIC MAD-IIC-2(L)": "MAD-IIC-2L",
    "SCORCH": "MAD-IIC-SC",
    "BOUNTY HUNTER II": "MAD-BH",
    "ALPHA": "MAD-AL",
    "MARAUDER MAD-9M(S)": "MAD-9MS",
    "MARAUDER II MAD-4A(S)": "MAD-4AS",
    "LINEBACKER LBK-H(L)": "LBK-HL",
    "KING CRAB KGC-001(S)": "KGC-001S",
    "KING CRAB KGC-000B(C)": "KGC-000BC",
    "KIT FOX KFX-G(L)": "KFX-GL",
    "PURIFIER": "KFX-PR",
    "SPIRIT BEAR": "KDK-SB",
    "KODIAK KDK-3(C)": "KDK-3C",
    "JAVELIN JVN-11F(L)": "JVN-11FL",
    "JAVELIN JVN-10N(S)": "JVN-10NS",
    "OXIDE": "JR7-IIC-OX",
    "JENNER IIC JR7-IIC(C)": "JR7-IICC",
    "JENNER JR7-F(C)": "JR7-FC",
    "VOID": "HLF-V",
    "HIGHLANDER IIC HGN-IIC-C(C)": "HGN-IIC-CC",
}


def login_to_mwo(ffox):
    """
    Prompt for username / passwd
    Open the selenium-driven browser
    Log in
    Return the browser object
    """
    try:
        print("Enter user email: ", end="")
        email = input()

        passwd = getpass("Enter user password: ")
    except KeyboardInterrupt:
        print("Aborted by user during username/password entry...")
        sys.exit()

    else:
        try:
            ffox.get(PROF_URL)

            login_link = ffox.find_element_by_link_text("LOGIN")
            login_link.click()

            email_input = ffox.find_element_by_id("email")
            email_input.send_keys(email)

            psswd_input = ffox.find_element_by_id("password")
            psswd_input.send_keys(passwd)
            psswd_input.submit()
        except (
            ProtocolError,
            MaxRetryError,
            NewConnectionError,
            WebDriverException,
        ):
            print("Aborted while attempting login. Bye!")
            ffox.quit()
            ffox.close()
            sys.exit()
        try:
            alert = ffox.find_element_by_class_name("alert alert-error").text.strip()
            if "Invalid email/password" in alert:
                print("Invalid email/password entered, please try again.")
                login_to_mwo(ffox)
        except NoSuchElementException:
            debug(5, ["Logged in!"])


def get_mechbays(ffox):
    """
    Retrieve the profile page
    Iterate over mechBay classed tags and return the dictionary of owned my_mechs
    """
    global args

    ffox.get(PROF_URL)
    debug(1, ["Retrieving data from:", PROF_URL])
    mech_bays = ffox.find_elements_by_class_name("mechBay")
    mech_bay = {}
    for bay in mech_bays:
        debug(2, [bay.text.strip()])
        try:
            mech_bay[bay.text.strip()] += 1
        except KeyError:
            mech_bay[bay.text.strip()] = 1

    return mech_bay


def get_stat_data(url, ffox):
    """
    Retrieve the specific stats page
    Find the table of stats and store each row as a dictionary entry under the first column
    Return the dictionary of stats
    """
    global args

    ffox.get(url)
    debug(1, ["Retrieving data from:", url])
    my_stats = {}
    stat_list = [x.text.strip() for x in ffox.find_elements_by_xpath("//thead/tr/th")]
    for obj in ffox.find_elements_by_xpath("//tbody/tr"):
        idx = 0
        obj_name = ""
        for stat in obj.find_elements_by_tag_name("td"):
            debug(3, [stat.text.strip()])
            if idx == 0:
                obj_name = stat.text.strip()
                my_stats[obj_name] = {}
            else:
                my_stats[obj_name][stat_list[idx]] = stat.text.strip()
            idx += 1

    return my_stats


def get_owner_data(mechbays, stats):
    """
    Check stats entries against mechbay contents to see if you currently own the mech
    """
    global args
    debug(1, ["Parsing mechbay data for stats"])
    for mech in stats.keys():
        bay = mech
        debug(4, [mech])
        if mech in MECH_NAME.keys():
            bay = MECH_NAME[mech]

        bay = bay.split(" ")[-1]  # Get the end of the mech name
        debug(2, [bay])
        stats[mech]["Owned"] = bool(bay in mechbays.keys())

    return stats


def debug(lvl, msg):
    """
    Print debug messages if the debug level is appropriate
    """
    if args.verbose >= lvl:
        print("Debug" + str(lvl), ":", " ".join(msg))


def main():
    """
    Main processing
    """
    global args

    # Set up the log location for the geckodriver so we can delete it later
    geckolog = args.log
    if args.log is None:
        print("Something went very wrong! Unable to log to 'None'. Aborting.")
        sys.exit()

    # Set up the webdriver instance here so we can close it no matter what happens
    browser = webdriver.Firefox(service_log_path=geckolog)

    try:
        # Prompt the user for email/password and log in
        login_to_mwo(browser)
    except KeyboardInterrupt:
        print("Aborted by user during login. Bye!")
        browser.quit()
        browser.close()
        sys.exit()

    try:
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

        if args.format == "dump":
            pprint.pprint(my_mechs)
            pprint.pprint(my_mech_stats)
            pprint.pprint(my_weap_stats)
            pprint.pprint(my_maps_stats)
            pprint.pprint(my_mode_stats)

    except KeyboardInterrupt:
        print("Aborted post-login by user. Bye!")
        browser.quit()
        browser.close()
        sys.exit()
    except (
        MaxRetryError,
        NewConnectionError,
        WebDriverException,
    ) as e:
        print(e)
        browser.quit()
        browser.close()
    finally:
        browser.close()
        browser.quit()

    if args.retain:
        os.unlink(geckolog)


def parse_args(argv):
    """
    parse command-line arguments
    """
    parser = argparse.ArgumentParser(description="Gather and Process player statistics from MWO profile")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument(
        "--log",
        action="store",
        help="Log file for geckodriver",
        default="/tmp/geckodriver.log",
    )
    parser.add_argument(
        "--retain",
        action="store_true",
        help="Retain the webdriver log after completing",
        default=False,
    )
    parser.add_argument(
        "--format",
        action="store",
        choices=["csv", "xml", "dump", "keys", "xls"],
        default="dump",
        help="Output format",
    )

    return parser.parse_args(argv)


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
        main()
    except KeyboardInterrupt:
        print("Aborting...")
