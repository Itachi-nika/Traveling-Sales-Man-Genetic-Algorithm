ALGORITHM CreatePopulation(number_of_cities, population_size)

    population ← empty list

    REPEAT population_size times

        route ← [0, 1, ..., number_of_cities - 1]

        Shuffle route randomly

        Add route to population

    END REPEAT

    RETURN population

END ALGORITHM