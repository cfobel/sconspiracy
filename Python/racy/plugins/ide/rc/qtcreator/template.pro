QT += core gui

TEMPLATE = app
TARGET = ${PRJ_NAME}
DEPENDPATH += .
INCLUDEPATH += .

HEADERS += \\

% for i in HEADERS:
    ${i} \\

%endfor

SOURCES += \\

% for i in SOURCES:
    ${i} \\

% endfor
