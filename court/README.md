# Court

Court is the directory for all things Judge related. In other words, this is where the evidence (a picture) is sent to and presented to the Judge (a classifier). The Judge makes a verdict and returns that rating back to the caller (the server).

In more detail:

A Judge consists of two things:
1. A classifier trained on the data
2. The feature extractor used to extract the features it was trained on

The first is used for prediction.

The second is required so that given an input string (the book summary) a feature vector can be extracted and used for prediction.