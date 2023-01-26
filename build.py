from subprocess import run
from node_generator import generate
import os

langs = [
	("c", "C"),
	("javascript", "JavaScript"),
	("python", "Python"),
	("scss", "SCSS"),
	("html", "HTML"),
	("typescript", "Typescript")
]

def generate_lang(native_name, cs_name):
    print(" -- building", native_name, "language support")
    print("    -- building native library")
    native_dir = f"langs-native/tree-sitter-{native_name}/src"
    dotnet_dir = f"TreeSitter.{cs_name}"
    print("    -- generating support code")
    if not os.path.exists(native_dir):
        native_dir = f"langs-native/tree-sitter-{native_name}/{native_name}/src"
    generate(f"{native_dir}/node-types.json", f"{dotnet_dir}/Generated.cs", cs_name)

def main():
	if not os.path.exists("./build"):
		os.makedirs("./build")
	print(" -- building main & natives libraries")
	run(["cmake", "../"], check=True, cwd="./build")
	run(["cmake", "--build", ".", "--config", "release"], check=True, cwd="./build")
	print(" -- generate libraries' types")
	for (native_name, cs_name) in langs:
		generate_lang(native_name, cs_name)
	print(" -- building dotnet libraries")
	run(["dotnet", "build"], check=True)

if __name__ == '__main__':
    main()
