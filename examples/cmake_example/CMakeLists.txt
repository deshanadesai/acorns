cmake_minimum_required(VERSION 3.1)
project(SimpleProject)


execute_process(COMMAND
python -c "import acorns; import sys; sys.stdout.write(acorns.__path__[0])"
OUTPUT_VARIABLE ACORNS_PATH)
SET(GENERATOR_COMMAND "python3 ${ACORNS_PATH}/forward_diff.py ${PROJECT_SOURCE_DIR}/functions/function_0.c energy --vars x --func function_0 --output_filename ${PROJECT_SOURCE_DIR}/ders/der_0")

add_custom_command(
OUTPUT
    ${PROJECT_SOURCE_DIR}/ders/der_0.c
    ${PROJECT_SOURCE_DIR}/ders/der_0.h
COMMAND
    ${GENERATOR_COMMAND}
DEPENDS
    ${PROJECT_SOURCE_DIR}/functions/function_0.c
)

add_library(derivative "ders/der_0.c")
target_include_directories(derivative PUBLIC ders)

# Link target derivative to main_executable

add_executable(main_target src/example.c)
target_link_libraries(main_target PUBLIC derivative m)
