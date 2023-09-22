tag @a remove bac_tracker.show_leaderboard
tag @a[scores={bac_leaderboard=1..}] add bac_tracker.show_leaderboard

tag @e remove bac_tracker.temp
tag @e[tag=bac_tracker.leaderboard] add bac_tracker.temp
execute if entity @a[tag=bac_tracker.show_leaderboard] run function bac_tracker:rec/show_leaderboard

scoreboard players reset @a[scores={bac_leaderboard=1..}] bac_leaderboard
scoreboard players enable @a bac_leaderboard
