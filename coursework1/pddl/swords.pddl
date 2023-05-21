(define 
    (problem makesword) 
    (:domain runescape)

    (:objects 
        Player - player
        Shed - storage
        Mine - mine
        Furnace - furnace
        Anvil - anvil
        Pickaxe - pickaxe
        Hammer - hammer
        Ore - ore
        Bars - bars
    )

    (:init
        (at Player Shed)
    )

    (:goal (and
        (has_sword Player)
    ))
)
