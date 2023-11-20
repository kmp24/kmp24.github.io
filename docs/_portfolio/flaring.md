---
title: "Automate Gas Flaring to Predict Oil Production"
excerpt: "Use VIIRS nighttime observations to detect thermal anomalies and refine the data for analysis"

sidebar:
  - title: "Role"
    text: "Geospatial Data Scientist/Engineer"
  - title: "Responsibilities"
    text: "Use VIIRS nighttime observations to detect thermal anomalies and refine the data for analysis"
---

For this project, we had an NGO client that wanted to be able to detect misreported oil production values in an area of interest to them using freely available satellite data with a methdology that could be reproduced. I developed a process to do this based on existing literature (primarily by Christopher Elvidge, Mikhail Zhizhin, and others). The process involved accessing over 10 years of VIIRS nighttime SDR swath data, downloading and processing the HDF files using xarray/pandas (as the SDR product was not streamable at the time of this project) via the LAADS DAAC. For the transformation portion of the processing pipeline, the following was required:

* Selecting thermal anomalies based the M10 band and storing the raw radiances and metadata for downstream analysis
* Estimating the hotspot temperature using Planck curve fitting across several infrared bands.
* After concatenating all of the flare data with temperatures exceeding 1500K, the DBSCAN clustering algorithm was used to validate flaring locations and aid in the removal of outliers with great accuracy.
* The final data was used to create a regression model, utilizing externally reported data. The model achieved high accuracy and was presented to the client for use in their decision-making.
