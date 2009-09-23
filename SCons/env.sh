#!/bin/bash


export YAMS_DEV_DIR=/Volumes/Development

export YAMS_CONFIG_DIR="$YAMS_DEV_DIR/Yams/Config"
export YAMS_BUILD_DIR="$YAMS_DEV_DIR/Yams/BuildDir"
export YAMS_INSTALL_DIR="$YAMS_DEV_DIR/Yams/CommonLib"
export YAMS_LIBEXT_DIR="$YAMS_DEV_DIR/CommonLibExt_darwin_gcc"
export YAMS_CODE_DIRS=$YAMS_DEV_DIR/yamsCode/:$YAMS_DEV_DIR/yamsCode/Bundles:$YAMS_DEV_DIR/yamsCode/SrcLib:$YAMS_DEV_DIR/yamsCode/launcher
