QT += core gui

TEMPLATE = app
TARGET = ${PRJ_NAME}
DEPENDPATH += .
INCLUDEPATH += . \\

% for i in DEPS_INCLUDES:
    ${i}${SEP}${PRJ_NAME}${SEP} \\

%endfor


HEADERS += \\

% for i in HEADERS:
    ${i} \\

%endfor

SOURCES += \\

% for i in SOURCES:
    ${i} \\

% endfor

OTHER_FILES += \\

% for i in OTHERS_FILE:
    ${i} \\

% endfor
