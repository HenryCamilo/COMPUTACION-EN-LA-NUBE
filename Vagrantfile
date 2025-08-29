# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # --------------------------------------------------
  # Máquina 1: Balanceador de carga con HAProxy
  # --------------------------------------------------
  config.vm.define "haproxy" do |haproxy|
    haproxy.vm.box = "bento/ubuntu-22.04"
    haproxy.vm.hostname = "haproxy"
    haproxy.vm.network :private_network, ip: "192.168.100.10"

    haproxy.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update -y
      sudo apt-get install -y haproxy

      echo '
global
  daemon
  maxconn 256

defaults
  mode http
  timeout connect 5000ms
  timeout client  60000ms
  timeout server  60000ms

frontend http-in
  bind *:80
  default_backend servers

backend servers
  server app1 192.168.100.11:3000 check
  server app2 192.168.100.12:3000 check

listen stats
  bind *:8404
  stats enable
  stats uri /
  stats refresh 5s
' | sudo tee /etc/haproxy/haproxy.cfg

      sudo systemctl enable haproxy
      sudo systemctl restart haproxy
    SHELL
  end

  # --------------------------------------------------
  # Función para crear servidores APP con NodeJS + Consul
  # --------------------------------------------------
  def provision_app(vm, ip, name, message)
    vm.vm.box = "bento/ubuntu-22.04"
    vm.vm.hostname = name
    vm.vm.network :private_network, ip: ip

    vm.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update -y
      sudo apt-get install -y nodejs npm unzip curl

      # Instalo Consul
      CONSUL_VERSION=1.17.0
      curl -O https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip
      unzip consul_${CONSUL_VERSION}_linux_amd64.zip
      sudo mv consul /usr/local/bin/

      # Creo la app NodeJS
      mkdir -p /home/vagrant/app
      echo "const http = require('http');
const server = http.createServer((req, res) => {
  res.end('#{message}');
});
server.listen(3000);" > /home/vagrant/app/server.js

      # Servicio systemd para Node
      echo "[Unit]
Description=Node.js App - #{name}
After=network.target

[Service]
ExecStart=/usr/bin/node /home/vagrant/app/server.js
Restart=always
User=vagrant
WorkingDirectory=/home/vagrant/app

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/nodeapp.service

      # Servicio systemd para Consul
      echo "[Unit]
Description=Consul Agent - #{name}
After=network.target

[Service]
ExecStart=/usr/local/bin/consul agent -dev -node=#{name} -bind=#{ip} -client=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/consul.service

      # Habilito y arranco los servicios
      sudo systemctl daemon-reexec
      sudo systemctl enable nodeapp
      sudo systemctl start nodeapp
      sudo systemctl enable consul
      sudo systemctl start consul
    SHELL
  end

  # --------------------------------------------------
  # Máquina 2: APP1
  # --------------------------------------------------
  config.vm.define "app1" do |app1|
    provision_app(app1, "192.168.100.11", "app1", "Hola desde APP1 en el puerto 3000!")
  end

  # --------------------------------------------------
  # Máquina 3: APP2
  # --------------------------------------------------
  config.vm.define "app2" do |app2|
    provision_app(app2, "192.168.100.12", "app2", "Hola desde APP2 en el puerto 3000!")
  end

end
