#!/usr/bin/env python3

from campaign import campaign

if __name__ == "__main__":
    my_campaign = campaign.Campaign(sys.argv[1])
    my_campaign.readCampaign()


