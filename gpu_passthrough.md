# 显卡透传原理

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

## 使用方法

使用脚本[passthrough_boot.sh](passthrough_boot.sh)测试

	./passthrough_boot.sh -hda disk.img -cdrom /path/to/iso/os.iso -name 'pass'
