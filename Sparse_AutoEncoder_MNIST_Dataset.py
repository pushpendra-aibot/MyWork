# -*- coding: utf-8 -*-
"""Ques_1_Assignment_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qQdoBss2TkknjPt5A8apAdrRPGOXQdoP

### Implement Sparse AutoEncoder on Digit MNIST dataset
"""

#imorting libraries
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras import layers
from keras import regularizers

#Loading the data from mnist 
(X_train, y_train), (X_test, y_test) = mnist.load_data()

#Normalizing data and transforming the data
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
X_train = X_train.reshape((len(X_train), np.prod(X_train.shape[1:])))
X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))

# Printing the shape of data
print(f'Training data shape: {X_train.shape}')
print(f'Test data shape: {X_test.shape}')

#Dimension size for encoding 
Dim_enc = 32  

input_image = keras.Input(shape=(784,))

#Using L1 regularizer to encode
encoded_layer = layers.Dense(Dim_enc, activation='relu', activity_regularizer=regularizers.l1(10e-5))(input_image)
decoded_layer = layers.Dense(784, activation='sigmoid')(encoded_layer)

#Completing the AutoEncoder 
AutoEncoder = keras.Model(input_image, decoded_layer)

encoder = keras.Model(input_image, encoded_layer)

encodedInput = keras.Input(shape=(Dim_enc,))
# Retrieve the last layer of the AE model
decodedLayer = AutoEncoder.layers[-1]
# Creating the decoder model from decoded layer
decoder = keras.Model(encodedInput, decodedLayer(encodedInput))

AutoEncoder.compile(optimizer='adam', loss='binary_crossentropy')

##Training the model
AutoEncoder.fit(X_train, X_train, epochs=100, batch_size=512, shuffle=True, validation_data=(X_test, X_test))
encoded_images = encoder.predict(X_test)
decoded_images = decoder.predict(encoded_images)

n = 5
#Visualizing the images
plt.figure(figsize=(20, 4))
for i in range(n):
    print('Actual Image')
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()
    print('Re-constructed Images')
#Reconstructed Image
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_images[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()

## Saving the model
AutoEncoder.save('/content/drive/MyDrive/ML-2_Assignments/Assignment-3/Ques_1/AutoEncoder.pth')

"""#### Testing with Kmeans and *BatchKMeans*"""

# Length Unique Labels available in Test set
labels = len(np.unique(y_test))
print(labels)

#Training the MiniBatchKmeans
kmeans = MiniBatchKMeans(n_clusters = labels)

kmeans.fit(X_train)
kmeans.labels_

def ClusterLabelsInfer(kmeans, actual_labels):
  inferred_labels = {}

  for i in range(kmeans.n_clusters):
      labels = []
      index = np.where(kmeans.labels_ == i)
      labels.append(actual_labels[index])

      if len(labels[0]) == 1:
          counts = np.bincount(labels[0])
      else:
          counts = np.bincount(np.squeeze(labels))
      if np.argmax(counts) in inferred_labels:

          inferred_labels[np.argmax(counts)].append(i)
      else:

          inferred_labels[np.argmax(counts)] = [i]

  return inferred_labels

def DataLabelsInfer(X_labels, ClusterLabels):

  predicted_labels = np.zeros(len(X_labels)).astype(np.uint8)

  for i, cluster in enumerate(X_labels):
      for key, value in ClusterLabels.items():
          if cluster in value:
              predicted_labels[i] = key
              
  return predicted_labels

#Training MiniBatch Kmeans
ClusterLabels = ClusterLabelsInfer(kmeans, y_train)
xClusters = kmeans.predict(X_train)
predicted_labels = DataLabelsInfer(xClusters, ClusterLabels)
print(predicted_labels[:20])
print(y_train[:20])

kmeans = MiniBatchKMeans(n_clusters = 20)
kmeans.fit(X_train)

centroids = kmeans.cluster_centers_

# reshape centroids into images
images = centroids.reshape(20, 28, 28)
images *= 255
images = images.astype(np.uint8)

# determine cluster labels
ClusterLabels = ClusterLabelsInfer(kmeans, y_train)

#Plotting the images
fig, axs = plt.subplots(4, 5, figsize = (20, 20))
plt.gray()

for i, ax in enumerate(axs.flat):
  
    for key, value in ClusterLabels.items():
        if i in value:
            ax.set_title('Inferred Label: {}'.format(key))
    
    # add image to subplot
    ax.matshow(images[i])
    ax.axis('off')

fig.show()

from sklearn.metrics import accuracy_score
print(f'Accuracy: {round(accuracy_score(y_train, predicted_labels)*100,2)}')

#Saving the model 
import pickle
pickle.dump(kmeans, open("/content/drive/MyDrive/ML-2_Assignments/Assignment-3/Ques_1/Kmeans_model.pkl", "wb"))

