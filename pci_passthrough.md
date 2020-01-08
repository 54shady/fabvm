# PCI透传原理

[参考 VGA GPU passthrough qemu虚拟桌面pci穿透](https://blog.csdn.net/hubbybob1/article/details/77101913)

## 系统配置

修改启动项

	GRUB_CMDLINE_LINUX=intel_iommu=on video=vesafb:off,efifb:off

查看DMAR 的映射

	dmesg | grep -e DMAR -e IOMMU
	[    0.000000] ACPI: DMAR 0x000000008C52B038 0000A8 (v01 INTEL  EDK2     00000001 INTL 00000001)
	[    0.000000] DMAR: IOMMU enabled
	[    0.025720] DMAR: Host address width 39
	[    0.025721] DMAR: DRHD base: 0x000000fed90000 flags: 0x0
	[    0.025726] DMAR: dmar0: reg_base_addr fed90000 ver 1:0 cap 1c0000c40660462 ecap 19e2ff0505e
	[    0.025727] DMAR: DRHD base: 0x000000fed91000 flags: 0x1
	[    0.025729] DMAR: dmar1: reg_base_addr fed91000 ver 1:0 cap d2008c40660462 ecap f050da
	[    0.025730] DMAR: RMRR base: 0x0000008cc23000 end: 0x0000008ce6cfff
	[    0.025731] DMAR: RMRR base: 0x0000008d800000 end: 0x0000008fffffff
	[    0.025732] DMAR-IR: IOAPIC id 2 under DRHD base  0xfed91000 IOMMU 1
	[    0.025732] DMAR-IR: HPET id 0 under DRHD base 0xfed91000
	[    0.025733] DMAR-IR: Queued invalidation will be enabled to support x2apic and Intr-remapping.
	[    0.027146] DMAR-IR: Enabled IRQ remapping in x2apic mode
	[    0.289580] DMAR: No ATSR found
	[    0.289599] DMAR: dmar0: Using Queued invalidation
	[    0.289746] DMAR: dmar1: Using Queued invalidation
	[    0.289964] DMAR: Setting RMRR:
	[    0.290013] DMAR: Setting identity map for device 0000:00:02.0 [0x8d800000 - 0x8fffffff]
	[    0.290052] DMAR: Setting identity map for device 0000:00:14.0 [0x8cc23000 - 0x8ce6cfff]
	[    0.290059] DMAR: Prepare 0-16MiB unity mapping for LPC
	[    0.290076] DMAR: Setting identity map for device 0000:00:1f.0 [0x0 - 0xffffff]
	[    0.290207] DMAR: Intel(R) Virtualization Technology for Directed I/O
	[  106.509326] DMAR: Setting identity map for device 0000:00:14.0 [0x8cc23000 - 0x8ce6cfff]
	[  106.750536] DMAR: Setting identity map for device 0000:00:02.0 [0x8d800000 - 0x8fffffff]

## 显卡透传

查看系统中的显卡信息(VGA)

	lspci -nn
	...
	00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:3e90]
	...

查看显卡对应的驱动(此时显示驱动使用的是i915)

	lspci -nnk -s 0000:00:02.0
	00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:3e90]
			DeviceName: Onboard - Video
			Subsystem: Intel Corporation Device [8086:3e90]
			Kernel driver in use: i915
			Kernel modules: i915

将驱动和显卡解除绑定

	echo 0000:00:02.0 > /sys/bus/pci/devices/0000:00:02.0/driver/unbind

安装vfio驱动并绑定显卡

	modprobe vfio
	modprobe vfio_pci
	echo "vfio-pci" > /sys/bus/pci/devices/0000:00:02.0/driver_override
	echo 8086 3e90 > /sys/bus/pci/drivers/vfio-pci/new_id

查看显卡对应的驱动(vfio-pci)

	lspci -nnk -s 0000:00:02.0
	00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:3e90]
			DeviceName: Onboard - Video
			Subsystem: Intel Corporation Device [8086:3e90]
			Kernel driver in use: vfio-pci
			Kernel modules: i915

## USB控制器透传

查看USB控制器信息(绑定的是xhci_hcd驱动)

	lspci -nn
	00:14.0 USB controller [0c03]: Intel Corporation Device [8086:a2af]

	lspci -nnk -s 0000:00:14.0
	00:14.0 USB controller [0c03]: Intel Corporation Device [8086:a2af]
			DeviceName: Onboard - Other
			Subsystem: Intel Corporation Device [8086:a2af]
			Kernel driver in use: xhci_hcd

解除绑定默认驱动

	echo 0000:00:14.0 > /sys/bus/pci/devices/0000:00:14.0/driver/unbind

使用vfio驱动

	echo "vfio-pci" > /sys/bus/pci/devices/0000:00:14.0/driver_override
	echo 8086 a2af > /sys/bus/pci/drivers/vfio-pci/new_id

## 使用脚本替代手动操作

使用[vfio_bind.sh](vfio_bind.sh)绑定成vfio驱动

	vfio_bind.sh 0000:00:02.0 0000:00:14.0

使用[vfio_unbind.sh](vfio_unbind.sh)解除vfio绑定

	vfio_unbind.sh 0000:00:02.0 0000:00:14.0

## 注意事项

透传中需要将同组的设备全部透传使用[脚本get_groups.sh](get_groups.sh)查看组信息

	./get_group.sh
	IOMMU Group:0  00:00.0 Host bridge [0600]: Intel Corporation Device [8086:3e0f] (rev 07)
	IOMMU Group:10  02:00.0 USB controller [0c03]: ASMedia Technology Inc. ASM1042A USB 3.0 Host Controller [1b21:1142]
	IOMMU Group:11  03:00.0 Ethernet controller [0200]: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller [10ec:8168] (rev 15)
	IOMMU Group:1  00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:3e90]
	IOMMU Group:2  00:14.0 USB controller [0c03]: Intel Corporation Device [8086:a2af]
	IOMMU Group:3  00:16.0 Communication controller [0780]: Intel Corporation Device [8086:a2ba]
	IOMMU Group:4  00:17.0 SATA controller [0106]: Intel Corporation Device [8086:a282]
	IOMMU Group:5  00:1c.0 PCI bridge [0604]: Intel Corporation Device [8086:a294] (rev f0)
	IOMMU Group:6  00:1d.0 PCI bridge [0604]: Intel Corporation Device [8086:a29a] (rev f0)
	IOMMU Group:7  00:1d.3 PCI bridge [0604]: Intel Corporation Device [8086:a29b] (rev f0)
	IOMMU Group:8  00:1f.0 ISA bridge [0601]: Intel Corporation Device [8086:a2ca]
	IOMMU Group:8  00:1f.2 Memory controller [0580]: Intel Corporation Device [8086:a2a1]
	IOMMU Group:8  00:1f.3 Audio device [0403]: Intel Corporation Device [8086:a2f0]
	IOMMU Group:8  00:1f.4 SMBus [0c05]: Intel Corporation Device [8086:a2a3]
	IOMMU Group:9  01:00.0 Network controller [0280]: Intel Corporation Wireless 3165 [8086:3165] (rev 81)

## 使用方法

使用脚本[passthrough_boot.sh](passthrough_boot.sh)测试

	./passthrough_boot.sh -hda disk.img -cdrom /path/to/iso/os.iso -name 'pass'
