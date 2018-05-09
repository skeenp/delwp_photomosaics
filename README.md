DELWP Photo Mosaics
===========

The Department of Environment, Land, Water and Planning provide free access to a number of historic images circa 1946 (approx) via their online site at  http://services.land.vic.gov.au/maps/photomaps.jsp. Images from the service are provided as jpg without any georeferenced information. This project aims to provide georeferencing information where available.

At a minimum, the entire image will be referenced to fit within the boundary of its tile. This will not include removing any borders within the image. Bounding boxes can be defined through arguements in the python script. Using bounding boxes, borders can be removed from the images. Some boundary boxes come populated, however these are largely within the west of the state. Contributes to the bounding box definitions are a welcome to the project.

# Metadata
The 'meta' folder contains a world file for a selection of tiles in the dataset, split up into zones as per the index. There is also an index geojson file for all possible tiles in the dataset.

## index.geojson
The index.geojson file describes the extent of each possible image tiles available from the photo mosaic server. The index is derived from standard grid system described at http://services.land.vic.gov.au/maps/imf/search/PhotoMapInformation.jsp, along with tile references for the dataset (below).

![](index.jpeg)

The dataset contains tiles including:
  - zone > Zone ID
  - sheet > Mapsheet (1:63,360)
  - des1 > Mapsheet designation 1  (1:31,680)
  - des2 > Mapsheet designation 2 (1:15,840)
  - des3 > Mapsheet designation 3 (1:7,920)
  - grid id > Mapsheet full reference (sheet as well as designations)

## World File (.jpw)
Each tile will be referenced by its upper left pixel and resolution, as per the ![https://en.wikipedia.org/wiki/World_file](world file standard). Consideration is given to any borders around images, and images are shifted to take this into account. All world files are provided in WGS84 EPSG:4326

# process.py
The process.py python script will allow you to generate the worldfile for one of the DELWP photomap tiles. To use it you must have python and cv2 (python module) installed. The cv2 module can be installed by calling:

''' pip install opencv-python '''

Once installed, the script should work, with the following arguements:

'''usage: process.py [-h] [--bbox x x x x] image path zone gridid

Applies georeference information to delwp historic photomosaic images

positional arguments:
  image path      path to photomosaic jpg
  zone            tile zone
  gridid          grid identifier

optional arguments:
  -h, --help      show this help message and exit
  --bbox x x x x  bounding box of photo in image (xmin, ymin, xmax, ymax in
                  image units)note: bypasses existing bbox values (where
                  available)'''

An example use case is as follows:

''' python process.py meta\zone6\0855A1.jpg 6 855A1 --bbox 132 70 6184 3573 '''

The python script exports a world file in the same location as the referenced image.

## To Do
Provide GDAL VRT files to clip datasets on the fly and manage projection information.
