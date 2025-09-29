---
layout: default
title: Special Session on Large Language and Foundation Models 2025
description: Co-located with DSAA 2025
---
<link rel="icon" type="image/x-icon" href="/assets/aml_lab_tight.ico" />

# From Theory to Practice: Special Session on Large Language and Foundation Models

**Location**: Composer’s Suite, Edgbaston Park Hotel, University of Birmingham, Birmingham, UK  
**Conference**: [DSAA 2025](https://dsaa.ieee.org/2025/) (IEEE International Conference on Data Science and Advanced Analytics)  
**Date**: October 9, 2025

Large language and foundation models have rapidly emerged as pivotal technologies in data science and analytics, 
offering unprecedented capabilities in text generation, knowledge extraction, and complex decision-making. This special 
session seeks to bridge cutting-edge theory with real-world applications, providing a venue for researchers and 
practitioners to exchange novel methodologies, deployment strategies, and impact-driven insights. By spot-lighting both 
breakthrough techniques and operational challenges, the session aims to foster cross-pollination of ideas, accelerate 
innovation, and elucidate pathways for seamless integration of large language models into diverse data-driven 
ecosystems.

- Submission Deadline: **May 16th, 2025** (Extended from May 2nd)
- Paper Notification: **July 24th, 2025**
- Paper Camera-Ready: **August 28th, 2025**
- Contact: `amllab[at]bit.uni-bonn.de`

## Agenda

| Time          | Paper / Speaker                                                                 | Presenter           |
|---------------|---------------------------------------------------------------------------------|---------------------|
| 11:00 – 11:30 | **Keynote:** Making GPUs go BRRRR: Scaling LLM pretraining to thousands of GPUs     | Max Lübbering       |
| 11:30 – 11:45 | Paper 197: Towards LLM-guided Healthcare Dataset Harmonization                  | Christos Smailis    |
| 11:45 – 12:00 | Paper 149: Reasoning LLMs in the Medical Domain: A Literature Survey            | Armin Berger        |
| 12:00 – 12:15 | Paper 159: Semi-Supervised Relation Extraction Informed by LLMs                 | Nikita Gautam       |
| 12:15 – 12:30 | Paper 29: Reproducibility and Case Sensitivity of LLMs for Anonymizing Tweets   | Sameen Mansha       |
| 12:30 – 13:30 | Lunch Break                                                                     |                     |
| 13:30 – 13:45 | Paper 136: A Survey on Large Language Model Quantization Methods                | Lorenz Sparrenberg  |
| 13:45 – 14:00 | Paper 84: Predicting Player Churn with LLMs                                     | Tobias Schneider    |
| 14:00 – 14:15 | Paper 44: Student-perceived Cognitive Load of LLM-generated Programming Tasks   | Ludia Eka Feri      |
| 14:15 – 14:30 | Paper 119: Digitizing P&IDs with Transformers                                   | —                   |
| 14:30 – 15:00 | **Keynote:** Topology-Informed Fine-Tuning and Quantization of Large Language Models| Cüneyt Gürcan Akçora|

## Keynotes

### Making GPUs go BRRRR: Scaling LLM pretraining to thousands of GPUs

**Max Lübbering**, Senior Research Scientist, Lamarr Institute

Max Lübbering is a Research Scientist at the Lamarr Institute and Fraunhofer IAIS, specializing in large-scale pretraining of multilingual large language models (LLMs). He is a founding member of the Eurolingua-GPT project, which trains a new family of European LLMs on leading European supercomputers.
He designed and now leads the development of Modalities, a PyTorch-native open-source framework for efficient and reproducible LLM pretraining at scale. Modalities scales training to thousands of GPUs, implements state-of-the-art parallelism and checkpointing techniques, and currently powers all Eurolingua trainings.
Max holds a Ph.D. in Computer Science from the University of Bonn, where he worked on uncertainty estimation in deep learning. He has published at EMNLP, NAACL, ECAI, ICSA, and ICDE Workshops, and is passionate about advancing boundaries of foundation model research.

**Abstract**: tba.

### Topology-Informed Fine-Tuning and Quantization of Large Language Models

**Cüneyt Gürcan Akçora**, Associate Professor, University of Central Florida

Cüneyt Gürcan Akçora is an Associate Professor at the University of Central Florida with joint appointments in the Finance Department and the AI Initiative. His research spans graph machine learning, topological data analysis, and large-scale data systems. He has published in leading venues such as ICLR, VLDB, KDD, NeurIPS, and IJCAI, with contributions on topological methods for blockchain analytics and graph machine learning.

**Abstract**: Fine-tuning and quantization are key to adapting large language models for practical use, yet both processes risk model degradation and unstable performance. This talk presents a topological perspective on monitoring and guiding these adaptations. By transforming attention weight matrices across training epochs into persistence diagrams and measuring Wasserstein distances, we capture how internal representations evolve during fine-tuning and low-rank adaptation. These signals help identify optimal stopping points, stable layers, and effective LoRA rank choices. We also explore how topology can shed light on quantization effects, revealing when model compression preserves or disrupts learned structures. Together, these methods offer new insights into reliable and efficient LLM deployment.

## Submission

To submit a paper to SSLLFM2025, go to: [OpenReview](https://openreview.net/group?id=IEEE.org/DSAA/2025/Conference), 
and select the "Special Session: From Theory to Practice: Special Session on Large Language and Foundation Models" 
track.

The length of each paper submitted to SSLLFM2024 should be no more than ten (10) pages and should be formatted 
following the standard 2-column U.S. letter style of IEEE Conference template. For further information and 
instructions, see the [IEEE Proceedings Author Guidelines](https://www.ieee.org/conferences/publishing/templates.html).

All submissions will be double-blind reviewed by the Program Committee based on technical quality, relevance to the 
special session’s topics of interest, originality, significance, and clarity. Author names and affiliations must not 
appear in the submissions, and bibliographic references must be adjusted to preserve author anonymity. Submissions 
failing to comply with paper formatting and authors anonymity will be rejected without reviews.

Because of the double-blind review process, non-anonymous papers that have been issued as technical reports or similar 
cannot be considered for SSLLFM2025. An exception to this rule applies to arXiv papers that were published in arXiv at 
least a month prior to SSLLFM2025 submission deadline. Authors can submit these arXiv papers to SSLLFM2025 provided 
that the submitted paper’s title and abstract are different from the one appearing in arXiv.

## Call for Papers

The topics of interest are, but not limited to:

- Model Training and Optimization:
  - Techniques to deal with hallucinations
  - Training data for LLMs
  - Efficient and stable techniques for training and finetuning LLMs 
  - Scalable approaches for distributed model training 
  - Middleware for scale out data preparation for LLM training 
  - Workflow orchestration for end-to-end LLM life cycle 
  - Resource management for compute and energy efficient model training 
  - Representation learning
- Model Utilization and Integration:
  - Using LLMs effectively as tools for Reinforcement Learning or search 
  - Enhancing LLM capabilities by using external tools such as search engines 
  - Visual Prompt Tuning and in-context learning 
  - Enable easy experimentation with high utilization to train foundational models in the cloud 
  - Strategies to scale resources for training/fine-tuning foundational models 
  - Instruction tuning including generation of instruction tuning data 
  - Parallel training: data model tensor (attention and weights)
  - Distributed workflows for data cleansing and model usage (Langchain)
  - Principled AI 
  - Investigating reasoning capabilities of LLMs 
  - Retrieval Augmented Generation 
  - Alternative architectures such as State Space Models 
- Compact Language Models and Knowledge Distillation:
  - Knowledge representations for training small/compact language models 
  - Evaluation of different teacher-student distillation and model compression strategies 
  - Techniques for efficient data encoding to maintain linguistic properties in compact models 
  - Deployment of lightweight models in resource-constrained environments 
  - Case studies on the effectiveness in various NLP tasks
- Application-Specific Models:
  - Math LLMs
  - Multimodal Foundation Models 
  - Trustworthy Foundation Models
  - Large-scale Visual Foundation Models
  - Timeseries foundation models for forecasting, prediction and control 
  - Multi-Agent System using LLMs
  - Recommender systems using LLMs
  - Knowledge management using LLMs
- Knowledge Incorporation and Adaptation:
  - Approaches to deal with knowledge recency to effectively update knowledge within LLMs 
  - Incorporating domain knowledge in LLMs
- Evaluation and Benchmarking:
  - Additional benchmarks to fill gap between human and automatic reference-based evaluation

## Proceedings and Indexing

All accepted full-length special session papers will be published by IEEE in the DSAA main conference proceedings under 
its Special Session scheme. All papers will be submitted for inclusion in the IEEEXplore Digital Library.


## Organizers

- Prof. Dr. Rafet Sifa (University of Bonn, Germany)
- Dr. Dhavel Patel (IBM Research, USA)
- Tobias Deußer (Fraunhofer IAIS, Germany)
- Dr. Lorenz Sparrenberg (University of Bonn, Germany)
