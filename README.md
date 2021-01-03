# Introduction

Generative Adversarial Networks (GAN) and Variational Auto Encoders (VAE) are generative models
that use unsupervised learning approach. GAN consists of a discriminator and a generator that can
create new data that will look similar to the training dataset. For example, if the training dataset
contains human faces then GAN will generate images of human faces. Similarly, VAE also a
generative model, contains an encoder and a decoder. The aim of the autoencoder is to regularize
the encodings so that its latent space has good properties to generate new data. These models are
tuned as generative models because they learn the data distribution from the training dataset and can
generate new data that looks similar to the training set. The paper makes use of MNIST(Modified
National Institute of Standards and Technology) dataset for training these two models. The dataset is
a computer vision dataset composed of handwritten digits where each image is a 28*28 pixel image.

Note: For details read Readme.pdf 
