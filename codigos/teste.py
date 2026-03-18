import hashlib

senha_para_testar = "123"

hash_gerado = hashlib.sha256(senha_para_testar.encode()).hexdigest()

print(f"A senha '{senha_para_testar}' gera o seguinte hash:")
print(hash_gerado)