using System;
using System.Runtime.InteropServices;

namespace TreeSitter.Typescript
{
    public class TypescriptLanguage
    {    
        private const string DllName = "tree-sitter-typescript";

        [DllImport(DllName)]
        private static extern IntPtr tree_sitter_typescript();

        public static Language Create() => new Language(tree_sitter_typescript());
    }
}