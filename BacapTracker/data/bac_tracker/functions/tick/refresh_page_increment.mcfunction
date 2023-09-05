scoreboard players add page_increment_count bac_tracker.vars 1
scoreboard players operation page_increment_count bac_tracker.vars %= page_increment bac_tracker.vars
execute if score page_increment_count bac_tracker.vars matches 0 run scoreboard players add page bac_tracker.vars 1
execute if score page_increment_count bac_tracker.vars matches 0 run scoreboard players operation page bac_tracker.vars %= page_count bac_tracker.vars
execute if score page_increment_count bac_tracker.vars matches 0 run function bac_tracker:display/refresh_page
