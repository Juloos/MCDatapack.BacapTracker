execute if score any bac_tracker.hidden matches 0 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"0","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 1 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"1","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 2 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"2","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 3 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"3","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 4 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"4","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 5 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"5","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 6 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"6","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 7 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"7","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 8 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"8","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 9 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"9","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 10 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"10","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 11 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"11","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 12 run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"12","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]
execute if score any bac_tracker.hidden matches 13.. run team modify bac_tracker.hidden suffix [{"text":": ","color":"gray"},{"text":"13","color":"yellow"},{"text":"/","color":"gold"},{"text":"13","color":"yellow"}]

execute if score any bac_tracker.hidden matches 13.. run team modify bac_tracker.hidden color green
execute unless score any bac_tracker.hidden matches 13.. run team modify bac_tracker.hidden color white
