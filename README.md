# 🚀 Provisionamento de Máquina Virtual no Azure com Python

Este script em Python automatiza o provisionamento de uma infraestrutura básica no Microsoft Azure, incluindo a criação de uma rede virtual, IP público, grupo de segurança de rede (NSG), interface de rede (NIC) e uma máquina virtual Linux acessível via SSH (porta 22). As configurações são carregadas a partir de um arquivo `.env`.

---

## 📋 Requisitos

- Conta no Azure com permissões para criar recursos.
- Azure CLI configurada e logada (`az login`).
- Chave pública SSH.
- Python 3.8+
- Bibliotecas Python:
  - `azure-identity`
  - `azure-mgmt-resource`
  - `azure-mgmt-network`
  - `azure-mgmt-compute`
  - `python-dotenv`

Instale os pacotes com:

```bash
pip install -r requirements.txt
