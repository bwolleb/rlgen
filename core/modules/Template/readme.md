# Description

This module is all syntaxic sugar, its only purpose is to be able to ship default templates and styles, so that creating a simple standard A4 document just takes a few lines, see [demo](../../../demo) or the example below.

The module works by looking into its own assets dir for the provided template name and load it using the [Include](../Include) mechanism.

## Block types
- template: load a predefined template

# Usage
## Args
- name: the name of the template file to include.

## Example
Creating a simple A4 document is simple as:

```
- type: module
  id: core.modules.Template

- type: template
  name: std_a4
```

# Content
The predefined templates are the following:

- std_modules: loads the most standard modules
- layout_a4: defines A4 portrait and landascape page styles
- std_fonts: defines standard fonts
- std_deco: defines a simple page numbering "x / tot" decoration at th bottom center of each page
- std_a4: includes all 4 templates above, so including this template is sufficient to have a simple, fully usable document
