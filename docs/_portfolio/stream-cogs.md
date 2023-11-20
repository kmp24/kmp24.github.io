---
title: "Stream COGs and save processed data"
excerpt: "Use Cloud Optimized Geotiffs to perform analysis in the cloud"
header:
  teaser: /assets/images/ndvi.jpg
sidebar:
  - title: "Role"
    text: "Geospatial Analyst, Verisk"
  - title: "Responsibilities"
    text: "Use Cloud Optimized Geotiffs to perform analysis in the cloud"
---


Our team regularly needed to download NAIP data from a variety of years/states. I wrote this code when I had a project where I needed data for the entire state of CA, and just wanted to do my analysis using NDVI. We had very limited storage space at the time, so I needed a way to either download, process, and delete the original file, or come up with another way. I found the data I needed was available on an Azure blob, and wrote this code to retrieve the NDVI/MSAVI/etc and saving as a jp2 instead of downloading the original data.

> ![Image Alt Text](/assets/images/ndvi.PNG)

<iframe src="https://nbviewer.org/github/kmp24/kmp24.github.io/blob/master/docs/assets/NAIP_COGS_NDVI.ipynb" width="800" height="600"></iframe>