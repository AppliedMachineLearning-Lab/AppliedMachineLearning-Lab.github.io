# AppliedMachineLearning-Lab.github.io

This repository contains the website for the Applied Machine Learning (AML) Lab at the University of Bonn.

## Getting Started Locally

Start here: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll

Then:

1. **Install dependencies**:
   ```bash
   bundle config set --local path 'vendor/bundle'
   bundle install
   ```

2. **Run the site locally**:
   ```bash
   bundle exec jekyll serve
   ```

3. **View the site**: Open `http://localhost:4000` in your browser


## Adding a Blog Entry

Create a new file in `_posts/` named `YYYY-MM-DD-your-title.md` with the following front matter:

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
author: Your Name
categories: [A list of categories]
description: false
---

Your content here...
```

The post will automatically appear on the [/news/](/news/) page. The date in the filename controls the sort order.

## Files

Please *do not* commit files for downloading (like lecture slides or assignments) into this repo. Create a separate repo or use a different hoster for this.
