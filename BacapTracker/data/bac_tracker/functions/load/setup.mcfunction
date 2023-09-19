scoreboard objectives add bac_tracker.vars dummy
scoreboard players set page bac_tracker.vars 0
scoreboard players set page_count bac_tracker.vars 3
# if unset: set to 200 (10 secondes)
execute unless score page_increment bac_tracker.vars = page_increment bac_tracker.vars run scoreboard players set page_increment bac_tracker.vars 200
scoreboard players set page_increment_count bac_tracker.vars 0

scoreboard objectives add UUID0 dummy
scoreboard objectives add UUID1 dummy
scoreboard objectives add UUID2 dummy
scoreboard objectives add UUID3 dummy
scoreboard objectives add bac_tracker.leaderboard dummy
scoreboard objectives add bac_tracker.playercount dummy
forceload add 0 0

scoreboard objectives add bac_tracker.progress_score dummy
scoreboard objectives setdisplay sidebar bac_tracker.progress_score


# scoreboard objectives add bac_tracker.milestone dummy
# team add bac_tracker.milestone
# team modify bac_tracker.milestone prefix [" "," "]
# team modify bac_tracker.milestone color white
# team join bac_tracker.milestone Milestone
###
###


team add bac_tracker.page
team join bac_tracker.page §p

# sidebar blanks
team leave §0
team leave §1
team leave §2
team leave §3
team leave §4
team leave §5
team leave §6
team leave §7
team leave §8
team leave §9


advancement revoke @a only bac_tracker:location
function bac_tracker:display/refresh_page
