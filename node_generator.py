import json
import re
from pprint import pprint

PREAMBLE = """//----------------------
// <auto-generated>
//     Generated by node_generator.py
//     source: {source}
// </auto-generated>
//----------------------

#nullable enable

using System.Linq;

namespace {ns} {{

    public abstract class {langclass}
    {{{convertMethod}
    
        public string Kind {{ get; set; }}

        protected {langclass}(TreeSitter.Node node)
        {{
            Kind = node.Kind;
        }}
    }}
    
    public class {stringclass} : {langclass}
    {{
        public {stringclass}(TreeSitter.Node node) : base(node)
        {{
        }}
    }}
    
    public class ErrorNode : {langclass}
    {{
        public ErrorNode(TreeSitter.Node node) : base(node)
        {{
        }}
    }}
"""

CONVERT_METHOD_CASE = """
                case "{name}": return new {classname}(node);"""

CONVERT_METHOD = """
        public static {langclass} FromNode(TreeSitter.Node node) {{
            if (node is null) throw new System.ArgumentNullException(nameof(node));
            if (!node.IsNamed) return new {stringclass}(node);
            switch (node.Kind) {{{cases}
                case "ERROR": return new ErrorNode(node);
                default: throw new System.ArgumentException("unknown node type: " + node.Kind, nameof(node));
            }}
        }}
"""

IFACE_HEADER = """
    public interface {name}{supertypes}
    {{
    }}
"""

CLASS_HEADER = """
    public class {name} : {supertypes}
    {{"""


CLASS_FIELD_EXACT = """
            this.{fieldName} = new {fieldType}(node.ChildByFieldName("{origName}"));"""

CLASS_FIELD_UNKNOWN = """
            this.{fieldName} = ({fieldType}) {langclass}.FromNode(node.ChildByFieldName("{origName}"))!;"""

CLASS_OPT_EXACT = """
            {{
                var tmp = node.ChildByFieldName("{origName}");
                this.{fieldName} = tmp is null ? null : new {bfType}(tmp);
            }}"""

CLASS_OPT_UNKNOWN = """
            {{
                var tmp = node.ChildByFieldName("{origName}");
                this.{fieldName} = tmp is null ? null : ({bfType}) {langclass}.FromNode(tmp);
            }}"""

GETTER_FIELD = """node.ChildrenByFieldName("{origName}")"""
GETTER_CHILDREN = """node.NamedChildrenWithFields
                .Where(x => x.Key == null && !x.Value.IsExtra)
                .Select(x => x.Value)
                """

CLASS_MULTI_EXACT = """
            this.{fieldName} = {getter}.Select(x => new {bfType}(x));"""

CLASS_MULTI_UNKNOWN = """
            this.{fieldName} = {getter}.Select(x => ({bfType}) {langclass}.FromNode(x)!);"""

CLASS_FIELD_MAP = {
    ("x", None): CLASS_FIELD_EXACT,
    ("u", None): CLASS_FIELD_UNKNOWN,
    ("x", "?"): CLASS_OPT_EXACT,
    ("u", "?"): CLASS_OPT_UNKNOWN,
    ("x", "*"): CLASS_MULTI_EXACT,
    ("u", "*"): CLASS_MULTI_UNKNOWN,
}

CLASS_CTOR = """
        public {name}(TreeSitter.Node node) : base(node)
        {{
            System.Diagnostics.Debug.Assert(node.Kind == "{origName}");
            {fields}
        }}"""

CLASS_FIELD = """
        public {type} {name} {{ get; set; }}"""

CLASS_FOOTER = """
    }}
"""

FILE_FOOTER = "}}"

SNAKE_RE = re.compile(r"_(.)")


def to_camel_case(name: str):
    return SNAKE_RE.sub(lambda m: m.group(1).upper(), name)


def to_pascal_case(name: str):
    name = to_camel_case(name)
    return name[0].upper() + name[1:]


def to_type_name(name: str):
    isInterface = False
    if name[0] == "_":
        isInterface = True
        name = name[1:]
    name = to_pascal_case(name)
    if isInterface:
        name = "I" + name
    return isInterface, name


# def deduce_type(children: list, default):
#     if not children:
#         return default
#     elif len(children) == 1:
#         return children[0]["type"]
#     raise Exception()


