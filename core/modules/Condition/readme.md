# Description

This hacky module allows to build and insert blocks conditionally, using an `if` `then` `else` syntax. The condition must be a python interpretable expression that returns a boolean. The expression is run using exec and has access to engine resources as locals.

Warning, the expression is interpreted at build time, not render time, therefore rendering variables like `pageNum` or `pageTot` can't be used.

## Block types
- if: insert a conditional block

# Usage
## Args
- condition: expression to execute
- then: List of blocks to build and insert if the condition is true

## Optional
- else: List of blocks to build and insert if the condition is false

# Example
```
type: if
condition: len(chapters["id"]) > 10
then:
  - type: text
    content: This is a big document
else:
  - type: text
    content: Meh, could write more
```
