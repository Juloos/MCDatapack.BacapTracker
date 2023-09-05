function bac_tracker:location/update_scoreboard

function bac_tracker:display/reset
execute if score page bac_tracker.vars matches 0 run function bac_tracker:display/page_1
execute if score page bac_tracker.vars matches 1 run function bac_tracker:display/page_2
execute if score page bac_tracker.vars matches 2 run function bac_tracker:display/page_3
execute if score page bac_tracker.vars matches 3 run function bac_tracker:display/page_4
execute if score page bac_tracker.vars matches 4 run function bac_tracker:display/page_5
