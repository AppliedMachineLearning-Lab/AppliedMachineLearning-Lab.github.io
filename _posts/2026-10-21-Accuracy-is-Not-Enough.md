---
layout: post
title: "Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs"
date: 2026-10-21
author: Shahzeb Qamar
categories: [Research]
description: false
tldr: "Quantized large language models can maintain benchmark accuracy while their predictions drift substantially from the original model. We show how measuring next-token distribution divergence alongside accuracy reveals hidden fidelity loss and helps distinguish quantization schemes with similar memory costs."
---

This is a short summary of our paper **"Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs"** by *Shahzeb Qamar, Lorenz Sparrenberg, Christian Bauckhage, Baha Rababah, Carson K. Leung, Murat Kantarcioglu, Cuneyt Gurcan Akcora, and Rafet Sifa*, published at IEEE DSAA 2026. See [here](https://arxiv.org/abs/2609.07664) for the open-access arXiv preprint.

## When accuracy hides what quantization changes

Large language models are expensive to run, and quantization makes them smaller and more practical to deploy on memory-constrained devices. But there is a catch: a quantized model can achieve nearly the same benchmark accuracy as its full-precision counterpart while producing substantially different predictions.

In *Accuracy is Not Enough*, we introduce a distribution-based approach to measure this hidden fidelity loss. Instead of checking only whether a model selects the correct answer, we compare its full next-token probability distribution against the original BF16 model using Total Variation Distance (TVD) and Jensen–Shannon Divergence (JSD).

We evaluate 120 configurations across five model architectures, four reasoning and knowledge benchmarks, and multiple quantization levels. The results show that accuracy can fluctuate non-monotonically and conceal substantial changes in model behavior. For example, on PIQA, Teuken-7B compressed with uniform 4-bit quantization (Q4\_0) loses only 0.2 percentage points in accuracy, yet its TVD reaches 0.560—indicating a substantial shift in its next-token probability distribution relative to the BF16 reference.

![Figure 1: Accuracy is Not Enough](/assets/blog/2026-10-21-Accuracy-is-Not-Enough.png)

We also find that, in the tested llama.cpp configurations, mixed-precision Q4\_K generally stays closer to the BF16 reference than uniform Q4\_0 at similar memory footprints. This suggests that model compression should be evaluated not only by size and task accuracy, but also by how much it changes the model's predictive behavior.

**The takeaway:** Accuracy tells us whether a model gets benchmark answers right; distributional divergence tells us how much its predictions have changed. Using both provides a more informative picture of quantized-model fidelity.
