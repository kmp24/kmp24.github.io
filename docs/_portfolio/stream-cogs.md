---
title: "Stream COGs and perform analysis"
excerpt: "Use Cloud Optimized Geotiffs to perform analysis in the cloud"
header:
  image: /assets/images/unsplash-gallery-image-1.jpg
  teaser: assets/images/unsplash-gallery-image-1-th.jpg
sidebar:
  - title: "Role"
    image_path: docs/assets/images/ndvi.PNG
    image_alt: "NDVI"
    url: "https://nbviewer.jupyter.org/github/kmp24/kmp24.github.io/blob/master/assets/docs/NAIP_COGs.ipynb"
    btn_label: "Read More"
    btn_class: "btn--primary"
    text: "Geospatial Analyst"
  - title: "Responsibilities"
    text: "Write some code that streams cogs via Azure blob, get ndvi, and save the reclassified data"
---

Our team regularly needed to download NAIP data from a variety of years/states. I wrote this code when I had a project where I needed the data for the entire state of CA and just needed NDVI. We had very limited storage space at the time, so I needed a way to either download, process, and delete the original file, or come up with some other way. I found the data I needed was available on an Azure blob, and wrote this code to retrieve the NDVI without downloading the file.