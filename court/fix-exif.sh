#!/bin/bash

exiftool -ResolutionUnit=inches image.jpg
exiftool -Orientation=1 -n image.jpg
convert image.jpg -rotate 90 image.jpg