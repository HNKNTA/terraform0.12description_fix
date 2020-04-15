#!/usr/bin/env python3

import re
import sys


def fix_variable_definition(variable_first_line, commented_description):
    proper_description = re.sub(r"#\s", "",
                                commented_description)
    proper_description = re.sub(r"(\"\$\{)(.+)(\}\")", r"\g<2>",
                                proper_description)
    return """{}\n  description = <<EOD\n{}EOD\n""".format(variable_first_line, proper_description)


if __name__ == "__main__":
    with open(sys.argv[1], "r+") as f:
        read_file = f.read()

        found_list = re.findall(r"(#.+?)(\b(variable|output)\b\s+?\".+?\".+?\s*?\{)", read_file, re.DOTALL)

        for _tuple in found_list:
            read_file = read_file.replace(_tuple[0], '')
            read_file = read_file.replace(
                _tuple[1],
                fix_variable_definition(_tuple[1], _tuple[0])
            )

        f.seek(0)
        f.write(read_file)
        f.truncate()
