# 创建虚拟机的脚本

## 启动虚拟机通用脚本

通用脚本参考[boot_vm.sh](boot_vm.sh)

## Spice OpenSSL加解密

[参考: spice下通道OpenSSL加密的过程和加密数据传输过程解密](https://blog.csdn.net/hubbybob1/article/details/54586249)

在spice服务端目录myca下生成openssl的ca证书

通过脚本[gen_ca.sh](gen_ca.sh)生成CA证书

	mkdir /path/to/myca
	./gen_ca.sh

生成的文件中ca-cert.pem就是证书

	ls /path/to/myca
	ca-cert.pem  ca-key.pem  server-cert.pem  server-key.csr server-key.pem  server-key.pem.secure

服务端启动虚拟机设置相关选项

	tls-port=47001,disable-ticketing,x509-dir=/path/to/myca,tls-channel=main,tls-channel=inputs

客户端使用证书连接(这里服务的和客户端都是本机,所以是localhost)

	remote-viewer --spice-ca-file=/path/to/myca/ca-cert.pem spice://localhost?tls-port=47001 --spice-host-subject="C=IL, L=Raanana, O=Red Hat, CN=my server"

## PCI透传

[PCI设备透传相关参考](pci_passthrough.md)

## HID(keyboard, mouse, tablet)

### 查看输入设备信息

- lsusb
- cat /proc/bus/input/devices
- xinput --list

### 使用不同的接口

没有指定输入设备接口时

- 默认使用ps2 keyboard和mouse
- 退出gtk窗口需要ctrl_alt_g组合键
- 鼠标不跟手,有飘动感
- lsusb无设备(因为用的是ps2)

指定使用usb keyboard,mouse接口(需要使用tablet驱动)

- 不需要ctrl_alt_g组合键即可退出gtk窗口
- 鼠标跟手情况良好,无飘动感
- lsusb能发现usb设备

qemu命令行参数添加

	-usb -device usb-tablet

- -usb使能usb控制器
- -device usb-tablet使用tablet驱动keyboard和mouse

单独使用usb-kbd或usb-mouse无法达到效果

tablet是绝对坐标而mouse是相对坐标

指定使用virtio-input设备

使用tablet设备,默认无鼠标指针(需要修改显示设置才有鼠标指针)

	-device virtio-tablet-pci

修改显示设置让鼠标指针显示

- Built-in Display ON
- 800x600(4:3)
- Rotation : Normal
- Launcher placement : All display
- Sticky edges : OFF
- Display with smallest controls

- 不需要ctrl_alt_g组合键即可退出gtk窗口
- 鼠标跟手情况良好,无飘动感

使用mouse

	-device virtio-mouse-pci

- 需要ctrl_alt_g组合键才能退出gtk窗口
- 鼠标有飘动异常

## [虚拟机中NAT网络模式](./vmnat.md)
## [虚拟机中SPDK](./spdk.md)
