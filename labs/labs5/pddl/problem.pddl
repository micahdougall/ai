
(define (problem car_build) 
    (:domain landrover)
    (:objects 
        RangeRover Discovery - car
        Engine1 Engine2 - engine
        Wheel1 Wheel2 Wheel3 Wheel4 Wheel5 Wheel6 Wheel7 Wheel8 - wheel
    )

    (:init
        (is_safe_to_start)
    )

    (:goal
        (and
            (is_inspected RangeRover)
            (is_inspected Discovery)
        )
    )
)
