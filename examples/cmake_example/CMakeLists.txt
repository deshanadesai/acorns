cmake_minimum_required(VERSION 2.8.9)
project(directory_test)

# Tell CMake to run python from the directory where this CMakeLists file exists.
execute_process(COMMAND python3 ext/forward_diff.py functions/func_1.c energy -ccode True -second_der False --vars a -func function_0 --output_filename ders/der_1
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

#However, the file(GLOB...) allows for wildcard additions:
file(GLOB SOURCES "src/*.c" "ders/*.c")
 
add_executable(example ${SOURCES})

target_link_libraries(example m)
