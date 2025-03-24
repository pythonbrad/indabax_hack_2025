#!/usr/bin/env bash

mkdir -p data


OUTPUT_FILE='cmr_admbnda_inc_20180104_shp.zip'

echo "Downloading of ${OUTPUT_FILE}..."
curl -LsSf https://data.humdata.org/dataset/b13f08ef-92ee-4446-9b0a-e219f5c25415/resource/20046324-ca41-4a5c-a010-d45ac356015a/download/cmr_admbnda_inc_20180104_shp.zip -o ${OUTPUT_FILE}

unzip ${OUTPUT_FILE} && rm ${OUTPUT_FILE}
mv cmr_admbnda_inc_20180104_SHP data/geo
