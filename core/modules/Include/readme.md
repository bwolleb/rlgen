# Description

Similar to the include instruction in many programming languages, the `include` block allows to load and insert the content of other file(s) at the current position in the document. Using this block allows to split the document in many files and include them as needed.

Including recursively a whole folder tree is also supported. In this case, the content of the directory is sorted and each entry is filtered using a regex to avoid including non-text files.

## Block types
- include: include file content or a whole folder, can be recursive

# Usage
## Args
- path: path to the file or folder to include

## Optional
- recursive: boolean, indicates to process the provided folder recursively (process all folder entries found in specified path), default is false
- match: regex used to filter files, only entries that match this expression are included, by default all files that ends with `.json` or `.yaml`.

# Example
Simple include:

```
type: include
path: chapterFive.yaml

```

Include folder recursively and filter files:

```
type: include
path: chapters
recursive: yes
match: intro_.*[.](json|yaml)$
```
