---
layout: post
title: "Towards Automated Recipe Reconstruction"
date: 2026-04-16
author: Svetlana Schmidt
categories: [Research]
description: false
---

This is a short summary of our paper **"Towards Automated Recipe Reconstruction: Optimization of Dietary Data Collection using Information Retrieval, Large Language Models and Mathematical Optimization"** by *Svetlana Schmidt, Linda Klasen, Ute Nöthlings, and Rafet Sifa* published in the proceedings of the 2025 IEEE International Conference on Big Data. See [here](https://bonndoc.ulb.uni-bonn.de/xmlui/handle/20.500.11811/14070) for the full paper.

Expanding nutritional databases for epidemiological research (specifically the NutriDiary system at the University of Bonn) currently relies on manual, labor-intensive recipe matching and simulation by dietitians, a process that is slow and error-prone.

Contributions:

**Information Retrieval (IR) Recommender System:** We propose a two-stage IR system that combines TF-IDF text similarity (product names + ingredients) with nutrient profile similarity to find matching food items in the database. A key enhancement is food category prediction, which narrows the search space before retrieval. Among the tested classifiers (Logistic Regression, SVM variants, neural networks, BERT, DistilBERT), the polynomial- and RBF-kernel SVCs performed best, achieving 99% and 98.6% accuracy, respectively. Adding category filtering boosted retrieval precision from 73.74% to 80.48%, while maintaining a 92% Success@K across all models.

**Recipe Simulation Pipeline (Roadmap):** For products that cannot be matched, we outline a hybrid pipeline combining:

- LLMs with Chain-of-Thought prompting for ingredient parsing and normalization
- Mathematical optimization (linear/quadratic programming) to estimate ingredient proportions constrained by declared nutrient values
- Expert-in-the-loop validation by dietitians as a quality gate

**Key Findings:** Kernel SVMs outperformed transformer models (BERT/DistilBERT) for food categorization, likely because TF-IDF captures domain-specific lexical patterns better than general-purpose contextual embeddings. Annotation inconsistencies in the dataset were also identified as a limiting factor requiring label harmonization.
