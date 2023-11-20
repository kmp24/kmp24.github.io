---
title: "Retrieve post-fire Landsat 8 imagery via S3"
excerpt: "Retrieve post-fire Landsat 8 imagery for model production"

sidebar:
  - title: "Role"
    text: "Geospatial Analyst"
  - title: "Responsibilities"
    text: "Retrieve post-fire Landsat 8 imagery for model production"
---

A crucial part of our yearly model production process was to download leaf-on Landsat 8 imagery with low cloud cover. We also needed the images to be post-wildfire - we needed the imagery to include all major wildfire events for the previous year. Our existing process was an internally designed software to fetch Landsat imagery between specified dates and land cloud cover percent, but it could not do the major task of screening by the last wildfire event in that Path/Row. My code solved this problem while drastically speeding up the download process by utilizing an existing S3 bucket. My code:

* Gathers national fire perimiter data and joins it to a Landsat WRS shapefile to retrieve the path/row information and most recent fire date for that tile
* Uses the metadata csv from s3 to get a list of all scenes
* filters by date of last fire for each tile, and updates the appropriate imagery daterange search
* Also adds additional tries for when the cloud cover parameters are not met

> ![Image Alt Text](/assets/images/l8scene.PNG)

<iframe src="https://nbviewer.org/github/kmp24/kmp24.github.io/blob/master/docs/assets/Download_L8Imagery_Post_Fire.ipynb" width="800" height="600"></iframe>