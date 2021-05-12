# Description

Insert a list of objects. A list can be numbered or just an enumeration with a bullet. This type uses the reportlab ListFlowable and is very customizable.

A numbered list begins by default at 1, but it can also start at a specified value, continue numbering where the previous list stopped, or continue any random list providing its id. The formatting by default is `0. ` but can be specified if needed.

A bullet list will by default use the bullet character, but it is possible to use one of th other pre-defined characters or specify a custom one. The pre-defined bullets are: a bullet, an empty bullet (circle), a dash or an arrow.

In both cases, the `item` content of the list can be:
- A string that references a resource, then this resource is loaded in place. The resource *should be a list*  as it will be iterated!
- A list of strings, each will be built as a normal text item using the current default font style
- A list of object (dictionnaries) which will be processed through the engine, each object is an item
- A list of list of objects (dictionnaries) which will be processed through the engine, each list of object is an item

Again, no check is performed on the inserted blocks, so don't put stupid or too complex things in lists.

## Block types
- list: insert a bullet or numbered list

# Usage
## Numbered list
### Args
- numbered: boolean, true (otherwise the list is not numbered)
- items: actual content of the list: string (path to resource), list of strings, list of objects or list of list of objects (see description)

### Optional
- id: identifier of the list, this allows to continue the counter anywhere in the document
- start: first value to count from, can be an int, `continue` which will get the last list counter, or the identifier of the list to get its counter. The default is 1.
- format: how to format the numbering bullet, default is `%s. `

## Bullet list
### Args
- items: actual content of the list: string (path to resource), list of strings, list of objects or list of list of objects (see description)

### Optional
- numbered: boolean, false (otherwise the list is numbered)
- bullet: specify the bullet to use, can be: longDash, bullet, emptyBullet, arrow or custom
- bulletChar: if bullet is set to custom, use this char as bullet

## General
In addition, the following properties of the ListFlowable can also be tuned as needed:

- bulletFontSize: font size of the bullet, set to the current default font size in numbered lists, and 6 otherwise
- bulletFontName: font of the bullet, set to the current default font in numbered lists, and Times-Roman otherwise
- bulletOffsetY: vertical offset of the bullet, can be tuned if not aligned, default is -4
- bulletDedent: bullet dedent, default is 15
- leftIndent: left indent, default is 30

# Example
Simple numbered list:

```
type: list
numbered: yes
items:
  - One
  - Two
  - Three
```

A more complex one that continues the previous:
```
type: list
numbered: yes
start: continue
format: "%s) "
items:
  - Four
  - type: text
    content: Five
  - Six
```

Simple bullet list:

```
type: list
items:
  - One
  - Two
  - Three
```

Custom bullet:
```
type: list
bullet: arrow
items:
  - Four
  - type: text
    content: Five
  - Six
```
