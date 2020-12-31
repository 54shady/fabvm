BSP: xilinx-zc702-2019.2

compile xilinx qemu

	git clone git://github.com/Xilinx/qemu.git
	./configure --target-list="aarch64-softmmu,microblazeel-softmmu" --enable-fdt --disable-kvm --disable-xen --disable-docs --disable-nettle --disable-gnutls --disable-gcrypt
	make -j4

boot with pre-build image

	qemu/aarch64-softmmu/qemu-system-aarch64 \
		-M arm-generic-fdt-7series \
		-machine linux=on \
		-serial /dev/null \
		-serial mon:stdio \
		-display none \
		-kernel zImage \
		-dtb system.dtb \
		--initrd rootfs.tar.gz
