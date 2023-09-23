execute as @a unless score @s bac_advfirst = @s bac_advfirst run scoreboard players set @s bac_advfirst 0

execute as @a store result score @s UUID0 run data get entity @s UUID[0]
execute as @a store result score @s UUID1 run data get entity @s UUID[1]
execute as @a store result score @s UUID2 run data get entity @s UUID[2]
execute as @a store result score @s UUID3 run data get entity @s UUID[3]

function bac_tracker:rec/single_player_per_coords
tag @a remove bac_tracker.flagged
execute at @a as @e[tag=bac_tracker.leaderboard] if score @p UUID0 = @s UUID0 if score @p UUID1 = @s UUID1 if score @p UUID2 = @s UUID2 if score @p UUID3 = @s UUID3 run tag @p add bac_tracker.flagged
# No markers: old versions compatibility
execute at @a[tag=!bac_tracker.flagged] in overworld run summon armor_stand ~ ~ ~ {Tags:[bac_tracker.leaderboard],Invulnerable:1b,Invisible:1b}
execute as @a[tag=!bac_tracker.flagged] at @s run scoreboard players operation @e[tag=bac_tracker.leaderboard,sort=nearest,limit=1] UUID0 = @s UUID0
execute as @a[tag=!bac_tracker.flagged] at @s run scoreboard players operation @e[tag=bac_tracker.leaderboard,sort=nearest,limit=1] UUID1 = @s UUID1
execute as @a[tag=!bac_tracker.flagged] at @s run scoreboard players operation @e[tag=bac_tracker.leaderboard,sort=nearest,limit=1] UUID2 = @s UUID2
execute as @a[tag=!bac_tracker.flagged] at @s run scoreboard players operation @e[tag=bac_tracker.leaderboard,sort=nearest,limit=1] UUID3 = @s UUID3

execute at @a as @e[tag=bac_tracker.leaderboard] if score @p UUID0 = @s UUID0 if score @p UUID1 = @s UUID1 if score @p UUID2 = @s UUID2 if score @p UUID3 = @s UUID3 store result entity @s Pos[0] double 0.000001 store result entity @s Pos[1] double 0 store result entity @s Pos[2] double 0 run scoreboard players get @p bac_advfirst

function bac_tracker:sort_players_rank
