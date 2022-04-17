from posixpath import split
from pprint import pprint as pp

class BaseAward:
    """Base Class for Awards

    Raises:
        ValueError: Award Name and Type can not be None
    """
    award_name = "Award Name"
    award_type = "Award Type"
    award_when = None


    @property
    def name(self) -> str:
        """Get the name of the award

        Returns:
            str: Name of the award
        """
        return self.award_name
    

    @name.setter
    def name(self,name):
        """Set the name of the award

        Args:
            name (str): Name of the award

        Raises:
            ValueError: Name can not be empty or None
        """
        if name is not None and name != "":
            self.award_name = name
        else:
            raise ValueError('Award name can not be empty')
    

    @property
    def awardtype(self) -> str:
        """Get the type of award

        Returns:
            str: Type of the award
        """
        return self.award_type
    

    @awardtype.setter
    def awardtype(self,atype):
        """Set the type of award

        Args:
            atype (str): Type of award (general, individual, lance, company, battalion, medical, performance, longevity)

        Raises:
            ValueError: Type can not be empty or none
        """
        if atype in self.valid_types:
            self.award_type = atype
        else:
            raise ValueError('Award type can not be empty')
    

    @property
    def when(self) -> dict:
        """Get the criteria for the award

        Returns:
            dict: Dictionary of criteria to check
        """
        return self.award_when
    

    @when.setter
    def when(self,criteria):
        """Set the criteria for the award

        Args:
            criteria (dict): Criteria to check
        """
        self.award_when = criteria
    

    def is_eligible(self) -> bool:
        """Base criteria

        Returns:
            True
        """
        return True


class KillAward(BaseAward):
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'pilot', 'lance', 'company', 'battalion' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen

    def __str__(self):
        return "{} is awarded to a {} with {} or more kills in a {}".format(self.name, self.awardtype, list(self.when.values())[0], list(self.when.keys())[0])

    # __repr__ = __str__


class PilotKillAward(KillAward):
    """Class for Pilot Kill Awards
    """
    # To do: define Pilot class to has method to retrieve kills in a given scenario as well as kills in a given mission
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the kill award.

        Returns:
            bool
        """
        # If sum of all pilot kills > when return True
        return False


class LanceKillAward(KillAward):
    """Class for lance-level Kill Awards
    """
    # To do: define Pilot class to has method to retrieve kills in a given scenario as well as kills in a given mission
    def is_eligible(self) -> bool:
        """Check if lance is eligible for the kill award.

        Returns:
            bool
        """
        # If sum of all pilot kills in lance > when return True
        return False

class CompanyKillAward(KillAward):
    """Class for company-level Kill Awards
    """
    # To do: define Pilot class to has method to retrieve kills in a given scenario as well as kills in a given mission
    def is_eligible(self) -> bool:
        """Check if company is eligible for the kill award.

        Returns:
            bool
        """
        # If sum of all pilot kills in company > when return True
        return False

class BattalionKillAward(KillAward):
    """Class for Battalion-level Kill Awards
    """
    # To do: define Pilot class to has method to retrieve kills in a given scenario as well as kills in a given mission
    def is_eligible(self) -> bool:
        """Check if battalion is eligible for the kill award.

        Returns:
            bool
        """
        # If sum of all pilot kills in battalion > when return True
        return False


class MedicalAward(BaseAward):
    """Class for medical awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'medical' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen

    # To do: define Pilot class to have method to retrieve whether pilot was injured in scenario
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the medical award (did they return from combat with an injury)

        Returns:
            bool
        """
        return False

    def __str__(self):
        return "{} is awarded to someone that received {} or more injures in combat".format(self.name, list(self.when.values())[0])


class SkillAward(BaseAward):
    """Class for skill awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'skill' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Pilot class to have method to retrieve skill levels
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the skill award

        Returns:
            bool
        """
        return False

    def __str__(self):
        return "{} is awarded to someone with a {} skill of {}".format(self.name, list(self.when.keys())[0], list(self.when.values()))


class StatusAward(BaseAward):
    """Class for status awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'status' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Pilot class to have method to retrieve status changes from activity log
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the status award (did their status change appropriately)

        Returns:
            bool
        """
        return False

    def __str__(self):
        if "prisoner" in self.when:
            return '{} is a awarded to someone with a {} log entry of "{}" and prisoner status of {}'.format(self.name, self.when['log'], self.when['status'], self.when['prisoner'])
        else:
            return '{} is a awarded to someone with a {} log entry of "{}"'.format(self.name, self.when['log'], self.when['status'])


class DurationAward(BaseAward):
    """Class for service (duration) awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'duration' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Pilot class to have method to retrieve time in service levels
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the award

        Returns:
            bool
        """
        return False

    def __str__(self):
        return "{} is awarded to someone who has served for {}".format(self.name, list(self.when.values()))


class CampaignAward(BaseAward):
    """Class for service (duration) awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'campaign' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Mission class to have method to retrieve employer, enemy, mission type, start, and end
    def is_eligible(self) -> bool:
        """Check if pilot participated in appropriate mission

        Returns:
            bool
        """
        return False

    def __str__(self):
        description = '{} is awarded to someone who participated in the {}'.format(self.name, self.when['name'])
        if "employer" in self.when:
            description = description + " for {}".format(self.when["employer"])
        if "enemy" in self.when:
            description = description + " against {}".format(self.when["enemy"])
        if "start" in self.when and "end" in self.when:
            description = description + " between {} and {}".format(self.when["start"], self.when["end"])
        return description


