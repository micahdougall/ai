;Domain definition for a medieval fantasy Multi-User dungeon video game (Runescape)

(define 
    (domain runescape)

    (:requirements :strips :equality :typing :universal-preconditions :conditional-effects)

    (:types
        player - object
        anvil farm forest furnace mine storage - location
        component material tool weapon - resource
        bars chickens ore rock trees wood - material
        arrowhead feathers shafts - component
        axe hammer knife pickaxe - tool
        arrow sword - weapon
    )

    (:predicates
        (at ?p - player ?l - location)
        (has ?o - (either player location) ?r - resource)
        (includes ?o - weapon ?c - component)
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
            ?item - resource
            ?location - storage
        )
        :precondition (and 
            (at ?character ?location)
            (has ?character ?item)
        )
        :effect (and 
            (has ?location ?item)
            (not (has ?character ?item))
        )
    )
    
    (:action equip
        :parameters (
            ?character - player
            ?item - resource
            ?location - storage
        )
        :precondition (and 
            (at ?character ?location)
            (forall (?t - tool)
                (not (has ?character ?t))
            )
            (has ?location ?item)
        )
        :effect (and 
            (has ?character ?item)
        )
    )
    
    (:action mine-rocks
        :parameters (
            ?miner - player
            ?location - mine
            ?tool - pickaxe
            ?material - rock
            ?resource - ore
        )
        :precondition (and 
            (at ?miner ?location)
            (has ?miner ?tool)
            (has ?location ?material)
        )
        :effect (and 
            (has ?miner ?resource)
        )
    )

    (:action smelt-ore
        :parameters (
            ?smelter - player
            ?location - furnace
            ?material - ore
            ?resource - bars
        )
        :precondition (and 
            (at ?smelter ?location)
            (has ?smelter ?material)
        )
        :effect (and 
            (has ?smelter ?resource)
            (not (has ?smelter ?material))
        )
    )

    (:action smithe-bars
        :parameters (
            ?smither - player
            ?location - anvil
            ?tool - hammer
            ?material - bars
            ?resource - (either arrowhead sword)
        )
        :precondition (and 
            (at ?smither ?location)
            (has ?smither ?material)
            (has ?smither ?tool)
        )
        :effect (and 
            (has ?smither ?resource)
            (not (has ?smither ?material))
        )
    )

    (:action chop-trees
        :parameters (
            ?lumberjack - player
            ?location - forest
            ?tool - axe
            ?material - trees
            ?resource - wood
        )
        :precondition (and 
            (at ?lumberjack ?location)
            (has ?lumberjack ?tool)
            (has ?location ?material)
        )
        :effect (and 
            (has ?lumberjack ?resource)
        )
    )

    (:action fletch-shafts
        :parameters (
            ?fletcher - player
            ?tool - knife
            ?material - wood
            ?resource - shafts
        )
        :precondition (and 
            (has ?fletcher ?material)
        )
        :effect (and 
            (has ?fletcher ?resource)
            (not (has ?fletcher ?material))
        )
    )

    (:action hunt-chicken
        :parameters (
            ?poacher - player
            ?location - farm
            ?material - chickens
            ?resource - feathers
        )
        :precondition (and 
            (has ?location ?material)
        )
        :effect (and 
            (has ?poacher ?resource)    
        )
    )
    
    (:action affix
        :parameters (
            ?archer - player
            ?weapon - arrow
            ?item - component
        )
        :precondition (and 
            (has ?archer ?item)
        )
        :effect (and 
            (includes ?weapon ?item)
            (not (has ?archer ?item))
            (when 
                (and
                    (exists (?a - arrowhead) 
                        (includes ?weapon ?a)
                    )
                    (exists (?f - feathers) 
                        (includes ?weapon ?f)
                    )
                    (exists (?s - shafts) 
                        (includes ?weapon ?s)
                    )
                )
                (and
                    (has ?archer ?weapon)
                )
            )
        )
    )
    
    
    ; (:axiom
    ;     :vars (?s - site)
    ;     :context (and
    ;         (walls-built ?s)
    ;         (windows-fitted ?s)
    ;         (cables-installed ?s)
    ;     )
    ;     :implies (site-built ?s)
    ; )
    

    ; (:event arrow-assembled
    ;     :parameters (
    ;         ?arrow - arrow
    ;     )
    ;     :precondition (and
    ;         (exists (?shafts - shafts) 
    ;             where (has ?arrow ?shafts)
    ;         )
    ;         (exists (?arrowhead - arrowhead) 
    ;             where (has ?arrow ?arrowhead)
    ;         )
    ;     )
    ;     :effect (and
    ;         (exists (?arrow) )
    ;     )
    ; )
    
)