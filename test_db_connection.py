from app import app, db

def test_connection():
    try:
        with app.app_context():
            db.engine.execute("SELECT 1")
            print("Conexão bem-sucedida!")
    except Exception as e:
        print("Erro na conexão:")
        print(str(e))

if __name__ == "__main__":
    test_connection()
