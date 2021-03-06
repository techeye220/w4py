
"""A bunch of utility functions for the PSP generator.

(c) Copyright by Jay Love, 2000 (mailto:jsliv@jslove.org)

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation or portions thereof, including modifications,
that you make.

This software is based in part on work done by the Jakarta group.
"""

# PSP Error classes

class PSPParserException(Exception):
    """PSP parser error."""


# Various utility functions

def removeQuotes(s):
    return s.replace(r'%\\>', '%>')


def isExpression(s):
    """Check whether this is a PSP expression."""
    if s.startswith('<%=') and s.endswith('%>'):
        return True
    else:
        return False


def getExpr(s):
    """Get the content of a PSP expression."""
    if s.startswith('<%=') and s.endswith('%>'):
        return s[3:-2]
    else:
        return ''


def checkAttributes(tagType, attrs, validAttrs):
    """Check for mandatory and optional atributes."""
    attrs = set(attrs)
    mandatoryAttrs = validAttrs[0]
    for attr in mandatoryAttrs:  # mandatory
        try:
            attrs.remove(attr)
        except KeyError:
            raise PSPParserException('%s: Mandatory attribute %s missing'
                % (tagType, attr))
    optionalAttrs = validAttrs[1]
    for attr in attrs:
        if attr not in optionalAttrs:
            raise PSPParserException('%s: Invalid attribute %s'
                % (tagType, attr))


def splitLines(text, keepends=False):
    """Split text into lines."""
    return text.splitlines(keepends)


def startsNewBlock(line):
    """Determine whether a code line starts a new block.

    Added by Christoph Zwerschke.
    """
    line = line.strip()
    if line.startswith('#'):
        return False
    try:
        compile(line, '<string>', 'exec')
    except SyntaxError:
        try:
            compile(line + '\n    pass', '<string>', 'exec')
        except Exception:
            pass
        else:
            return True
    else:
        return False
    return line.endswith(':')


def normalizeIndentation(pySource):
    """Take a code block that may be too indented, and move it all to the left.

    See PSPUtilsTest for examples.

    First written by Winston Wolff; improved version by Christoph Zwerschke.
    """
    lines = splitLines(pySource, True)
    minIndent = None
    indents = []
    for line in lines:
        strippedLine = line.lstrip(' \t')
        indent = len(line) - len(strippedLine)
        indents.append(len(line) - len(strippedLine))
        if strippedLine.lstrip('\r\n') and not strippedLine.startswith('#'):
            if minIndent is None or indent < minIndent:
                minIndent = indent
                if not minIndent:
                    break
    if minIndent:
        pySource = ''.join([line[min(minIndent, indent):]
            for line, indent in zip(lines, indents)])
    return pySource
