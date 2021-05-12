# Description

This module is responsible of building entries that will be collected and displayed in the [table of content](../Toc). Loading it is sufficient to make the chapters automatically appear in the table of contents, but it can also be used to insert a manual entry.

## Block types
- tocEntry: insert a manual entry in the table of contents

# Usage
## Args
- text: actual text to display in the table of contents

## Optional
- id: identifier of the entry, default is a uid
- level: level of the entry, default is 0

## Example
```
type: tocEntry
level: 1
text: Hello World
```
