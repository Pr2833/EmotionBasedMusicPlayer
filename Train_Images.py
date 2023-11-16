from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
import pandas  as pd
import numpy as np
import os
import scipy

data_dir = "C:/Users/chenn/OneDrive/Desktop/MUSIC_PLAYER/data"

train_data = ImageDataGenerator(rescale=1./255)
validation_data = ImageDataGenerator(rescale=1./255)

train_generator = train_data.flow_from_directory(
    os.path.join(data_dir,'train'),
    target_size=(48,48),
    batch_size=64,
    color_mode="grayscale",
    class_mode="categorical",
)

validation_generator = validation_data.flow_from_directory(
    os.path.join(data_dir,'test'),
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode="categorical",
)

emotion_model = Sequential()

emotion_model.add(Conv2D(32,kernel_size=(3,3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2,2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))

emotion_model.add(Dense(6, activation='softmax'))

emotion_model.compile(loss='categorical_crossentropy',metrics=['accuracy'])

emotion_model_info = emotion_model.fit(
    train_generator,
    steps_per_epoch= 26709//64,

    epochs=50,
    validation_data= validation_generator,
    validation_steps=6578//64
)

model_json = emotion_model.to_json()
with open('emotion_model.json','w') as json_file:
    json_file.write(model_json)

emotion_model.save_weights('emotion_model.h5')