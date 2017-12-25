project(PackageTest C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(COMPONENTS)
if(ENABLE_MINIZIP)
    set(COMPONENTS minizip)
endif()

find_package(ZLIB REQUIRED ${COMPONENTS})

enable_testing()

add_executable(test_zlib_compress test_zlib_compress)
target_link_libraries(test_zlib_compress ZLIB::ZLIB)
set_target_properties(test_zlib_compress
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_zlib_compress
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_zlib_compress
)

if(ENABLE_MINIZIP)
    add_executable(test_minizip_compress test_minizip_compress.c)
    target_link_libraries(test_minizip_compress ZLIB::minizip)
    set_target_properties(test_minizip_compress
        PROPERTIES
        INSTALL_RPATH "$ORIGIN"
        BUILD_WITH_INSTALL_RPATH True
    )
    add_test(
        NAME test_minizip_compress
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
        COMMAND test_minizip_compress
    )
endif()
