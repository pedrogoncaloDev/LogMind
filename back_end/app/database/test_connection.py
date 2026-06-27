# Arquivo com o único objetivo de testar se o back_end 
# consegue estabelecer conexão com o banco de dados

from sqlalchemy import text
from app.database.connection import engine

try: 
	with engine.connect() as conn:
		result = conn.execute(text("SELECT 1"))
		print(result.scalar())

		print("Conexão OK")
except Exception as e:
	print(f"Erro: {e}")