import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import (
    HardwareProfile, NetworkProfile, OSProfile,
    LinuxConfiguration, SshConfiguration, SshPublicKey,
    StorageProfile, OSDisk, DiskCreateOptionTypes, VirtualMachine
)

# Carrega variáveis do .env
load_dotenv("var.env")

# Autenticação e configs
credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
location = os.getenv("AZURE_LOCATION")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")

# Criação do Resource Group (caso não exista)
resource_client = ResourceManagementClient(credential, subscription_id)
print(f"📁 Verificando/CRIANDO Resource Group '{resource_group}'...")
resource_client.resource_groups.create_or_update(
    resource_group, {"location": location}
)

# Variáveis de recursos
vm_name = os.getenv("AZURE_VM_NAME")
admin_username = os.getenv("AZURE_ADMIN_USERNAME")
ssh_key_path = os.path.expanduser(os.getenv("AZURE_SSH_KEY_PATH"))
vnet_name = os.getenv("AZURE_VNET_NAME")
subnet_name = os.getenv("AZURE_SUBNET_NAME")
nic_name = os.getenv("AZURE_NIC_NAME")
ip_name = os.getenv("AZURE_IP_NAME")
disk_name = os.getenv("AZURE_DISK_NAME")

# Carrega chave SSH pública
with open(ssh_key_path, "r") as f:
    ssh_key = f.read()

# Clientes Azure
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

print(f"🛠️ Criando IP público...")
ip_params = {
    "location": location,
    "public_ip_allocation_method": "Dynamic"
}
ip_address = network_client.public_ip_addresses.begin_create_or_update(
    resource_group, ip_name, ip_params).result()

print(f"🛠️ Criando VNet e Subnet...")
vnet = network_client.virtual_networks.begin_create_or_update(
    resource_group, vnet_name, {
        "location": location,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
        "subnets": [{"name": subnet_name, "address_prefix": "10.0.0.0/24"}]
    }).result()
subnet = network_client.subnets.get(resource_group, vnet_name, subnet_name)

print(f"🛠️ Criando NIC...")
nic_params = {
    "location": location,
    "ip_configurations": [{
        "name": f"{nic_name}-ipconfig",
        "subnet": {"id": subnet.id},
        "public_ip_address": {"id": ip_address.id}
    }]
}
nic = network_client.network_interfaces.begin_create_or_update(
    resource_group, nic_name, nic_params).result()

print(f"🖥️ Criando máquina virtual '{vm_name}'...")
vm_params = {
    "location": location,
    "storage_profile": StorageProfile(
        image_reference={
            "publisher": "Canonical",
            "offer": "UbuntuServer",
            "sku": "18.04-LTS",
            "version": "latest"
        },
        os_disk=OSDisk(
            create_option=DiskCreateOptionTypes.from_image,
            #create_option=DiskCreateOptionTypes.from_string("fromImage"),
            name=disk_name
        )
    ),
    "hardware_profile": HardwareProfile(vm_size="Standard_B1s"),
    "os_profile": OSProfile(
        computer_name=vm_name,
        admin_username=admin_username,
        linux_configuration=LinuxConfiguration(
            disable_password_authentication=True,
            ssh=SshConfiguration(
                public_keys=[
                    SshPublicKey(
                        path=f"/home/{admin_username}/.ssh/authorized_keys",
                        key_data=ssh_key
                    )
                ]
            )
        )
    ),
    "network_profile": NetworkProfile(
        network_interfaces=[{"id": nic.id}]
    )
}
vm_creation = compute_client.virtual_machines.begin_create_or_update(
    resource_group, vm_name, VirtualMachine(**vm_params)
)
vm_result = vm_creation.result()
print(f"✅ VM criada com sucesso: {vm_result.name}")

# 🔐 Criando NSG com regra para porta 22 (SSH)
nsg_name = f"{vm_name}-nsg"
print(f"🔐 Criando Network Security Group '{nsg_name}' com regra para SSH...")

nsg_params = {
    "location": location,
    "security_rules": [{
        "name": "Allow-SSH",
        "protocol": "Tcp",
        "direction": "Inbound",
        "access": "Allow",
        "priority": 1000,
        "source_address_prefix": "*",
        "source_port_range": "*",
        "destination_address_prefix": "*",
        "destination_port_range": "22"
    }]
}

nsg = network_client.network_security_groups.begin_create_or_update(
    resource_group, nsg_name, nsg_params).result()

# 🛠️ Criando NIC com NSG associado
print(f"🛠️ Criando NIC com associação ao NSG...")
nic_params = {
    "location": location,
    "ip_configurations": [{
        "name": f"{nic_name}-ipconfig",
        "subnet": {"id": subnet.id},
        "public_ip_address": {"id": ip_address.id}
    }],
    "network_security_group": {"id": nsg.id}
}
nic = network_client.network_interfaces.begin_create_or_update(
    resource_group, nic_name, nic_params).result()

# (...) restante do seu código continua igual

print(f"✅ VM criada com sucesso: {vm_result.name}")
print(f"🌐 IP público da VM: {ip_address.ip_address}")