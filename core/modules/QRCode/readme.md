# Description

Allow to generate and insert a QR code in the document flow using reportlab graphics. The size, color, level and version of the QR code to generate are configurable. By default a small border is drawn around the QR code in order to avoid it to be too close from other blocks.

## Block types
- qr: insert a QR code in the document

# Usage
## Args
- data: actual data to encode in the QR code
- width: width of the QR code to generate in cm

## Optional
- height: manually change the height, in cm, in order to have a rectangle QR code instead of a square one, by default it is equal to the provided width
- color: change color of the QR code, black by default
- border: change the QR code border, the default is 1
- level: change the QR code level (redundancy, see QR code specifications), default is L
- version: change the QR code version (amount of data, see QR code specifications), default None (automatic) 

## Example
Simple QR code
```
type: qr
data: This is a test QR code
width: 4
```

Bigger, rectangle, orange QR code with much redundancy
```
type: qr
data: >
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel arcu ac enim vestibulum
  luctus ac ac est. Pellentesque tincidunt arcu nibh, id aliquam dui congue eu.
width: 10
height: 8
level: Q
color: cc7700
```
