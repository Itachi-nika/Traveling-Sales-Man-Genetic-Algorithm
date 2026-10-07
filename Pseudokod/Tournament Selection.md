ALGORITHM TournamentSelection(
    population,
    tournament_size
)

    competitors ← randomly select
                  tournament_size individuals
                  without replacement

    winner ← competitor with smallest tour distance

    RETURN copy of winner

END ALGORITHM