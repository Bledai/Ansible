
Vagrant.configure("2") do |config|
  ip=["192.168.198.101","192.168.198.102"] 
  box="sbeliakou/centos"
  servers=[
  {
    :hostname => "webserver",
    :ip => ip[0],
    :box => "sbeliakou/centos",
    :ram => 2048,
    :cpu => 2
    
  },
  {
    :hostname => "appserver",
    :ip => ip[1],
    :box => "sbeliakou/centos",
    :ram => 2048,
    :cpu => 4
    
  }
]
    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
            node.vm.box = machine[:box]
            node.vm.hostname = machine[:hostname]
            node.vm.network "private_network", ip: machine[:ip]
            node.vm.provider "virtualbox" do |vb|
                vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
            
            end
            
          
        end
    end

end
