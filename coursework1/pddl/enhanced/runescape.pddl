;Domain definition for a medieval fantasy Multi-User dungeon video game (Runescape)

(define 
    (domain runescape)

    (:requirements :strips :equality :typing :universal-preconditions :conditional-effects :fluents :negative-preconditions)

    ; Using object hierarchy to allow polymorphism within predicates
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
        ; Where the player is
        (at ?p - player ?l - location)
        ; Does a player/location have a given resource
        (has ?o - (either player location) ?r - resource) 
        ; Does the state of a weapon currently include a component part
        (includes ?o - weapon ?c - component)
    )

    ; For later version of PDDL, track the distance travelled
    (:functions
        (travelled)
    )

    ; Moves a player form one location to another
    (:action move-to
        :parameters (
            ?character - player
            ?from - location
            ?to - location
        )
        ; Player must be at the from location
        :precondition (and
            (at ?character ?from)
            (not (at ?character ?to))
            (not (= ?from ?to))
        )
        :effect (and 
            (at ?character ?to)
            (not (at ?character ?from))
            (increase (travelled) 1)
        )
    )

    ; Player stores an item at a given location
    (:action store
        :parameters (
            ?character - player
            ?item - resource
            ?location - storage
        )
        ; Player must have the item and be at the given location
        :precondition (and 
            (at ?character ?location)
            (has ?character ?item)
        )
        :effect (and 
            (has ?location ?item)
            (not (has ?character ?item))
        )
    )
    
    ; Player equips themselves with an item from a location
    (:action equip
        :parameters (
            ?character - player
            ?item - resource
            ?location - storage
        )
        ; Player must be at the given location which has the item
        ; Additionl arbitrary constraint that the player can only carry one tool
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
    
    ; Player mines rocks
    (:action mine-rocks
        :parameters (
            ?miner - player
            ?location - mine
            ?tool - pickaxe
            ?material - rock
            ?resource - ore
        )
        ; Mining can only take place at a mine when a player has a pickaxe and the mine has rocks
        :precondition (and 
            (at ?miner ?location)
            (has ?miner ?tool)
            (has ?location ?material)
        )
        ; Mine yields ore
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

    ; Player smelts bars at an anvil
    (:action smithe-bars
        :parameters (
            ?smither - player
            ?location - anvil
            ?tool - hammer
            ?material - bars
            ?resource - (either arrowhead sword)
        )
        ; Player must be at the anvil with the bars and a hammer
        :precondition (and 
            (at ?smither ?location)
            (has ?smither ?material)
            (has ?smither ?tool)
        )
        ; The anvil yields either an arrowhead or a sword and consumes the bars
        :effect (and 
            (has ?smither ?resource)
            (not (has ?smither ?material))
        )
    )

    ; Player chops trees in a forest
    (:action chop-trees
        :parameters (
            ?lumberjack - player
            ?location - forest
            ?tool - axe
            ?material - trees
            ?resource - wood
        )
        ; Player must be at the forest with an axe
        :precondition (and 
            (at ?lumberjack ?location)
            (has ?lumberjack ?tool)
            (has ?location ?material)
        )
        ; The forest yields wood
        :effect (and 
            (has ?lumberjack ?resource)
        )
    )

    ; Player fletches shafts
    (:action fletch-shafts
        :parameters (
            ?fletcher - player
            ?tool - knife
            ?material - wood
            ?resource - shafts
        )
        ; Player must have wood and a knife
        :precondition (and 
            (has ?fletcher ?material)
            (has ?fletcher ?tool)
        )
        :effect (and 
            (has ?fletcher ?resource)
            (not (has ?fletcher ?material))
        )
    )

    ; Player hunts chickens for feathers
    (:action hunt-chicken
        :parameters (
            ?poacher - player
            ?location - farm
            ?material - chickens
            ?resource - feathers
        )
        ; Player must be at a farm which has chickens
        :precondition (and 
            (at ?poacher ?location)
            (has ?location ?material)
        )
        :effect (and 
            (has ?poacher ?resource)    
        )
    )
    
    ; Player constructs an arrow from components
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
            ; Composite conditional effect to declare that the player has the weapon once all the components are affixed - this could be an axiom instead
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
)