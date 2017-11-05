#!/bin/bash

fuggit="/home/ubuntu/judge-mental/court/"

exiftool -ResolutionUnit=inches /home/ubuntu/judge-mental/court/image.jpg
exiftool -Orientation=1 -n /home/ubuntu/judge-mental/court/image.jpg
convert /home/ubuntu/judge-mental/court/image.jpg -rotate 90 /home/ubuntu/judge-mental/court/image.jpg