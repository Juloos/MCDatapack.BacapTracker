execute as @a unless score @s bac_advfirst = @s bac_advfirst run scoreboard players set @s bac_advfirst 0

execute as @a store result score @s bac_leaderboard.UUID0 run data get entity @s UUID[0]
execute as @a store result score @s bac_leaderboard.UUID1 run data get entity @s UUID[1]
execute as @a store result score @s bac_leaderboard.UUID2 run data get entity @s UUID[2]
execute as @a store result score @s bac_leaderboard.UUID3 run data get entity @s UUID[3]

function bac_leaderboard:rec/single_player_per_coords
tag @a remove bac_leaderboard.flagged
execute as @e[tag=bac_leaderboard.ranker] at @a if score @p bac_leaderboard.UUID0 = @s bac_leaderboard.UUID0 if score @p bac_leaderboard.UUID1 = @s bac_leaderboard.UUID1 if score @p bac_leaderboard.UUID2 = @s bac_leaderboard.UUID2 if score @p bac_leaderboard.UUID3 = @s bac_leaderboard.UUID3 run tag @p add bac_leaderboard.flagged
# No markers: old versions compatibility
execute at @a[tag=!bac_leaderboard.flagged] in overworld run summon armor_stand ~ ~ ~ {Tags:[bac_leaderboard.ranker],Invulnerable:1b,Invisible:1b,NoGravity:1b,Small:1b,Marker:1b}
execute as @a[tag=!bac_leaderboard.flagged] at @s in overworld run loot replace entity @e[tag=bac_leaderboard.ranker,sort=nearest,limit=1] armor.head loot bac_leaderboard:player_head
execute as @a[tag=!bac_leaderboard.flagged] at @s in overworld run scoreboard players operation @e[tag=bac_leaderboard.ranker,sort=nearest,limit=1] bac_leaderboard.UUID0 = @s bac_leaderboard.UUID0
execute as @a[tag=!bac_leaderboard.flagged] at @s in overworld run scoreboard players operation @e[tag=bac_leaderboard.ranker,sort=nearest,limit=1] bac_leaderboard.UUID1 = @s bac_leaderboard.UUID1
execute as @a[tag=!bac_leaderboard.flagged] at @s in overworld run scoreboard players operation @e[tag=bac_leaderboard.ranker,sort=nearest,limit=1] bac_leaderboard.UUID2 = @s bac_leaderboard.UUID2
execute as @a[tag=!bac_leaderboard.flagged] at @s in overworld run scoreboard players operation @e[tag=bac_leaderboard.ranker,sort=nearest,limit=1] bac_leaderboard.UUID3 = @s bac_leaderboard.UUID3

execute as @e[tag=bac_leaderboard.ranker] at @a if score @p bac_leaderboard.UUID0 = @s bac_leaderboard.UUID0 if score @p bac_leaderboard.UUID1 = @s bac_leaderboard.UUID1 if score @p bac_leaderboard.UUID2 = @s bac_leaderboard.UUID2 if score @p bac_leaderboard.UUID3 = @s bac_leaderboard.UUID3 run scoreboard players operation @s bac_leaderboard.value = @p bac_advfirst
tp @e[tag=bac_leaderboard.ranker] 0 -128 0
execute as @e[tag=bac_leaderboard.ranker] store result entity @s Pos[0] double 0.000001 run scoreboard players get @s bac_leaderboard.value

function bac_leaderboard:sort_players_rank
