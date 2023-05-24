
(define (domain landrover)

    (:requirements :strips :equality :typing)

    (:types 
        car - object
        wheel engine - part
    )

    (:predicates
        (is_safe_to_start)
        (is_attached ?p - part ?c - car)
        (is_inspected ?c - car)
    )

    (:action attach
        :parameters (
            ?p - part
            ?c - car
        )
        :precondition (and 
            (forall (?a - car)
                (not (is_attached ?p ?a))
            )
        )
        :effect (and 
            (is_attached ?p ?c)
        )
    )

    (:action attach-wheels
        :parameters (
            ?w1 - wheel
            ?w2 - wheel
            ?w3 - wheel
            ?w4 - wheel
            ?c - car
        )
        :precondition (and 
            (forall (?a - car)
                (not (is_attached ?w1 ?a))
            )
            (forall (?a - car)
                (not (is_attached ?w2 ?a))
            )
            (forall (?a - car)
                (not (is_attached ?w3 ?a))
            )
            (forall (?a - car)
                (not (is_attached ?w4 ?a))
            )
        )
        :effect (and 
            (is_attached ?w1 ?c)
            (is_attached ?w2 ?c)
            (is_attached ?w3 ?c)
            (is_attached ?w4 ?c)
        )
    )
    

    (:action inspect
        :parameters (?c - car)
        :precondition (and 
            (exists (?e - engine) 
                (is_attached ?e ?c)
            )
            (exists (?w - wheel) 
                (is_attached ?w ?c)
            )
            (not (is_inspected ?c))
        )
        :effect (and 
            (is_inspected ?c)
        )
    )
)