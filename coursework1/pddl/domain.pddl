;Domain definition for a medieval fantasy Multi-User dungeon video game (Runescape)

(define 
    (domain runescape)

    ;TODO: Investigate libraries
    ; (:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

    ; (:requirements :strips :equality :fluents)
    (:requirements :strips :equality :conditional-effects)
    ; :disjunctive-preconditions = allow use of or
    ; :equality (= 1 1)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        player
        storage mine furnace anvil - location
        axe pickaxe hammer - tool
        ; sword
        
    )
    ; (:constants
    ;     P - player
    ; )

    ; un-comment following line if constants are needed
    ;(:constants )

    ; Create condition to limit tools in hand


    (:predicates ;todo: define predicates here
        (at ?p - player ?l - location)
        ; (at_mine ?p - player)
        (has_rock ?p - player)
        (has_ore ?p - player)
        (has_smithable_bars ?p - player)
        ; (has_ore ?p - player)
        ; (has_pickaxe ?p - player)
        (equipped ?p - player ?t - tool)
        ; (has_axe ?p - player)
        (has_sword ?p - player)
    )

    ; ()


    ; Not availabe in 1.2
    ; (:functions ;todo: define numeric functions here
    ;     (rock-count ?p - player)
    ; )

    
    (:action move-to
        :parameters (
            ?p - player
            ?from - location
            ?to - location
        )
        :precondition (and
            (at ?p ?from)
            (not (at ?p ?to))
            (not (= ?from ?to))
        )
        :effect (and 
            (at ?p ?to)
            (not (at ?p ?from))
        )
    )

    (:action sheath
        :parameters (
            ?p - player
            ?t - tool
            ?l - storage
        )
        :precondition (and 
            (at ?p ?l)
            (equipped ?p ?t)
        )
        :effect (and 
            (not (equipped ?p ?t))
        )
    )
    
    
    (:action equip
        :parameters (
            ?p - player
            ?t - tool
            ?l - storage
        )
        :precondition (and 
            (at ?p ?l)
            ; (not (equipped ?p ?t))
            (forall (?x - tool)
                (not (equipped ?p ?x))
            )
        )
        :effect (and 
            (equipped ?p ?t)
        )
    )
    


    ;define actions here
    (:action mine-rocks
        :parameters (
            ?p - player
            ?l - mine
            ?t - pickaxe
        )
        ; :parameters (?l - location)
        :precondition (and 
            (at ?p ?l)
            (has_rock ?p)
            ; (has_pickaxe ?p)
            (equipped ?p ?t)
            ; (exists (?r - rock))
        )
        :effect (and 
            (has_ore ?p)
            (not (has_rock ?p))
            ; (increase (rock-count ?p) 1)
        )
    )

    (:action smelt-ore
        :parameters (
            ?p - player 
            ?l - furnace
        )
        :precondition (and 
            (at ?p ?l)
            (has_ore ?p)
        )
        :effect (and 
            (has_smithable_bars ?p)
            (not (has_ore ?p))
        )
    )

    (:action smith-bars
        :parameters (
            ?p - player
            ?l - anvil
            ?t - hammer
        )
        :precondition (and 
            (at ?p ?l)
            (has_smithable_bars ?p)
            (equipped ?p ?t)
        )
        :effect (and 
            (has_sword ?p)
        )
    )
    


    
    

    ; (axiom)

)