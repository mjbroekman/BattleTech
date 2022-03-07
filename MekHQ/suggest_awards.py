#!/usr/bin/env python3
"""
Parse a campaign file and determine which awards are appropriate for personnel

# TODO:
- check for first combat (Combat Action)
- check for end of current mission/contract (Marksmanship / Expert Marksmanship)
- check for employer / enemy and date (various contract type rewards)
"""

import sys
import gzip
import xml.etree.ElementTree as ETree
import getopt
import os
import re

check_campaign = False
file_name = "MyCampaign.cpnx"
debug = False
campaign = ""
save_date = ""
cumulative = False
current_toe = False


def main(argv):
    """
    Process command-line arguments
    """
    global file_name
    global debug
    global check_campaign
    global cumulative
    global current_toe

    try:
        opts, args = getopt.getopt(
            argv,
            "hcdf:nv",
            ["--help", "--cumulative", "--debug", "--filename=", "--now", "--verify"],
        )
        if len(args) > 0:
            print(args)
    except getopt.GetoptError as err:
        usage(str(err))

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage("")
        elif opt in ("-f", "--filename"):
            if not os.path.exists(arg):
                usage("File " + arg + " is missing")
            file_name = arg
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-v", "--verify"):
            check_campaign = True
        elif opt in ("-c", "--cumulative"):
            cumulative = True
        elif opt in ("-n", "--now"):
            current_toe = True
        else:
            usage("unknown option")

    open_campaign()


def open_campaign():
    """
    open up the campaign file and make sure it's proper
    """
    file_xml = ""
    try:
        with gzip.open(file_name, "rb") as cpg_file:
            file_xml = cpg_file.read()
    except gzip.BadGzipFile as gzip_e:
        if debug:
            print(gzip_e)
        try:
            with open(file_name, "r") as big_file:
                file_xml = big_file.read()
        except FileNotFoundError as file_e:
            print("File not found but path exists")
            print(file_e)
            sys.exit(len(file_e))
        except IsADirectoryError as file_e:
            print(file_name + " is a directory.")
            sys.exit(len(file_e))
        except PermissionError as file_e:
            print("Permissions error.")
            sys.exit(len(file_e))

    if debug:
        print(len(file_xml))

    parse_campaign(file_xml)


def parse_campaign(file_xml):
    """
    parse the campaign XML file
    """
    global campaign
    global save_date
    campaign = ETree.fromstring(file_xml)
    save_date = campaign.find("info").find("calendar").text
    print("Parsing campaign as of " + save_date)

    check_awards()


def check_awards():
    """
    Check for eligible awards
    """
    check_personal_awards()
    check_mission_awards()
    check_scenario_awards()


def check_personal_awards():
    """
    Check for personal awards
    """
    for person in campaign.find("personnel"):
        person_id = person.find("id").text
        person_name = get_pilot_name(person_id)
        if len(person_name) == 0:
            continue
        if ETree.iselement(person.find("prisonerStatus")):
            if debug:
                print(person_name + " is a prisoner")
            continue

        if person.find("status").text != "ACTIVE":
            if debug:
                print(person_name + " is " + person.find("status").text)
            continue

        if debug:
            print(person_name + " is a full member")

        if not ETree.iselement(person.find("personnelLog")):
            print("No personnelLog found for " + person_name)
            continue

        check_personnel_log(person)


def check_mission_awards():
    """
    parse the mission structure in a campaign
    """
    global current_toe
    global save_date
    global check_campaign

    for mission in campaign.find("missions"):
        mission_type = mission.find("type").text
        mission_name = mission.find("name").text
        mission_start = mission.find("startDate").text
        mission_end = mission.find("endDate").text
        mission_emp = mission.find("employerCode").text
        mission_type = mission.find("type").text
        mission_foe = mission.find("enemyCode").text

        if mission_type == "Pirate Hunting" and is_major_house(mission_emp):
            print(mission_name + " grants the 'Galactic War on Pirating' to all members of the unit on " + mission_end)

        if mission_start >= "2866-01-01" and mission_end <= "3025-12-31" and is_3sw(mission_emp, mission_foe):
            print(mission_name + " grants the 'Third Succession War Campaign' to all members of the unit on " + mission_end)

        if mission_start >= "3028-08-19" and mission_end <= "3029-12-31" and is_4sw(mission_emp, mission_foe):
            print(mission_name + " grants the 'Fourth Succession War Campaign' to all members of the unit on " + mission_end)

        if mission_start >= "3030-09-01" and mission_end <= "3040-03-19" and is_andurien(mission_emp, mission_foe):
            print(mission_name + " grants the 'Andurien Wars Campaign' to all members of the unit on " + mission_end)

        if mission_start <= save_date <= mission_end and not check_campaign:
            continue


