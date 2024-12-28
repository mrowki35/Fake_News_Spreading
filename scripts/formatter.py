import os
import sys
import re
import textwrap


def fix_indentation(code, spaces=4):
    return code.replace('\t', ' ' * spaces)


def limit_line_length(code, max_length=80):
    lines = code.split('\n')
    new_lines = []
    for line in lines:
        if len(line) > max_length:
            wrapped = textwrap.fill(line, width=max_length, subsequent_indent=' ' * 4)
            new_lines.append(wrapped)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def remove_trailing_whitespace(code):
    lines = code.split('\n')
    new_lines = [line.rstrip() for line in lines]
    return '\n'.join(new_lines)


def sort_imports(code):
    import_lines = []
    other_lines = []
    for line in code.split('\n'):
        if line.startswith('import ') or line.startswith('from '):
            import_lines.append(line)
        else:
            other_lines.append(line)
    sorted_imports = sorted(import_lines)
    return '\n'.join(sorted_imports + [''] + other_lines)


def standardize_string_quotes(code, quote_style="'"):
    if quote_style not in ["'", '"']:
        quote_style = "'"
    pattern = r'\"([^\"]*)\"' if quote_style == "'" else r"\'([^\']*)\'"
    replacement = f"{quote_style}\\1{quote_style}"
    return re.sub(pattern, replacement, code)


def add_newline_at_eof(code):
    if not code.endswith('\n'):
        return code + '\n'
    return code


def format_code(code):
    code = fix_indentation(code)
    code = remove_trailing_whitespace(code)
    code = sort_imports(code)
    code = standardize_string_quotes(code, quote_style="'")
    code = limit_line_length(code)
    code = add_newline_at_eof(code)
    return code


def format_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        formatted_content = format_code(content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_content)
        print(f"Formatted: {file_path}")
    except Exception as e:
        print(f"Error formatting {file_path}: {e}")


def format_all_py_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                format_file(file_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python formatter.py <path_to_directory>")
    else:
        root_directory = sys.argv[1]
        format_all_py_files(root_directory)
        print(f"All .py files in {root_directory} have been formatted.")
