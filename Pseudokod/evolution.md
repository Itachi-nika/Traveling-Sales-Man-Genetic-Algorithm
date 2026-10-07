ALGORITHM CreateNextGeneration(
    population,
    cities,
    config
)

    Sort population from shortest
    to longest tour distance

    next_population ← copies of the
                      best elitism individuals

    WHILE size(next_population) < population_size

        parent1 ← TournamentSelection(population)
        parent2 ← TournamentSelection(population)

        IF random_number < crossover_rate
            child1, child2 ← OrderCrossover(
                parent1,
                parent2
            )
        ELSE
            child1 ← copy of parent1
            child2 ← copy of parent2
        END IF

        IF random_number < mutation_rate
            child1 ← SwapMutation(child1)
        END IF

        IF random_number < mutation_rate
            child2 ← SwapMutation(child2)
        END IF

        Add child1 to next_population

        IF next_population is not full
            Add child2 to next_population
        END IF

    END WHILE

    RETURN next_population

END ALGORITHM