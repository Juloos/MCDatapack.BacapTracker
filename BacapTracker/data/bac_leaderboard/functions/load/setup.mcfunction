scoreboard objectives add bac_leaderboard.vars dummy
scoreboard players set update bac_leaderboard.vars 0
# if unset: set to 20 (1 second)
execute unless score update_increment bac_leaderboard.vars = update_increment bac_leaderboard.vars run scoreboard players set update_increment bac_leaderboard.vars 20

scoreboard objectives add bac_leaderboard trigger
scoreboard objectives add bac_leaderboard.UUID0 dummy
scoreboard objectives add bac_leaderboard.UUID1 dummy
scoreboard objectives add bac_leaderboard.UUID2 dummy
scoreboard objectives add bac_leaderboard.UUID3 dummy
scoreboard objectives add bac_leaderboard.rank dummy
scoreboard objectives add bac_leaderboard.value dummy
scoreboard objectives add bac_leaderboard.playercount dummy

# We need our armor_stands to be loaded for rank sorting 
forceload add 0 0
