scoreboard players add update bac_tracker.vars 1
scoreboard players operation update bac_tracker.vars %= update_increment bac_tracker.vars

execute if score update bac_tracker.vars matches 0 run function bac_tracker:update_scoreboard
