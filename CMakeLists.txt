cmake_minimum_required(VERSION 3.10)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS 1)

project(TreeSitter)
include_directories("${PROJECT_SOURCE_DIR}/tree-sitter/lib/src" "${PROJECT_SOURCE_DIR}/tree-sitter/lib/include")
add_library(TreeSitter SHARED 
	"${PROJECT_SOURCE_DIR}/tree-sitter/lib/src/lib.c"
	"${PROJECT_SOURCE_DIR}/free.c"
)
set_target_properties(TreeSitter
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter
		OUTPUT_NAME "tree-sitter"
)
target_include_directories(TreeSitter
  INTERFACE "${PROJECT_SOURCE_DIR}/tree-sitter/lib/include"
)

project(TreeSitterC)
add_library(TreeSitterC SHARED "${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-c/src/parser.c")
set_target_properties(TreeSitterC
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.C
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.C
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.C
		OUTPUT_NAME "tree-sitter-c"
)

project(TreeSitterJavascript)
add_library(TreeSitterJavascript SHARED 
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-javascript/src/parser.c"
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-javascript/src/scanner.c"
)
set_target_properties(TreeSitterJavascript
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.JavaScript
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.JavaScript
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.JavaScript
		OUTPUT_NAME "tree-sitter-javascript"
)

project(TreeSitterPython)
add_library(TreeSitterPython SHARED 
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-python/src/parser.c"
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-python/src/scanner.cc")
set_target_properties(TreeSitterPython
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Python
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Python
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Python
		OUTPUT_NAME "tree-sitter-python"
)

project(TreeSitterTypescript)
add_library(TreeSitterTypescript SHARED 
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-typescript/typescript/src/parser.c"
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-typescript/typescript/src/scanner.c")
set_target_properties(TreeSitterTypescript
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Typescript
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Typescript
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.Typescript
		OUTPUT_NAME "tree-sitter-typescript"
)


project(TreeSitterScss)
add_library(TreeSitterScss SHARED 
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-scss/src/parser.c"
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-scss/src/scanner.c")
set_target_properties(TreeSitterScss
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.SCSS
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.SCSS
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.SCSS
		OUTPUT_NAME "tree-sitter-scss"
)

project(TreeSitterHTML)
add_library(TreeSitterHTML SHARED 
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-html/src/parser.c"
	"${PROJECT_SOURCE_DIR}/langs-native/tree-sitter-html/src/scanner.cc")
set_target_properties(TreeSitterHTML
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.HTML
        RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.HTML
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${PROJECT_BINARY_DIR}/../TreeSitter.HTML
		OUTPUT_NAME "tree-sitter-html"
)