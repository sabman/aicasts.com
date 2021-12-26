---
title: "Spatial Statistics in Practice"
date: 2021-12-09T00:04:43+05:00
draft: false
ShowToc: true
tags: ["geo"]
---

[Cheetsheet](https://geodacenter.github.io/cheatsheet.html)

# Box Map

What is the map equalent to a box plot? Lets remind oursevles of what a box plot is.

![](../../static/posts/000-box-plot.png)

A box map (Anselin 1994) is the mapping counterpart of the idea behind a box plot. The point of departure is again a quantile map, more specifically, a quartile map. But the four categories are extended to **six bins**, to separately identify the lower and upper outliers. The definition of outliers is a function of a multiple of the inter-quartile range (IQR), the difference between the values for the 75 and 25 percentile. As we will see in a later chapter in our discussion of the box plot, we use two options for these cut-off values, or hinges, 1.5 and 3.0. The box map uses the same convention.


