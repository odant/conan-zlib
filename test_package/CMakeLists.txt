project(PackageTest C)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(COMPONENTS)
if(ENABLE_MINIZIP)
    set(COMPONENTS minizip)
endif()

find_package(ZLIB REQUIRED COMPONENTS ${COMPONENTS})

enable_testing()

add_executable(test_zlib test_zlib.c)
target_link_libraries(test_zlib ZLIB::ZLIB)
set_target_properties(test_zlib
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_zlib
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_zlib
)

if(ENABLE_MINIZIP)
    add_executable(test_minizip test_minizip.c)
    target_link_libraries(test_minizip ZLIB::minizip)
    set_target_properties(test_minizip
        PROPERTIES
        INSTALL_RPATH "$ORIGIN"
        BUILD_WITH_INSTALL_RPATH True
    )
    add_test(
        NAME test_minizip
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
        COMMAND test_minizip
    )
endif()

