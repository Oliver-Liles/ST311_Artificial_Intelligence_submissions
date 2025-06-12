This was on an individual project.

### Feedback:

50537

CONTENT

Data: describe the data and explain why you didn’t use the full 60k training set, and 10k validation set.

Baseline: a benchmark model is required for comparative purposes. It looks like `model` is your natural baseline model, but you didn’t say so.

Overfitting: the baseline model may be used to show there is overfitting, and then you may apply regularisation methods, thus allowing you to see the effectiveness or otherwise of regularisation.

Shallow model:  The width – the key hyperparameter of this architecture- needs to be determined by tuning.

REPORT

As there are a lot of experimentation and plots, bring some of the plots together and report.

Conclusion: the performance are about the same. Why? The image data is simple: no distortions, just a single object in the image and centred. So one would expect both shallow and deep FFN to do well if reasonably tuned and trained.

More reading of ML papers (which you will do for the project) will improve your writing up of ML papers. 

# To improve:

- Add grid or random search for model architecture
- Write up in ML paper (e.g., NeurIPS format)
- Add distortions? (e.g., rotations)
- ...
