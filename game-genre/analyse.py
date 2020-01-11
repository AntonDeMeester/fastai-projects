from fastai.vision import cnn_learner, models
from fastai.metrics import error_rate

from preprocess import preprocess_csv


if __name__ == "__main__":
    data = preprocess_csv()
    learner = cnn_learner(data, models.resnet34, metrics=error_rate)
    learner.fit(100)
    print(learner.save("100-epochs", return_path=True))
    # interpretation = ClassificationInterpretation.from_learner(learner)

