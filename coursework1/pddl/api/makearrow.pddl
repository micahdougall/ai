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
        (forall (?item - resource)
            (not (has Player ?item))
        )
    ))
)
