"""Static documentation and Python source audit."""
import ast
import os
import re
from pathlib import Path
from .phrases import ISMNVALIDATION, NOISMNVALIDATION, GENERIC_NAMES


def _pattern(phrases):
    return re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(x) for x in sorted(phrases, key=lambda x: (-len(x), x))) + r')(?!\w)')

YES = _pattern(ISMNVALIDATION)
NO = _pattern(NOISMNVALIDATION)


def claims(text):
    lines = []
    fence = None
    for line in text.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line[m.end():].strip():
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        lines.append(line)
    yes = no = False
    for paragraph in re.split(r'\n\s*\n', '\n'.join(lines)):
        normalized = re.sub(r'\s+', ' ', paragraph.lower().replace('n’t', ' not').replace("n't", ' not').replace('-', ' '))
        no |= bool(NO.search(normalized))
        normalized = NO.sub(' ', normalized)
        yes |= bool(YES.search(normalized))
    return yes, no


def evidence(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return False
    imports = {}
    definitions = set()
    bound = set()
    def bind(node):
        if isinstance(node, ast.Name):
            bound.add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for item in node.elts:
                bind(item)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                name = a.asname or a.name.split('.')[0]
                imports[name] = a.name if a.asname else a.name.split('.')[0]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            for a in node.names:
                imports[a.asname or a.name] = node.module + '.' + a.name
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                bind(target)
        elif isinstance(node, ast.AnnAssign):
            bind(node.target)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    bind(item.optional_vars)
    shadow = definitions | bound
    def path(node):
        if isinstance(node, ast.Name):
            if node.id in shadow:
                return None
            return imports.get(node.id)
        if isinstance(node, ast.Attribute):
            base = path(node.value)
            return base + '.' + node.attr if base else None
        return None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            resolved = path(func)
            if resolved and (resolved in {'stdnum.ismn.validate', 'stdnum.ismn.is_valid', 'stdnum.ismn.ismn_type'} or resolved.rsplit('.', 1)[-1] in GENERIC_NAMES) and resolved.rsplit('.', 1)[-1] not in definitions:
                return True
        elif isinstance(func, ast.Attribute):
            base = func.value
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and base.id in imports and base.id in shadow:
                continue
            if func.attr in definitions:
                continue
            if func.attr in GENERIC_NAMES:
                return True
            if func.attr in {'validate', 'is_valid', 'ismn_type'} and path(func.value) == 'stdnum.ismn':
                return True
    return False


def audit(root, ignore=()):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise OSError('repository is not a readable directory: ' + str(root))
    production = test = yes = no = False
    def ignored(rel):
        return any(rel == x.rstrip('/') or rel.startswith(x.rstrip('/') + '/') for x in ignore)
    def onerror(exc):
        raise exc
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=onerror):
        base = Path(directory)
        dirs[:] = [d for d in dirs if not (base / d).is_symlink() and not ignored((base / d).relative_to(root).as_posix())]
        for name in sorted(files):
            file = base / name
            rel = file.relative_to(root)
            if file.is_symlink() or ignored(rel.as_posix()):
                continue
            parts = rel.parts
            if (rel.as_posix() == 'README.md' or ('docs' in parts and file.suffix == '.md')):
                y, n = claims(file.read_text(encoding='utf-8'))
                yes |= y
                no |= n
            if file.suffix != '.py' or any(x in parts for x in ('fixtures', 'docs', 'examples')):
                continue
            is_test = 'tests' in parts or name.startswith('test_') or name.endswith('_test.py')
            if evidence(file.read_text(encoding='utf-8')):
                if is_test:
                    test = True
                else:
                    production = True
    findings = []
    if yes and not production:
        findings.append({'id': 'documented-ismn-validation-claim-false', 'severity': 'MEDIUM' if test else 'HIGH'})
    if no and production:
        findings.append({'id': 'documented-no-ismn-validation-claim-false', 'severity': 'HIGH'})
    return findings
