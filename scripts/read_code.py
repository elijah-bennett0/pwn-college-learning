from tree_sitter import Language, Parser
import tree_sitter_c
import re

parser = Parser()
parser.language = Language(tree_sitter_c.language())

code = open(input("Path to C source > "), 'rb').read()
tree = parser.parse(code)

root = tree.root_node

def walk(node, inside_main=False):
	if node.type == "function_definition":
		name = node.child_by_field_name("declarator").text.decode()
		if name.startswith("main"):
			inside_main = True

	if inside_main and node.type == "if_statement":
		text = node.text.decode()
		if "magic_number" in text:
			matches = re.findall(r"magic_number\[(\d+)\]\s*!=\s*'([^']+)'", text)
			magic_number = ''.join(x[1] for x in matches)
			print("[!] MAGIC NUMBER FOUND...")

		if "version" in text:
			print("[!] VERSION FOUND...")
			version = re.findall(r"version\s!=\s(\d+)", text)[0]

		if "width" in text:
			print("[!] WIDTH FOUND...")
			width = re.findall(r"width\s!=\s(\d+)", text)[0]

		if "height" in text:
			print("[!] HEIGHT FOUND...")
			height = re.findall(r"height\s!=\s(\d+)", text)[0]

	# Here is the size calculation:
	# unsigned long data_size = cimg.header.width * cimg.header.height * sizeof(pixel_t);
	# TODO: make a way to automatically evaluate it
	if node.type == "declaration" and node.child_by_field_name("declarator").text.decode().startswith("data_size"):
		print(node.text.decode())

	for child in node.children:
		walk(child, inside_main)



if __name__ == "__main__":
	walk(root)
