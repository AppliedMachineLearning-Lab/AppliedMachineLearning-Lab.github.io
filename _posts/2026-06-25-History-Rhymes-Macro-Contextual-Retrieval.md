---
layout: post
title: "History Rhymes: Macro-Contextual Retrieval for Robust Financial Forecasting"
date: 2026-06-25
author: Muskaan Chopra
categories: [Research]
description: false
tldr: "Forecasting becomes more robust when the model stops treating today as isolated and instead asks which past macroeconomic regimes today resembles."
---

This is a short summary of our paper **"History Rhymes: Macro-Contextual Retrieval for Robust Financial Forecasting"** by *Sarthak Khanna, Armin Berger, Muskaan Chopra, David Berghaus, and Rafet Sifa*, published in the proceedings of the 2025 IEEE International Conference on Big Data. See [here](https://xplorestaging.ieee.org/document/11400811) for the published version and [here](https://publica.fraunhofer.de/entities/publication/51ca8ad1-eaf3-464a-99a6-8ff9f07743c2) for the open-access Fraunhofer Publica version.

Financial forecasting models often look convincing during validation and then fail when the market regime changes. This is not surprising: markets are non-stationary. Inflation, unemployment, interest-rate spreads, GDP growth, sector narratives, and investor behavior all shift over time.

The idea behind this paper is simple: financial history does not repeat exactly, but it often rhymes.

We introduce a macro-contextual retrieval framework that grounds each prediction in historically similar macroeconomic situations. Instead of relying only on today’s price indicators or news sentiment, the model retrieves past periods with similar combinations of financial text and macro indicators such as CPI, unemployment, yield spread, and GDP growth. These retrieved historical analogues then provide context for the forecast.

The system is trained on S&P 500 data from 2007-2023 and evaluated out-of-distribution on AAPL and XOM in 2024. The important part is that retrieval is causal: for each prediction, the model can only retrieve earlier historical periods, not future information.

The main result is that macro-conditioned retrieval is more robust under distribution shift than static numeric, text-only, or naive multimodal baselines. It achieves the only positive out-of-sample trading outcomes on both AAPL and XOM, while also producing interpretable evidence chains through retrieved historical neighbors.