def is_major_house(faction):
    """
    Check if the faction is a great house
    """
    if faction in ("LA", "CC", "FWL", "DC", "FS", "FC"):
        return True

    return False


def is_3sw(employer, enemy):
    """
    Check if the mission is between combatants of the 3rd succession war
    """
    if is_major_house(employer) and is_major_house(enemy):
        return True

    return False


def is_4sw(employer, enemy):
    """
    Check if the faction is a 4th Succession War house
    """
    if employer == "FWL" or enemy == "FWL":
        return False

    if is_major_house(employer) and is_major_house(enemy):
        return True

    return False


def is_andurien(employer, enemy):
    """
    Check if the faction was part of the Andurien Wars
    """
    return all(f in ["FWL", "Andurien", "MoC", "CC"] for f in [employer, enemy])


def check_scenario_awards():
    """
    Check for end-of-scenario awards
    """
    check_scenario_kills()
    # check_personnel_log()


def check_scenario_kills():
    """
    Check for kill-related scenario awards
    """
    if debug:
        print("In check_scenario_kills()")
    kill_list = {}
    for kill in campaign.find("kills"):
        kill_date = kill.find("date").text
        if debug:
            print("Found a kill on " + kill_date + " by " + kill.find("pilotId").text)
        if kill_date in kill_list.keys():
            kill_list[kill_date].append(kill.find("pilotId").text)
        else:
            kill_list[kill_date] = []
            kill_list[kill_date].append(kill.find("pilotId").text)

    for date in sorted(kill_list.keys(), reverse=True):
        if debug:
            print("Processing kills on " + date)
        pilot_kills = {}
        for pilot in kill_list[date]:
            if pilot in pilot_kills.keys():
                pilot_kills[pilot] += 1
            else:
                pilot_kills[pilot] = 1

        for pilot in pilot_kills.keys():
            if debug:
                print("Checking kill awards for "+ get_pilot_name(pilot))
            get_kill_award(pilot_kills[pilot], pilot, date)

        if check_campaign is False:
            break


def get_kill_award(kills, pilot_id, date):
    """
    Get the awards for number of kills
    """
    global check_campaign
    global cumulative

    pilot_name = get_pilot_name(pilot_id)
    if debug:
        print("Checking kill awards for "+ pilot_name)
    if len(pilot_name) > 0:
        if kills >= 12:
            if check_stackable_award(pilot_id, date, "Combat Cross"):
                print(date + " : " + pilot_name + " has earned a COMBAT CROSS")
            if check_stackable_award(pilot_id, date, "Silver Star") and cumulative is True:
                print(date + " : " + pilot_name + " has earned a SILVER STAR")
            if check_stackable_award(pilot_id, date, "Bronze Star") and cumulative is True:
                print(date + " : " + pilot_name + " has earned a BRONZE STAR")

        elif kills >= 8:
            if check_stackable_award(pilot_id, date, "Silver Star"):
                print(date + " : " + pilot_name + " has earned a SILVER STAR")
            if check_stackable_award(pilot_id, date, "Bronze Star") and cumulative is True:
                print(date + " : " + pilot_name + " has earned a BRONZE STAR")

        elif kills >= 4:
            if check_stackable_award(pilot_id, date, "Bronze Star"):
                print(date + " : " + pilot_name + " has earned a BRONZE STAR")


