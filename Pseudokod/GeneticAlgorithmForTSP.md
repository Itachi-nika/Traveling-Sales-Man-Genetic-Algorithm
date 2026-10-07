
ALGORITHM GeneticAlgorithmForTSP(cities, config, seed)

    Initialize random generator using seed

    population ← CreatePopulation(
        number_of_cities,
        population_size
    )

    Evaluate population
    Record best distance and mean distance for generation 0

    best_route ← route with smallest tour distance
    best_distance ← TourDistance(best_route)

    FOR generation ← 1 TO number_of_generations

        population ← CreateNextGeneration(
            population,
            cities,
            config
        )

        Evaluate population

        Record:
            best distance
            mean distance

        generation_best ← individual with smallest tour distance
        generation_best_distance ← TourDistance(generation_best)

        IF generation_best_distance < best_distance
            best_distance ← generation_best_distance
            best_route ← copy of generation_best
        END IF

    END FOR

    RETURN best_route,
           best_distance,
           history,
           runtime,
           number_of_population_evaluations

END ALGORITHM