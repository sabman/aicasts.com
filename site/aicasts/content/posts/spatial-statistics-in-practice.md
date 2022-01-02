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

![](../../posts-assets/000-box-plot.png)

A box map (Anselin 1994) is the mapping counterpart of the idea behind a box plot. The point of departure is again a quantile map, more specifically, a quartile map. But the four categories are extended to **six bins**, to separately identify the lower and upper outliers. The definition of outliers is a function of a multiple of the inter-quartile range (IQR), the difference between the values for the 75 and 25 percentile. As we will see in a later chapter in our discussion of the box plot, we use two options for these cut-off values, or hinges, 1.5 and 3.0. The box map uses the same convention.


## Standard deviation map
The third type of extreme values map is a standard deviation map. In some way, this is a parametric counterpart to the box map, in that the standard deviation is used as the criterion to identify outliers, instead of the inter-quartile range.

In a standard deviation map, the variable under consideration is transformed to standard deviational units (with mean 0 and standard deviation 1). This is equivalent to the z-standardization we have seen before.

The number of categories in the classification depends on the range of values, i.e., how many standard deviational units cover the range from lowest to highest. It is also quite common that some categories do not contain any observations.


## Quantile map

A quantile map is based on sorted values for a variable that are then grouped into bins that each have the same number of observations, the so-called quantiles. The number of bins corresponds to the particular quantile, e.g., five bins for a quintile map, or four bins for a quartile map, two of the most commonly used categories.

### Problems of Quantile map

Any time there are ties in the ranking of observations that align with the values for the breakpoints, the classification in a quantile map will be problematic and result in categories with an unequal number of observations.

## Natural breaks map

A natural breaks map uses a nonlinear algorithm to group observations such that the within-group homogeneity is maximized, following the pathbreaking work of Fisher (1958) and Jenks (1977). In essence, this is a clustering algorithm in one dimension to determine the break points that yield groups with the largest internal similarity.

In comparison to the quartile map, the natural breaks criterion is better at grouping the extreme observations. The three observations with zero values make up the first category, whereas the five high rent areas in Manhattan make up the top category. Note also that in contrast to the quantile maps, the number of observations in each category can be highly unequal.

## Equal intervals map

An equal intervals map uses the same principle as a histogram to organize the observations into categories that divide the range of the variable into equal interval bins. This contrasts with the quantile map, where the number of observations in each bin is equal, but the range for each bin is not. For the equal interval classification, the value range between the lower and upper bound in each bin is constant across bins, but the number of observations in each bin is typically not equal.


## Choropleth Map for Rates
### Spatially extensive and spatially intensive variables

We start our discussion of rate maps by illustrating something we should not be doing. This pertains to the important difference between a *spatially extensive and a spatially intensive variable*. In many applications that use public health data, we typically have access to a count of events, such as the **number of cancer cases** (a spatially extensive variable), as well as to the relevant population at risk, which allows for the calculation of a **rate** (a spatially intensive variable).


A major problem with spatially extensive variables like total counts, in that they tend to vary with the size (population) of the areal units. So, everything else being the same, we would expect to have more lung cancer cases in counties with larger populations.


Instead, we opt for a spatially intensive variable, such as the ratio of the number of cases over the population. More formally, if O_i is the number of cancer cases in area i, and P_i is the corresponding population at risk (in our example, the total number of white females), then the raw or crude rate or proportion follows as:

`r_i = O_i/P_i`

### Variance instability

The crude rate is an estimator for the unknown underlying risk. In our example, that would be the risk of a white woman to be exposed to lung cancer. The crude rate is an unbiased estimator for the risk, which is a desirable property. However, its variance has an undesirable property, namely

`Var[ri]=πi(1−πi)/Pi,`

where πi is the underlying risk in area i.4 This implies that the larger the population of an area (Pi in the denominator), the smaller the variance for the estimator, or, in other words, the greater the precision.

*The flip side of this result is that for areas with sparse populations (small Pi), the estimate for the risk will be imprecise (large variance).*

Moreover, since the population typically varies across the areas under consideration, the precision of each rate will vary as well. This variance instability needs to somehow be reflected in the map, or corrected for, to avoid a spurious representation of the spatial distribution of the underlying risk. This is the main motivation for *smoothing rates*, to which we return below.


$$
f(a)={\frac {1}{2\pi i}}\oint _{\gamma }{\frac {f(z)}{z-a}}\,dz
\tag{1}
$$
