# Description

Allows to insert a title in the document. Titles are just standard paragraphs with a few automation:

- Automatic style according to chapter level
- Automatic numbering (if wanted) according to chapter level
- Automatic bookmarking so the chapter can be referenced anywhere, if the module is loaded
- Automatic insertion of the chapter in the table of content if the module is loaded
- Dynamic resource where all chapter data can be found and used

Chapter levels begin at 0 and no level can be skipped: you can't insert a title level 0 and a title level 2 skipping level 1, but you can jump from a level x to a lower level at any time (see reportlab documentation for more details).

## Title formatting
By default, numbered chapters are formatted all levels, using arab numbers separated with dots, separated from the title with a dot and a space:

`[arab t0][levelSep][arab t1][levelSep]...[numberingEnd][title]` which translates to `1.2.3. My Chapter`.

Both `levelSep` and `numberingEnd` are configurable, either as args when the module is loaded, or using the `set` instruction of [ModuleLoader](../ModuleLoader) instruction.

### Custom numbers
By default, each level is rendered using standard arab numbers, but this can be changed using the `titleNum` block to the following available formatters for any level:

- 1: standard arab format (1, 2, 3), default
- A: upper alphabetic format (A, B, C, ..., AA, AB)
- a: lower alphabetic format (a, b, c, ..., aa, ab)
- Aa: capitalized alphabetic format (A, B, C, ..., Aa, Ab)
- I: upper roman format (I, II, III, IV, V)
- i: lower roman format (i, ii, iii, iv, v)
- Ii: capitalized roman format (I, Ii, Iii, Iv, V)

### Custom format
For advanced use, the rendering itself can be changed using the `titleFormat` for any level using python format string. The following variables are available:

- current levels: `t0`, `t1`, `t2`, ... `tx` which are rendered according to their current `titleNum` format, arab by default
- current level: `current` which is rendered according to the current `titleNum` format, arab by default

## Chapter resource
The module creates and maintain the `chapters` resource containing the following items:
- counters: list of integers keeping track of the current chapter numbering, for example [2, 3, 1] if the current chapter is 2.3.1
- id: map to all chapters of the document, this allows to access chapter data using its id
- current: dict of the current chapter, if any

Each chapter is stored as a dict containing the following items:
- text: Original text of the title
- id: identifier of the chapter
- level: level of the title, begins at 0
- number: numbering of the chapter level, for example the value is 4 for chapter 2.3.4
- fullnumber: full, displayable chapter numbering like 4.5.6
- fulltext: full, displayable chapter text like "1.2.3. My Chapter"

Currently, no block allows to manually manipulate the chapter counters, for example to reset them inside the document, but it is easy as changing the `chapters/counters` list content.

## Block types
- title: insert a title
- chapter: alias for `title`
- titleStyle: change the default chapter font styles
- titleNum: change title level number format
- titleFormat: change title number formatting

# Usage
## Insert a title
### Args
- text: Actual text of the title to insert

### Optional
- level: chapter level, begins at 0, default is 0
- id: identifier of the chapter, useful to reference anywhere in the document, default is a uid
- numbered: boolean to enable/disable numbereing, default is true

## Assign title styles
### Args
- style: font style(s) to use for the titles, can be:
  - a string, which is the identifier of an existing font style to use for the specified chapter level
  - a list of strings, where each one is the identifier of an existing font style to use for the corresponding chapter level, this syntax allows to define all styles at once
  - a dict, which defines a new font style in place using the [FontLoader](../FontLoader) syntax for the specified chapter level

### Optional
- level: specify level to assign the style to, mandatory if the `style` is a string or a dict

## Change title level number format
### Args
- num: number formatter to use, can be:
  - a string, which is the formatter to use for level numbers, applied to the specified `level` if provided, all levels otherwise
  - a list of strings, where each one is the formatter to use for corresponding levels
  - `null` which clears all current formatting for all levels

### Optional
- level: specify level to assign the format to, can only be used if `num` is a string

## Change title number formatting
### Args
- format: python format string to use, can be:
  - a string, which is the formatter to use for level format, applied to the specified `level` if provided, all levels otherwise
  - a list of strings, where each one is the formatter to use for corresponding levels
  - `null` which clears all current formatting for all levels

### Optional
- level: specify level to assign the format to, can only be used if `format` is a string

## Example
Insert a simple, level 0 chapter:
```
type: title
text: Introduction
```

Insert a level 1 chapter
```
type: chapter
text: The universe
level: 1
id: universeChap
```

Insert a level 1 chapter
```
type: chapter
text: The universe
level: 1
id: universeChap
```

Insert an unnumbered title, using title style of level 2
```
type: chapter
text: The planets
level: 2
numbered: no
```

Assign all title styles
```
type: titleStyle
style: [title1, title2, title3]
```

Change level 1 style
```
type: titleStyle
style: anotherStyle
level: 1
```

Define level 2 style in place
```
type: titleStyle
level: 2
style:
  font: Times-Roman
  name: awesomeStyle3
  size: 14
  align: left
  color: "ff0000"
```

Define level 2 number format to capital roman
```
type: titleNum
level: 2
num: I
```

Define number format for 4 levels
```
type: titleNum
num: [A, a, "1", I]
```

Define level 0 format string
```
type: titleFormat
level: 0
format: "{t0:.2f}: "
```

Define format string for 3 levels
```
type: titleFormat
format: ["{t0}_", "{t0}_{t1}", "{t0}_{t1}____{t3}"]
```

Define format for all levels
```
type: titleFormat
format: "__{current}__"
```

Use the chapter resource system:
```
type: text
content: So we are now in chapter {{data(chapters/current/fulltext)}} which is the best one!
```

Reset chapter counters within the document using the [Exec](../Exec) module
```
type: exec
python: |
  engine.resources["chapters"]["counters"] = []
```
