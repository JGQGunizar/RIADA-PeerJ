# RIADA

RIADA: a machine-learning based infrastructure for recognising the emotions of Spotify songs

## ML_models: Contains all the process for building the models for mood prediction.

      Datasets:
            fSP_lSP.csv : Contains the Spotify id of the songs and the label generated from the playlistminer
            fSP_lAB.csv : Contains the Spotify id of the songs and the label obtained from AcusticBrainz
            Datasets_creation: Scripts used for the creation of the datasets described before
                  Read_SP.py: Script for the creation of the fSP_lSP.csv, extraction of audio features and label addition
                  Read_AB.py: Script for the creation of the fSP_lAB.csv, extraction of audio features and label addition
                  playlistminer/crawl.py: Script for downloading the Spotify song's id using keyword search
                  playlistminer/proc.py: Script for processing the metrics of the songs crawled
      
      Models:
            features*: Binary files with the features used in each model
            model*: Binary files with the model for each emotion
      
      Building_models:
            SS_GE_4 : Feature selection and training models from fSP_lSP dataset
            Cross_validation_1v3: Validation of the models against AcousticBrainz dataset
            Tools : Defined methods to work with the models

## Riada_sample/riada_ex.csv: Example of RiadaDB with 100.000 records

#Template.ini: Template for config parameters
