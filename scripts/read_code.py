from tree_sitter import Language, Parser
import tree_sitter_c
import re

parser = Parser()
parser.language = Language(tree_sitter_c.language())

code = open(input("Path to C source > "), "rb").read()
tree = parser.parse(code)

root = tree.root_node
symbols = {}
header_fields = []

type_sizes = {
	"char": 1,
	"uint8_t": 1,
	"uint16_t": 2,
	"uint32_t": 4,
	"uint64_t": 8,
}

def walk(node, inside_main=False, inside_header=False):
	if node.type == "struct_specifier":
		name_node = node.child_by_field_name("name")
		inside_header = name_node is not None and name_node.text.decode() == "cimg_header"

	if inside_header and node.type == "field_declaration":
		text = node.text.decode().strip().rstrip(";")
		parts = text.split()

		if len(parts) >= 2:
			typ = parts[0]
			name = parts[1]

			if typ not in type_sizes:
				return

			array = re.search(r"(\w+)\[(\d+)\]", name)
			if array:
				field = array.group(1)
				size = int(array.group(2)) * type_sizes[typ]
			else:
				field = name
				size = type_sizes[typ]

			header_fields.append((field, size))

	if node.type == "function_definition":
		name = node.child_by_field_name("declarator").text.decode()
		if name.startswith("main"):
			inside_main = True

	if inside_main and node.type == "if_statement":
		text = node.text.decode()

		if "magic_number" in text:
			matches = re.findall(r"magic_number\[(\d+)\]\s*!=\s*'([^']+)'", text)
			symbols["magic_number"] = ''.join(x[1] for x in matches)

		for child in node.children:
			if child.type == "parenthesized_expression":
				for expr in child.children:
					if expr.type == "binary_expression":
						varName = expr.child_by_field_name("left")
						varVal = expr.child_by_field_name("right")

						if varName and varVal and varVal.type == "number_literal":
							symbols[varName.text.decode()] = int(varVal.text.decode(), 0)
							print(f"[!] VALUE FOUND: {varName.text.decode()} = {varVal.text.decode()}")

	if node.type == "declaration" and node.child_by_field_name("declarator").text.decode().startswith("data_size"):
		text = node.text.decode()
		size_expr = text.split("=", 1)[1].strip().rstrip(";")

		for name in sorted(symbols, key=len, reverse=True):
			size_expr = size_expr.replace(name, str(symbols[name]))

		size_expr = size_expr.replace("sizeof(pixel_t)", "1")
		size = eval(size_expr)
		print("SIZE:", size)

		header = b""

		for field, field_size in header_fields:
			if field == "magic_number":
				header += symbols[field].encode()
			else:
				for name, val in symbols.items():
					if name.endswith("." + field):
						header += val.to_bytes(field_size, "little")
						break

		payload = header + b"A" * size

		with open("/tmp/payload.cimg", "wb") as f:
			f.write(payload)

		print("[!] Payload written to /tmp/payload.cimg")

	for child in node.children:
		walk(child, inside_main, inside_header)


if __name__ == "__main__":
	walk(root)
