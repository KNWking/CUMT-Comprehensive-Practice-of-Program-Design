# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\proj01_myCalculator_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\proj01_myCalculator_autogen.dir\\ParseCache.txt"
  "proj01_myCalculator_autogen"
  )
endif()
