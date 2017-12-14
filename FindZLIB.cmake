message(STATUS "Conan: Advance FindZLIB.cmake, adjusting variable ZLIB_LIBRARY")

list(GET CONAN_LIBS_ZLIB 0 _zlib_name)
find_library(ZLIB_LIBRARY
    NAMES ${_zlib_name}
    PATHS ${CONAN_LIB_DIRS_ZLIB}
    NO_DEFAULT_PATH
)

include(${CMAKE_ROOT}/Modules/FindZLIB.cmake)

if(ZLIB_FOUND)
    message(STATUS "Conan: ZLIB_INCLUDE_DIRS => ${ZLIB_INCLUDE_DIRS}")
    message(STATUS "Conan: ZLIB_LIBRARIES => ${ZLIB_LIBRARIES}")
    get_target_property(INTERFACE_INCLUDE_DIRECTORIES ZLIB::ZLIB INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS "Conan: ZLIB::ZLIB INTERFACE_INCLUDE_DIRECTORIES => ${INTERFACE_INCLUDE_DIRECTORIES}")
    get_target_property(IMPORTED_LOCATION ZLIB::ZLIB IMPORTED_LOCATION)
    message(STATUS "Conan: ZLIB::ZLIB IMPORTED_LOCATION => ${IMPORTED_LOCATION}")
    
    unset(INTERFACE_INCLUDE_DIRECTORIES)
    unset(IMPORTED_LOCATION)

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
    
        foreach(_item ${CONAN_LIBS_ZLIB})
            set(_minizip_name)
            if(${_item} MATCHES "minizip")
                set(_minizip_name ${_item})
            endif()
        endforeach()
        find_library(MINIZIP_LIBRARY
            NAMES ${_minizip_name}
            PATHS ${CONAN_LIB_DIRS_ZLIB}
            NO_DEFAULT_PATH
        )
        
        set(MINIZIP_FIND_REQUIRED ON)
        include(${CMAKE_ROOT}/Modules/FindPackageHandleStandardArgs.cmake)
        find_package_handle_standard_args(MINIZIP
            REQUIRED_VARS MINIZIP_LIBRARY MINIZIP_INCLUDE_DIR
        )
        
        if(MINIZIP_FOUND)
            set(MINIZIP_INCLUDE_DIRS ${MINIZIP_INCLUDE_DIR})
            set(MINIZIP_LIBRARIES ${MINIZIP_LIBRARY})

            if(NOT TARGET ZLIB::minizip)
                add_library(ZLIB::minizip UNKNOWN IMPORTED)
                set_target_properties(ZLIB::minizip PROPERTIES
                    INTERFACE_INCLUDE_DIRECTORIES "${MINIZIP_INCLUDE_DIRS}"
                    IMPORTED_LOCATION "${MINIZIP_LIBRARIES}"
                    INTERFACE_LINK_LIBRARIES "ZLIB::ZLIB"
                )
            endif()

            mark_as_advanced(MINIZIP_INCLUDE_DIR MINIZIP_LIBRARY)

            message(STATUS "Conan: MINIZIP_INCLUDE_DIRS => ${MINIZIP_INCLUDE_DIRS}")
            message(STATUS "Conan: MINIZIP_LIBRARIES => ${MINIZIP_LIBRARIES}")
            get_target_property(INTERFACE_INCLUDE_DIRECTORIES ZLIB::minizip INTERFACE_INCLUDE_DIRECTORIES)
            message(STATUS "Conan: ZLIB::minizip INTERFACE_INCLUDE_DIRECTORIES => ${INTERFACE_INCLUDE_DIRECTORIES}")
            get_target_property(IMPORTED_LOCATION ZLIB::minizip IMPORTED_LOCATION)
            message(STATUS "Conan: ZLIB::minizip IMPORTED_LOCATION => ${IMPORTED_LOCATION}")
            
            unset(INTERFACE_INCLUDE_DIRECTORIES)
            unset(IMPORTED_LOCATION)
        endif()

    endif()

endif()

unset(_zlib_name)
unset(_enable_minizip)
unset(_item)
