scoreboard objectives add bac_tracker.vars dummy
scoreboard players set page bac_tracker.vars 0
# Max 5 for reading convenie
scoreboard players set page_count bac_tracker.vars 3
scoreboard players set page_increment bac_tracker.vars 200
scoreboard players set page_increment_count bac_tracker.vars 0

scoreboard objectives add bac_tracker.progress_score dummy
scoreboard objectives setdisplay sidebar bac_tracker.progress_score

scoreboard objectives add bac_tracker.total dummy
scoreboard objectives add bac_tracker.adventure dummy
scoreboard objectives add bac_tracker.animal dummy
scoreboard objectives add bac_tracker.bacap dummy
scoreboard objectives add bac_tracker.beginning dummy
scoreboard objectives add bac_tracker.biomes dummy
scoreboard objectives add bac_tracker.building dummy
scoreboard objectives add bac_tracker.challenges dummy
scoreboard objectives add bac_tracker.combat dummy
scoreboard objectives add bac_tracker.enchanting dummy
scoreboard objectives add bac_tracker.end dummy
scoreboard objectives add bac_tracker.farming dummy
scoreboard objectives add bac_tracker.mining dummy
scoreboard objectives add bac_tracker.monsters dummy
scoreboard objectives add bac_tracker.nether dummy
scoreboard objectives add bac_tracker.potion dummy
scoreboard objectives add bac_tracker.redstone dummy
scoreboard objectives add bac_tracker.statistics dummy
scoreboard objectives add bac_tracker.weaponry dummy


team add bac_tracker.total
team modify bac_tracker.total prefix [" "," "]
team modify bac_tracker.total color white
team join bac_tracker.total Total

team add bac_tracker.adventure
team modify bac_tracker.adventure prefix [" "," "]
team modify bac_tracker.adventure color white
team join bac_tracker.adventure Adventure

team add bac_tracker.animal
team modify bac_tracker.animal prefix [" "," "]
team modify bac_tracker.animal color white
team join bac_tracker.animal Animal

team add bac_tracker.bacap
team modify bac_tracker.bacap prefix [" "," "]
team modify bac_tracker.bacap color white
team join bac_tracker.bacap BlazeandCave

team add bac_tracker.beginning
team modify bac_tracker.beginning prefix [" "," "]
team modify bac_tracker.beginning color white
team join bac_tracker.beginning Beginning

team add bac_tracker.biomes
team modify bac_tracker.biomes prefix [" "," "]
team modify bac_tracker.biomes color white
team join bac_tracker.biomes Biomes

team add bac_tracker.building
team modify bac_tracker.building prefix [" "," "]
team modify bac_tracker.building color white
team join bac_tracker.building Building

team add bac_tracker.challenges
team modify bac_tracker.challenges prefix [" "," "]
team modify bac_tracker.challenges color white
team join bac_tracker.challenges Challenges

team add bac_tracker.combat
team modify bac_tracker.combat prefix [" "," "]
team modify bac_tracker.combat color white
team join bac_tracker.combat Combat

team add bac_tracker.enchanting
team modify bac_tracker.enchanting prefix [" "," "]
team modify bac_tracker.enchanting color white
team join bac_tracker.enchanting Enchanting

team add bac_tracker.end
team modify bac_tracker.end prefix [" "," "]
team modify bac_tracker.end color white
team join bac_tracker.end End

team add bac_tracker.farming
team modify bac_tracker.farming prefix [" "," "]
team modify bac_tracker.farming color white
team join bac_tracker.farming Farming

team add bac_tracker.mining
team modify bac_tracker.mining prefix [" "," "]
team modify bac_tracker.mining color white
team join bac_tracker.mining Mining

team add bac_tracker.monsters
team modify bac_tracker.monsters prefix [" "," "]
team modify bac_tracker.monsters color white
team join bac_tracker.monsters Monsters

team add bac_tracker.nether
team modify bac_tracker.nether prefix [" "," "]
team modify bac_tracker.nether color white
team join bac_tracker.nether Nether

team add bac_tracker.potion
team modify bac_tracker.potion prefix [" "," "]
team modify bac_tracker.potion color white
team join bac_tracker.potion Potion

team add bac_tracker.redstone
team modify bac_tracker.redstone prefix [" "," "]
team modify bac_tracker.redstone color white
team join bac_tracker.redstone Redstone

team add bac_tracker.statistics
team modify bac_tracker.statistics prefix [" "," "]
team modify bac_tracker.statistics color white
team join bac_tracker.statistics Statistics

team add bac_tracker.weaponry
team modify bac_tracker.weaponry prefix [" "," "]
team modify bac_tracker.weaponry color white
team join bac_tracker.weaponry Weaponry

team add bac_tracker.page
team join bac_tracker.page §p

team leave §0
team leave §1
team leave §2
team leave §3
team leave §4
team leave §5
team leave §6
team leave §7
team leave §8
team leave §9


function bac_tracker:display/refresh_page
