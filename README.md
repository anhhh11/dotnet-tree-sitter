# dotnet-tree-sitter

Dotnet bindings for [tree-sitter](https://tree-sitter.github.io/tree-sitter/).

## Cloning

Be sure to clone with `--recurse-submodules`, or run

```shell
git submodule update --init --recursive
```

if you have already cloned.

## Building

To build everything, run the `build.py` script:

```shell
python build.py
```

This will use cmake (`visual studio 2022` (tested), `gcc` not tested) for building native libraries, which are distributed as submodules.

## Usage

(these examples are somewhat taken from the [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter) repo).

### Basic parsing

Create a parser and set its language to a Python language instance.

```c#
using TreeSitter;
using TreeSitter.Python;

var language = PythonLanguage.Create();
var parser = new Parser {Language = language};
```

Parse some source code:

```c#
var tree = parser.Parse(@"
def foo():
    bar()
");
```

> NOTE: Parsing a string will convert it into UTF-16 bytes, thus all byte indices will be double the character indices in the C# string.

Inspect the resulting tree:

```c#
Debug.Assert(tree.Root.ToString() == Trim(
    @"(module (function_definition
        name: (identifier)
        parameters: (parameters)
        body: (block (expression_statement (call
            function: (identifier)
            arguments: (argument_list))))))"));
```

(`Trim` is a utility function that replaces multiple whicespace characters with a single space).

## Integrating with a new language (clone)
1. Add module to git .i.e Ruby
git submodule add https://github.com/tree-sitter/tree-sitter-ruby
2. Clone TreeSitter.C and change name .i.e TreeSitter.Ruby
3. Modify CMakeLists.txt clone new project from .i.e TreeSitter.C (CLanguage.cs -> RubyLanguage.cs, TreeSitter.C.csproj -> TreeSitter.Ruby.csproj; change content of TreeSitter.C.csproj from .C -> .Ruby)
4. Add TreeSitter.Ruby to content of tree-sitter.sln (clone TreeSitter.C and edit UUID - .i.e increase by 1)
5. Add to build.py#langs list
6. Run
```shell
python build.py
```
To compile the language native modules, as a platform-dependant (`.so`/`.dylib`/`.dll`) shared library.
7. Add test by using reference from https://tree-sitter.github.io/tree-sitter/playground


## Integrating with a new language (details)
1. Compile the language native modules, as a platform-dependant (.so/.dylib/.dll) shared library.
2. Declare the [DllImport("...")] extern IntPtr tree_sitter_LANG(); function.
3. The Language constructor must be passed the IntPtr result of calling that function.
4. Take a look at CLanguage class to see how it is done for the C language, including the helper Create function.