# Module Interface
All modules should inherit the `ModuleInterface` to ensure keeping the module mechanism consistent and full-featured. A typical module inheriting the `ModuleInterface` **must**:

- call the `ModuleInterface` constructor providing the `Engine` as parameter
- reimplement the `identifier` method that returns a unique module identifier as string

**should** (in case it processes blocks):

- set the appropriate `mandatoryArgs` for associated block type(s) (see below)
- reimplement the `handles` method that returns a list of block types that can be processed through this module
- reimplement the `process` method that actually transforms the block to reportlab flowable objects

**can**

- reimplement the `validate` method to provide a more accurate block check

**should not**

- change the `processBlock` method

## Processing blocks
Each block processed by the engine is basically a map / python dict which contains key-value data. In order to process them properly, they should all define a `type`. When modules are instanciated, the engine asks them which block type they are able to process by calling their `handles` method, and maintains a mapping that allow to call the right module when a certain block type is encountered.

Each time a block is processed through the engine, its block type is read and the appropriate module is called through the `processBlock` -> `process` mechanism of the module system.

The current implementation won't work correctly if a certain block type is handled by several modules. The type-to-module mapping is dumb and the latest loaded module will replace the existing one(s).

When processing a block, a basic check is operated by the ModuleInterface through the `validate` method, using the `mandatoryArgs` list/dict. This structure allows to define keys that have to exist in the current processed block. For example a `text` block must have a `content` key whose value is the actual text to insert, and a text block without content has no sense and is mostly caused by a user mistake (mistyping `content` for example), and an error is displayed.

- If `mandatoryArgs` is a list, all its value must exist in all processed block, this is the most simple way to check input.
- If `mandatoryArgs` is a dict, the keys must be the specific block `type` to check and the values for each should be a list of mandatory keys for associated block type. This is useful when a module can process several block types which have different mandatory content.
- If necessary, the whole `validate` method can be reimplemented if the simple "keys exist in input block" is not sufficient and the input must be check in a more deep way.

# Callbacks
Callbacks are one of the most important mechanism to allow the plugins to fulfill their role, as some features require to be able to trigger specific functions at a specific time.

For example, the [PageCounter](core/modules/PageCounter) module is responsible of providing `pageNum` and `pageTot` variables at build time which allows to print a "page x of y" decoration on each page of the document. This module works by registering the following callbacks:

- when the build begins, to create the `pageNum` variable
- when the build ends, to set the `pageTot` variable
- when each page begins, to increment the `pageNum` variable

And many other tricks are done this way. Callbacks can be registered on many places, even on modules themselves. In fact, as the ModuleInterface is able to run callbacks before and after each processed block, one can register a callback each time a specific block is encountered. The following callbacks are currently defined:

- beforeBuildCallbacks: offered by the `Engine`, these callbacks are called immediately before calling reportlab's build mechanism and receive the `Engine` instance, the `DocTemplate` instance and the whole list of blocks passed to reportlab. For example, the [PageCounter](core/modules/PageCounter) module uses it add its special flowable at the very end of the build list.

- buildBeginCallbacks: offered by the `Engine` (through the special `BuildTrigger` flowable), these callbacks are called at the beginning of each reportlab build, which means several times until all indexing flowables are satisfied, and receive the `Engine` instance and the `DocTemplate` instance. For example, the [PageCounter](core/modules/PageCounter) module uses it to create the `pageNum` variable.

- buildEndCallbacks: offered by the `Engine` (through the special `BuildTrigger` flowable), these callbacks are called at the end of each reportlab build, which means several times until all indexing flowables are satisfied, and receive the `Engine` instance and the `DocTemplate` instance. For example, the [PageCounter](core/modules/PageCounter) module uses it to set the `pageTot` variable.

- pageBeginCallbacks: offered by the `Engine` (through the `DocTemplate`), these callbacks are called at the beginning of each page and receive the `Engine` instance, the `DocTemplate` instance and the reportlab `Canvas`. For example, the [PageCounter](core/modules/PageCounter) module uses it to increment the `pageNum` variable.

- pageEndCallbacks: offered by the `Engine` (through the `DocTemplate`), these callbacks are called at the end of each page and receive the `Engine` instance, the `DocTemplate` instance and the reportlab `Canvas`. For example, the [Decorator](core/modules/Decorator) module uses it to draw page decorations.

- beforeLastBuildCallbacks: offered by the [PageCounter](core/modules/PageCounter) module, these callbacks are called when the second-to-last builds begin (all except the first one) and receive the `Engine` instance and the `DocTemplate` instance. For example, the [Image](core/modules/Image) module uses it for its internal rendering optimization.

- buildTextCallbacks: offered by the [Text](core/modules/Text) module, these callbacks are called each time a `Paragraph` is built and receive the `Paragraph` and the text block (if available, can be none). For example, the [TextProcessor](core/modules/TextProcessor) module uses it to dynamically process the text if it contains special markups or formatting instructions.

- beforeProcessCallbacks: offered by the `ModuleInterface` and therefore by each module inheriting it, these callbacks are called immediately before processing a block whose type can be processed by the module and they receive the module, the block and the current path. For example, the [Debug](core/modules/Debug) module uses it to debug the block content of certain types before processing.

- afterProcessCallbacks: offered by the `ModuleInterface` and therefore by each module inheriting it, these callbacks are called immediately after processing a block whose type can be processed by the module and they receive the module, the block the current path and the resulting built blocks. For example, the [Debug](core/modules/Debug) module uses it to debug the block content of certain types after processing.

# Engine
The engine is the central entity of the document and is mostly an interface that allows all modules to communicate, and contains document properties like page styles, font styles and resources. It is also responsible of calling a few callbacks and rendering the final PDF document (by calling reportlab's build mechanism).

The `Engine` class itself is actually quite dumb, as it contains almost no logic. As much as possible, all logic and special reportlab tricks should be implemented in modules and their own special flowables, or possibly on the custom `DocTemplate` if necessary.

As the engine is a stateful object, an instance of it should generate no more than a document, or a clear method should be implemented in the engine and the modules, which are also stateful objects.

# Module dependencies
When module are created, the `engine` is provided, which allows to interact with the document properties. However, each module should work independently of other modules. The modules are loaded explicitely, so a specific module may not be loaded by a document if its features are not required, so a module should not hardly depend on other.

Exceptions exist with modules which are considered essential, such as the [PageStyle](core/modules/PageStyle), [ModuleLoader](core/modules/ModuleLoader), [Text](core/modules/Text) and such, as the engine can not even build a document without them.

Of course, it is possible to interact or even, sometimes, require another module for a specific functionality. For example, the [Title](core/modules/Title) module will try to interact with the [Bookmark](core/modules/Bookmark) and the [TocEntry](core/modules/TocEntry) modules in order to create a PDF bookmark for the title and insert an entry in the table of content.

The preffered way to do this is to call the `getModule` method of the `Engine` providing the unique module identifier. If the module is loaded, it is returned and can be used normally, otherwise a null value is returned and the caller must try to work without it. In some cases, the dependent module is necessary to work, and passing `load=True` to the `getModule` method will try to load in place (which could still fail though). Keeping the example, the [Title](core/modules/Title) module depends on the [Text](core/modules/Text) module to actually insert the title as displayable text in the document, but this is fine as the [Text](core/modules/Text) module is considered essential.

TL;DR Try to avoid hard dependencies on non-essential modules
