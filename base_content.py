"""Read legacy content definitions without executing its writing loops."""
import ast
from pathlib import Path
_source=Path(__file__).with_name('build_v10.py')
_tree=ast.parse(_source.read_text())
_definitions=ast.Module(body=[n for n in _tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))],type_ignores=[])
exec(compile(_definitions,str(_source),'exec'),globals())
