# Description

This hacky module is a POC for bibliography support, it is **not** considered stable. The module allows to load one or more LaTeX "bib" bibliography files and render the bibliography list. The module uses the `pybtex` package for databse parsing and rendering. In short the module is able to:

- Parse bib database files
- Allow to make references within text through specialized text processors
- Render the full bibliography with the default formatting style

Currently, the generated bibliography is generated in the order the items were referenced within text (if using the "used" render option) or the items order from the bib file, a future improvement should be to sort the output by date, author of title.

## Initialization
When the module is loaded, the following values can be overriden:

- `update`: when set to "auto" (the default value) the module will keep track of which items in the database were actually referenced in the text and allow to render only that subset. Set to None if you don't need this.
- `backend`: specifies the pybtex backend to use for text rendering. The "plain" backend will just render simple text, and the "custom" backend will format it a bit (titles in italic, clickable links). The custom backend is a modified alternative to the normal html backend of pybtex as this one would product markups that won't be processed well by reportlab. The default is "custom".
- `numFormat`: is the formatting template to render the `no` reference (see text processors below), the default is [{num}]

## Block types
- bib: load a bibliography database file
- bibliography: generate the bibliography of referenced or all items in the database

## Chapter resource
When a bib database is loaded, each item is actually pre-formatted and inserted in the `biblio` resource, maintained by this module. The resource can be used like any other within the document, for example with the normal `res()` text processor. Actually, using `res(biblio/ref/title)` is strictly equivalent to `cite(ref, title)`. Each item has the following keys:

- `author`: formatted shortened author string, like "Lastname et al."
- `authors`: formatted list of all authors
- `title`: formatted title of the document
- `formatted`: full reference string (authors, title, editor, url, etc...)
- `num`: number assigned of the item (only known when the bibliography is actually inserted in the document)
- `link`: in-document link to the rendered item in the bibliography (only known when the bibliography is actually inserted in the document)

# Usage

## Text processor
The module will attempt to register text processors to allow creating reference within text. This will only work if the [TextProcessor](../../core/modules/TextProcessor) module is already loaded. Actually, the module registers one text processor `cite` that can format several things. The processor signature is `cite(ref, [format])` where ref is the unique identifier of the item to cite, and the optional format key is:

- `al`: Cite the shortened authors like "Lastname et al."
- `authors`: Cite the full list of authors
- `title`: Cite the title of the item
- `no`: Print the number of the item with the current numFormat, creating a clickable item to the rendered bibliography. Note, like all text processors, it will not be formatted if something is missing, in this case if the bibliography is not inserted in the document, no link exists to it and the text processor won't insert the number, meaning you can not use the number format if you don't insert the actual bibliography somewhere.

Other formats will be implemented in the future to look more LaTeX-ish.

## Load database
### Args
- path: relative path to the bib file to load

## Print bibliography
### Optional
- render: set to "used" to generate the bibliography only using the referenced items, or remove this key ir set any other value like "all" to generate the full database

# Examples

Load a bib file:
```
- type: bib
  path: ref.bib
```

Reference an article in text:
```
- type: text
  content: >
    Fusce pellentesque mattis dui. Vestibulum ante ipsum primis in faucibus orci luctus et {{cite(lorem2002,al)}} in {{cite(lorem2002,title)}} see {{lorem2002)}}.
```

Generate the full bibliography:
```
- type: bibliography
  render: all
```
