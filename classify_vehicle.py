import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# CNN Model to classify vehicles (car, ambulance, etc.)
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(3, activation='softmax')  # Assume 3 classes: 'Car', 'Ambulance', 'Other'
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Training model on a vehicle dataset
def train_model():
    train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory('data/train', target_size=(64, 64), batch_size=32, class_mode='categorical')
    test_set = test_datagen.flow_from_directory('data/test', target_size=(64, 64), batch_size=32, class_mode='categorical')

    model = create_model()
    model.fit(training_set, epochs=10, validation_data=test_set)
    model.save('vehicle_classifier.h5')
