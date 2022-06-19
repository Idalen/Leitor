# Leitor

## Collaborators
* [Daniel Martins Vieira](https://github.com/Idalen) (11215719)
* [Guilherme Alves Lindo](https://github.com/Guial07) (8504480)
* [Jayro Boy Neto](https://github.com/jayroboy) (9762880)
* [Marcus Vinícius Santos](https://github.com/marcus_v_rodrigues) (11218862)

---

## Abstract

Leitor project has the main goal of converting images of texts into machine-encoded text. In other words, the program will extract the text from an image which contains it written or printed and will turn it into a string of characters.

At first, for the sake of simplicity, the project scope will only cover images of white background pages containing printed text. These images are taken from screenshots of websites or photographies of books. These images may have noise, blur and uncontrolled lighting conditions.

This objective must be achieved using digital image processing techniques.

---

## Inputs

Here are some few scaled down example images that will have their embedded text extracted.

* Scanned Text Snippet<br>
<img title="Scanned Text Snippet from Geometria analítica - um tratamento vetorial" alt="Text Snippet" src="data/other_images/boulos-snippet.png" width="600" height="300">

* Website Screenshot<br>
<img title="Website Screenshot" alt="Website print" src="data/print_only_images/images/31.JPG"
width="600" height="200">
<img title="Website Screenshot" alt="Website print" src="data/print_only_images/images/1.JPG"
width="600" height="200">

* Book Page Photo <br>
<img title="Book Page Photo" alt="Book Page Photo" src="data/photo_only_images/7.jpg" width="600" height="300">
<img title="Book Page Photo" alt="Book Page Photo" src="data/photo_only_images/2.jpg" width="600" height="300">

All images below were taken by the members of the project with a cellphone camera or taking screenshots from webpages on the internet.



---

## Methods

The project will apply the following techniques in order to achieve its objective:

### Grayscaling

Once the text is generally not affected by color, the images are converted into grayscale in order to manipulate them easier.

### Gaussian Blur

A small gaussian blur is applied to smooth out the image and thus reduce the noise in it. With the image smoothed out, treshould approaches can perform better.

### Gaussian Adaptative Treshoulsing

Now our goal is to find areas with text, i.e. text blocks of the image. To make text block detection easier we will invert and maximize the colors of our image, that will be achieved via thresholding. So now text becomes white and background is black. Gaussian adaptative tresholding is used in this due it better performances in images with noise and uncontrolled lighting.

In order to reduce noise and detect transistions, some sort of enhancement and filtering image processing technique will be used.

### Image Segmentation

For text extraction from image and then separate each character from the text, the project may use some kind of segmentation techniques.

### Pattern Matching

The project will use some kind of pattern recognition technique to identify the characters extracted in segmentation step.
For this task, image correlation, feature extraction and machine learning algorithms may be used.

---

## Data

The data used in this project was found on kaggle:
* [Text images](https://www.kaggle.com/datasets/volkandl/optical-character-recognition-ocr-texts)
* [Characters Images](https://www.kaggle.com/datasets/preatcher/standard-ocr-dataset)

---
