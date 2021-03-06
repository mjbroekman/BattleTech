# Contents
* [Introduction](#introduction)
* [Scoring Mechanics](#scoring-mechanics)
  * [Point Values](#point-values)
  * [Optimal Scoring Tips](#tips-for-optimal-scoring)
  * [Scoring Ranks](#career-scoring-ranks)
* [Difficulty Setting Info](#difficulty-settings-and-dsm-impact)
  * [Setting Details](#difficulty-settings)
* [Reputation and Mission Availability](#final-note-about-reputation-and-mission-availability)
* [Mech Chassis Completion Lists](#mechs-for-weight-class-completion)
  * [Light Mechs](#lights)
  * [Medium Mechs](#mediums)
  * [Heavy Mechs](#heavies)
  * [Assault Mechs](#assaults)
  * [Additional Chassis](#additional-chassis-for-mech-chassis-score)
* [Misc Thoughts](#misc-thoughts-and-links)
* [Update History](#update-list)

# Introduction
Career Scoring is a touchy subject. Some people think it's broken because certain ratings "can't be obtained". Some folks don't quite understand how it "works" (UPDATE: turns I'm one of them because it doesn't make sense).

## Update 1.6 - Addition of Difficulty Score Multiplier
**Score Multiplier is based on the *LOWEST* settings that you have EVER applied to the game. There is no benefit to starting easy and spiking the difficulty in the end game, nor starting hard and making the game easier.**

DSM range:
* Minimum value: 0.05
* Maximum value: 1.00

This is a DIRECT Multiplier and not 'bonus' points on top of the regular points. This means that, for example the Mech Weight Class Completion category will grant you 10,000 points per completed weight class at "maximum" difficulty but only 5,000 points per weight class at minimum difficulty.

Career-mode games that were started BEFORE update 1.6 do NOT have values associated with the difficulty settings and, _as a result_, **DO NOT REFLECT THE ACTUAL Difficulty Score Multiplier of the settings**. To take full advantage of the DSM values, you need to start a new career.

## Update 1.6.2  - Change to Difficulty Score multiplier
Update 1.6.2 changed the minimum possible DSM from 0.50 to 0.05 which means that games started prior to update 1.6 will have their DSM set to 0.05 and scores will be modified accordingly.

# Scoring Mechanics
Based on scores that have been reported and the "way" the JSON file is laid out, it appears there are two types of categories:
* Those that have a *defined* limit based on in-game content.
* Those that do not.

Examples of categories with limits based on in-game content:
* Weight Class Completion - There are only 4 weight classes. You can *never* receive this award more than four times.
* Argo Upgrades - There are 35 upgrades available to the Argo. You can *never* get more than those 35.

Examples of categories without limits on in-game content but that are capped to certain level:
* Contracts - You get 50 points for every level of contract difficulty you complete. 1 skull = 2 levels of difficulty.
* Mechwarrior Experience - You get 1 point for every 50xp gained by your mechwarriors.

Also note that some "limited" categories allow for a variety of ways to reach the target goal
* Mech Chassis - This has a "displayed" maximum that accounts for 55 of the original, base game chassis. If you collect DLC, 1.3+, or SLDF chassis, you can reach the target without getting all the base game chassis.


## Point Values
The scoring for each category below is modified by the Difficulty Score Multiplier to get the real value recorded in game. The target values below assume a Difficulty Score Modifier of 1.00.

* C-Bills
  * This is clear enough. You get 1 point for every 10,000 c-bills that enters your hand. Whether it's contract completion or selling to stores, every 10k == 1 point.
  * Money you spend does not reduce this score.
  * **The maximum amount of C-Bills that you can have is 2,147,483,647**. Any more and it wraps over into negative amounts. (This has been reported and hopefully HBS changes the C-Bill variable from a signed 32-bit integer to a long / bigint)
  * Target == 800 **MILLION** C-Bills in 1200 days to get 80k points.
* Contracts
  * Every half-skull of contract difficulty you complete gives you 50 points.
  * Target == 700 skulls worth of contracts
* 'Mech Chassis
  * 1273 points per mech chassis (active in Mechbays or in storage)
  * There is a pre-1.6, confirmed score from Prussian Havoc that would only be accessible by collecting 61 chassis. Higher scores will result from more mech chassis.
  * Starting in 1.6, you do not gain bonus points for having more than 55 chassis, though all chassis contribute points to reach this target.
  * Target == 55 mech chassis.
* 'Mech Weight Class Completion
  * 10,000 points per weight class. Completing a weight class involves collecting all the non-SLDF, pre-1.3 mechs for weight class. See the [Mech Chassis Completion Lists](#mechs-for-weight-class-completion) below for the list of mechs for each class.
  * There are four weight classes.
  * Target == 40k (all four weight classes)
* 'Mech Chassis Completion
  * Target == 25,000 for completing all four weight classes
* Mechwarrior Experience
  * Every 50xp gained by mechwarriors that live in the Barracks gives you 1 point.
  * Since your Commander lives in the Captain's Quarters, not the Barracks, they do not count towards this XP.
  * Losing a mechwarrior causes you to lose the points for that mechwarrior.
  * Hiring experienced mechwarriors gives you points for the XP they have spent.
  * **You do not need to spend XP on skill nodes for the XP to count**
  * Maximized training pods give you 1 point per mechwarrior that can use them PER DAY.
  * Mechwarriors with "All 10s" continue to gain XP in missions and continue to add to this score.
  * Target == 55,000 for 2750000 xp (or 14000 xp beyond 24 pilots @ all 10s)
    * Papaduuu reached this target with an astounding *8* pilots that each had *almost 700,000 xp* each. Check out [their post on the PDX Forum](https://forum.paradoxplaza.com/forum/index.php?threads/career-mode-scoring-guide.1139530/page-10#post-26082864)
* Star Systems Visited
  * You gain 500xp for every **jump point** you visit. This only occurs the *FIRST* time you visit it.
  * One technique for maximizing this is to overshoot your target so you get time to pause the game at a jump point. Since you are at a jump point and *not traveling to orbit* you can change your destination and travel to new places. At 3 days per jump point, you can visit 170 systems in 510 days (assuming you don't stop for other things like contracts).
  * Target == 170 systems.
* Star System Completion
  * Target == 25,000 for visiting 170 star systems.
* Positive / Negative Faction Reputation
  * 100 points for every positive or negative point of reputation you have.
  * All reputations are capped + or - 100
  * There are **_EIGHT_** factions that count towards this, meaning you must go +100 with four factions and -100 with four factions in order to maximize your score.
  * The Arano Restoration does not count towards positive or negative reputation [as noted by Freakonair (Paradox Forums)](https://forum.paradoxplaza.com/forum/index.php?goto/post&id=25006903#post-25006903).
  * Target == +/- 400 reputation.
* Faction Reputation Completion
  * 10,000 points for hitting +/- 100 with the factions
  * It is confirmed that scores can exceed the displayed maximum. Scores up to 80,000 have been reported.
  * Post 1.6, this is capped at 50k
  * Target == 50k for 5 Factions
* Argo Upgrades
  * 2,000 points per Argo Upgrade completed
  * Target == All upgrades (35 of them)
* Argo Completion
  * Target = 25,000 for finishing all 35 Argo upgrades
* Morale
  * 500 points per point of Morale
  * Target == 50 morale
* MRB Reputation
  * 45 points per point of reputation with the Mercenary Review Board
  * Post 1.6, this is capped at 1000 reputation (confirmed by Cyttorak001)
  * Target == 1000 reputation
* MRB Reputation Completion
  * Target == 25,000 for getting at least 900 reputation with the MRB.

## Tips for optimal scoring
* Know your allies and your enemies. Contract availability is key to maximizing every one of the scoring categories *except* Star Systems Visited. Without contracts, you can't raise / lower reputation, you can't improve your MRB rating, you can't earn cbills, build mechs, improve the Argo, or raise your Contracts score. Knowing which factions to raise or lower reputation with is KEY.
  * Major Faction w/ Fewest Enemies: Free Worlds League. Marik has *three* enemies: The Lyran Commonwealth, Capellan Confederation, and Pirates. Raising reputation with Marik and becoming an Ally will leave your reputation alone with more factions than any other.
  * Major Faction w/ Most Enemies: Capellan Confederation. Everyone other than the Draconis Combine and Arano Restoration is an enemy of the Capellans. Becoming an ally of Liao will **seriously hamper** contract availability as your reputation with your enemies can't exceed 0.
  * Minor Faction w/ Fewest Enemies: Arano Restoration. You can't ally with them, but their only enemies are the Directorate and Pirates. (Conversely, the Arano Restoration IS an enemy if you Ally with the Taurian Concordate). **Additionally, Arano Restoration reputation DOES NOT COUNT in the postive or negative reputation category** [as noted by Freakonair (Paradox Forums)](https://forum.paradoxplaza.com/forum/index.php?goto/post&id=25006903#post-25006903)
  * Minor Faction w/ Most Enemies: Pirates. Everyone hates the Pirates (except for Marik and the Taurians). Probably because they steal all the rum. If you ally with pirates, expect a very limited selection of contracts as your reputation with your enemies can't exceed 0.
  * Being Honored or Loathed by all factions should be a goal for attaining the highest score (and getting the most out of the rep completion bonus)
  * All that being said, **_remember that becoming an ally of a faction will remove ALL positive reputation from that faction's enemies_ AND PREVENT YOU FROM GAINING POSITIVE REPUTATION WITH THEM**. DO NOT join an Alliance if you have positive reputation with the enemies if you want to keep your score from dropping.
  * Being Honored by the Pirates will make a heck of a lot of missions available in unaligned space.
* Get the third Training Pod upgrade as soon as possible.
  * This will also allow you to have 24 pilots.
  * Every day with the 3rd training pod upgrade means your pilots who have less than 30k xp (including pre-existing skills) will gain another 50xp. That translates to 1 point / day / pilot that can use the pods.
  * You should aim to get the third Training Pod upgrade _BEFORE_ you reach 600 days left in the Career scoring period.
  * You should avoid filling up your Barracks until _AFTER_ you get the third Training Pod upgrade, but _BEFORE_ you have less than 600 days left. It only takes 600 days for a Mechwarrior to exhaust their ability to gain XP from the training pods once the third upgrade is installed.
  * Mechwarriors seem to stop accruing additional XP between 27,000 and 28,000 xp depending on starting stats. I had a number of 2/2/3/2 pilots that stopped at 27,550xp with dozens of days remaining in my career.
  * If you spend 30k xp on a pilot, that will raise their skills to two 7s and two 6s (if evenly spread)
  * DO NOT SPEND XP except when necessary. The XP score increments regardless of *spent* XP, so there is no need to spend XP and increase maintenance unless absolutely necessary.
* Get the third Drive System upgrade as soon as possible.
  * This will reduce travel time between systems, allowing you to visit more systems and complete more contracts in the 1200 days.
* "Punch Up"
  * Taking contracts above your weight limit and being successful at it is key to four metrics:
    * Contract score (higher difficulty)
    * Chassis scores (heavier mechs) - Heavier mechs early means completing heavier chassis categories earlier and, as a result, leaving you time to farm the lighter ones.
    * Mechwarrior experience (more XP)
    * CBills (better rewards, more salvage, selling more in the stores)
  * Being successful at taking more difficult contracts early will help maximize those scores.
* Do NOT use your Commander.
  * Their XP doesn't count towards the Experience score since there is no risk of losing that XP through death.
  * The fluff reasoning behind this is that only pilots in the Barracks contribute to this number. And because your Commander doesn't live in the barracks (they live in the Captain's Quarters), they don't contribute to the Mechwarrior XP.
* Inventory management
  * **Keep 1 of each chassis in your Mechbay or in storage**. If you *sell* the last copy of a chassis, you *will lose the points for it across all categories that it applies to*.
  * Example: If you have a Firestarter in a Mechbay and 3 in storage, you can sell all three from storage because the one in the Mechbay *still counts*.
  * Example: If you have a dozen Locust 1S in storage and zero Locusts in your Mechbays and sell them all, you will lose the Mech Chassis, the Weight Class Completion (for lights), and the Mech Chassis Completion points. In order to keep the points, **you need to have one copy in a MechBay or in storage**.
  * End up in a system you can purchase from. Sell everything else on the last day. And then buy everything you can. And then repeat. Until you can't buy any more. The score only counts the money coming in, not the actual ending balance so ending with 0 c-bills is not an issue.
  * Skill to Tactics9 as soon as possible.
  * While not directly score related, pushing your pilots to Tactics9 will give them 'Called Shot Mastery' which will greatly increase the odds of Precision Shot yielding head hits (2% for Tactics5 and lower; 5% for Tactics8 and lower; 18% for Tactics9+) and larger quantities of mech parts.
* Get a Marauder (MAD-3R) EARLY
  * The Marauder gives an insane boost to called shots (prone targets or precision shot). Headshots with a Tactics9 pilot (Called Shot Mastery) in a Marauder can be as high as *35%*. This makes it much easier to get mech parts and complete higher rated contracts.

## Career Scoring Ranks
Below is the list of scoring ranks and their point values:
1. Unknown = 0+
2. Green = 80,000+
3. Regular = 160,000+
4. Veteran = 320,000+
5. Elite = 480,000+
6. Legendary = 640,000+
7. Kerensky = 760,000+
*  Maximum Score (as of 1.6) = 770,016

# Difficulty Settings and DSM impact
**NOTE**: The Difficulty Score Multiplier (DSM) is based on the *LOWEST* settings that you have EVER applied to the game. There is no benefit to starting easy and spiking the difficulty in the end game, nor starting hard and making the game easier.

DSM range:
* Minimum value: 0.05
* Maximum value: 1.00

This is a DIRECT Multiplier and not 'bonus' points on top of the regular points. This means that, for example the Mech Weight Class Completion category will grant you 10,000 points per completed weight class at "maximum" difficulty but only 5,000 points per weight class at minimum difficulty.

# DSM Note (Update 1.6 / 1.6.2)
Career-mode games that were started BEFORE update 1.6 do NOT have values associated with the difficulty settings and, _as a result_, **DO NOT REFLECT THE ACTUAL Difficulty Score Multiplier of the settings**. To take full advantage of the DSM values, you need to start a new career.

Update 1.6.2 changed the minimum possible DSM from 0.50 to 0.05 which means that games started prior to update 1.6 will have their DSM set to 0.05 and scores will be modified accordingly.


## Difficulty settings
* Ironman Mode
  * Toggles whether or not the game maintains a single save file (enabled) or generates a new loadable save point before and after missions, at events, and on entering orbit.
  * **DSM** Impact: 0.20 if enabled
* Randomize Starting 'Mechs
  * Toggles whether you start with the normal Vindicator, Jenner, Commando 1B, Spider, Panther or a random selection.
  * Randomized start picked based on slot (1 - 5)
    1. Blackjack BJ-1, Vindicator VND-1R, Centurion CN9-A, Enforcer ENF-4R
    2. Blackjack BJ-1, Vindicator VND-1R, Centurion CN9-A, Enforcer ENF-4R
    3. Commando COM-1B, Commando COM-2D, Jenner JR7-D, Panther PNT-9R
    4. Commando COM-1B, Commando COM-2D, Spider SDR-5V, Cicada CDA-2A, Cicada CDA-3C
    5. Locust LCT-1M, Locust LCT-1S, Locust LCT-1V, Urbanmech UM-R60, Spider SDR-5V, Commando COM-1B, Commando COM-2D
  * **DSM** Impact: none
* Parts / Mech
  * This will influence how quickly you get mechs, which will in turn influence how quickly you complete the various Chassis-related categories as well as how many C-Bills you gain (from selling excess chassis)
  * This can not be changed during the game.
  * **DSM** Impact: 0.05 per part above 3. 3 parts == no modifier, 4 parts == 0.05, ... 8 parts == 0.25
* Salvage
  * This will influence Chassis and C-Bills related categories
  * This can be changed during the game if you feel like you aren't getting enough salvage.
  * **DSM** Impact: Generous == no modifier, Normal == 0.10, Stingy == 0.15
* Contract Payment
  * This will influence C-Bill categories (and to some extent Chassis categories as you can more easily purchase parts from the stores)
  * This can be changed during the game, so if you feel that you aren't getting enough cbills, you can always adjust this.
  * **DSM** Impact: Generous == no modifier, Normal == 0.10, Stingy == 0.15
* Unequipped Mechs
  * Enabling 'Unequipped Mechs' will mean that you do not get the 'bonus' parts when building a mech from salvage, reducing the amount of saleable equipment you have.
  * This can not be changed during the game.
  * **DSM** Impact: 0.20 if enabled
* Enemy Force Strength
  * Changing this will adjust the difficulty of missions. Harder missions mean more contract points. Easier missions give you fewer contract points.
  * This is adjustable during the game, so once you get assaults, you may increase this in order to get more contract points.
  * Starting the game with this on "Hard" will accelerate your access to heavier mechs, but it can be dangerous if you aren't careful with your tactics.
  * **DSM** Impact: Easy == no modifier, Normal == 0.05, Hard == 0.10
* Mech Destruction
  * Enabling Mech Destruction will mean you run the risk of losing a chassis and any points associated with it if it was the only copy in your inventory.
  * This can be changed during the game, so if you feel like you are losing too many mechs, you can turn this off.
  * **DSM** Impact:0.10 if enabled
* Lethality
  * Enabling Lethality will mean you run a MUCH higher risk of losing pilots and the XP associated with them.
  * This can be changed during the game, so if you feel like you are losing too many pilots, you can turn this off.
  * **DSM** Impact:0.10 if enabled
* No Rare Salvage
  * Enabling this will make the stores your only source of + items, reducing your unit's effectiveness and saleable equipment.
  * **DSM** Impact: 0.10 if enabled
* Mechwarrior Progression
  * Slowing down progression means less XP per mission. Less XP means a lower score.
  * If you feel like your pilots aren't getting enough XP, you can change this. However, "Normal" is the fastest progression there is. Everything else is slower.
  * **DSM** Impact: Normal == 0.05, Slow == 0.10, Very Slow == 0.20
* Advanced Mechwarriors
  * This sets the frequency of high skill mechwarriors in the hiring halls. It allows for a quick and dirty point boost by hiring experienced pilots without having to train them.
  * If you feel the need to hire expensive, higher skilled pilots, you can change this.
  * **DSM** Impact: Often == no modifier, Normal == 0.05, Rare == 0.10

## DSM Strategies
Because the DSM is capped at 1.00, you are not forced into setting all the Difficulty Settings to maximum values in order to reach a 1.00 multiplier (aka full value).

For example, you can reach 1.00 with the following settings:
* Ironman
* 3 parts / mechs
* Unequipped mechs
* Hard enemy forces
* Mech destruction
* Generous salvage
* Pilot lethality
* Rare Advanced Mechwarriors
* Stingy contract payment
* Normal Mechwarrior progression
* YES Rare Salvage

This would give you lots of salvage opportunity with quick mech builds, rare salvage, and normal amounts of XP for missions, letting you build and sell chassis quickly and building up the Mech and c-bill categories (from selling excess salvage) while still gaining XP reasonably quickly.

Happy Hunting and may Kerensky bless your Career.

## Final note about reputation and mission availability
In playing my current career, I initially became disliked by the pirates but then there were a few juicy anti-Capellan pirate missions and my rep went positive. Once I was Liked by pirates, it seemed like pirate missions became much more common. It is entirely possible that a 'good' strategy with regard to reputation is this:
* Become 'Honored' by pirates. Not only for the reputation (and reputation completion) but also for mission availability in un-aligned space.
* Become 'Loathed' by Steiner and Kurita. Neither of these factions have 'faction space', so you will never suffer contract and shop penalties from being loathed with them.
* Become 'Loathed' by two of the remaining 5 factions and 'Honored' by three others. The *easiest* remaining faction to become Loathed by is Liao.
* If you are aiming for being Loathed by Steiner and Liao, Marik and Davion become easier to become Honored by.
* If you are aiming for being Honored by Davion, the Taurians become easier to become Loathed by.
* In order to reach Kerensky, you **MUST** be playing at 1.00 difficulty score multiplier _AND_ you can only miss 10,015 points as there is a maximum point total of 770,016.

# Mechs for Weight Class Completion
## Lights
* PNT-9R
* LCT-1M
* LCT-1S
* LCT-1V
* COM-1B
* COM-2D
* SDR-5V
* UM-R60
* FS9-H
* JR7-D

## Mediums
* CDA-2A
* CDA-3C
* BJ-1
* VND-1R
* CN9-A
* CN9-AL
* ENF-4R
* HBK-4G
* HBK-4P
* TBT-5N
* GRF-1N
* GRF-1S
* KTO-18
* SHD-2D
* SHD-2H
* WVR-6K
* WVR-6R

## Heavies
* DRG-1N
* QKD-4G
* QKD-5A
* CPLT-C1
* CPLT-K2
* JM6-A
* JM6-S
* TDR-5S
* TDR-5SE
* TDR-5SS
* CTF-1X
* GHR-5H
* BL-6-KNT
* ON1-K
* ON1-V

## Assaults
* AWS-8Q
* AWS-8T
* VTR-9B
* VTR-9S
* ZEU-6S
* BLR-1G
* STK-3F
* HGN-733
* HGN-733P
* BNC-3E
* BNC-3M
* AS7-D
* KGC-0000

## Additional Chassis that contribute to Mech Chassis Score
The following chassis will contribute to Mech Chassis Score, but not the 'Completion' categories and will not push the Mech Chassis Score over the target indicated in-game.
* BSC - Flashpoint reward Big Steel Claw
* GRF-2N/4N - Flashpoint reward - Star League Griffin
* BL-6b-KNT - Star League Black Knight
* HGN-732b - Star League Highlander
* AS7-D-HT - Star League Atlas
* CP-10-Q - Flashpoint content
* CP-10-Z - Flashpoint content
* CRB-20 - Flashpoint content
* HCT-3F - Flashpoint content
* BJ-1DB - 1.6 content
* BNC-3S - 1.6 content
* CPLT-C4 - 1.6 content
* HCT-3X - 1.6 content
* UM-R60L - 1.6 content
* UM-R90 - 1.6 content
* VND-1AA - 1.6 content
* JVN-10F - Urban Warfare content
* JVN-10N - Urban Warfare content
* RVN-1X - Urban Warfare content
* MAD-3R - 1.8 content
* WHM-6D - 1.8 content
* WHM-6R - 1.8 content
* ANH-1A - Heavy Metal content
* ARC-2R - Heavy Metal content
* ARC-2S - Heavy Metal content
* ASN-101 - Heavy Metal content
* ASN-21 - Heavy Metal content
* BSK-M3 - Heavy Metal content
* BSK-MAZ - Heavy Metal content
* FLE-15 - Heavy Metal content
* FLE-4 - Heavy Metal content
* PXH-1 - Heavy Metal content
* PXH-1K - Heavy Metal content
* RFL-3C - Heavy Metal content
* RFL-3N - Heavy Metal content
* VL-2T - Heavy Metal content
* VL-5T - Heavy Metal content

  
# Misc Thoughts and Links
- CSX
> The Kerensky achievement might not have been intended to be achieved until Urban Warfare, or even the third DLC is out. With the spoiler mechs and extra mechs from Flashpoint counting to the score, the later DLCs might be intended to add more points.

- ninte000 posted their score screenshots and some pretty amazing insights [here (Paradox Forums)](https://forum.paradoxplaza.com/forum/index.php?threads/career-mode-final-score-travel-route-and-thoughts.1144098/)

# Update List
* UPDATED (18/Dec/2018) to clarify inventory management based on questions from Icewraith and Prussian Havoc
* UPDATED (18/Dec/2018) further testing based on feedback [here (Paradox Forums)](https://forum.paradoxplaza.com/forum/index.php?threads/battletech-impossible-to-attain-kerensky-rank-in-career-mode.1136859/#post-24982736) led to updates above. It appears that, at the very least, C-Bills and Experience are capped.
* UPDATED (19/Dec/2018) further information from Prussian Havoc about his career scoring.
* UPDATED (19/Dec/2018) added Difficulty setting information.
* UPDATED (19/Dec/2018) with further tip about alliances and reputation.
* UPDATED (19/Dec/2018) with additional tip about repeatedly performing sell/buy/sell for higher c-bill scores.
* UPDATED (19/Dec/2018) with additional information from CSX confirming scores above the target level.
* UPDATED (20/Dec/2018) with additional thought on reputation and mission availability.
* UPDATED (20/Dec/2018) with spoiler tagged mech chassis information
* UPDATED (4/Jan/2019) with reputation update
* UPDATED (4/Jan/2019) with MRB Reputation / Completion update
* UPDATED (5/Jan/2019) noting that Freakonair discovered the Arano reputation issue before I did.
* UPDATED (5/Jan/2019) added link to ninte000's scoring post with their great resources and insights.
* UPDATED (9/Jan/2019) with additional note about the Enemy Strength setting and also a 'key' about pilot skills.
* UPDATED (11/Jun/2019) with 1.6/UW changes to career scoring and mech chassis
* UPDATED (19/Jun/2019) converted to GitHub Markdown
* UPDATED (19/Jun/2019) included some findings from Cyttorak001
* UPDATED (20/Jun/2019) confirmed that cbills, mechwarrior xp, systems visited, faction reputation completion are now CAPPED
* UPDATED (20/Jun/2019) updated with Cyttorak001's confirmation on MRB rating cap.
* UPDATED (7/Jan/2020) updated with mech lists from Heavy Metal/1.8, Marauder tip for optimal scoring, and a link to Papaduuu's screenshots from their Kerensky run
