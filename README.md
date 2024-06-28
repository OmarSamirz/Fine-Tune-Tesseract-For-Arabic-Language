# Fine-Tuning an Arabic OCR Model using Tesseract 5

## Table of Contents

* [Introduction](#introduction)
* [Key Areas of Focus](#Key-areas-of-focus)
* [Methodology](#methodology)
  * [Data Collection and Preprocessing](#data-collection-and-preprocessing)
  * [Dataset Composition](#dataset-composition)
  * [Image Generation](#image-generation)
* [Data Augmentation](#data-augmentation)
* [Training](#training)
* [Evaluation](#evaluation)
* [Results](#results)

## Introduction
Optical Character Recognition (OCR) is essential for digital processing and preservation of textual information. Despite advancements in OCR for various languages, Arabic OCR remains challenging due to its complex script. This project aims to fine-tune an Arabic OCR system using **Tesseract 5.0**, achieving high accuracy in text recognition.

## Key Areas of Focus
* Data Collection and Preprocessing
* Dataset Composition
* Image Generation
* Training and Evaluation
* Challenges and Limitations

## Methodology

### Data Collection and Preprocessing
We built a comprehensive Arabic dataset by collecting Arabic words from various online sources, ensuring quality through preprocessing steps like removing non-Arabic characters and normalizing text.

### Dataset Composition
Our dataset included about **1 million** Arabic sentences, split into:

* **60%** tashkeel-free sentences
* **40%** tashkeel-included sentences

This balance helps the OCR model handle both scenarios effectively.

### Image Generation
Using the **Text Recognition Data Generator (TRDG)** library, we created images from Arabic text, ensuring diversity with three distinct **Arabic fonts**: `Baghdad`, `Bahij`, and `Rakkas`. Images were generated in `.tif` format with corresponding ground truth text in `.gt.txt` format.

### Data Augmentation
Future improvements will include advanced data augmentation techniques to enhance the model's robustness, such as `noise injection`, `background variation`, and `character distortions`.

## Training
We fine-tuned the pre-trained Arabic model `ara.traineddata` from the official Tesseract repository. Key parameters included:

**Maximum iterations**: *1000*
**Lang type**: *RTL*
**PSM**: *13*

## Evaluation
We evaluated the model using the `ocreval` tool to measure its performance. The evaluation was conducted on a benchmarking dataset created by **Hegghammer**, which provided a comprehensive and rigorous assessment of our model's capabilities. We compared the results with pre-trained models and benchmarks from related research, focusing on metrics such as `character error rate` (**CER**) and `word error rate` (**WER**).

## Results
Our fine-tuned model demonstrated **significant improvements** in word error rate (WER) on datasets without noise, outperforming both the pre-trained Tesseract model and Hegghammer's Tesseract benchmarking results. However, on datasets that included noise, our model's performance was not as strong, highlighting areas for potential improvement in handling noisy data.

### License
This project is licensed under the <ins>MIT License</ins>.
