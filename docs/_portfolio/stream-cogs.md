---
title: "Stream COGs and save processed data"
excerpt: "Use Cloud Optimized Geotiffs to perform analysis in the cloud"
sidebar:
  - title: "Role"
    url: "https://nbviewer.jupyter.org/github/kmp24/kmp24.github.io/blob/master/assets/docs/DownloadNAIP.ipynb"
    btn_label: "Read More"
    btn_class: "btn--primary"
    text: "Geospatial Analyst"
  - title: "Responsibilities"
    text: "Use Cloud Optimized Geotiffs to perform analysis in the cloud"
---


Our team regularly needed to download NAIP data from a variety of years/states. I wrote this code when I had a project where I needed the data for the entire state of CA and just needed NDVI. We had very limited storage space at the time, so I needed a way to either download, process, and delete the original file, or come up with some other way. I found the data I needed was available on an Azure blob, and wrote this code to retrieve the NDVI, MSAVI, or whatever analysis we needed without downloading the file and taking up physical server space (before we transitioned completely to the cloud).

> ![Image Alt Text](/assets/images/ndvi.PNG)

<iframe src="https://nbviewer.org/github/kmp24/kmp24.github.io/blob/master/docs/assets/NAIP_COGS_NDVI.ipynb" width="800" height="600"></iframe>