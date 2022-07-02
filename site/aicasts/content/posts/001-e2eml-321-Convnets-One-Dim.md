---
title: "Convolution Neural Network in One Dimension"
date: 2020-09-15T11:30:03+00:00
# weight: 1
aliases: ["/001-e2eml-321-Convnets-One-Dim"]
tags: ["convnets", "e2eml"]
author: "Me"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
description: "This is a summary of what I learnt doing this course https://end-to-end-machine-learning.teachable.com/courses/776160/lectures/14555482"
canonicalURL: "https://canonical.url/to/page"
disableHLJS: true # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
editPost:
    URL: "https://github.com/<path_to_repo>/content"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---


# Introduction


We should be able to answer the following by the end of this course:

- [ ] How convolution works
- [ ] How to create a convolution layer for a neural network
- [ ] What considerations need to be taken when working with one-dimension data
- [ ] How to modify a convolution neural network to get good performance

As well as some general questions about NNs

- [ ] How to use a neural network to perform classification tasks
- [ ] How a softmax layer works and how to implement it
- [ ] How a batch normalization layer works and how to implement it
- [ ] How to create a neural network out of any differentiable function you like


When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$ and they are 
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$


Mathjax block:
  
{{< mathjax/block >}}
\[a \ne 0\]
{{< /mathjax/block >}}

Inline shortcode {{< mathjax/inline >}}\(a \ne 0\){{< /mathjax/inline >}} with
Mathjax.
