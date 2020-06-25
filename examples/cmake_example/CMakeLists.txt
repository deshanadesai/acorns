cmake_minimum_required(VERSION 3.1)
project(SimpleProject)

add_custom_command(
OUTPUT
    ${PROJECT_SOURCE_DIR}/ders/der_0.c
    ${PROJECT_SOURCE_DIR}/ders/der_0.h
COMMAND
    acorns_autodiff
        ${PROJECT_SOURCE_DIR}/functions/function_0.c energy
        --vars x --func function_0
        --output_filename ${PROJECT_SOURCE_DIR}/ders/der_0
DEPENDS
    ${PROJECT_SOURCE_DIR}/functions/function_0.c
)
add_library(derivative "ders/der_0.c")
target_include_directories(derivative PUBLIC ders)

add_executable(main_target src/example.c)

# Link target derivative to main_executable
target_link_libraries(main_target PUBLIC derivative)
