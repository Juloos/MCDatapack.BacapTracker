scoreboard players add update bac_leaderboard.vars 1
scoreboard players operation update bac_leaderboard.vars %= update_increment bac_leaderboard.vars

execute if score update bac_leaderboard.vars matches 0 run function bac_leaderboard:update_leaderboard
