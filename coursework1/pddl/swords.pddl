(define 
    (problem makesword) 
    (:domain runescape)

    (:objects 
        p1 - player
        shed - storage
        m1 - mine
        f1 - furnace
        a1 - anvil
        pA - pickaxe
        h1 - hammer
    )

    (:init
        ;todo: put the initial state's facts and numeric values here
        ; (= (rock-count p1) 0)
        ; (not (has_sword p1))
        ; (at_mine p1)


        ; (at p1 m1)
        (at p1 shed)
        (has_rock p1)
        ; (has_pickaxe p1)
        ; (in_hand pA)
    )

    (:goal (and
        ;todo: put the goal condition here
        ; (= (rock-count p1) 3)
        ; (has_ore p1)
        ; (has_smithable_bars p1)
        (has_sword p1)
    ))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
