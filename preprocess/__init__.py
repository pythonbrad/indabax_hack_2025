import pandas as pd
import pathlib
import geopandas as gpd
import json
import re
import logging

from . import utils


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


__all__ = ["preprocess"]


# Clean and prepare data for analysis and visualization.
def preprocess(
    dataset_file: str,
    pre_dataset_file,
    geodata_file: str,
    pre_geodata_file,
):
    assert pathlib.Path(dataset_file).exists()
    assert pathlib.Path(geodata_file).exists()

    # Create output folder if not exists
    pathlib.Path(pre_dataset_file).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(pre_geodata_file).parent.mkdir(parents=True, exist_ok=True)

    # Load the sheets
    logger.info("Loading of dataset...")
    dataframe_a = pd.read_excel(dataset_file, sheet_name=0)
    dataframe_b = pd.read_excel(dataset_file, sheet_name=2)
    dataframe_c = pd.read_excel(dataset_file, sheet_name=1)
    logger.info("Dataset loaded!")

    logger.info("Data cleaning...")

    # Clean dataframe column names
    dataframe_a.rename(columns=lambda x: x.strip(), inplace=True)
    dataframe_b.rename(columns=lambda x: x.replace("_", " ").strip(), inplace=True)
    dataframe_c["Sexe"] = dataframe_c["Sexe"].map({"F": "Femme", "M": "Homme"})
    dataframe_c.rename(
        columns={"Horodateur": "Date de remplissage de la fiche", "Sexe": "Genre"},
        inplace=True,
    )

    # Concat data
    dataframe = pd.concat([dataframe_a, dataframe_b, dataframe_c]).astype(str)

    # Clean names
    name_columns = [
        "Arrondissement de résidence",
        "Quartier de Résidence",
        "Religion",
        "Nationalité",
        "Situation Matrimoniale (SM)",
        "Profession",
        "Niveau d'etude",
    ]
    dataframe[name_columns] = dataframe[name_columns].map(utils.clean_name)

    # Clean dates.
    date_columns = ["Date de remplissage de la fiche", "Date de naissance"]
    dataframe[date_columns] = dataframe[date_columns].map(utils.clean_date)
    dataframe["Date de remplissage de la fiche"] = pd.to_datetime(
        dataframe["Date de remplissage de la fiche"]
    )
    dataframe["Date de naissance"] = pd.to_datetime(dataframe["Date de naissance"])

    # Adding of the missing age infos.
    computed_ages = (
        dataframe["Date de naissance"]
        .map(lambda x: utils.calculate_age(x) if pd.notnull(x) else 0)
        .astype(float)
    )
    dataframe["Age"] = (
        dataframe["Age"].map(lambda x: int(x) if x.isdigit() else 0).astype(float)
        + computed_ages
    )
    dataframe["Age"] = dataframe["Age"].map(lambda x: x if x else None)

    # Precompute date infos.
    dataframe["Year"] = dataframe["Date de remplissage de la fiche"].dt.year
    dataframe["Month"] = dataframe["Date de remplissage de la fiche"].dt.month

    # Clean poids and taille.
    column_names = ["Poids", "Taille"]
    dataframe[column_names] = (
        dataframe[column_names]
        .map(lambda x: int(x) if x.isdigit() else 0)
        .astype(int)
        .map(lambda x: x if x else None)
    )

    # Digitalize retention.
    dataframe["A-t-il (elle) déjà donné le sang"] = dataframe[
        "A-t-il (elle) déjà donné le sang"
    ].map(lambda x: 1 if x.lower().strip() == "oui" else 0)

    # Digitalize the eligibility and the health conditions
    start_column = dataframe.columns.get_loc("ÉLIGIBILITÉ AU DON.")
    end_column = dataframe.columns.get_loc("Si autres raison préciser")

    dataframe.iloc[:, start_column:end_column] = dataframe.iloc[
        :, start_column:end_column
    ].map(lambda x: 1 if x.lower() in ["eligible", "oui"] else 0)

    # Estimate the illigibility
    dataframe["Eligible"] = (
        dataframe.iloc[:, start_column + 1 : end_column].sum(axis=1) == 0
    )

    # Update column names to reflect criteria description
    dataframe.rename(columns=lambda x: re.sub(r".*\[|\]", "", x), inplace=True)

    # Geo data preparation
    logger.info("Preprocess of the GEO data...")
    gdf = gpd.read_file(geodata_file)
    gdf.to_file(pre_geodata_file, driver="GeoJSON")
    logger.info("GEO data preproccessed!")

    # Browse the map and apply text similarity to detect the best one
    logger.info("Attempt to fix geo data in the dataset...")
    # Load GeoJSON for mapping
    with open(pre_geodata_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    geo_arrs = [x["properties"]["ADM3_FR"] for x in geojson_data["features"]]

    # Attempt to fix the arrondissement names.
    dataframe["Arrondissement de résidence"] = dataframe[
        "Arrondissement de résidence"
    ].apply(lambda x: utils.fix_arrondissement(x, geo_arrs))

    logger.info("Attempt to digitalize feedback using sentiment analysis...")
    # Applying sentiment analysis on feedback
    dataframe["Health feedback analysis"] = dataframe["Si autres raison préciser"].map(
        utils.sentiment_analysis
    )

    logger.info("Dataset cleaned!")

    # Save the preprocessed data
    logger.info("Saving of the dataset...")
    dataframe.to_excel(pre_dataset_file)
    logger.info("Dataset saved!")

    return dataframe
