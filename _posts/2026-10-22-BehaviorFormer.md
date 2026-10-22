---
layout: post
title: "BehaviorFormer: Discovering Behavioral Patterns via Clusterable Next-Token Prediction"
date: 2026-10-22
author: Tobias Schneider
categories: [Research]
description: false
tldr: "Player behavior in open-ended games has no ground truth, so we let a Transformer with deep clustering discover it directly from raw game logs, yielding interpretable behavioral patterns that are shared across players."
---

This is a short summary of our paper **"BehaviorFormer: Discovering Behavioral Patterns via Clusterable Next-Token Prediction"** by *Tobias Schneider, Danial Fahrner, Soren Antebi, Daniel Uedelhoven, Lennard Bodden, Sandra Halscheidt, and Rafet Sifa*, published at the IEEE Conference on Games 2026. See [here](https://arxiv.org/abs/2610.16322) for the open-access arXiv version.

What do players do when a game gives them nothing to do? In open-ended games like Minecraft, there is no objective shaping behavior and no ground truth for what counts as a behavioral pattern. Classic approaches rely on hand-crafted features or self-reported labels. Both force us to define the patterns upfront, and both miss anything that does not fit the predefined taxonomy. The idea behind this paper is simple: **let the model find the patterns on its own.**

We treat gameplay as language. Every block broken, item crafted, and step taken becomes a token, and a Transformer learns to predict what a player does next. Next-Token Prediction (NTP) alone already produces representations with cluster-like structure, but the boundaries are blurry. We therefore add Deep Clustering using Soft Silhouette (DCSS), which pushes the model to **form compact, well-separated clusters** while it learns (Figure 1). Each cluster corresponds to a behavioral pattern.

![Figure 1: t-SNE visualization of embedding spaces learned by NTP alone (left) and DCSS (right), colored by DCSS cluster assignment](/assets/blog/2026-10-22-BehaviorFormer.png)

*Figure 1: t-SNE visualization of embedding spaces learned by NTP alone (left) and DCSS (right), colored by DCSS cluster assignment.*

We tested this on a controlled six-hour Minecraft session with 26 players and no given goal, yielding 11,234 sequences of roughly 30 seconds each. **Without any labels**, the model uncovers 23 well-separated behavioral patterns that group into seven interpretable categories: Stationary, Roaming, Travel, Base work, Mining, Logging, and Farming. Looking closer, each category resolves into distinct variants: mining splits into tunneling, caving, and excavating, and travel ranges from short overland sprints to sustained boat crossings. Crucially, the patterns are global. Every cluster covers at least 10 of the 26 players, and nearly half cover at least 24. The model **captures shared behavior, not individual playstyles.**

Next, we want to test generalization across games and longer sessions and revisit tokenization and sequence construction.
