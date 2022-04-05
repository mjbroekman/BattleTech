import sys
import re

from pprint import pprint as pp

class Campaign:
    """Class to hold any/all campaign information for a MekHQ campaign
    """

    campaign_config_file = ""
    campaign_save = ""
    campaign_config = {}

    def __init__(self,campaign_config):
        self.campaign_config_file = campaign_config

    def readCampaign(self):
        """Read in the latest campaign save and prepares it for queries

        Args:
            none
        
        Returns:
            maybe, but probably not
        
        Exceptions:
            probably
        """
        self._load_config()
        pp(self.campaign_config)
        self._get_campaign_file()
        self._parse_campaign_file()


    def _parse_campaign_file(self):
        """Reads and parses the campaign save

        Args:
            none

        Returns:
            none
        
        Exceptions:
            probably
        """
        pass


    def _get_campaign_file(self):
        """Finds the latest campaign file

        Args:
            none
        
        Returns:
            none
        
        Exceptions:
            probably
        """
        import os
        
        pass


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


    def _error(exception, message):
        """Prints a message or raises exception depending on context
        
        Args:
            exception: Exception to print or raise
            message: supplementary message to print
        
        Raises:
            exception passed in
        """
        if __name__ == '__main__':
            print(exception + message)
        else:
            raise exception


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
                    'name' : 'My Campaign',
                    'compressed' : 'yes', },
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