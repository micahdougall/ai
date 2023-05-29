(define 
    (problem makearrow) 
    (:domain runescape)

    (:objects 
        Player - player
        Shed - storage
        Anvil - anvil
        Farm - farm
        Forest - forest
        Furnace - furnace
        Mine - mine
        Axe - axe
        Hammer - hammer
        Knife - knife
        Pickaxe - pickaxe
        Bars - bars
        Chickens - chickens
        Ore - ore
        Rock - rock
        Trees - trees
        Wood - wood
        Arrowhead - arrowhead
        Feathers - feathers
        Shafts - shafts
        Arrow - arrow
    )

    (:init
        (at Player Shed)
        (has Shed Axe)
        (has Shed Hammer)
        (has Shed Knife)
        (has Shed Pickaxe)
        (has Mine Rock)
        (has Farm Chickens)
        (has Forest Trees)
    )

    (:goal (and
        (has Shed Arrow)
        (not (has Player bars))
        (not (has Player chickens))
        (not (has Player ore))
        (not (has Player rock))
        (not (has Player trees))
        (not (has Player wood))
        (not (has Player arrowhead))
        (not (has Player feathers))
        (not (has Player shafts))
        (not (has Player axe))
        (not (has Player hammer))
        (not (has Player knife))
        (not (has Player pickaxe))
    ))
)
