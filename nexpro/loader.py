"""Parse an entry file and resolve its NexPro imports."""

from posixpath import dirname, isabs, join, normpath

from nexpro.ast import Import, Module, Program
from nexpro.errors import ImportError, SourceError
from nexpro.lexer import Lexer
from nexpro.parser import Parser


def load_program(entry, read_source, filename_for=str):
    """Resolve legacy imports within each scope and retain isolated modules."""
    active = set()
    modules = {}

    def load(path, source, loaded):
        active.add(path)
        statements = []
        filename = filename_for(path)
        try:
            source = source.replace("\r\n", "\n").replace("\r", "\n")
            try:
                tree = Parser(Lexer(source, filename).tokenize(), filename).parse()
            except SourceError as error:
                error.locate(source)
                raise
            for node in tree.statements:
                if isinstance(node, Import):
                    statements.extend(load_import(path, source, node, loaded))
                else:
                    statements.append(node)
        finally:
            active.remove(path)
        loaded.add(path)
        return statements

    def load_import(importer, source, node, loaded):
        module = node.path
        path = normpath(join(dirname(importer), module))

        def diagnostic(message):
            error = ImportError(message, node.line, node.column, filename_for(importer))
            error.locate(source)
            return error

        if (
            not module.endswith(".pa") or isabs(module) or "\\" in module
            or ":" in module or "\0" in module or path.startswith("../")
        ):
            raise diagnostic("Expected a relative .pa module path inside the entry directory")
        if path in active:
            raise diagnostic(f"Circular import of '{path}'")
        if node.alias is None and path in loaded:
            return []
        if node.alias is None or path not in modules:
            try:
                module_source = read_source(path)
            except (OSError, UnicodeError) as error:
                message = error.strerror if isinstance(error, OSError) and error.strerror else str(error)
                raise diagnostic(f"Cannot read module '{path}': {message}") from error
            if node.alias is None:
                return load(path, module_source, loaded)
            modules[path] = load(path, module_source, set())
        imported = Module(node.alias, path)
        imported.location = node.location
        return [imported]

    program = Program(load(entry, read_source(entry), set()))
    program.modules = modules
    return program
