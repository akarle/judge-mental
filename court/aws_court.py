from court import go_to_court
import sys

go_to_court('/home/ubuntu/judge-mental/court',
            '/usr/bin/tesseract', sys.argv[1])
