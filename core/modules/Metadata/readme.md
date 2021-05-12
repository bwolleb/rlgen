# Description

Allows to define the PDF metadata on the generated file. The PDF standard defines the following fields:

- Title
- Author
- Subject
- Keywords
- Creator
- Producer

Inserting more than one `meta` block is useless, the last inserted one will override the others. If no metadata block is used, the default values defined by reportlab will be used:

- Title: untitled
- Author: anonymous
- Subject: unspecified
- Keywords: ""
- Creator: ReportLab PDF Library - www.reportlab.com
- Producer: ReportLab PDF Library - www.reportlab.com

## Block types
- meta: set metadata of the generated PDF document

# Usage
## Optional

- title: define the author field, empty by default
- author: define the author field, empty by default
- subject: define the subject field, empty by default
- keywords: define the keywords field, empty by default
- creator: define the creator field, "rlgen" by default
- producer: define the producer field, "ReportLab PDF Library" by default

## Example
```
type: meta
title: My test document
author: Me, Myself and I
subject: Testing the metadata block
keywords: test metadata
creator: beloved computer
producer: beloved generator
```
