tag @e remove bac_leaderboard.visited
scoreboard players set playercount bac_leaderboard.vars 0
execute if entity @e[tag=bac_leaderboard.ranker] run function bac_leaderboard:rec/sort_players_rank
