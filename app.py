from flask import Flask, render_template, request, send_from_directory
import os
import instaloader

app = Flask(__name__)

# Pasta para salvar os downloads
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Por favor, insira um link válido do Instagram.", 400

    try:
        # Inicializa o Instaloader
        loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER)
        
        # Extrai o shortcode do link
        shortcode = url.split("/")[-2]

        # Faz o download do post
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        if post.is_video:
            loader.download_post(post, target=DOWNLOAD_FOLDER)
            return send_from_directory(DOWNLOAD_FOLDER, os.listdir(DOWNLOAD_FOLDER)[-1], as_attachment=True)
        else:
            return "O link fornecido não é um vídeo.", 400
    except Exception as e:
        return f"Erro ao processar o link: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
