using System;
using System.Runtime.InteropServices;

namespace TreeSitter.SCSS
{
    public class ScssLanguage
    {    
        private const string DllName = "tree-sitter-scss";

        [DllImport(DllName)]
        private static extern IntPtr tree_sitter_scss();

        public static Language Create() => new Language(tree_sitter_scss());
    }
}