# Description

This hacky module is a POC for listing support, it is **not** considered stable. The module tries to mimic the listing feature of other text processors by displaying the code and highlighting the keywords. A default font name can be provided at initialization, but that's not necessary. Internally, the text is processed through a syntax processor that will detect and highlight comments, keywords, strings etc and render the result as a reportlab XPreformatted object. To make the output look neatier, you can place it in a table with a light grey background.

## Block types
- lst: insert a code listing

## Syntax
The syntax mechanism is a simple file which contains regex that allow to detect and format the language features. A syntax file should contain the following items:

- `comments`: list of regex that match single or multiline comments, this is important to disable the syntax styling within comments (you don't want your comment "Took this line from stackoverflow" to have the "from" highlighted as it is a registered python keyword).
- `match`: list of tuples containing a regex and a key. The syntax processor will detect all occurences of the regex and apply the style defined by the key.
- `italic`: list of keys that should be formatted as italic text.
- `bold`: list of keys that should be formatted as bold text.
- `color`: mapping of key -> hex color to format the matching text.

See the (partial) [python syntax](syntax/python.yaml) file for a working example.

# Usage
## Args
- content: The actual code to render (use yaml's | syntax for this)

## Optional
- font: the font name to use (you want to use mono fonts for clean code output), will use the current default font otherwise.
- syntax: the syntax to use for highlighting. Can be a string which identifies an already loaded syntax, or a dict with a `path` to the syntax file and a `name` to register it.

# Examples

Format python code with syntax highlighting:
```
type: lst
syntax: python
font: codett12
content: |
  import sys, os

  # Custom implementation, copied from stackoverflow

  class CustomThing(BaseThing):
      default_suffix = '.html'
```

Format imaginary code with a custom syntax but using the current default font:
```
type: lst
syntax:
  name: futuristic
  path: ../futuristiclang.yaml
content: |
  <|-- Wow such interesting code --|>
  var a, b, c;
  func(a);
```
