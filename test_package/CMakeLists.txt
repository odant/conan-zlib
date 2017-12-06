project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(COMPONENTS)
if(ENABLE_MINIZIP)
    set(COMPONENTS minizip)
endif()

find_package(ZLIB REQUIRED ${COMPONENTS})

add_executable(test_zlib test_zlib.cpp)
target_link_libraries(test_zlib ZLIB::ZLIB)
enable_testing()
add_test(
    NAME test_zlib
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_zlib
)

if(ENABLE_MINIZIP)
    add_executable(test_minizip test_minizip.cpp)
    target_link_libraries(test_minizip ZLIB::ZLIB ZLIB::minizip)
    enable_testing()
    add_test(
        NAME test_minizip
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
        COMMAND test_minizip
    )
endif()