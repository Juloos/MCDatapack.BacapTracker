execute as @r[scores={bac_tracker.playercount=2..}] at @s run tp ~ ~0.000001 ~
execute as @a store result score @s bac_tracker.playercount if entity @a[distance=0]
execute if entity @a[scores={bac_tracker.playercount=2..}] run function bac_tracker:rec/single_player_per_coords
