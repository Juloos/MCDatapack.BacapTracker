scoreboard players add playercount bac_leaderboard.vars 1
execute positioned 0 -128 0 in overworld at @e[tag=bac_leaderboard.ranker,tag=!bac_leaderboard.visited,sort=nearest,limit=1] unless entity @e[tag=bac_leaderboard.ranker,tag=bac_leaderboard.visited,distance=..0.0000005] run scoreboard players operation playerrank bac_leaderboard.vars = playercount bac_leaderboard.vars
execute positioned 0 -128 0 in overworld as @e[tag=bac_leaderboard.ranker,tag=!bac_leaderboard.visited,sort=nearest,limit=1] run scoreboard players operation @s bac_leaderboard.rank = playerrank bac_leaderboard.vars
execute positioned 0 -128 0 in overworld as @e[tag=bac_leaderboard.ranker,tag=!bac_leaderboard.visited,sort=nearest,limit=1] run tag @s add bac_leaderboard.visited
execute if entity @e[tag=bac_leaderboard.ranker,tag=!bac_leaderboard.visited] run function bac_leaderboard:rec/sort_players_rank
