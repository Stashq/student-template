import numpy as np
import tensorflow as tf

num_classes = 5


def pixel_accuracy(y_true, y_pred):
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)
    correct_pixels = tf.reduce_sum(
        tf.cast(tf.equal(y_true, y_pred), tf.float32)
    )
    total_pixels = tf.size(y_true, out_type=tf.float32)
    return correct_pixels / total_pixels


def mean_iou(y_true, y_pred, num_classes=num_classes):
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)

    iou = []
    for i in range(num_classes):
        intersection = tf.reduce_sum(
            tf.cast((y_pred == i) & (y_true == i), tf.float32)
        )
        union = tf.reduce_sum(
            tf.cast((y_pred == i) | (y_true == i), tf.float32)
        )
        iou.append(intersection / (union + tf.keras.backend.epsilon()))
    return tf.reduce_mean(iou)


def dice_coefficient(y_true, y_pred, smooth=1e-6):
    y_true_f = tf.reshape(y_true, [-1])
    y_pred_f = tf.reshape(y_pred, [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    return (2.0 * intersection + smooth) / (
        tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth
    )


def precision(y_true, y_pred, num_classes=num_classes):
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)

    precisions = []
    for i in range(num_classes):
        true_positives = tf.reduce_sum(
            tf.cast((y_pred == i) & (y_true == i), tf.float32)
        )
        predicted_positives = tf.reduce_sum(tf.cast(y_pred == i, tf.float32))
        precisions.append(
            true_positives / (predicted_positives + tf.keras.backend.epsilon())
        )
    return tf.reduce_mean(precisions)


def recall(y_true, y_pred, num_classes=num_classes):
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)

    recalls = []
    for i in range(num_classes):
        true_positives = tf.reduce_sum(
            tf.cast((y_pred == i) & (y_true == i), tf.float32)
        )
        actual_positives = tf.reduce_sum(tf.cast(y_true == i, tf.float32))
        recalls.append(
            true_positives / (actual_positives + tf.keras.backend.epsilon())
        )
    return tf.reduce_mean(recalls)


def f1_score(y_true, y_pred, num_classes=num_classes):
    prec = precision(y_true, y_pred, num_classes)
    rec = recall(y_true, y_pred, num_classes)
    return 2 * (prec * rec) / (prec + rec + tf.keras.backend.epsilon())