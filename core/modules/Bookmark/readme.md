# Description

This module is mainly useful when loaded with the [Title](../Title) module and will be automatically used to create a bookmark for each title. It can also be used to manually bookmark a position in the document. The bookmark can then be reached using its identifier, for example in a `{{ref(bookmarkname,text)}}` markup (See [TextProcessor](../TextProcessor)).

All created bookmarks uids are stored in the `resources/bookmark` map.

## Block types
- bookmark: create a bookmark that references this document position, can be used to jump to any particular position with a link

# Usage
## Args
- name: identifier of the bookmark

# Example
```
type: bookmark
name: testbookmark
```
