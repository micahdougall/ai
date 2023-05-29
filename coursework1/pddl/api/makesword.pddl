(define (problem makesword)
    (:domain runescape)

    (:objects
        Player - player
        Shed - storage
        Mine - mine
        Furnace - furnace
        Anvil - anvil
        Pickaxe - pickaxe
        Hammer - hammer
        Rock - rock
        Ore - ore
        Bars - bars
        Sword - sword
    )

    (:init
        (at Player Shed)
        (has Shed Pickaxe)
        (has Shed Hammer)
        (has Mine Rock)
    )

    (:goal
        (and
            (has Shed Sword)
            (forall
                (?item - resource)
                (not (has Player ?item))
            )
        )
    )
)