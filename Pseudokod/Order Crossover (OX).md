ALGORITHM OrderCrossover(parent1, parent2)

    Randomly select two different crossover positions

    start ← smaller position
    end ← larger position

    child1 ← empty route
    child2 ← empty route

    Copy parent1[start ... end] into
    the same positions in child1

    Copy parent2[start ... end] into
    the same positions in child2

    Starting after end in parent2:
        Read cities in circular order
        Ignore cities already present in child1
        Fill remaining empty positions in child1

    Starting after end in parent1:
        Read cities in circular order
        Ignore cities already present in child2
        Fill remaining empty positions in child2

    RETURN child1, child2

END ALGORITHM