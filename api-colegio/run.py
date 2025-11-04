from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 API Colégio Porto - Servidor Iniciado!")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📚 Documentação: http://localhost:5000/docs")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)