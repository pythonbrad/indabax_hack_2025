import plotly.express as px
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

import config


__all__ = ["Dashboard"]


class Dashboard:
    _dataframe = None

    def __init__(self, dataframe):
        self._dataframe = dataframe

        # Health conditions
        start_column = dataframe.columns.get_loc("ÉLIGIBILITÉ AU DON.")
        end_column = dataframe.columns.get_loc("Si autres raison préciser")
        self.health_conditions = list(
            dataframe.iloc[:, start_column + 1 : end_column].columns
        )
        # Years
        self.years = sorted(dataframe["Year"].dropna().unique())

    def get_dataframe(self):
        return self._dataframe.copy()

    def map_donor_distribution(self, map_view=True):
        df = self.get_dataframe()

        # Data preprocessing
        # Ensure the column names match exactly with those in your dataset
        df = df[["Arrondissement de résidence"]].dropna()

        df_counts = (
            df.groupby("Arrondissement de résidence")
            .size()
            .reset_index(name="Donor Count")
        )

        if not map_view:
            fig = px.bar(
                df_counts,
                x="Arrondissement de résidence",
                y="Donor Count",
                color="Arrondissement de résidence",
                title="Donor Distribution by Arrondissement",
            )

            return fig

        # Load GeoJSON for mapping (you need a GeoJSON file with arrondissement boundaries)
        geojson_path = config.PREPROCESSED_GEO_DATASET_FILE  # Replace with actual path
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        fig = px.choropleth_map(
            df_counts,
            geojson=geojson_data,
            locations="Arrondissement de résidence",
            featureidkey="properties.ADM3_FR",  # Adjust based on your GeoJSON structure
            color="Donor Count",
            color_continuous_scale="Reds",
            map_style="carto-positron",
            zoom=10,
            center={"lat": 4.05, "lon": 9.7},  # Adjust based on your region
            opacity=0.6,
            title="Donor Distribution by Arrondissement",
        )

        return fig

    def health_conditions_and_eligibility(self, condition: str | None = None):
        df = self.get_dataframe()

        # Count eligible vs non-eligible donors
        df_eligibility = df["Eligible"].value_counts().reset_index()
        df_eligibility.columns = ["Eligibility", "Count"]
        df_eligibility["Eligibility"] = df_eligibility["Eligibility"].map(
            {True: "Eligible", False: "Non-Eligible"}
        )

        if not condition:
            return px.pie(
                df_eligibility,
                names="Eligibility",
                values="Count",
                title="Overall Donor Eligibility",
                color_discrete_sequence=["green", "red"],
            )
        elif condition == "all":
            df_impact_of_health_cond = df[self.health_conditions].mean()
            fig = px.bar(
                df_impact_of_health_cond,
                x=df_impact_of_health_cond.index,
                y=df_impact_of_health_cond.values,
                title="Overall Impact of health conditions on Eligibility",
                labels={"y": "Impact"},
            )

            return fig

        condition_counts = (
            df.groupby([condition, "Eligible"]).size().reset_index(name="Count")
        )
        condition_counts["Eligible"] = condition_counts["Eligible"].map(
            {True: "Eligible", False: "Non-Eligible"}
        )
        condition_counts[condition] = condition_counts[condition].map(
            {1: "Positif", 0: "Negatif"}
        )
        condition_counts.rename(columns={"Eligible": "Eligibility"}, inplace=True)

        fig = px.bar(
            condition_counts,
            x=condition,
            y="Count",
            color="Eligibility",
            barmode="group",
            title=f"Impact of {condition} on Eligibility",
            color_discrete_map={"Eligible": "green", "Non-Eligible": "red"},
        )

        return fig

    def profiling_ideal_donors(self, paired_with: str = "Religion"):
        # Selecting relevant columns for clustering
        demographic_features = [
            "Age",
            "Genre",
            paired_with,
        ]

        df = self.get_dataframe()
        # Filter illigible donors
        df = df[df["Eligible"]]
        df_profiling = df[demographic_features].dropna()

        # Encoding categorical features
        gender_le = LabelEncoder()
        paired_with_le = LabelEncoder()
        df_profiling["Genre"] = gender_le.fit_transform(df_profiling["Genre"])
        df_profiling[paired_with] = paired_with_le.fit_transform(
            df_profiling[paired_with]
        )

        # Standardizing data
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_profiling)

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=len(demographic_features), random_state=42)
        df_profiling["Cluster"] = kmeans.fit_predict(df_scaled)

        # Apply PCA for visualization
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(df_scaled)
        df_profiling["PCA1"] = df_pca[:, 0]
        df_profiling["PCA2"] = df_pca[:, 1]

        # Generate insights into the characteristics of the ideal blood donor
        ideal_donor = df_profiling[
            df_profiling["Cluster"] == df_profiling["Cluster"].mode()[0]
        ]
        insights = [
            round(ideal_donor["Age"].mean(), 1),
            gender_le.inverse_transform([ideal_donor["Genre"].mode()[0]])[0],
            paired_with_le.inverse_transform([ideal_donor[paired_with].mode()[0]])[0],
        ]

        return px.scatter(
            df_profiling,
            x="PCA1",
            y="PCA2",
            color=df_profiling["Cluster"].astype(str),
            title="Donor Clusters (PCA Reduced)",
            color_discrete_sequence=px.colors.qualitative.Set1,
            hover_data=demographic_features,
        ), insights

    def campaign_effectiveness(self, selected_year: int):
        df = self.get_dataframe()

        # Aggregate donation counts per month
        donation_trends = (
            df.groupby(["Year", "Month"]).size().reset_index(name="Donations")
        )

        filtered_data = df[df["Year"] == selected_year]

        # Line Chart - Monthly Donation Trends
        trend_fig = px.line(
            donation_trends[donation_trends["Year"] == selected_year],
            x="Month",
            y="Donations",
            title=f"Monthly Donation Trends in {selected_year}",
            labels={"Month": "Month", "Donations": "Number of Donations"},
            markers=True,
        )

        # Bar Chart - Donations by Gender
        gender_fig = px.bar(
            filtered_data.groupby("Genre").size().reset_index(name="Count"),
            x="Genre",
            y="Count",
            title=f"Donations by Gender in {selected_year}",
            color="Genre",
        )

        # Bar Chart - Donations by Education Level
        education_fig = px.bar(
            filtered_data.groupby("Niveau d'etude").size().reset_index(name="Count"),
            x="Niveau d'etude",
            y="Count",
            title=f"Donations by Education Level in {selected_year}",
            color="Niveau d'etude",
        )

        # Bar Chart - Donations by Profession
        profession_fig = px.bar(
            filtered_data.groupby("Profession").size().reset_index(name="Count"),
            x="Profession",
            y="Count",
            title=f"Donations by Profession in {selected_year}",
            color="Profession",
        )

        return trend_fig, gender_fig, education_fig, profession_fig

    def donor_retention(self, selected_year: int):
        df = self.get_dataframe()

        # Identify repeat donors
        donor_counts = (
            df.groupby("A-t-il (elle) déjà donné le sang")
            .size()
            .reset_index(name="Donation Count")
        )
        df = df.merge(donor_counts, on="A-t-il (elle) déjà donné le sang", how="left")

        # Categorize retention levels
        df["Retention Category"] = df["A-t-il (elle) déjà donné le sang"].map(
            {0: "First-Time", 1: "Repeat Donor"}
        )

        filtered_data = df[df["Year"] == selected_year]

        # Pie Chart - Repeat Donation Frequency
        pie_fig = px.pie(
            filtered_data.groupby("Retention Category")
            .size()
            .reset_index(name="Count"),
            values="Count",
            color="Retention Category",
            names="Retention Category",
            title=f"Overall Donor Retention in {selected_year}",
        )

        # Bar Chart - Retention by Age Group
        age_fig = px.bar(
            filtered_data.groupby(["Age", "Retention Category"])
            .size()
            .reset_index(name="Count"),
            x="Age",
            y="Count",
            color="Retention Category",
            title=f"Donor Retention by Age in {selected_year}",
            barmode="group",
        )

        # Bar Chart - Retention by Genre Group
        genre_fig = px.bar(
            filtered_data.groupby(["Genre", "Retention Category"])
            .size()
            .reset_index(name="Count"),
            x="Genre",
            y="Count",
            color="Retention Category",
            title=f"Donor Retention by Genre in {selected_year}",
            barmode="group",
        )

        # Bar Chart - Retention by Profession
        profession_fig = px.bar(
            filtered_data.groupby(["Profession", "Retention Category"])
            .size()
            .reset_index(name="Count"),
            x="Profession",
            y="Count",
            color="Retention Category",
            title=f"Donor Retention by Profession in {selected_year}",
            barmode="group",
        )

        # Bar Chart - Retention by Region
        region_fig = px.bar(
            filtered_data.groupby(["Arrondissement de résidence", "Retention Category"])
            .size()
            .reset_index(name="Count"),
            x="Arrondissement de résidence",
            y="Count",
            color="Retention Category",
            title=f"Donor Retention by Region in {selected_year}",
            barmode="group",
        )

        return pie_fig, age_fig, genre_fig, profession_fig, region_fig

    def feedback_analysis(self, selected_year: int, group_with: str):
        df = self.get_dataframe()

        df_counts = df["Health feedback analysis"].value_counts()
        df = df.merge(df_counts, on="Health feedback analysis", how="left")

        filtered_data = df[df["Year"] == selected_year]

        pie_fig = px.pie(
            filtered_data.groupby("Health feedback analysis")
            .size()
            .reset_index(name="Count"),
            values="Count",
            color="Health feedback analysis",
            names="Health feedback analysis",
            title=f"Overall Feedback Analysis in {selected_year}",
        )

        arr_fig = px.bar(
            filtered_data.groupby(["Health feedback analysis", group_with])
            .size()
            .reset_index(name="Count"),
            x=group_with,
            y="Count",
            color="Health feedback analysis",
            barmode="group",
            title=f"Feedback Analysis per {group_with} in {selected_year}",
        )

        return pie_fig, arr_fig
