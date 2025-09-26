import hashlib

# Coloque aqui a senha exata que você está tentando usar para logar
senha_para_testar = "123"

hash_gerado = hashlib.sha256(senha_para_testar.encode()).hexdigest()

print(f"A senha '{senha_para_testar}' gera o seguinte hash:")
print(hash_gerado)