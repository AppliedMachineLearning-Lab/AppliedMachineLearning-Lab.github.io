---
layout: default
title: Muskaan Chopra
description: false
---

![Muskaan Chopra](/assets/muskaan.png){: style="float: right; margin: 0 0 1em 1em; max-width: 250px; border-radius: 4px;"}

I am a PhD researcher at the **Applied Machine Learning Lab (AML Lab)** at the **University of Bonn** and the **Lamarr Institute for Machine Learning and Artificial Intelligence**.

My research is centered around a question that sounds simple, but turns out to be surprisingly difficult:

**When should a machine learning model trust its own prediction — and when should it know that it does not have enough information?**

I am particularly interested in **reliable and resource-efficient language models**, with a focus on small and compact models that can reason, recognize uncertainty, and make better decisions under limited information or computational resources. My current work studies **context sufficiency, abstention, calibration, and selective prediction**, including how these behaviours emerge during training and whether the signals we can observe inside a model are actually used when it makes a decision.

A second thread of my work looks at what happens when models become smaller or more efficient. I have worked extensively on **quantization and compact language models for critical error detection in machine translation**, studying where compression is essentially free and where it begins to affect reliability. More broadly, I am interested in evaluation settings where aggregate accuracy alone is not enough and individual mistakes can have very different consequences.

Before moving towards language models, much of my research focused on **self-supervised learning and medical imaging**, particularly diabetic retinopathy screening. This continues to shape how I think about trustworthy AI: models should not only perform well, but should also communicate when their predictions are unreliable.

Across these areas, I am especially interested in models that are **small enough to study carefully, efficient enough to deploy, and reliable enough to know their limits**.

## Research interests

- **Reliable & Trustworthy Machine Learning:** Understanding when models fail, when they should abstain, and how reliability can be evaluated beyond average accuracy.
- **Small & Efficient Language Models:** Compact models, quantization, compression, and the relationship between model efficiency and behavioural robustness.
- **Context Sufficiency & Abstention:** Studying whether language models can recognize when the available information is sufficient to answer, and how this signal influences their decisions.
- **Mechanistic & Developmental Analysis:** Investigating where reliability-related signals are represented inside neural networks, whether they are causally used, and how they emerge during training.
- **Selective Prediction & Calibration:** Designing systems that can defer uncertain or risky predictions instead of treating every input as equally answerable.
- **Machine Learning for High-Stakes Applications:** Reliable evaluation in areas such as machine translation and medical AI, where seemingly small errors can have disproportionate consequences.

## Selected recent work

### Knowing When Not to Predict

**Self-Supervised Learning and Abstention for Safer Diabetic Retinopathy Screening**

*IJCAI-ECAI 2026*

We study how self-supervised pretraining influences not only classification performance but also a model's ability to identify cases on which it should abstain. The work explores selective prediction as a way of moving beyond accuracy towards safer medical AI.

### Towards Reliable Machine Translation

**Scaling LLMs for Critical Error Detection and Safety**

*ECIR 2026*

We investigate how language models of different scales perform at detecting meaning-critical translation errors and examine the trade-offs between model size, reliability, and computational cost.

[\[Paper\]](https://arxiv.org/abs/2602.11444)

### How Small Can You Go?

**Compact Language Models for On-Device Critical Error Detection in Machine Translation**

*IEEE BigData 2025*

This work explores how far language models can be compressed while retaining their ability to detect critical translation errors, with particular attention to parameter-efficient and quantized models.

[\[Paper\]](https://arxiv.org/abs/2511.09748)

### SynCED-EnDe 2025

**A Synthetic and Curated English-German Dataset for Critical Error Detection in Machine Translation**

*ECIR 2026*

We introduce a structured benchmark for critical error detection containing fine-grained error categories designed to support more systematic evaluation of both compact and large language models.

[\[Paper\]](https://arxiv.org/abs/2510.05144)

### Functional Knowledge Transfer with Self-Supervised Representation Learning

*IEEE International Conference on Image Processing (ICIP), 2023*

Our earlier work studied how self-supervised representations can support label-efficient knowledge transfer across domains, forming part of my broader interest in robust learning under limited supervision.

[\[Paper\]](https://ieeexplore.ieee.org/document/10222142)

## Beyond research

I enjoy being involved in the research community beyond my own projects. I have served as a reviewer for **IJCAI-ECAI** and **IJCNN**, and I have been involved in mentoring students through the **MINERVA Mentoring Program at the University of Bonn**.

I am always happy to talk about reliable language models, small models, abstention, unusual model behaviours, or research ideas somewhere between *"this probably should not work"* and *"why does this actually work?"*

## Contact

If you would like to get in touch, feel free to email me at

**mchopra[at]uni-bonn.de**.