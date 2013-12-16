CONFIG +=  compile_examples qpa largefile precompile_header sse2 sse3 ssse3 sse4_1 sse4_2 absolute_library_soname pcre
QT_BUILD_PARTS += libs tools examples
QT_LFLAGS_ODBC   = -lodbc
DEFINES *= QT_EDITION=QT_EDITION_DESKTOP
styles += mac fusion windows
DEFINES += QT_NO_LIBUDEV
DEFINES += QT_NO_EVDEV
DEFINES += QT_NO_XCB
DEFINES += QT_NO_XKBCOMMON
PRECOMPILED_DIR = .pch/debug-shared
OBJECTS_DIR = .obj/debug-shared
MOC_DIR = .moc/debug-shared
RCC_DIR = .rcc/debug-shared
UI_DIR = .uic/debug-shared
sql-drivers = 
sql-plugins = 
