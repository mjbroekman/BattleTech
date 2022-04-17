import sys
import re
import io
import gzip
import os.path
import awards

from pathlib import Path
from pprint import pprint as pp


class Campaign:
    """Class to hold any/all campaign information for a MekHQ campaign
    """
    campaign_config_file = ""
    campaign_config = {}
    campaign_data = None
    award_data = {}
    award_config = {}

    def __init__(self,campaign_config):
        """Initializes a campaign object

        Args:
            campaign_config (string): Path to the campaign configuration file
        """
        self.campaign_config_file = campaign_config
        try:
            self._load_config()
            self._check_config()
        except Exception as e:
            self._error(e,'Configuration error detected')

        try:
            self._load_awards()
            self._parse_awards()
        except Exception as e:
            self._error(e,'Error loading award data')

        try:
            self._find_latest_save()
        except Exception as e:
            self._error(e,'Error finding latest save')


    def readCampaign(self):
        """Read in the latest campaign save and prepares it for queries

        Args:
            none
        
        Returns:
            maybe, but probably not
        
        Exceptions:
            probably
        """
        self._open_campaign_file()


    def _load_awards(self):
        """Load awards from the Awards Stuff sub-directory of the install directory
        """
        try:
            award_file = self.campaign_config['CAMPAIGN']['installdir'] / "docs/Award Stuff" / "Award Guide.md"
            with open(award_file,'rt') as awards:
                award_list = False
                award_name = re.compile(r'^\#\#\#.*?\!\[\]\(.*?png\) (.*?)$')
                award_crit = re.compile(r'^\*\*_Criteria:_\*\* (.*?)$')
                award_play = re.compile(r'^\*\*_Gameplay:_\*\* (.*?)$')
                last_award = None
                criteria = None
                for line in awards:
                    if not award_list and 'Available Awards' in line:
                        continue
                    if not award_list:
                        award_list = True
                        continue
                    name = award_name.search(line)
                    if name is None and last_award is None:
                        continue
                    if name is not None and name.group(1) not in self.award_data.keys():
                        last_award = name.group(1)
                        self.award_data[last_award] = { "criteria": None, "gameplay": None }
                        continue
                    criteria = award_crit.search(line)
                    if criteria is not None and last_award is not None:
                        self.award_data[last_award].update({ "criteria": criteria.group(1) })
                        criteria = None
                        continue
                    gameplay = award_play.search(line)
                    if gameplay is not None and last_award is not None:
                        self.award_data[last_award].update({ "gameplay": gameplay.group(1) })
                        gameplay = None
                        continue
        except Exception as e:
            self._error(e,"Error opening or reading from Awards file")


    def _parse_awards(self):
        """Parse the Awards file into Awards objects

        This is ugly as heck
        """
        kill_award = re.compile(r'(\d+) (pilot|lance|company|battalion) kills in a (mission|scenario)',re.IGNORECASE)
        skill_award = re.compile(r'(\w+) skill of (\d+) or (\d+)',re.IGNORECASE)
        campaign_ribbon = re.compile(r'^Partook.*?in support of (?:the )?(.*?) (?:under the employment of (?:the )?(.*?) )?between (.*?) and (.*?)\.$',re.IGNORECASE)
        alt_campaign = re.compile(r'^Partook.*?(?:in support of|on a|against) (fedcom civil war|periphery world|pirates)\.$',re.IGNORECASE)
        duration_award = re.compile(r'^(?:Award for (every)|Served (?:a total of|over)?) ?(\d+) (\w+)? ?(months|years)(?: in(?: a)? (foreign theatre)| with (no disciplinary action))?',re.IGNORECASE)
        training_award = re.compile(r'Graduate of (.*?)\.$',re.IGNORECASE)
        training_req = re.compile(r'status changed? to "([^\'"]+)" for (\d+) (\w+)',re.IGNORECASE)
        basic_req = re.compile(r'non-ranked.*?(green)',re.IGNORECASE)
        service_award = re.compile(r'served as (.*?)\.$',re.IGNORECASE)
        instructor_req = re.compile(r'instructor',re.IGNORECASE)
        service_req = re.compile(r'Recommended at (?:the )?end of (?:a )?(.*?) mission',re.IGNORECASE)
        for award, data in list(self.award_data.items()):
            criteria = data['criteria']
            gameplay = data['gameplay']

            kills = kill_award.search(criteria)
            if kills is not None:
                self.award_config.update({ award: awards.GetAward(award,kills.group(2), { kills.group(3): kills.group(1)} ) })
                self.award_data.pop(award)
                continue

            skills = skill_award.search(criteria)
            if skills is not None:
                self.award_config.update({ award: awards.GetAward(award, "skill", { skills.group(1): ( skills.group(2), skills.group(3) ) } ) })
                self.award_data.pop(award)
                continue

            campaigns = campaign_ribbon.search(criteria)
            if campaigns is not None:
                employers = campaigns.group(2)
                if employers is None:
                    employers = campaigns.group(1)
                self.award_config.update({ award: awards.GetAward(award, "campaign", { "name": campaigns.group(1), "employer": list(filter(lambda x: x != "", re.split(r'(?:,\s*|or |a |the )',employers))), 'start': campaigns.group(3), 'end': campaigns.group(4) } ) })
                self.award_data.pop(award)
                continue

            campaigns = alt_campaign.search(criteria)
            if campaigns is not None:
                self.award_config.update({ award: awards.GetAward(award, "campaign", { "name": "fighting", "enemy": campaigns.group(1) } ) })
                self.award_data.pop(award)
                continue

            duration = duration_award.search(criteria)
            if duration is not None:
                self.award_config.update({ award: awards.GetAward(award, "duration", { 'duration': duration.groups() }) })
                self.award_data.pop(award)
                continue

            training = training_award.search(criteria)
            if training is not None:
                requirement = training_req.search(gameplay)
                if requirement is None:
                    requirement = basic_req.search(gameplay)
                
                if requirement.group(1).title() == "Green":
                    self.award_config.update({ award: awards.GetAward(award, "training", { 'deployment': 'training' } ) })
                else:
                    self.award_config.update({ award: awards.GetAward(award, "training", { 'status': requirement.group(1), 'duration': "{}:{}".format(requirement.group(2),requirement.group(3)) } ) })
                self.award_data.pop(award)
                continue

            service = service_award.search(criteria)
            if service is not None:
                requirement = service_req.search(gameplay)
                commander = instructor_req.search(criteria)
                if commander is not None:
                    self.award_config.update({ award: awards.GetAward(award, "role", { "mission_type": requirement.group(1), "commander": True } ) })
                else:
                    self.award_config.update({ award: awards.GetAward(award, "role", { "mission_type": requirement.group(1), "commander": False } ) })
                self.award_data.pop(award)
                continue

            if award == 'PURPLE HEART':
                self.award_config.update({ award: awards.GetAward(award, "medical", { 'scenario': 1} ) })
            if award == 'PRISONER OF WAR':
                self.award_config.update({ award: awards.GetAward(award, "status", { 'log': 'personnel', 'status': 'recovered from mia' }) })
            if award == 'COMBAT ACTION':
                self.award_config.update({ award: awards.GetAward(award, "status", { 'log': 'mission', 'status': 'participated in', 'prisoner': False } )})
            if award == 'HOUSE DEFENSE':
                self.award_config.update({ award: awards.GetAward(award, "campaign", { 'name': 'defense', 'employer': "House", 'mission_type': [ 'Cadre Duty', 'Garrison Duty' ], "when": "mission" } ) })
            if award == 'EXPEDITIONARY':
                self.award_config.update({ award: awards.GetAward(award, "campaign", { 'name': 'combat', 'employer': "any", 'mission_type': [ 'Guerilla', 'Extraction Raid' ], 'state': 'non-war', "when": "mission" } ) })
            if award == 'COVERT OPS':
                self.award_config.update({ award: awards.GetAward(award, "campaign", { 'name': 'covert', 'employer': "any", 'mission_type': [ 'Guerilla', 'Extraction Raid' ], "when": "mission" } ) })
            if award == 'HUMANITARIAN SERVICE':
                self.award_config.update({ award: awards.GetAward(award, "campaign", { 'name': 'defense', 'employer': "civilians", 'when': "scenario" } ) })
            if award == 'SUPPORT PERSON OF THE YEAR':
                self.award_config.update({ award: awards.GetAward(award, "support", { 'when': 'annual' } ) })
            if award == 'MEDAL OF HONOR':
                # This is not an award that can or should be 'suggested'. Ever. This is GM discretion.
                pass
            self.award_data.pop(award)
            continue

        for value in self.award_config.values():
            print(value.__str__())

    def _open_campaign_file(self):
        """Opens the campaign file

        Returns:
            Nothing
        """
        try:
            if os.path.splitext(self.campaign_config['CAMPAIGN']['latest'])[1] == ".gz":
                self._parse_campaign_file(gzip.open(self.campaign_config['CAMPAIGN']['latest'],'rt'))
            if os.path.splitext(self.campaign_config['CAMPAIGN']['latest'])[1] == ".cpnx":
                self._parse_campaign_file(open(self.campaign_config['CAMPAIGN']['latest'],'rt'))
        except OSError as e:
            self._error(e,'Error attempting to open ()'.format(self.campaign_config['CAMPAIGN']['latest']))


    def _parse_campaign_file(self,opened_file: io.TextIOWrapper):
        """Reads and parses the campaign save

        Args:
            none

        Returns:
            none
        
        Exceptions:
            probably
        """
        self.campaign_data = None # This will hold the parsed data
        for line in opened_file.readlines():
            pass
        
        opened_file.close()


    def _load_config(self):
        """Loads the config file passed to the constructor

        Args:
            none
        
        Returns:
            none
        
        Exceptions:
            OSError through self._error
        """
        self.campaign_config = self._get_defaults()
        section = re.compile(r"^\[\s*([^]]+)\s*\]")
        config = re.compile(r"^(\w+)[\s=:]+([^\r\n]+)[\r\n]*$")

        try:
            with open(self.campaign_config_file,mode='rt',encoding='utf-8') as configfile:
                current_section = ''
                for line in configfile:
                    section_name = section.match(line)
                    if section_name is not None:
                        current_section = section_name.group(1)
                        next

                    if current_section == '':
                        next

                    config_value = config.match(line)
                    if config_value is not None:
                        self.campaign_config[current_section][config_value.group(1)] = config_value.group(2)
                        next
                    next

        except OSError as e:
            self._error(e, 'Error accessing ' + self.campaign_config_file)


    def _check_config(self):
        """Checks and validates that the configuration is good

        Args:
            none
        
        Returns:
            none
        
        Exceptions:
            through self._error
        """
        def yesno(value) -> bool:
            if value == "yes" or value == "no":
                return True
            else:
                return False

        error_msg = 'Section "{}" setting "{}" must be "yes" or "no", not "{}"'
        for section in self.campaign_config:
            if section == 'AWARDS':
                for setting in self.campaign_config[section]:
                    if not yesno(self.campaign_config[section][setting]):
                        self._error(TypeError, error_msg.format(section, setting, self.campaign_config[section][setting]))

            if section == 'CAMPAIGN':
                self._get_dir("savedir")
                self._get_dir("installdir")


    def _find_latest_save(self):
        """Finds the latest savegame file

        This searches the savedir for files matching {save_regex}.
        {latest} is set to the datestamp in the filename if the datestamp is later than {latest}

        Raises:
            OSError if no savegame file is found
        """
        latest = 0
        savedir = Path(self.campaign_config['CAMPAIGN']['savedir'])
        save_regex = self._get_save_regex()

        for savegame in savedir.rglob("*" + self.campaign_config['CAMPAIGN']['name'] + "*"):
            gamefile = save_regex.search(savegame.as_posix())
            if gamefile is not None:
                if int(gamefile.group(1)) > latest:
                    latest = int(gamefile.group(1))
                    self.campaign_config['CAMPAIGN']['latest'] = savegame

        if self.campaign_config['CAMPAIGN']['latest'] is None:
            self._error(OSError,'No savegame found matching {}'.format(save_regex))


    def _get_save_regex(self) -> re:
        """Builds the savegame regex for matching based on campaign configuration

        Uses the 'compressed' campaign configuration:
            'compressed' == "yes"  : regex ends in .gz
            'compressed' == "no"   : regex ends in .cpnx
            'compressed' == "auto" : regex ends in (?:\.gz)?

        Returns:
            re: Regular expression for matching
        """
        saveglob = r"(?:Autosave-\d+-)?{}-?(\d+)\.cpnx".format(self.campaign_config['CAMPAIGN']['name'])

        if self.campaign_config['CAMPAIGN']['compressed'] == "yes":
            saveglob = saveglob + "\.gz"
        if self.campaign_config['CAMPAIGN']['compressed'] == "auto":
            saveglob = saveglob + "(?:\.gz)?"
        saveglob = saveglob + "$"
        return re.compile(saveglob)


    def _get_dir(self, setting):
        """Confirms the specified directory

        Args:
            setting: path object to the directory specified in the campaign configuration
        
        Raises:
            OSError (through self._error) is the directory does not exist
        """
        config_dir = Path(self.campaign_config['CAMPAIGN'][setting]).expanduser()
        if not config_dir.exists():
            self._error(OSError,'No such directory: {}'.format(config_dir))
        else:
            self.campaign_config['CAMPAIGN'][setting] = config_dir
        

    def _error(self, exception: Exception, message):
        """Prints a message or raises exception depending on context
        
        Args:
            exception: Exception to print or raise
            message: supplementary message to print
        
        Raises:
            exception passed in
        """
        if __name__ == '__main__':
            print(str(exception) + message)
            raise Exception(message) from exception
        else:
            raise Exception(message) from exception


    def _get_defaults(self):
        """Default campaign settings in case the user didn't provide all values

        Args:
            none

        Returns:
            dict - default values
        """
        return {
                'CAMPAIGN' : {
                    'savedir' : '/home',
                    'installdir': '/home/user/mekhq',
                    'name' : 'My Campaign',
                    'compressed' : 'yes',
                    'latest' : None,
                },
                'AWARDS' : {
                    'same_day' : 'yes',
                    'validate' : 'no',
                    'individual' : 'yes',
                    'lance' : 'yes',
                    'company' : 'yes',
                    'scenario' : 'yes',
                    'mission' : 'yes',
                    'campaign' : 'yes',
                }
            }


if __name__ == "__main__":
    campaign = Campaign(sys.argv[1])
    campaign.readCampaign()



#
#
# Testing: ~/.../PyMek $ python src/pymek/campaign.py campaign.config
# class campaign
#
#   class mission
#     missionId
#     missionName
#     missionStart
#     missionEnd
#
#     list scenarios
#
#     class scenario
#       scenarioId
#
#       class kill(?)
#
#   class force
#     forceId
#     forceName
#
#   class unit
#     unitId
#     driverId = personId
#     gunnerId = personId
#
#   class person
#     personId
#     personName
#     personRole
#
#     unit = unitId
#
#      list awards
#       date
#       name
#
#     list activity_log
#       dict log_entry
#         date
#         type
#         desc