# CalibrationCurve

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Install

``` sh
pip install CalibrationCurve
```

## How to use

First we generate some data to work with.

``` python
# generate training data and sample data
test_data = pd.DataFrame({'concentration': [0.2, 0.05, 0.1, 0.8, 0.6, 0.4], "abs": [0.221, 0.057, 0.119, 0.73, 0.599, 0.383]})
sample_data = pd.DataFrame({'unknown': [0.490, 0.471, 0.484, 0.473, 0.479, 0.492]})
```

Now, we create a
[`CalibrationModel`](https://Rhys-McAlister.github.io/CalibrationCurve/core.html#calibrationmodel)
object and pass the predictor and response variables from our dataset as
the x and y values respectively. Additionally we specific the amount of
replicates for our unknown.

``` python
cal = CalibrationModel(x=test_data['concentration'], y=test_data['abs'], test_replicates=6)
```

When we call `.fit_ols()`, a least squares regression is fit to the data
and the slope, intercept and $R^2$ values are stored in the object and
can be retrieved by calling `object.slope`, `object.intercept` and
`object.r_squared` respectively.

``` python
cal.fit_ols()

print(f"Slope: {cal.slope: .3f}" )
print(f"Intercept: {cal.intercept: .3f}" )
print(f"R2: {cal.r_squared: .3f}" )
```

    Slope:  0.904
    Intercept:  0.027
    R2:  0.998

Finally, we can calculate an inverse prediction from unknown data and
retrieve the uncertainty but calling `.inverse_prediction()` and
`.calculate_uncertainty()` respectively.

The uncertainty is calculated according to the following expression:

$${S_{\hat{x}}}_0 = \frac{S_{y/x}}{b} \sqrt{\frac{1}{m} + \frac{1}{n}} $$

``` python
pred = cal.inverse_prediction(sample_data['unknown'])
print(f"Predicted concentration: {pred: .3f} +- {cal.calculate_uncertainty(): .3f}")
```

    Predicted concentration:  0.502 +-  0.037
