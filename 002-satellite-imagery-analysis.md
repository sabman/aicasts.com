## 002-satellite-imagery-analysis.md

- [x] https://youtu.be/RM3QGyu4Fpg?t=683 Serverless for satellite imagery
- [ ] https://www.youtube.com/watch?v=DjP24I_WKWw Understanding the Earth: ML With Kubeflow Pipelines (Cloud Next '19)
- [ ] https://xview2.org/
- [ ] https://www.kaggle.com/kmader/segmenting-buildings-in-satellite-images
- [ ] https://appsilon.com/satellite-imagery-generation-with-gans/
- [ ] https://github.com/robmarkcole/satellite-image-deep-learning
- [ ] Datasets https://github.com/chrieke/awesome-satellite-imagery-datasets
- [ ] https://github.com/dronedeploy/dd-ml-segmentation-benchmark

# wine plantations satellite imagery

https://github.com/westnordost/StreetComplete/issues/368
https://books.google.de/books?id=cP5azjPgdIQC&pg=PA244&lpg=PA244&dq=wine+plantations+satellite+imagery&source=bl&ots=FfWkRu8Vnn&sig=ACfU3U1esTbBE3uaXiHO_YVyOhPUXgq1dg&hl=en&sa=X&ved=2ahUKEwjv-uP0mJvpAhUSC-wKHWSEBAMQ6AEwEHoECAkQAQ#v=onepage&q=wine%20plantations%20satellite%20imagerywine&f=false

https://www.researchgate.net/publication/28231298_Vineyard_area_estimation_using_medium_spatial_resolution_satellite_imagery

# GANS for satellite imagery

https://appsilon.com/satellite-imagery-generation-with-gans/

```r
image_height <- 80 # Image height in pixels
image_width <- 80 # Image width in pixels
image_channels <- 3 # Number of color channels - here Red, Green and Blue
noise_dim <- 80 # Length of gaussian noise vector for generator input

# Setting generator input as gaussian noise vector
generator_input <- layer_input(shape = c(noise_shape))

# Setting generator output - 1d vector will be reshaped into an image array
generator_output <- generator_input %>%
  layer_dense(units = 64 * image_height / 4 * image_width / 4) %>%
  layer_activation_leaky_relu() %>%
  layer_reshape(target_shape = c(image_height / 4, image_width / 4, 64)) %>%
  layer_conv_2d(filters = 128, kernel_size = 5, padding = "same") %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d_transpose(filters = 128, kernel_size = 4, strides = 2, padding = "same") %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d_transpose(filters = 256, kernel_size = 4, strides = 2, padding = "same") %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 256, kernel_size = 5, padding = "same") %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 256, kernel_size = 5, padding = "same") %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = image_channels, kernel_size = 7, activation = "tanh", padding = "same")

# Setting up the model
generator <- keras_model(generator_input, generator_output)

```

```r
# Setting discriminator input as an image array
discriminator_input <- layer_input(shape = c(image_height, image_width, image_channels))

# Setting discriminator output - the probability that image is real or not
discriminator_output <- discriminator_input %>%
  layer_conv_2d(filters = 256, kernel_size = 4) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 256, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 128, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 128, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 128, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 128, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_conv_2d(filters = 128, kernel_size = 2, strides = 2) %>%
  layer_activation_leaky_relu() %>%
  layer_flatten() %>%
  layer_dropout(rate = 0.3) %>%
  layer_dense(units = 1, activation = "sigmoid")

# Setting up the model
discriminator <- keras_model(discriminator_input, discriminator_output)
```

define loss function

```r
discriminator %>% compile(
  optimizer = optimizer_rmsprop(
    lr = 0.0006,
    clipvalue = 1.0,
    decay = 1e-7
  ),
  loss = "binary_crossentropy"
)
```

```r
freeze_weights(discriminator)
gan_input <- layer_input(shape = c(noise_shape))
gan_output <- discriminator(generator(gan_input))
gan <- keras_model(gan_input, gan_output) gan %>% compile(
  optimizer = optimizer_rmsprop(
    lr = 0.0003,
    clipvalue = 1.0,
    decay = 1e-7
  ),
  loss = "binary_crossentropy"
)

# Training the GAN doesn't follow the simplicity as we could experience while working with Convolutional Networks. In simplification, we have to train both networks separately in a loop.
for(i in 1:1000) {
  # TRAIN THE DISCRIMINATOR
  # TRAIN THE GAN
 # You can find full code of the training process for similar example in https://www.manning.com/books/deep-learning-with-r
}
```
