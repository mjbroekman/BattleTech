#!/usr/bin/env python3

import sys
import campaign

if __name__ == "__main__":
    my_campaign = campaign.Campaign(sys.argv[1])
    my_campaign.readCampaign()


