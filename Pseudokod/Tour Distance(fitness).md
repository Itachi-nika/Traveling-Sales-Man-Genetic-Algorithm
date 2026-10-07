ALGORITHM TourDistance(route, cities)

    total_distance ← 0

    FOR each position i in route

        current_city ← route[i]
        next_city ← route[(i + 1) mod number_of_cities]

        distance ← EuclideanDistance(
            current_city,
            next_city
        )

        total_distance ← total_distance + distance

    END FOR

    RETURN total_distance

END ALGORITHM