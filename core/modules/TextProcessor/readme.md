# Description

When a paragraph is inserted in the document using the [Text](../Text) module, its content is processed through the available text processors if this module is loaded. Text processors are special markups that allow to insert dynamic content, such as data from a resource, or the link to a chapter. As the resources are the main mechanism to track all chapters, lists, bookmarks and such, inserting it through text processors allows to do pretty much anything. Modules can also register custom text processors, as long as the TextProcessor module is loaded before them.

Using text processors is simple: write the function you want to use and its arguments (if required) in the special `{{func(arg)}}` markup, and it will be tracked and processed.

Internally, text processors can be processed at different times:
- When the paragraph is built
- Just before the document is rendered

This is necessary because some data are only available when the document has finished building, like links to further chapters or bookmarks.

## Python formatting
Alternatively, another (work in progress) way to format data in a paragraph is to provide a `format` dict in the text block, where the keys are standard formatting keys present in the text, and the values are txt processors or path to resources.

## Available text processors
- data: insert data from the specified resource, which must be stringifiable, takes the path to the resource as argument
- chapter: insert a link to the specified chapter displaying its full text (numbering and text), takes the chapter identifier as argument. A second argument allows to override the label so that the displayed text can be any field of the chapter data (original text or just the chapter number), see [Title](../Title) module.
- ref: insert a link to the specified bookmark displaying the specified text, takes the bookmark identifier and text to display
- now: insert the current datetime, the format can be specified as arg (using the python datetime strftime format) but uses "%d.%m.%Y %H:%M:%S" if nothing is provided

## Example
The block:

```
type: text
content: >
  Hello world, now is {{now()}}, so the current date is {{now(%Y-%m-%d)}}.
  See chapter {{chapter(chap2)}} for more interesting stuff about {{data(sheet2/subject)}}.
  Or go straight to the report {{chapter(chapConcl,text)}}.
  See a picture of my cat {{ref(meow,here)}}.
```
produces:
```
Hello world, now is 16.05.2021 13:37:49, so the current date is 2021-05-16. See
chapter 2.3 Algorithms for more interesting stuff about computer science. Or go
straight to the report Conclusion. See a picture of my cat here.
```

Using the special format dict:
```
type: text
content: >
  The value of pi is about {pi:.2f} but has infinite decimals! For more scientific stuff,
  go to chapter {mathChap}.
format:
  pi: mathResource/constants/piRaw
  mathChap: chapter(mathStuff)
```
produces:
```
The value of pi is about 3.14 but has infinite decimals! For more scientific stuff, go to
chapter 4.1 Advanced Maths.
```
