import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

mnist = tf.keras.datasets.mnist  # 28x28 images of hand written digits 0-9

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
# print(x_train[0])

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))  # relu similar to sigmoid
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
model.compile(optimizer='adam',  # adam or stochastic
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=3)

val_loss, val_acc = model.evaluate(x_test, y_test)

print("Total Loss vs Accuracy")
print(val_loss, "vs", val_acc)

# model.save('num_reader.model')  # if you want to save the model
# new_model = tf.keras.models.load_model('num_reader.model')
predictions = model.predict([x_test])

print("predictions matrix")
print(predictions)
print("Predicted to be a (check the image if I guessed correctly): ", np.argmax(predictions[5]))

plt.imshow(x_test[1])  # , cmap=plt.cm.binary for black and white
plt.show()
