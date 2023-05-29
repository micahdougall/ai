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
        (at Player Shed) ; Begin with the player at the shed
        (has Shed Axe) ; Shed must have available tools
        (has Shed Hammer)
        (has Shed Knife)
        (has Shed Pickaxe)
        (has Mine Rock) ; Minimum resources required
        (has Farm Chickens)
        (has Forest Trees)
    )

    ; Succeeded once the player has deposited all resources at the shed including the desired arrow
    (:goal (and
        (has Shed Arrow)
        (forall (?item - resource)
            (not (has Player ?item))
        )
    ))

    ; Minimise the distance travelled
    (:metric (minimize (
        (travelled)
    )))
)
