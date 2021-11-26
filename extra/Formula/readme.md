# Description

Allows to render math formula LaTeX style in the document. The formula is rendered as a pure vector pdf object (not an image). 

Warning, this module requires `matplotlib` which is used to render the actual formula. Installing this module will install tons of things in your python environment.

There is a known issue which causes a formula to be cropped when rendered, this is caused by some internal matplotlib black magic. If it happens, a workaround is to add a padding around the formula, a small value like 0.05 (inches) is enough. See the [matplotlib.figure.Figure.savefig](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig) documentation.

Also, the matplotlib rendering seems to only support partial LaTeX notation, it is kind of fragile, so use with care.

## Block types
- formula: insert a formula in the document

# Usage
## Args
- expression: the LaTeX-ish formula to render, note that it must start and end with a dollar sign.

## Optional
- width: rendered formula width in cm, default is main frame width
- align: LEFT, CENTER, RIGHT, default is CENTER
- pad: optional padding to add around formula is rendering crops it, the default is 0.

## Example
Simple formula
```
type: formula
width: 2
expression: $a^2 + b^2 = c^2$
```

A more complex one, expression can be multiline:
```
type: formula
width: 5
expression: >
  $\lim_{n \to \infty}
  \sum_{k=1}^n \frac{1}{k^2}
  = \frac{\pi^2}{6}
  \lim_{n \to \infty}
  \sum_{k=1}^n \frac{1}{k^2}
  = \frac{\pi^2}{6}$
```
