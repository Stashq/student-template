import os
import sys
import tensorflow as tf
from keras import layers, models
from keras.layers import Conv2D, Input, Concatenate, BatchNormalization, MaxPooling2D, Conv2DTranspose, Cropping2D, Add
from keras.models import Model

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "u_net"))
)
from unet_model import unet

CHECKPOINT_PATH_UNET = "./artifacts/models/unet/unet_checkpoint.keras"


def semantic_feature_extractor(input_tensor, dropout_rate):

    # Encoder Path
    c1 = Conv2D(64, (3, 3), padding='same', activation='relu')(input_tensor)
    b1 = BatchNormalization()(c1)
    c2 = Conv2D(64, (3, 3), padding='same', activation='relu')(b1)
    p1 = MaxPooling2D((2, 2), strides=2)(c2)
    
    c3 = Conv2D(128, (3, 3), padding='same', activation='relu')(p1)
    b2 = BatchNormalization()(c3)
    c4 = Conv2D(128, (3, 3), padding='same', activation='relu')(b2)
    p2 = MaxPooling2D((2, 2), strides=2)(c4)
    
    c5 = Conv2D(256, (3, 3), padding='same', activation='relu')(p2)
    c6 = Conv2D(256, (3, 3), padding='same', activation='relu')(c5)
    b3 = BatchNormalization()(c6)
    c7 = Conv2D(256, (3, 3), padding='same', activation='relu')(b3)
    p3 = MaxPooling2D((2, 2), strides=2)(c7)
    
    c8 = Conv2D(512, (3, 3), padding='same', activation='relu')(p3)
    c9 = Conv2D(512, (3, 3), padding='same', activation='relu')(c8)
    b4 = BatchNormalization()(c9)
    c10 = Conv2D(512, (3, 3), padding='same', activation='relu')(b4)
    p4 = MaxPooling2D((2, 2), strides=2)(c10)
    
    c11 = Conv2D(512, (3, 3), padding='same', activation='relu')(p4)
    c12 = Conv2D(512, (3, 3), padding='same', activation='relu')(c11)
    b5 = BatchNormalization()(c12)
    c13 = Conv2D(512, (3, 3), padding='same', activation='relu')(b5)
    p5 = MaxPooling2D((2, 2), strides=2)(c13)
    
    c14 = Conv2D(4096, (3, 3), padding='same', activation='relu')(p5)
    c15 = Conv2D(4096, (1, 1), padding='same', activation='relu')(c14)
    c16 = Conv2D(5, (1, 1), padding='same', activation='relu')(c15)
    
    # Decoder Path
    d1 = Conv2DTranspose(5, (4, 4), strides=(2, 2), padding='same', activation='relu')(c16)
    c17 = Conv2D(5, (1, 1), padding='same', activation='relu')(d1)
    r1 = Cropping2D(cropping=((0, 0), (0, 0)))(c13)
    r1 = Conv2D(5, (1, 1), padding='same', activation='relu')(r1)  # Match channels to 5
    s1 = Add()([r1, c17])
    
    d2 = Conv2DTranspose(5, (4, 4), strides=(2, 2), padding='same', activation='relu')(s1)
    c18 = Conv2D(5, (1, 1), padding='same', activation='relu')(d2)
    r2 = Cropping2D(cropping=((0, 0), (0, 0)))(c10)
    r2 = Conv2D(5, (1, 1), padding='same', activation='relu')(r2)  # Match channels to 5
    s2 = Add()([r2, c18])
    
    d3 = Conv2DTranspose(5, (4, 4), strides=(2, 2), padding='same', activation='relu')(s2)
    d4 = Conv2DTranspose(5, (4, 4), strides=(2, 2), padding='same', activation='relu')(d3)
    d5 = Conv2DTranspose(5, (4, 4), strides=(2, 2), padding='same', activation='relu')(d4)
    r3 = Cropping2D(cropping=((0, 0), (0, 0)))(d5)  # Adjust the cropping values based on dimensions

    # Output
    output = Conv2D(5, (1, 1), padding='same', activation='softmax')(r3)

    return output


def detail_feature_extractor(input_tensor):
    c1 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c1")(input_tensor)
    c2 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c2")(c1)
    c3 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c3")(c2)
    c4 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c4")(c3)
    c5 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c5")(c4)
    c6 = Conv2D(16, (3, 3), activation="relu", padding="same", name="c6")(c5)
    c7 = Conv2D(32, (5, 5), activation="relu", padding="same", name="c7")(c6)
    c8 = Conv2D(32, (5, 5), activation="relu", padding="same", name="c8")(c7)
    c9 = Conv2D(32, (5, 5), activation="relu", padding="same", name="c9")(c8)
    c10 = Conv2D(64, (5, 5), activation="relu", padding="same", name="c10")(c9)
    c11 = Conv2D(64, (5, 5), activation="relu", padding="same", name="c11")(c10)
    c12 = Conv2D(64, (5, 5), activation="relu", padding="same", name="c12")(c11)
    output = Conv2D(5, (1, 1), activation="softmax", name="c13")(c12)

    return output


def fusion_module(y1_output, y2_output):
    f1 = Concatenate(name="concatenate")([y1_output, y2_output])
    c1 = Conv2D(16, (3, 3), activation="relu", padding="same", name="f1")(f1)
    c2 = Conv2D(16, (3, 3), activation="relu", padding="same", name="f2")(c1)
    c3 = Conv2D(32, (3, 3), activation="relu", padding="same", name="f3")(c2)
    c4 = Conv2D(32, (3, 3), activation="relu", padding="same", name="f4")(c3)
    outputs = Conv2D(5, (1, 1), activation="softmax", name="output")(c4)
    return outputs


def build_ynet(img_width, img_height, channel_size, dropout_rate):
    input_shape = (img_width, img_height, channel_size)
    inputs = Input(input_shape)
    
    # Semantic Feature Extractor
    y1_output = semantic_feature_extractor(inputs, dropout_rate)
    
    # Detail Feature Extractor
    y2_output = detail_feature_extractor(inputs)
    outputs = fusion_module(y1_output, y2_output)

    model = Model(inputs, outputs, name="Y-Net")

    model.summary()
    return model


def build_feature_extractor_for_pretraining(img_width, img_height, channel_size, dropout_rate):
    input_shape = (img_width, img_height, channel_size)
    inputs = Input(input_shape)
    
    # Semantic Feature Extractor
    y1_output = semantic_feature_extractor(inputs, dropout_rate)

    model = Model(inputs, y1_output, name="Pretraining_Model")
    model.summary()
    return model

def build_ynet_with_pretrained_semantic_extractor(img_width, img_height, channel_size, dropout_rate, pretrained_weights_path):
    input_shape = (img_width, img_height, channel_size)
    inputs = Input(input_shape)
    
    # Semantic Feature Extractor
    y1_output = semantic_feature_extractor(inputs, dropout_rate)
    
    # Detail Feature Extractor
    y2_output = detail_feature_extractor(inputs)
    
    # Fusion Module
    outputs = fusion_module(y1_output, y2_output)

    # Model definition
    model = Model(inputs, outputs, name="Y-Net")

    # Load pretrained weights
    semantic_extractor_model = build_feature_extractor_for_pretraining(img_width, img_height, channel_size, dropout_rate)
    semantic_extractor_model.load_weights(pretrained_weights_path, by_name=True)
    
    for layer in model.layers:
        if layer.name.startswith('conv') or layer.name.startswith('batch_normalization'):
            layer.set_weights(semantic_extractor_model.get_layer(layer.name).get_weights())

    model.summary()
    return model
