#!/usr/bin/env python3

import sys
from pymek import campaign

if __name__ == "__main__":
    my_campaign = campaign.Campaign(sys.argv[1])
    my_campaign.readCampaign()


