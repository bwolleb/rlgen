# Description

Allows to iterate on a resource, kind of like a foreach in programming languages. The blocks in `content` will be built for each item. Loops can be nested or combined with other special blocks like a [Condition](../Condition) to generate richer content. Iterable resources are usually lists, but dicts are supported as well. In this case, the block must have a `keys` list.

Inside the loop, it is possible to access to the following special resources:

- itemid: identifier of the current item (index for lists, key for dicts)
- currentitem: current item
- nbitems: total number of items
- loops/loopid: dict containing the data above, this is mostly useful for nested loops so blocks can use the data for any loop level

It is also possible to provide a `prefix` to use for these special resources so that `itemid`, `currentitem` and `nbitems` don't overlap. Once the iteration ends, these resources are destroyed.

Warning, no check is performed on resource creation/deletion, therefore `itemid`, `currentitem` and `nbitems` will be inconsistent if no prefix is given in nested loops.

## Block types
- loop: loop over a resource and render blocks at each iteration

# Usage
## Args
- data: path to the resource to iterate, must be either a list or a dict
- content: blocks to build for each item of the loop

## Optional
- id: give an identifier to the loop so that it is possible to access any `loop/loopid` resource in nested loops. By default, a unique id is generated
- prefix: specify a prefix for the first-level `itemid`, `currentitem` and `nbitems` resources, mostly useful for nested loops
- keys: list of keys when iterating on a dict, useless for a list

# Example
Simple iteration on a dict:

```
type: loop
data: test/looptest1
keys: [abc, def, ghi]
content:
  - type: text
    content: "id: {{data(itemid)}}, data: {{data(currentitem)}} of {{data(nbitems)}}"
```

Iterate on a list, build richer blocks using a condition:
```
type: loop
data: test/looptest2
content:
  - type: text
    content: "id: {{data(itemid)}}, data: {{data(currentitem)}} of {{data(nbitems)}}"
  - type: if
    condition: "itemid < 2"
    then:
      - type: text
        content: before third item
    else:
      - type: text
        content: after third item
```

Nested loops, each item of looptest3 is a list, using both `prefix` and `loopid` ways to get item data:

```
type: loop
id: myloop1
prefix: myloop1_
data: test/looptest3
content:
  - type: text
    content: "List {{data(myloop1_itemid)}} of {{data(loops/myloop1/nbitems)}}"
  - type: loop
    id: myloop2
    prefix: myloop2_
    data: myloop1_currentitem
    content:
      - type: text
        content: "Item {{data(myloop2_itemid)}} of {{data(loops/myloop2/nbitems)}}: {{data(loops/myloop2/currentitem)}}"
```
