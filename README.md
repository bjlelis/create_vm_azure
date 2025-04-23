# ☁️ Azure VM Provisioning com Python

Este projeto tem como objetivo provisionar de forma automatizada uma infraestrutura básica no **Microsoft Azure**, incluindo:

- Grupo de recursos
- IP público
- Rede virtual (VNet) e sub-rede
- Network Security Group (NSG) com acesso via **SSH (porta 22)**
- Interface de rede (NIC)
- Máquina virtual Linux (Ubuntu)

As configurações são parametrizadas através de variáveis de ambiente definidas em um arquivo `.env`.

---

## 📦 Tecnologias Utilizadas

- **[Python 3.8+](https://www.python.org/)**
- **Azure SDK for Python:**
  - `azure-identity`
  - `azure-mgmt-resource`
  - `azure-mgmt-network`
  - `azure-mgmt-compute`
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**

---

## 🚀 Como Funciona

O script realiza os seguintes passos:

1. **Carrega variáveis de ambiente** do arquivo `var.env`.
2. **Autentica no Azure** usando `DefaultAzureCredential`.
3. **Cria o grupo de recursos**, se não existir.
4. **Cria um IP público** com alocação dinâmica.
5. **Cria uma Virtual Network** com uma sub-rede.
6. **Cria um Network Security Group (NSG)** com regra de liberação para SSH (porta 22).
7. **Cria uma interface de rede (NIC)** associando-a ao IP e NSG.
8. **Cria uma máquina virtual Ubuntu** com autenticação via chave SSH.
9. **Exibe o IP público da VM** ao final da execução.

---

## ⚙️ Preparando o Ambiente

### 1. Clonando o repositório:

```bash
git clone https://github.com/seu-usuario/azure-vm-provisioning.git
cd azure-vm-provisioning

### 2. Instalando dependências:

pip install -r requirements.txt

### 3. Criando arquivo var.env:

AZURE_SUBSCRIPTION_ID='Sua_subscription_ID'
AZURE_LOCATION='defina_sua_regiao'
AZURE_RESOURCE_GROUP='defina_seu_Grupo_Recursos'
AZURE_VM_NAME='nome_VM'
AZURE_ADMIN_USERNAME='nome_usuario_do_SO'
AZURE_SSH_KEY_PATH=~/.ssh/id_rsa.pub
AZURE_VNET_NAME='Defina_sua_VNet'
AZURE_SUBNET_NAME='defina_sua_Subnet'
AZURE_NIC_NAME='defina_sua_NIC'
AZURE_IP_NAME='nome_do_seu_PIP'
AZURE_DISK_NAME='disk_name'

### 4. Executando o Script:

A) Esteja logado no azure via CLI: az login

B) criar e ativar o ambiente virtual no python 
python3 -m venv venv
source venv/bin/activate

C) Executar o script: python vm.py

### 5. Acessando a VM:

ssh azureuser@<PIP_gerado_ao_final_do_script>

### 6. Limpando recursos:

az group delete --name <seu_resource_group> --yes --no-wait

### 7. Estrutura do projeto:

azure-vm-provisioning/
│
├── vm.py              # Script 
├── var.env            # Variáveis de ambiente (não versionar)
├── requirements.txt   # Dependências do projeto
└── README.md          



