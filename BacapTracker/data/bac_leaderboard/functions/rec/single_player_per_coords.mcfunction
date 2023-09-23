execute as @r[scores={bac_leaderboard.playercount=2..}] at @s run tp ~ ~0.000001 ~
execute as @a store result score @s bac_leaderboard.playercount if entity @a[distance=0]
execute if entity @a[scores={bac_leaderboard.playercount=2..}] run function bac_leaderboard:rec/single_player_per_coords