class TrainingAward(BaseAward):
    """Class for service (duration) awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'training' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Force class to have method to retrieve pilots
    # To do: define Mission/Scenario classes to know which forces are deployed in what roles
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the status award (did their status change appropriately)

        Returns:
            bool
        """
        return False

    def __str__(self):
        description = '{} is awarded to someone who spent '.format(self.name)
        if "status" in self.when and "duration" in self.when:
            duration = self.when["duration"].split(":")
            description = description + "{} {} in academy training as {}".format(duration[0],duration[1],self.when["status"])
        if "deployment" in self.when:
            description = description + "time in a {} lance".format(self.when["deployment"])
        return description


class RoleAward(BaseAward):
    """Class for service (duration) awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'role' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Force class to have method to retrieve commander (highest ranked pilot)
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the role award (did act in some capacity)

        Returns:
            bool
        """
        return False

    def __str__(self):
        description = '{} is awarded to someone who {} in a {} mission.'.format(self.name,"commanded a training force" if self.when['commander'] else "participated",self.when['mission_type'])
        return description


class SupportAward(BaseAward):
    """Class for service (duration) awards
    """
    def __init__(self,aname: str,atype: str,awhen: dict):
        self.valid_types = [ 'support' ]
        self.name = aname
        self.awardtype = atype
        self.when = awhen


    # To do: define Force class to have method to retrieve commander (highest ranked pilot)
    def is_eligible(self) -> bool:
        """Check if pilot is eligible for the role award (did act in some capacity)

        Returns:
            bool
        """
        return False

    def __str__(self):
        description = '{} is awarded to someone for outstanding support on an {} basis.'.format(self.name, self.when['when'])
        return description


def GetAward(aname,atype,criteria):
    """Class for kill awards

    These are awards based on the number of kills in a scenario or mission

    Criteria ('when' setter):
        { 'scenario or mission': number_of_kills } => If 'type' has greater than or equal to the number_of_kills in (scenario|mission)

    """
    awardmap = {
        "pilot": PilotKillAward,
        "lance": LanceKillAward,
        "company": CompanyKillAward,
        "battalion": BattalionKillAward,
        "medical": MedicalAward,
        "skill": SkillAward,
        "status": StatusAward,
        "duration": DurationAward,
        "campaign": CampaignAward,
        "training": TrainingAward,
        "role": RoleAward,
        "support": SupportAward,
    }

    try:
        award = awardmap[atype](aname,atype,criteria)
        return award
    except Exception as e:
        raise(TypeError,'Unknown Award type {}'.format(atype))


