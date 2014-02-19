SET(XBMC_INCLUDE_DIR /imx6/xbmc/include)
LIST(APPEND CMAKE_MODULE_PATH /imx6/xbmc/lib/xbmc)
ADD_DEFINITIONS(-DTARGET_POSIX -DTARGET_LINUX -D_LINUX)

include(xbmc-addon-helpers)
