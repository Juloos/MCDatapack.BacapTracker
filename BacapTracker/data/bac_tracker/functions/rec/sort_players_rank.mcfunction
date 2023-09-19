scoreboard players add playercount bac_tracker.vars 1
execute positioned 0 0 0 in overworld at @e[tag=bac_tracker.leaderboard,tag=!bac_tracker.visited,sort=nearest,limit=1] unless entity @e[tag=bac_tracker.leaderboard,tag=bac_tracker.visited,distance=..0.0000005] run scoreboard players operation playerrank bac_tracker.vars = playercount bac_tracker.vars
execute positioned 0 0 0 in overworld as @e[tag=bac_tracker.leaderboard,tag=!bac_tracker.visited,sort=nearest,limit=1] at @a if score @s UUID0 = @p UUID0 if score @s UUID1 = @p UUID1 if score @s UUID2 = @p UUID2 if score @s UUID3 = @p UUID3 run scoreboard players operation @p bac_tracker.leaderboard = playerrank bac_tracker.vars
execute positioned 0 0 0 in overworld as @e[tag=bac_tracker.leaderboard,tag=!bac_tracker.visited,sort=nearest,limit=1] run tag @s add bac_tracker.visited
execute if entity @e[tag=bac_tracker.leaderboard,tag=!bac_tracker.visited] run function bac_tracker:rec/sort_players_rank
