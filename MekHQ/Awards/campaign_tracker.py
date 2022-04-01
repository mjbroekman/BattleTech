import configparser

with open('campaign.config','r') as configfile:
    config.read(configfile)

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