def generate(inputFile, outputFile, langname):
    with open(inputFile) as f:
        data = json.load(f)

    ns = "TreeSitter." + langname + ".Nodes"

    supertypes = {}
    abstract = set()
    fields = {}
    concrete = set()

    for typ in data:
        name = typ["type"]
        named = typ["named"]

        if "subtypes" in typ:
            abstract.add(name)
            for subtype in typ["subtypes"]:
                v = supertypes.setdefault(subtype["type"], [])
                v.append(name)
        elif named:
            concrete.add(name)

        if "fields" in typ or "children" in typ:
            fields[name] = []
            children = [("children", typ["children"])] if "children" in typ else []
            for k, v in list(typ.get("fields", {}).items()) + children:
                cardinal = None
                if v["multiple"]:
                    cardinal = "*"
                elif not v["required"]:
                    cardinal = "?"

                fields[name].append((k, v["types"], cardinal))

    langclass = langname + "LanguageNode"
    stringclass = langclass + "TerminalNode"

    with open(outputFile, "w") as f:
        convertCases = [
            CONVERT_METHOD_CASE.format(name=name, classname=to_type_name(name)[1])
            for name in concrete
        ]
        convertMethod = CONVERT_METHOD.format(
            langclass=langclass,
            stringclass=stringclass,
            cases="".join(convertCases),
        )
        f.write(
            PREAMBLE.format(
                source=inputFile,
                ns=ns,
                langclass=langclass,
                stringclass=stringclass,
                convertMethod=convertMethod,
            )
        )

        for typ in data:
            if not typ["named"]:
                continue
            name = typ["type"]
            _, classname = to_type_name(typ["type"])
            isInterface = name in abstract
            if isInterface:
                st = supertypes.get(name, ())
                if st:
                    st = " : " + ", ".join(to_type_name(x)[1] for x in st)
                else:
                    st = ""
                f.write(IFACE_HEADER.format(name=classname, supertypes=st))
            else:
                st = [langclass] + supertypes.get(name, [])
                st = ", ".join(to_type_name(x)[1] for x in st)
                f.write(CLASS_HEADER.format(name=classname, supertypes=st))

                ctorConv = []

                for fieldName, fieldTypes, fieldCard in fields.get(name, ()):
                    if len(fieldTypes) > 1:
                        if all(not x["named"] for x in fieldTypes):
                            fieldType = stringclass
                            typeConv = "x"
                        else:
                            # todo: detect least upper bound
                            fieldType = langclass
                            typeConv = "u"
                    else:
                        fieldType = fieldTypes[0]
                        if fieldType["named"]:
                            typeConv = "u" if fieldType["type"] in abstract else "x"
                            fieldType = to_type_name(fieldType["type"])[1]
                        else:
                            fieldType = stringclass
                            typeConv = "x"

                    bfType = fieldType
                    cardConv = None
                    if fieldCard == "*" or fieldName == "children":
                        fieldType = "System.Collections.Generic.IEnumerable<" + fieldType + ">"
                        cardConv = "*"
                    elif fieldCard == "?":
                        fieldType = fieldType + "?"
                        cardConv = "?"

                    resName = to_pascal_case(fieldName)
                    if resName == classname:
                        resName = "The" + resName
                    f.write(CLASS_FIELD.format(type=fieldType, name=resName))
                    ctorConv.append(
                        (typeConv, cardConv, fieldName, resName, fieldType, bfType)
                    )

                fieldsString = "".join(
                    CLASS_FIELD_MAP[tc, cc].format(
                        fieldName=fieldName,
                        fieldType=fieldType,
                        origName=origName,
                        langclass=langclass,
                        bfType=bfType,
                        getter=GETTER_CHILDREN
                        if origName == "children"
                        else GETTER_FIELD.format(origName=origName),
                    )
                    for tc, cc, origName, fieldName, fieldType, bfType in ctorConv
                )
                f.write(
                    CLASS_CTOR.format(
                        fields=fieldsString,
                        name=classname,
                        origName=name,
                    )
                )

                f.write(CLASS_FOOTER.format())

        f.write(FILE_FOOTER.format())


if __name__ == "__main__":
    import sys

    generate(*sys.argv[1:])
