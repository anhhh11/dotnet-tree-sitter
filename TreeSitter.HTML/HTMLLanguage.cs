using System;
using System.Runtime.InteropServices;

namespace TreeSitter.HTML
{
    public class HtmlLanguage
    {    
        private const string DllName = "tree-sitter-html";

        [DllImport(DllName)]
        private static extern IntPtr tree_sitter_html();

        public static Language Create() => new Language(tree_sitter_html());
    }
}