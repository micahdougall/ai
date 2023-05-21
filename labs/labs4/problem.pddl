
(define (problem clean_areas) 
    (:domain housekeeping)
    (:objects 
        left - area
        right - area
    )

    (:init
        (not (is_clean left))
        (not (is_clean right))
        (is_in_area left)
    )

    (:goal (and
        (is_clean left)
        (is_clean right)
    ))
)
