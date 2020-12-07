# QEMU使用SPDK

## 获取代码

源码下载

	git clone https://github.com/spdk/spdk
	cd spdk
	git submodule update --init

安装依赖包

	./scripts/pkgdep.sh

编译

	./configure
	make

## 配置并启动vhost

设置大页内存并启动vhost应用程序(指定路径在/var/tmp下)

	HUGEMEM=2048 ./scripts/setup.sh
	build/bin/vhost -S /var/tmp -s 1024 -m 0x3

创建SPDK bdev(SPDK中对多种存储后端storage backend的抽象)

后端存储包括如下

- ceph RBD
- ramdisk
- NVMe
- iSCSI
- 逻辑卷
- virtio

### VHOST-SCSI

创建基于ramdisk的spdk bdev,名为Malloc0,总大小128M,块大小4096

	./scripts/rpc.py bdev_malloc_create -b Malloc0 128 4096

创建一个vhost-scsi控制器(vhost.0),qemu通过该控制器来使用

	./scripts/rpc.py vhost_create_scsi_controller --cpumask 0x1 vhost.0

将Malloc0绑定到vhost.0控制器上

	./scripts/rpc.py vhost_scsi_controller_add_target vhost.0 1 Malloc0

### VHOST-BLK

创建基于ramdisk的spdk bdev,名为Malloc1,总大小64M,块大小512

	./scripts/rpc.py bdev_malloc_create -b Malloc1 64 512

创建一个vhost-blk控制器(vhost.1)并绑定Malloc1

	./scripts/rpc.py vhost_create_blk_controller --cpumask 0x2 vhost.1 Malloc1

### QEMU中使用

[qemu参数添加如下boot-arm.sh](./boot-arm.sh)

	-m 4G -object memory-backend-file,id=mem0,size=4G,mem-path=/dev/hugepages,share=on -numa node,memdev=mem0

	-chardev socket,id=spdk_vhost_scsi0,path=/var/tmp/vhost.0 \
	-device vhost-user-scsi-pci,chardev=spdk_vhost_scsi0,num_queues=4,bootindex=2 \

	-chardev socket,id=spdk_vhost_blk0,path=/var/tmp/vhost.1 \
	-device vhost-user-blk-pci,chardev=spdk_vhost_blk0,bootindex=3 \