def get_pilot(pilot_id):
    """
    Return the pilot object associated with the pilot ID or None if it can't be found
    """
    for person in campaign.find("personnel"):
        if person.find("id").text == pilot_id:
            return person

    return None


def get_pilot_name(pilot_id):
    """
    Return the pilot's name or the empty string if the pilot ID can't be found
    """
    person = get_pilot(pilot_id)
    if person is not None:
        return person.find("givenName").text + " " + person.find("surname").text

    return ""


def check_personnel_log(person):
    """
    Check the personnel log for the specified pilot object
    """
    person_name = person.find("givenName").text + " " + person.find("surname").text
    injury_list = []
    ph_list = []
    s_date = get_service_date(person)
    for logentry in person.find("personnelLog").findall("logEntry"):
        l_date = logentry.find("date").text
        if l_date <= s_date:
            continue
        if logentry.find("type").text == "MEDICAL":
            date = logentry.find("date").text
            if re.search("Returned from combat", logentry.find("desc").text) is not None:
                injury_list.append(date)

    awards = person.find("awards")
    if awards is not None:
        for award in person.find("awards").findall("award"):
            if award.find("name").text == "Purple Heart":
                for date in award.findall("date"):
                    ph_list.append(date.text)

    if len(injury_list) > len(ph_list):
        if debug:
            print("Injury dates:", end="")
            print(injury_list)
            print("Award dates: ", end="")
            print(ph_list)
        print(person_name + " is eligible for " + str(len(injury_list) - len(ph_list)) + " additional Purple Hearts")


def get_service_date(person):
    """
    get the beginning of service date for the person
    """
    date = person.find("recruitment")
    if date is None:
        return ""
    return date.text


def check_stackable_award(pilot_id, date, award_name, stackable=True):
    """
    Check the pilot for a specific award
    """
    pilot = get_pilot(pilot_id)
    if ETree.iselement(pilot.find("awards")):
        for award in pilot.find("awards").findall("award"):
            if award.find("name").text == award_name and not stackable:
                return False

            if award.find("name").text == award_name and stackable:
                for dates in award.findall("date"):
                    if debug:
                        print("Checking for " + award_name + " granted on " + date + " or " + save_date)
                    if date == dates.text or save_date == dates.text:
                        return False
                return True

    return True


def parse_personnel(roster):
    """
    parse the personnel structure in a campaign
    """
    personnel_list = []

    for person in roster:
        personnel_id = person.find("id").text
        personnel_name = person.find("givenName").text + " " + person.find("surname").text
        personnel_list.append([personnel_id, personnel_name])

    return personnel_list


def parse_units(units):
    """
    parse the unit structure in a campaign
    """
    unit_list = {}
    for unit in units:
        unit_id = unit.get("id")
        unit_list[unit_id] = []

        for crew in unit.findall("driverId"):
            try:
                unit_list[unit_id].index(crew.text)
            except ValueError:
                unit_list[unit_id].append(crew.text)
        for crew in unit.findall("gunnerId"):
            try:
                unit_list[unit_id].index(crew.text)
            except ValueError:
                unit_list[unit_id].append(crew.text)
        for crew in unit.findall("vesselCrewId"):
            try:
                unit_list[unit_id].index(crew.text)
            except ValueError:
                unit_list[unit_id].append(crew.text)

    return unit_list


def parse_forces(toe):
    """
    parse the forces structure in a campaign
    """
    force_list = {}
    for force in toe:
        force_name = force.find("name").text

        if ETree.iselement(force.find("subforces")):
            force_list[force_name] = parse_forces(force.find("subforces"))

        if ETree.iselement(force.find("units")):
            unit_list = []
            for unit in force.find("units"):
                unit_list.append(unit.get("id"))
                if debug:
                    print(unit.get("id"))
            force_list[force_name] = unit_list

    return force_list


def usage(msg):
    """
    Show the usage statement with an optional message
    """
    if len(msg) > 0:
        print(msg)
    else:
        print("suggest_awards.py -f <filename>")
    sys.exit(len(msg))


if __name__ == "__main__":
    main(sys.argv[1:])
