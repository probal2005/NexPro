"""Parse an entry file and resolve its NexPro imports."""

from posixpath import dirname, isabs, join, normpath

from nexpro.ast import Import, Program
from nexpro.errors import ImportError, SourceError
from nexpro.lexer import Lexer
from nexpro.parser import Parser


def load_program(entry, read_source, filename_for=str):
    """Return a program with each imported file included at its first import."""
    loaded = set()
    active = set()
    statements = []

    def load(path, source):
        filename = filename_for(path)
        active.add(path)
        try:
            source = source.replace("\r\n", "\n").replace("\r", "\n")
            try:
                tree = Parser(Lexer(source, filename).tokenize(), filename).parse()
            except SourceError as error:
                error.locate(source)
                raise

            for statement in tree.statements:
                if isinstance(statement, Import):
                    load_import(path, source, statement)
                else:
                    statements.append(statement)
        finally:
            active.remove(path)
        loaded.add(path)

    def load_import(importer, source, statement):
        module = statement.path
        path = normpath(join(dirname(importer), module))

        def diagnostic(message):
            error = ImportError(message, statement.line, statement.column, filename_for(importer))
            error.locate(source)
            return error

        if (
            not module.endswith(".pa") or isabs(module) or "\\" in module
            or ":" in module or "\0" in module or path.startswith("../")
        ):
            raise diagnostic("Expected a relative .pa module path inside the entry directory")
        if path in active:
            raise diagnostic(f"Circular import of '{path}'")
        if path in loaded:
            return
        try:
            module_source = read_source(path)
        except (OSError, UnicodeError) as error:
            message = error.strerror if isinstance(error, OSError) and error.strerror else str(error)
            raise diagnostic(f"Cannot read module '{path}': {message}") from error
        load(path, module_source)

    load(entry, read_source(entry))
    return Program(statements)
