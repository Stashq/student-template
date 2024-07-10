import os
import sys
import keras.metrics
from keras.models import load_model
import wandb
from loss_functions import combined_loss

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from custom_callbacks import dice_score, specificity_score
from data_loader import create_testdataset_for_segnet_training
from processing import add_prediction_to_list, safe_predictions_locally

os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"

TEST_IMG_PATH = "data/training_test/images_mixed"
TEST_MASK_PATH = "data/training_test/labels_mixed"
CHECKPOINT_PATH = "artifacts/models/deeplab/deeplab_checkpoint.h5"
PRED_IMG_PATH = "artifacts/models/deeplab/pred"

IMG_WIDTH = 512
IMG_HEIGHT = 512
IMG_CHANNEL = 3

BATCH_SIZE = 4
APPLY_CRF = True

test_dataset, test_images, test_masks = create_testdataset_for_segnet_training(
    directory_test_images=TEST_IMG_PATH,
    directory_test_masks=TEST_MASK_PATH,
    img_width=IMG_WIDTH,
    img_height=IMG_HEIGHT,
    batch_size=BATCH_SIZE,
)

model = load_model(CHECKPOINT_PATH, compile=False)
model.compile(
    optimizer="adam",
    loss=combined_loss,
    metrics=[
        "accuracy",
        keras.metrics.BinaryIoU(),
        keras.metrics.Precision(),
        keras.metrics.Recall(),
        specificity_score,
        dice_score,
    ],
)

predictions, binary_predictions = add_prediction_to_list(
    test_dataset, model=model, batch_size=BATCH_SIZE, apply_crf=APPLY_CRF
)

safe_predictions_locally(
    range=range(20),
    iterator=None,
    test_images=test_images,
    predictions=binary_predictions,
    test_masks=test_masks,
    pred_img_path=PRED_IMG_PATH,
    val=False,
)

os.environ["WANDB_DIR"] = "wandb/test_deeplab"

wandb.init(
    project="deeplab",
    entity="fabio-renn",
    name="test-deeplab",
    mode="offline",
    config={"metric": "accuracy"},
    dir=os.environ["WANDB_DIR"],
)

test_results = model.evaluate(test_images, test_masks, return_dict=True)
print(test_results)
wandb.log(test_results)
wandb.finish()
