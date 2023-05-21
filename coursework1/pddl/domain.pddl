;Domain definition for a medieval fantasy Multi-User dungeon video game (Runescape)

(define 
    (domain runescape)
    
    (:requirements :strips :equality :conditional-effects)

    (:types
        player
        storage mine furnace anvil - location
        axe pickaxe hammer - tool
        rock ore bars - material
    )

    (:predicates
        (at ?p - player ?l - location)
        (equipped ?p - player ?t - tool)
        ; (has ?a -  ?m - )
        (has ?p - player ?m - material)
        (has_sword ?p - player)
    )

    (:action move-to
        :parameters (
            ?character - player
            ?from - location
            ?to - location
        )
        :precondition (and
            (at ?character ?from)
            (not (at ?character ?to))
            (not (= ?from ?to))
        )
        :effect (and 
            (at ?character ?to)
            (not (at ?character ?from))
        )
    )

    (:action store
        :parameters (
            ?character - player
            ?item - tool
            ?location - storage
        )
        :precondition (and 
            (at ?character ?location)
            (equipped ?character ?item)
        )
        :effect (and 
            (not (equipped ?character ?item))
        )
    )
    
    (:action equip
        :parameters (
            ?character - player
            ?item - tool
            ?location - storage
        )
        :precondition (and 
            (at ?character ?location)
            (forall (?t - tool)
                (not (equipped ?character ?t))
            )
        )
        :effect (and 
            (equipped ?character ?item)
        )
    )
    
    (:action mine-rocks
        :parameters (
            ?miner - player
            ?location - mine
            ?tool - pickaxe
            ?produces - ore
        )
        :precondition (and 
            (at ?miner ?location)
            (equipped ?miner ?tool)
        )
        :effect (and 
            (has ?miner ?produces)
        )
    )

    (:action smelt-ore
        :parameters (
            ?smelter - player
            ?location - furnace
            ?material - ore
            ?produces - bars
        )
        :precondition (and 
            (at ?smelter ?location)
            (has ?smelter ?material)
        )
        :effect (and 
            (has ?smelter ?produces)
            (not (has ?smelter ?material))
        )
    )

    (:action smithe-bars
        :parameters (
            ?smither - player
            ?location - anvil
            ?tool - hammer
            ?produces - bars
        )
        :precondition (and 
            (at ?smither ?location)
            (has ?smither ?produces)
            (equipped ?smither ?tool)
        )
        :effect (and 
            (has_sword ?smither)
        )
    )
)