# TeCNNis: Predicting Tennis Shot Landings in Real-Time

**Result:** *75%* (1st Class Mark)

The paper introduces a fast NN-based method to predict the landing point of a tennis ball using part of the video frames before the balls lands taken from a single camera angle. The use case requires more emphasis – reading it I am not sure how it benefits a user (but see my point in Evaluation).

*Lit review*: 

overview with citations helps reader to place the work in the current research. Would be worth including in this section a brief overview of  traditional trajectory prediction models such as using Kalman filters, and how your work compares to it. Looking at this from the point of view of someone applying the KF, they could assess the performance of the KF using different number of measurements of the ball – this is similar to using different number of frames in your CNN2. What siutations would your system be suited than the traditional tracking methods?

*Data*: 

some EDA on areas of the court where ball is hit and lands. Expect predictions to be poor in areas of the court with few data points.

*Methodology*: 

Varied experiments on training stratgies and comparisons to fine-tuned models. In the system, nine consecutive frames were used by CNN2 to predict the landing point. Some sensitvity analysis of the results for low/medium/high # frames repoted along with latency would give us an understanding of the trade-off of # frames, latency, and accuracy.

The methodology may be improved by considering a simpler classification problem: partition the court in blocks and predict landing block. Initially the blocks can be made to be big, and gradually reduce the size of the blocks which makes the problem beomce closer and closer to your regression problem. Or try a hierachical approach that has been used in image geolocation:  First predict the region of the court (classifcation) the ball will land, followed by the prediction (regression) of the landing point. Compare the accuracy vs latency against the  results of the paper.

*Evaluation*: 

For this application MSE and latency may be augmented with accuracy of in vs out predictions as this seems to the the most important for betting real time.

*Slides*: 

well-structure and suits a general audience

*Code*: 

full marks for this part.
