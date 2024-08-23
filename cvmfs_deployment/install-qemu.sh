#!/bin/bash -ex
QEMU_RELS="https://github.com/multiarch/qemu-user-static/releases/download/"
VER="$1"
SET_LATEST=true
[ "${2}" != "true" ] && SET_LATEST=false

if [ "$VER" = "" ] ; then
  echo "ERROR: Missing qemu version."
  exit 1
fi

source $(dirname $0)/utils.sh
INST_DIR="${CVMFS_BASEDIR}/proot"

if [ ! -d ${INST_DIR}/${VER} ] ; then
  mkdir -p $VER
  for arch in ppc64le aarch64 ; do
    wget -O $VER/qemu-${arch} "${QEMU_RELS}/${VER}/qemu-${arch}-static"
    chmod +x $VER/qemu-${arch}
  done
fi
cvmfs_transaction /proot
if [ -d $VER ] ; then
  mkdir -p $INST_DIR
  mv $VER $INST_DIR/$VER
fi
if $SET_LATEST ; then
  ln -sf $VER ${INST_DIR}/latest
fi
cvmfs_server publish
