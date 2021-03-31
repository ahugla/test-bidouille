




cd /tmp
yum install -y wget


# add user and create conf dir
useradd -s /sbin/nologin -d /opt/minio minio
mkdir -p /opt/minio/bin


#download minIO
wget https://dl.minio.io/server/minio/release/linux-amd64/minio -O /opt/minio/bin/minio
chmod +x /opt/minio/bin/minio



# folder for minio storage file
mkdir -p /var/www/minio_storage/
chown -R minio:minio /var/www/minio_storage/



# minIO config
cat >/opt/minio/minio.conf <<EOF
MINIO_VOLUMES="/var/www/minio_storage/"
MINIO_OPTS="--address :9100"
MINIO_ACCESS_KEY= test
MINIO_SECRET_KEY= changeme
EOF



# create service
cat >/etc/systemd/system/minio.service <<EOF
[Unit]
Description=Minio
Documentation=https://docs.minio.io
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/opt/minio/bin/minio
[Service]
WorkingDirectory=/opt/minioUser=minio
Group=minioPermissionsStartOnly=true
EnvironmentFile=-/opt/minio/minio.conf
ExecStartPre=/bin/bash -c "[ -n \"${MINIO_VOLUMES}\" ] || echo \"Variable MINIO_VOLUMES not set in /opt/minio/minio.conf\""ExecStart=/opt/minio/bin/minio server $MINIO_OPTS $MINIO_VOLUMESStandardOutput=journal
StandardError=inherit# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536# Disable timeout logic and wait until process is stopped
TimeoutStopSec=0# SIGTERM signal is used to stop Minio
KillSignal=SIGTERM
SendSIGKILL=no
SuccessExitStatus=0[Install]
WantedBy=multi-user.target
EOF

# Reload and start service
systemctl daemon-reload
systemctl start minio
systemctl enable minio




# install nginx
yum install -y nginx
systemctl start nginx
systemctl enable nginx


# nginx conf
cat >/etc/nginx/conf.d/minio.conf <<EOF
server {
    listen 80;
    server_name  minio.domain.com www.minio.domain.com;    #this config will force through ssl / https
    return 301 https://$server_name$request_uri;    root /var/www/html;
    index index.html index.php;    access_log /var/log/nginx/minio-access.log;
    error_log /var/log/nginx/minio-error.log;    location / {
      proxy_pass          http://localhost:9100;
      }
   }server {
     listen 443;
     server_name minio.domain.com www.minio.domain.com;
     ssl    on;
        
     #change max size upload file as you want
     client_max_body_size 300M;
        
     ssl_certificate         /path/to/ssl/certificate;
     ssl_certificate_key     /path/to/ssl/certificate_key;     ssl_session_cache shared:SSL:1m;
     ssl_session_timeout  10m;
     ssl_ciphers HIGH:!aNULL:!MD5;
     ssl_prefer_server_ciphers on;     access_log   /var/log/nginx/minio-access.log;
     error_log    /var/log/nginx/minio-error.log;     root /var/www/html;
     index index.php;     location / {
          proxy_pass          http://localhost:9100;
          proxy_set_header    Host             $host;
          proxy_set_header    X-Client-DN      $ssl_client_s_dn;
          proxy_set_header    X-SSL-Subject    $ssl_client_s_dn;
          proxy_set_header    X-SSL-Issuer     $ssl_client_i_dn;
          proxy_read_timeout 1800;
          proxy_connect_timeout 1800;
          }
}
EOF

# restart nginx
systemctl restart nginx



