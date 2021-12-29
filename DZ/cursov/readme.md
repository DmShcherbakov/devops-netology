# Курсовая работа по итогам модуля "DevOps и системное администрирование" - Дмитрий Щербаков
### 1. Создайте виртуальную машину Linux.
```commandline
$ cat ~/vagrant_curs/Vagrantfile | grep -vE '^( *#|$)'
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
config.vm.network "public_network", type: "dhcp", :bridge => 'enp7s0'
end
```

### 2. Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.
```commandline
# ufw allow ssh
# ufw allow in 443
# ufw allow 8200/tcp
# ufw allow in on lo
# ufw allow out on lo
# ufw default deny incoming
# ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere                  
443                        ALLOW IN    Anywhere                  
8200/tcp                   ALLOW IN    Anywhere                  
Anywhere on lo             ALLOW IN    Anywhere                  
22/tcp (v6)                ALLOW IN    Anywhere (v6)             
443 (v6)                   ALLOW IN    Anywhere (v6)             
8200/tcp (v6)              ALLOW IN    Anywhere (v6)             
Anywhere (v6) on lo        ALLOW IN    Anywhere (v6)             

Anywhere                   ALLOW OUT   Anywhere on lo            
Anywhere (v6)              ALLOW OUT   Anywhere (v6) on lo   
```

### 3. Установите hashicorp vault
```commandline
# curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
# apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
# apt-get update && sudo apt-get install vault
...
# vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         1.9.2
Storage Type    file
Cluster Name    vault-cluster-de2e5efe
Cluster ID      9948b389-1bcd-222e-a3c2-d1fdf25b4b76
HA Enabled      false
```

### 4. Cоздайте центр сертификации по инструкции и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).
```commandline
root@vagrant:~/vault# vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
root@vagrant:~/vault# vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
root@vagrant:~/vault# vault write -field=certificate pki/root/generate/internal common_name="netology.test" ttl=87600h > CA_cert.crt
root@vagrant:~/vault# vault write pki/config/urls issuing_certificates="$VAULT_ADDR/v1/pki/ca" crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls
root@vagrant:~/vault# vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
root@vagrant:~/vault# vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
root@vagrant:~/vault# vault write -format=json pki_int/intermediate/generate/internal common_name="netology.test Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.csr
root@vagrant:~/vault# vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.pem
root@vagrant:~/vault# vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
root@vagrant:~/vault# vault write pki_int/roles/netology-dot-test allowed_domains="netology.test" allow_subdomains=true max_ttl="745h"
Success! Data written to: pki_int/roles/netology-dot-test
root@vagrant:~/vault# vault write pki_int/issue/netology-dot-test common_name="test.netology.test" ttl="745h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDqjCCApKgAwIBAgIUNTMcAhypYSBwDCWjTJedM2UFPKcwDQYJKoZIhvcNAQEL
...
8xcW0xKXplBYwC1ized4ESgyAGCr1fF/6ZW49lxJ
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgITJOoASa65NuFoQjXJH4SD3VRIwDANBgkqhkiG9w0BAQsF
...
tmltWas5CKB8E++lLP11
-----END CERTIFICATE-----
expiration          1643307946
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDqjCCApKgAwIBAgIUNTMcAhypYSBwDCWjTJedM2UFPKcwDQYJKoZIhvcNAQEL
...
8xcW0xKXplBYwC1ized4ESgyAGCr1fF/6ZW49lxJ
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwf9tOtrMXRMHV0mNbJ004vN5Wa7fWpkLsIcLOAtHW4VECo5d
...
P5HwW+zW032DjMe+HL56SjBOB9BOJQ/2tFy0sw997UUulDwhRYN1
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       24:ea:00:49:ae:b9:36:e1:68:42:35:c9:1f:84:83:dd:54:48:c0
```
### 5. Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.
![](./Chrome_CA.png)

### 6. Установите nginx
```commandline
root@vagrant:~/vault# dpkg -l | grep nginx
ii  libnginx-mod-http-image-filter       1.18.0-0ubuntu1.2                 amd64        HTTP image filter module for Nginx
ii  libnginx-mod-http-xslt-filter        1.18.0-0ubuntu1.2                 amd64        XSLT Transformation module for Nginx
ii  libnginx-mod-mail                    1.18.0-0ubuntu1.2                 amd64        Mail module for Nginx
ii  libnginx-mod-stream                  1.18.0-0ubuntu1.2                 amd64        Stream module for Nginx
ii  nginx                                1.18.0-0ubuntu1.2                 all          small, powerful, scalable web/proxy server
ii  nginx-common                         1.18.0-0ubuntu1.2                 all          small, powerful, scalable web/proxy server - common files
ii  nginx-core                           1.18.0-0ubuntu1.2                 amd64        nginx web/proxy server (standard version)
```

### 7. По инструкции (ссылка) настройте nginx на https, используя ранее подготовленный сертификат:
### - можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
### - можно использовать и другой html файл, сделанный вами;
```commandline
root@vagrant:~# cat /etc/nginx/sites-enabled/default | grep -vE '(#|^$)'
server {
	listen 443 ssl default_server;
	ssl_certificate		/etc/nginx/certs/test.netology.test.pem;
	ssl_certificate_key	/etc/nginx/certs/test.netology.test.key;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name test.netology.test;
	location / {
		try_files $uri $uri/ =404;
	}
}
```

### 8. Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.
![](./site.png)

### 9. Создайте скрипт, который будет генерировать новый сертификат в vault:
### - генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
### - перезапускаем nginx для применения нового сертификата.
```commandline
root@vagrant:~# cat /root/scripts/cert_update.sh 
#!/usr/bin/env bash

cd /root/scripts/tmp/

vault write -format=json pki_int/issue/netology-dot-test \
    common_name="test.netology.test" \
    alt_names="test.netology.test" \
    ttl="745h" > test.netology.test.crt

cat test.netology.test.crt | jq -r .data.certificate > test.netology.test.crt.pem
cat test.netology.test.crt | jq -r .data.issuing_ca >> test.netology.test.crt.pem
cat test.netology.test.crt | jq -r .data.private_key > test.netology.test.crt.key

cp test.netology.test.crt.pem /etc/nginx/certs/test.netology.test.pem
cp test.netology.test.crt.key /etc/nginx/certs/test.netology.test.key

systemctl restart nginx
```

### 10. Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.
```commandline
root@vagrant:~# cat /etc/crontab | grep cert_update
40 8	29 * *	root	/root/scripts/cert_update.sh
root@vagrant:~# date
Wed Dec 29 08:40:44 MSK 2021
root@vagrant:~# tail -100 /var/log/syslog | grep -A 5 cert_update
Dec 29 08:40:01 vagrant CRON[3005]: (root) CMD (/root/scripts/cert_update.sh)
Dec 29 08:40:01 vagrant systemd[1]: Stopping A high performance web server and a reverse proxy server...
Dec 29 08:40:01 vagrant systemd[1]: nginx.service: Succeeded.
Dec 29 08:40:01 vagrant systemd[1]: Stopped A high performance web server and a reverse proxy server.
Dec 29 08:40:01 vagrant systemd[1]: Starting A high performance web server and a reverse proxy server...
Dec 29 08:40:01 vagrant systemd[1]: Started A high performance web server and a reverse proxy server.
root@vagrant:~# ls -l /etc/nginx/certs/
total 40
-rw-r--r-- 1 root root 1675 Dec 29 08:40 test.netology.test.key
-rw-r--r-- 1 root root 2579 Dec 29 08:40 test.netology.test.pem
```
![](./site_after_update.png)
