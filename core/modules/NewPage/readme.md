# Description

Jump to next page. Internally, the page will only break if there is less than 90% space left on the current page, according to currnt page style. This allows to avoid having two blank page if reportlab already decided to break the current page.

Without argument, the next page will use the same page style, and using the `nextPage` key allows to switch page style. The value can either be the identifier of an existing page style or an object that defines the page style to use, same format as defining a page style the normal way, see [PageStyle](../PageStyle).

## Block types
- newpage: insert a page break, using current page style or a custom one

# Usage
## Optional
- nextPage: identifier of the page style or specification of the page style to use for the next page

## Example
Simple page break:
```
type: newpage
```

Switch to landscape:
```
type: newpage
nextPage: landscape
```

Switch to a new page style:
```
type: newpage
nextPage:
  name: a4_landscape
  size: A4
  orientation: landscape
  frames:
    - margin_left: 5
      margin_right: 5
      margin_top: 5
      margin_bottom: 5
```
