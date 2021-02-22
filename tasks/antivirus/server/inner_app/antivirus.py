#!/usr/bin/env python3

import sys
import os
import importlib.util


ext = sys.argv[1]
path = sys.argv[2]


script = os.path.dirname(os.path.realpath(__file__))
plugin = os.path.join(script, "plugins", f"{ext}.py")
spec = importlib.util.spec_from_file_location("checker", plugin)
module = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(module)
except FileNotFoundError:
    print(f"Не удалось проверить файл {path}: плагин {plugin} не найден")
    raise

try:
    virus = module.check(path)
except:
    print(f"Не удалось проверить файл {path}")
    raise

if virus is not None:
    print(virus)
    sys.exit(2)
else:
    sys.exit(0)

