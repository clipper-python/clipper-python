# This is a CMake example for Python
cmake_minimum_required(VERSION 2.8.8)
project(clipper-python C CXX)
cmake_policy(SET CMP0054 NEW)

set(CMAKE_MODULE_PATH
    ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/")

FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})


if(APPLE)
find_program(PYTHON NAMES $ENV{PYTHON} ccp4-python python2.7 python.exe
                    HINTS ${CMAKE_INSTALL_PREFIX}/bin
                    PATHS [HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.7\\InstallPath])
else()
find_program(PYTHON NAMES $ENV{PYTHON} python2.7 python.exe
                    HINTS ${CMAKE_INSTALL_PREFIX}/bin
                    PATHS [HKEY_LOCAL_MACHINE\\SOFTWARE\\Python\\PythonCore\\2.7\\InstallPath])
endif()
message(STATUS "Python interpreter: ${PYTHON}")

#if(APPLE OR WIN32)
  # avoid FindPythonLibs as it can find libpython from different interpreter
  execute_process(COMMAND ${PYTHON} -c "import sys; sys.stdout.write(sys.prefix)"
                  OUTPUT_VARIABLE _PY_PREFIX
                  RESULT_VARIABLE failure)
  if (failure)
    message(FATAL_ERROR "Failed to run ${PYTHON}: ${failure}")
  endif()
  message(STATUS "Python sys.prefix: ${_PY_PREFIX}")
#  find_library(PYTHON_LIBRARY NAMES python2.7 python27 python3.6 python36 python3.6m
#               HINTS ${_PY_PREFIX}/lib ${_PY_PREFIX}/lib64 ${_PY_PREFIX}/libs
#               NO_DEFAULT_PATH)
#  if (NOT PYTHON_LIBRARY)
#    message(FATAL_ERROR "Python library not found.")
#  endif()
#  message(STATUS "Python library: ${PYTHON_LIBRARY}")
#  find_path(PYTHON_INCLUDE_DIR NAMES Python.h
#            HINTS ${_PY_PREFIX}/include
#                  ${_PY_PREFIX}/include/python2.7
#                  ${_PY_PREFIX}/include/python3.6m
#            NO_DEFAULT_PATH)
#  message(STATUS "Python.h is in: ${PYTHON_INCLUDE_DIR}")
#  if (NOT PYTHON_INCLUDE_DIR)
#    message(FATAL_ERROR "Python header not found.")
#  endif()
#  set(PYTHON_LIBRARIES ${PYTHON_LIBRARY})
#endif()

execute_process(COMMAND ${PYTHON} -c "from distutils import sysconfig; import sys; sys.stdout.write(sysconfig.get_python_inc())"
		OUTPUT_VARIABLE PYTHON_INCLUDE_DIR
                RESULT_VARIABLE failure)
message(STATUS "Python include dir: ${PYTHON_INCLUDE_DIR}")

if (failure)
  message(FATAL_ERROR "Failed to find include dir for ${PYTHON}")
endif()

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})

SET(CMAKE_SWIG_FLAGS "")

find_package(CCP4 REQUIRED mmdb2 clipper-core clipper-mmdb clipper-ccp4
                           clipper-cif clipper-minimol clipper-contrib ccp4c
                  HINTS ${CMAKE_INSTALL_PREFIX}/share)


execute_process(COMMAND ${PYTHON} -c "import numpy; import sys; sys.stdout.write(numpy.get_include())"
                OUTPUT_VARIABLE PYTHON_NUMPY_INCLUDE_PATH
                RESULT_VARIABLE failure)

message(STATUS "Numpy include dir: ${PYTHON_INCLUDE_DIR}")


if (failure)
  message(FATAL_ERROR "Failed to find Numpy include dir for ${PYTHON}")
endif()

execute_process(COMMAND ${PYTHON} -c "import sys; sys.stdout.write(str(sys.version_info.major))"
                OUTPUT_VARIABLE PYTHON_MAJOR_VERSION
                RESULT_VARIABLE failure)

set(PYTHON_VERSION_STRING python)
if (${PYTHON_MAJOR_VERSION} GREATER 2)
  set(CMAKE_SWIG_FLAGS -modern -py3)
endif()

#find_package(NumPy REQUIRED)

include_directories(${CCP4_INCLUDE_DIRS}
                    "${CCP4_INCLUDE_DIRS}/clipper"
                    "${CCP4_INCLUDE_DIRS}/clipper/core"
                    "${CMAKE_SOURCE_DIR}"
                    ${PYTHON_NUMPY_INCLUDE_PATH}
                    "${PYTHON_INCLUDE_DIR}")

SET_SOURCE_FILES_PROPERTIES(${CMAKE_SOURCE_DIR}/src/clipper_python_core.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(clipper_python_core python ${CMAKE_SOURCE_DIR}/src/clipper_python_core.i )

#SET(CMAKE_CXX_FLAGS -std=c++11)     


IF(WIN32)
    SET(SWIG_CLIPPER_MODULE_SUFFIX "pyd")
ELSE()
    SET(SWIG_CLIPPER_MODULE_SUFFIX "so")
ENDIF()

string(REGEX REPLACE "clipper-cif" "clipper-phs" CLIPPER-PHS_LIBRARY ${CLIPPER-CIF_LIBRARY})

set(PYTHON_LINKER_OPTIONS "")

if(APPLE)
  set(PYTHON_LINKER_OPTIONS "-undefined dynamic_lookup")
endif()

SWIG_LINK_LIBRARIES(clipper_python_core ${PYTHON_LINKER_OPTIONS} ${CLIPPER-MMDB_LIBRARY} ${CLIPPER-CIF_LIBRARY} ${CLIPPER-CCP4_LIBRARY}
    ${CLIPPER-CONTRIB_LIBRARY} ${CLIPPER-PHS_LIBRARY} ${CLIPPER-CORE_LIBRARIES} ${CLIPPER-MINIMOL_LIBRARY} ${MMDB2_LIBRARY} ${CCP4C_LIBRARY} m)

set ( PYTHON_MODULE_PATH ${CMAKE_INSTALL_PREFIX}/lib)
 
message(STATUS "Python module path: ${PYTHON_MODULE_PATH}")

INSTALL ( FILES ${CMAKE_CURRENT_BINARY_DIR}/_clipper_python_core.${SWIG_CLIPPER_MODULE_SUFFIX} DESTINATION ${PYTHON_MODULE_PATH} )
INSTALL ( FILES ${CMAKE_CURRENT_BINARY_DIR}/clipper_python_core.py DESTINATION ${PYTHON_MODULE_PATH} )
INSTALL ( FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/__init__.py DESTINATION ${PYTHON_MODULE_PATH} )
INSTALL ( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/ DESTINATION ${CMAKE_INSTALL_PREFIX} FILES_MATCHING PATTERN "*.py" )
INSTALL ( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/clipper_tools DESTINATION ${PYTHON_MODULE_PATH} )
