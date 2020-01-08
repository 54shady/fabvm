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
