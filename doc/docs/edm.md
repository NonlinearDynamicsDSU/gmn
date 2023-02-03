## The EDM Framework
---
The EDM framework is predicated on the availability of a multidimensional
representation of the system dynamics.  For example, the well-known
[Rössler attractor](https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor)
is a 3-dimensional (3-D) system that can express chaotic dynamics.
The set of 3 equations that define the Rössler system define an _attractor_
or _manifold_ defining the _state-space_ or _phase-space_ of the system. 
Often, one does not have complete information regarding the system
dynamics, in which case we can invoke Takens embedding theorem.

### Takens Theorem
[Takens theorem](https://en.wikipedia.org/wiki/Takens%27s_theorem) 
is a remarkable mathematical result that allows one to reconstruct a
representation of the system dynamics (state-space manifold) from a
single (univariate, 1-D) timeseries observed from the system.  The embedding
results in generation of a higher-dimensional representation of the system.

### Embedding
The process of creating this representation is termed _embedding_.
Embedding is performed implicitly in GMN/EDM functions unless the `embedded` 
argument is set `True` indicating that the data are already embedded. 
Default embeddings are time-delay (lagged) with _τ_ = -1.

### Nearerst Neighbor Forecasting: Simplex and S-map
GMN/EDM implements two timeseries prediction algorithms:
[`Simplex()`](https://en.wikipedia.org/wiki/Empirical_dynamic_modeling#Simplex),
and [`SMap()`](https://en.wikipedia.org/wiki/Empirical_dynamic_modeling#S-Map).
Both operate in the embedding state-space, using nearest neighbors
of a query point (location in the state-space from which a prediction is
desired) to project a new estimate along the manifold.

[`Simplex()`](https://en.wikipedia.org/wiki/Empirical_dynamic_modeling#Simplex)
uses the centroid of the k-nearest neighbors (knn) of the query point as the 
estimate.  The number of neighbors, knn, is conventionally set as the number 
of dimensions plus one: knn = E + 1. 

[`SMap()`](https://en.wikipedia.org/wiki/Empirical_dynamic_modeling#S-Map)
uses a linear regression of query point neighbors to project a new estimate
along the manifold.  By default, the number of
neighbors knn in the regression are set to the total number of state-space
observation points. An exponential localisation function F(θ) = exp(-θd/D)
is used to selectively ignore neighbors beyond the localisation radius. 
θ is the localisation parameter, d a neighbor distance, and D the mean
distance to all neighbors.  This allows one to vary the
extent to which local neighbors are considered in the linear projection,
effectively modeling different local "resolutions" on the attractor.
The effect of this knn localisation can be assessed with the EDM
[`PredictNonlinear()`](https://sugiharalab.github.io/EDM_Documentation/edm_functions/#predictnonlinear) function that
evaluates S-map predictive skill over a range of localisations θ. 

---

### Introduction to Empirical Dynamic Modeling
<iframe width="100%" height="350"
src="https://www.youtube.com/embed/fevurdpiRYg"
frameborder="0" allow="autoplay; gyroscope; 
picture-in-picture" allowfullscreen></iframe>

---

### Constructing Empirical Dynamic Models: Takens Theorem
<iframe width="100%" height="350"
src="https://www.youtube.com/embed/QQwtrWBwxQg" 
frameborder="0" allow="autoplay; gyroscope; 
picture-in-picture" allowfullscreen></iframe>

---

### Convergent Cross Mapping (CCM)
<iframe width="100%" height="350"
src="https://www.youtube.com/embed/NrFdIz-D2yM"
frameborder="0" allow="autoplay; gyroscope;
picture-in-picture" allowfullscreen></iframe>
