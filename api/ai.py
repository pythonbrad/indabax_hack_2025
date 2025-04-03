import pandas as pd


class EligibilityPrediction:
    def __init__(self, datafile: str):
        # should be use in read only
        self.dataframe = pd.read_excel(datafile)

    def predict(
        self,
        health_conditions: list[str] = [],
        genre: str | None = None,
        professions: list[str] = [],
        age: int | None = None,
    ) -> float:
        """
        Returns the probability that a person is eligible for donation.

        Note that p=1 if eligible.
        """

        eligible = self.dataframe[self.dataframe["Eligible"]]

        # If no criteria, we predict globally
        if not (health_conditions or genre or professions or age):
            prop = eligible["Eligible"].count() / self.dataframe["Eligible"].count()

            return prop

        # We start by assumpt that the person is eligible
        prop = 1

        # p(1/genre)
        if genre:
            eprop_genre = eligible[eligible[["Genre"]] == genre]["Genre"].count() or 1
            prop_genre = (
                self.dataframe[self.dataframe[["Genre"]] == genre]["Genre"].count() or 1
            )
            prop *= eprop_genre / prop_genre

        # p(1/profession)
        for profession in professions:
            eprop_profession = (
                eligible[eligible["Profession"] == profession]["Profession"].count()
                or 1
            )
            prop_profession = (
                self.dataframe[self.dataframe["Profession"] == profession][
                    "Profession"
                ].count()
                or 1
            )
            prop *= eprop_profession / prop_profession

        # p(1/age)
        if age:
            eprop_age = eligible[eligible["Age"] == age]["Age"].count() or 1
            prop_age = self.dataframe[self.dataframe["Age"] == age]["Age"].count() or 1
            prop *= eprop_age / prop_age

        # p(1/health_condition) = 0
        for health_condition in health_conditions:
            if (self.get_health_conditions() == health_condition).any():
                prop *= 0

        return prop

    def get_health_conditions(self):
        start_column = self.dataframe.columns.get_loc("ÉLIGIBILITÉ AU DON.")
        end_column = self.dataframe.columns.get_loc("Si autres raison préciser")
        data = self.dataframe.columns[start_column + 1 : end_column]

        return data

    def get_professions(self):
        return self.dataframe["Profession"].unique()

    def get_genres(self):
        return self.dataframe["Genre"].unique()
