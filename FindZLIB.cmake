find_path(ZLIB_INCLUDE_DIR
    NAMES zlib.h
    PATHS ${CONAN_INCLUDE_DIRS_ZLIB}
    NO_DEFAULT_PATH
)

find_library(ZLIB_LIBRARY
    NAMES z zlib zlibd zlibstatic zlibstaticd
    PATHS ${CONAN_LIB_DIRS_ZLIB}
    NO_DEFAULT_PATH
)

if(ZLIB_INCLUDE_DIR AND EXISTS ${ZLIB_INCLUDE_DIR}/zlib.h)
    file(STRINGS ${ZLIB_INCLUDE_DIR}/zlib.h ZLIB_H REGEX "^#define ZLIB_VERSION \"[^\"]*\"$")

    string(REGEX REPLACE "^.*ZLIB_VERSION \"([0-9]+).*$" "\\1" ZLIB_VERSION_MAJOR "${ZLIB_H}")
    string(REGEX REPLACE "^.*ZLIB_VERSION \"[0-9]+\\.([0-9]+).*$" "\\1" ZLIB_VERSION_MINOR  "${ZLIB_H}")
    string(REGEX REPLACE "^.*ZLIB_VERSION \"[0-9]+\\.[0-9]+\\.([0-9]+).*$" "\\1" ZLIB_VERSION_PATCH "${ZLIB_H}")
    set(ZLIB_VERSION_STRING "${ZLIB_VERSION_MAJOR}.${ZLIB_VERSION_MINOR}.${ZLIB_VERSION_PATCH}")

    # only append a TWEAK version if it exists:
    set(ZLIB_VERSION_TWEAK "")
    if( "${ZLIB_H}" MATCHES "ZLIB_VERSION \"[0-9]+\\.[0-9]+\\.[0-9]+\\.([0-9]+)")
        set(ZLIB_VERSION_TWEAK "${CMAKE_MATCH_1}")
        string(APPEND ZLIB_VERSION_STRING ".${ZLIB_VERSION_TWEAK}")
    endif()

    set(ZLIB_MAJOR_VERSION "${ZLIB_VERSION_MAJOR}")
    set(ZLIB_MINOR_VERSION "${ZLIB_VERSION_MINOR}")
    set(ZLIB_PATCH_VERSION "${ZLIB_VERSION_PATCH}")
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(ZLIB
    REQUIRED_VARS ZLIB_LIBRARY ZLIB_INCLUDE_DIR
    VERSION_VAR ZLIB_VERSION_STRING
)

if(ZLIB_FOUND)
    set(ZLIB_INCLUDE_DIRS ${ZLIB_INCLUDE_DIR})
    set(ZLIB_LIBRARIES ${ZLIB_LIBRARY})
    mark_as_advanced(ZLIB_INCLUDE_DIR ZLIB_LIBRARY)

    if(NOT TARGET ZLIB::ZLIB)
      add_library(ZLIB::ZLIB UNKNOWN IMPORTED)
      set_target_properties(ZLIB::ZLIB PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES ${ZLIB_INCLUDE_DIRS}
        IMPORTED_LOCATION ${ZLIB_LIBRARY}
      )
    endif()

    set(_enable_minizip)
    foreach(_item ${${CMAKE_FIND_PACKAGE_NAME}_FIND_COMPONENTS})
        if(${_item} STREQUAL minizip)
            set(_enable_minizip ON)
        endif()
    endforeach()

    if(_enable_minizip)
        find_path(MINIZIP_INCLUDE_DIR
            NAMES zip.h
            PATHS ${CONAN_INCLUDE_DIRS_ZLIB}/minizip
            NO_DEFAULT_PATH
        )
    
        find_library(MINIZIP_LIBRARY
            NAMES minizip minizipd minizipstatic minizipstaticd
            PATHS ${CONAN_LIB_DIRS_ZLIB}
            NO_DEFAULT_PATH
        )
        
        set(MINIZIP_VERSION_MAJOR 1)
        set(MINIZIP_VERSION_MINOR 1)
        set(MINIZIP_VERSION_PATCH 0)
        set(MINIZIP_VERSION_STRING "${MINIZIP_VERSION_MAJOR}.${MINIZIP_VERSION_MINOR}.${MINIZIP_VERSION_PATCH}")
        
        set(MINIZIP_FIND_REQUIRED ON)
        find_package_handle_standard_args(MINIZIP
            REQUIRED_VARS MINIZIP_LIBRARY MINIZIP_INCLUDE_DIR
            VERSION_VAR MINIZIP_VERSION_STRING
        )
        
        if(MINIZIP_FOUND)
            set(MINIZIP_INCLUDE_DIRS ${MINIZIP_INCLUDE_DIR})
            set(MINIZIP_LIBRARIES ${MINIZIP_LIBRARY})
            mark_as_advanced(MINIZIP_INCLUDE_DIR MINIZIP_LIBRARY)

            if(NOT TARGET ZLIB::minizip)
                add_library(ZLIB::minizip UNKNOWN IMPORTED)
                set_target_properties(ZLIB::minizip PROPERTIES
                    INTERFACE_INCLUDE_DIRECTORIES ${MINIZIP_INCLUDE_DIR}
                    IMPORTED_LOCATION ${MINIZIP_LIBRARY}
                    INTERFACE_LINK_LIBRARIES ZLIB::ZLIB
                )
            endif()
        endif() # if(MINIZIP_FOUND)
    endif() # if(_enable_minizip)
endif() # if(ZLIB_FOUND)

