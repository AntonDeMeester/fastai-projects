from fastai.vision import cnn_learner, models, ClassificationInterpretation
from fastai.metrics import error_rate, accuracy_thresh, fbeta, partial

from preprocess import preprocess_csv


if __name__ == "__main__":
    data = preprocess_csv()
    metrics = [
        partial(accuracy_thresh, thresh=i/10)
        for i in range(1,11)
    ]
    learner = cnn_learner(
        data,
        models.resnet34,
        metrics=metrics
    )
    learner.fit_one_cycle(20)
    # learner.fit(100)
    # print(learner.save("100-epochs", return_path=True))
    # interpretation = ClassificationInterpretation.from_learner(learner)
