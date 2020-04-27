#!/bin/bash

# default without xml suffix
SEED_TEMPLATE="idv-template"
XML_SUFFIX=".xml"

# target preix
TARGET_PREFIX="inst"

# target suffix
TARGET_SUFFIX=".qcow2"

# target virtual machine name prefix
TARGET_VM_NAME="demo"

# stub names
INST_IMAGE_STUB="inst-image-stub"
BASE_IMAGE_STUB="base-image-stub"
VM_NAME_STUB="vmstubname"
EDIT_BASE_STUB="edit-base-stub"
UUID_CODE_STUB="uuidstubcode"
MACADDR_CODE_STUB="macstubcode"

print_usage()
{
	echo "Usage : $0 [-e edit_image] <-b base_image> [-t template] [-n number] [-h]"
	exit 1
}

# default values
BASE_IMAGE="nop-base"
EDIT_IMAGE="nop-edit-base"
NUMBER=1

while getopts "b:e:t:n:h" flag; do
	case $flag in
		e) EDIT_IMAGE="$OPTARG" ;;
		b) BASE_IMAGE="$OPTARG" ;;
		t) SEED_TEMPLATE="$OPTARG" ;;
		n) NUMBER="$OPTARG" ;;
		h) print_usage $0 ;;
		*) print_usage $0 ;;
	esac
done

[ $EDIT_IMAGE != "nop-edit-base" ] && BASE_IMAGE=$EDIT_IMAGE && NUMBER=1

[ $BASE_IMAGE == "nop-base" ] && echo "No base, exit" && exit 1
[ $SEED_TEMPLATE == "idv-template" ] && echo "No template, using $SEED_TEMPLATE"
echo "Base ==> $BASE_IMAGE"
echo "Template ==> $SEED_TEMPLATE"
echo "Instance ==> $NUMBER"

##for i in `seq 1 3`; do virsh destroy demo_$i; virsh undefine demo_$i; done
for i in `seq 1 $NUMBER`
do
	# fork the SEED_TEMPLATE to instance xml file
	TARGET_XML_FULL_NAME=$TARGET_PREFIX.$i$XML_SUFFIX
	cp $SEED_TEMPLATE $TARGET_XML_FULL_NAME

	# remove the backingStore TAG
	[ $EDIT_IMAGE != "nop-edit-base" ] && sed -i '/backingStore/,/\/backingStore/d' $TARGET_XML_FULL_NAME

	uuid=`uuidgen`
	mac1=`openssl rand -base64 8 | md5sum | cut -c1-2`
	mac2=`openssl rand -base64 8 | md5sum | cut -c1-2`
	sed -i "s/$UUID_CODE_STUB/$uuid/" $TARGET_XML_FULL_NAME

	#DISK_FILE_FULL_NAME=$TARGET_PREFIX$TARGET_SUFFIX
	#(( [ $EDIT_IMAGE !=  "edit-base" ] ? TARGET_DISK_FULL_NAME=$EDIT_IMAGE : TARGET_DISK_FULL_NAME=${TARGET_PREFIX}_$i$TARGET_SUFFIX ))
	TARGET_DISK_FULL_NAME=$([ "$EDIT_IMAGE" != "nop-edit-base" ] && echo $EDIT_IMAGE || echo $PWD/${TARGET_PREFIX}_$i$TARGET_SUFFIX)
	# so the TARGET_DISK_FULL_NAME should be create with qemu-img
	# qemu-img create -f qcow2 -b backingfile TARGET_DISK_FULL_NAME
	# for i in `seq 1 5`; do qemu-img create -f qcow2 -b image.base inst_$i.qcow2; done

	# to avoid the to many escape '/' in path name, using "#' as the divide symbol
	sed -i "s#$INST_IMAGE_STUB#$TARGET_DISK_FULL_NAME#" $TARGET_XML_FULL_NAME
	sed -i "s#$BASE_IMAGE_STUB#$BASE_IMAGE#" $TARGET_XML_FULL_NAME
	# create the instance file if it not exist
	[ $EDIT_IMAGE != "nop-edit-base" ] || [ -f $TARGET_DISK_FULL_NAME ] || qemu-img create -f qcow2 -b $BASE_IMAGE $TARGET_DISK_FULL_NAME

	#echo "Replace $DISK_FILE_FULL_NAME ==> $TARGET_DISK_FULL_NAME"
	#sed -i "s/$DISK_FILE_FULL_NAME/$TARGET_DISK_FULL_NAME/" $TARGET_XML_FULL_NAME

	#(( [ $EDIT_IMAGE == "edit-base" ] ? TARGET_VM_FULL_NAME=$EDIT_IMAGE : TARGET_VM_FULL_NAME=${TARGET_VM_NAME}_$i ))
	TARGET_VM_FULL_NAME=$([ "$EDIT_IMAGE" != "nop-edit-base" ] && echo "edit-base" || echo ${TARGET_VM_NAME}-$i)
	sed -i "s/$VM_NAME_STUB/$TARGET_VM_FULL_NAME/" $TARGET_XML_FULL_NAME

	#echo "Replace $VM_NAME_STUB ==> $TARGET_VM_FULL_NAME"

	sed -i "s/$MACADDR_CODE_STUB/$mac1:$mac2/" $TARGET_XML_FULL_NAME
	virsh define $TARGET_XML_FULL_NAME
	virsh start $TARGET_VM_FULL_NAME
done
