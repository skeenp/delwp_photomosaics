"""Processes delwp photomosaic images, adding georeferencing information"""
import argparse
import cv2
import grid_reference as grid

#Setup arg parser
ARG_PARSER = argparse.ArgumentParser(
    description='Applies georeference information to delwp historic photomosaic images')
ARG_PARSER.add_argument(
    'file', metavar='image path', help='path to photomosaic jpg')
ARG_PARSER.add_argument(
    'zone', metavar='zone', help='tile zone')
ARG_PARSER.add_argument(
    'gridid', metavar='gridid', help='grid identifier')
ARG_PARSER.add_argument(
    '--bbox', metavar='x', type=int, nargs=4,
    help='bounding box of photo in image (xmin, ymin, xmax, ymax in image units)'\
    'note: bypasses existing bbox values (where available)')
ARGS = ARG_PARSER.parse_args()

def process(file_path, zone, grid_id, bbox):
    """processes data parsed from args"""
    grid_dim = len(grid_id)-2
    img = cv2.imread(file_path)
    height, width, channels = img.shape

    #Get grid reference
    grid_ref = grid.ref['z{0}'.format(zone)]['r{0}'.format(grid_id)]

    #Check if bounding box exists in reference
    if not grid_ref['bbox'] is None:
        #Set bbox
        bbox = grid_ref['bbox']

    #Check if bounding box exists in cmd line
    if not bbox is None:
        #Build width and height
        width = int(bbox[2]) - int(bbox[0])
        height = int(bbox[3]) - int(bbox[1])

    #Process resolutions of image
    if grid_dim == 1:
        x_res = 0.5/width
        y_res = 0.25/height
    elif grid_dim == 2:
        x_res = 0.25/width
        y_res = 0.125/height
    elif grid_dim == 3:
        x_res = 0.125/width
        y_res = 0.0625/height
    elif grid_dim == 4:
        x_res = 0.0625/width
        y_res = 0.03125/height
    else:
        raise BaseException("cannot parse resolution, grid sheets or designations")

    #Setup offset where bbox exists
    if bbox is None:
        x_offset = 0
        y_offset = 0
    else:
        x_offset = int(bbox[0])
        y_offset = int(bbox[1])

    #Get image x and y ref
    x_ref = grid_ref["x"]-(x_offset * x_res)-(0.5*x_res)
    y_ref = grid_ref["y"]+(y_offset * y_res)+(0.5*y_res)

    #Write world file
    with open(file_path.replace('.jpg', '.jpw'), 'w') as wld_file:
        wld_file.write('{0}\n0\n0\n{1}\n{2}\n{3}'.format(x_res, -y_res, x_ref, y_ref))

#Run process
process(ARGS.file, ARGS.zone, ARGS.gridid, ARGS.bbox)
