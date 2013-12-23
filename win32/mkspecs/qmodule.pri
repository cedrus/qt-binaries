QT_BUILD_PARTS += libs tools examples

DEFINES        *= QT_EDITION=QT_EDITION_DESKTOP
#Qt for Windows CE c-runtime deployment
QT_CE_C_RUNTIME = no
CONFIG += minimal-config small-config medium-config large-config full-config pcre debug compile_examples sse2 sse3 ssse3 sse4_1 sse4_2 avx largefile
QMAKE_QT_VERSION_OVERRIDE = 5
OBJECTS_DIR     = .obj/debug_shared
MOC_DIR         = .moc/debug_shared
RCC_DIR         = .rcc/debug_shared
sql-plugins    += sqlite
styles         += windows fusion windowsxp windowsvista
