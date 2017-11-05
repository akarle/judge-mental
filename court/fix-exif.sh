#!/bin/bash

fuggit="/home/ubuntu/judge-mental/court/"

exiftool -ResolutionUnit=inches /home/ubuntu/judge-mental/court/image-original.jpg
exiftool -Orientation=1 -n /home/ubuntu/judge-mental/court/image-original.jpg
convert /home/ubuntu/judge-mental/court/image-original.jpg -rotate 90 /home/ubuntu/judge-mental/court/image-original.jpg