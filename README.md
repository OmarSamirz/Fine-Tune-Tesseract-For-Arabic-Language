# Fine-Tuning an Arabic OCR Model using Tesseract 5

## Table of Contents

* [Introduction](#introduction)
* [Key Areas of Focus](#Key-fareas-of-focus)
* [Methodology](#methodology)
  * [Data Collection and Preprocessing](#data-collection-and-preprocessing)
  * [Dataset Composition](#dataset-composition)
  * [Image Generation](#image-generation)
* [Data Augmentation](#data-augmentation)
* [About Tesseract OCR](#about-tesseract-ocr)
* [Training](#training)
* [Evaluation](#evaluation)
* [Results](#results)

## Introduction
Optical Character Recognition (OCR) is essential for digital processing and preservation of textual information. Despite advancements in OCR for various languages, Arabic OCR remains challenging due to its complex script. This project aims to fine-tune an Arabic OCR system using **Tesseract 5.0**, achieving high accuracy in text recognition.

## Key Areas of Focus
* [Data Collection and Preprocessing]
* [Dataset Composition]
* [Image Generation]
* [Training and Evaluation]
* [Challenges and Limitations]

## Methodology

### Data Collection and Preprocessing


### Dataset Composition
Our dataset included 1 million Arabic sentences, split into:
* [60% tashkeel-free sentences]
* [40% tashkeel-included sentences]

This balance helps the OCR model handle both scenarios effectively.

### Image Generation
Using the **Text Recognition Data Generator (TRDG)** library, we created images from Arabic text, ensuring diversity with three distinct **Arabic fonts**: `Baghdad`, `Bahij`, and `Rakkas`. Images were generated in `.tif` format with corresponding ground truth text in `.gt.txt` format.


