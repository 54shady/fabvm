#!/bin/bash

SERVER_KEY=server-key.pem
# creating a key for our ca 生成证书的加密长度为1024
if [ ! -e ca-key.pem ]; then
	openssl genrsa -des3 -out ca-key.pem 1024
fi
# creating a ca  生成证书的有效时长为1095天，关键字为 -subj "/C=IL/L=Raanana/O=Red Hat/CN=my CA"

if [ ! -e ca-cert.pem ]; then
	openssl req -new -x509 -days 1095 -key ca-key.pem -out ca-cert.pem -utf8 -subj "/C=IL/L=Raanana/O=Red Hat/CN=my CA"
fi
# create server key
if [ ! -e $SERVER_KEY ]; then
	openssl genrsa -out $SERVER_KEY 1024
fi
# create a certificate signing request (csr)
if [ ! -e server-key.csr ]; then
	openssl req -new -key $SERVER_KEY -out server-key.csr -utf8 -subj "/C=IL/L=Raanana/O=Red Hat/CN=my server"
fi
# signing our server certificate with this ca
if [ ! -e server-cert.pem ]; then
	openssl x509 -req -days 1095 -in server-key.csr -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
fi
# now create a key that doesn't require a passphrase
openssl rsa -in $SERVER_KEY -out $SERVER_KEY.insecure
mv $SERVER_KEY $SERVER_KEY.secure
mv $SERVER_KEY.insecure $SERVER_KEY
# show the results (no other effect)
openssl rsa -noout -text -in $SERVER_KEY
openssl rsa -noout -text -in ca-key.pem
openssl req -noout -text -in server-key.csr
openssl x509 -noout -text -in server-cert.pem
openssl x509 -noout -text -in ca-cert.pem
