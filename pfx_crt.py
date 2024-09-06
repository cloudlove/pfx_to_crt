import OpenSSL
import re
import os

def pfx_to_crt(pfx_path, pfx_password, crt_path, key_path):
    # 读取 PFX 文件
    with open(pfx_path, 'rb') as f:
        pfx_file = f.read()
    p12 = OpenSSL.crypto.load_pkcs12(pfx_file, pfx_password)
    
    # 提取证书和私钥
    cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate())
    key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey())
    
    # 提取证书链并反转
    chain = [OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert) 
             for cert in reversed(p12.get_ca_certificates())]
    
    # 写入证书和私钥到 CRT 和 KEY 文件
    with open(crt_path, 'wb') as f:
        f.write(cert)
    with open(key_path, 'wb') as f:
        f.write(key)
    
    # 将证书链追加到 CRT 文件
    with open(crt_path, 'ab') as f:
        for chain_cert in chain:
            f.write(chain_cert)
if __name__ == '__main__':
  passwd ="Admin@2024" #证书密码
  for file in os.listdir("/tmp/test/20240502SSL"):
      if file.endswith(".pfx"):
            path = os.path.join("/tmp/test/20240502SSL", file)
            crt = os.path.join("/tmp/test", os.path.splitext(file)[0] + ".crt")
            key = os.path.join("/tmp/test", os.path.splitext(file)[0] + ".key")
            print(path, crt, key)
            pfx_to_crt(path, passwd, crt, key)
