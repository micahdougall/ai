
;Header and description

(define (domain housekeeping)

    (:requirements :strips :equality)

    (:types 
        area
    )

    (:predicates
        (is_clean ?a - area) ; is the area clean
        (is_in_area ?a - area) ; is cleaner in area
    )

    (:action move
        :parameters (?a - area) ; area to move to
        :precondition (and 
            (not (is_in_area ?a))
        )
        :effect (and 
            (is_in_area ?a) ; move the cleaner to the area
        )
    )

    (:action clean
        :parameters (?a - area) ; area to clean
        :precondition (and 
            (is_in_area ?a) ; cleaner is in the area
            (not (is_clean ?a)) ; don't allow an area to be re-cleaned
        )
        :effect (and 
            (is_clean ?a) ; clean the area
        )
    )
)