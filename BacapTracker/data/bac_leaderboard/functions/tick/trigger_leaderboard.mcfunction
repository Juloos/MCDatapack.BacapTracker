tag @a remove bac_leaderboard.show_leaderboard
tag @a[scores={bac_leaderboard=1..}] add bac_leaderboard.show_leaderboard

tag @e remove bac_leaderboard.temp
tag @e[tag=bac_leaderboard.ranker] add bac_leaderboard.temp
execute if entity @a[tag=bac_leaderboard.show_leaderboard] run function bac_leaderboard:rec/show_leaderboard

scoreboard players reset @a[scores={bac_leaderboard=1..}] bac_leaderboard
scoreboard players enable @a bac_leaderboard
