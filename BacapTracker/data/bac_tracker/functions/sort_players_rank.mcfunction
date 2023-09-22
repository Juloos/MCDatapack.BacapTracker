tag @e remove bac_tracker.visited
scoreboard players set playercount bac_tracker.vars 0
execute if entity @e[tag=bac_tracker.leaderboard] run function bac_tracker:rec/sort_players_rank
