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
        (at Player Shed) ; Begin with the player at the shed
        (has Shed Pickaxe) ; Shed must have available tools
        (has Shed Hammer)
        (has Mine Rock) ; Minimum resource required
    )

    ; Succeeded once the player has deposited all resources at the shed including the desired sword
    (:goal
        (and
            (has Shed Sword)
            (forall
                (?item - resource)
                (not (has Player ?item))
            )
        )
    )

    ; Minimise the distance travelled
    (:metric (minimize (
        (travelled)
    )))
)