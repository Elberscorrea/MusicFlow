# MusicFlow

**MusicFlow** é um projeto inspirado no Spotify que permite pesquisar e explorar faixas de música. Utilizando a API do [Spotify Scraper](https://rapidapi.com), o projeto permite buscar músicas, exibir resultados e gerenciar informações de faixas e artistas.

## Funcionalidades

- **Busca de Músicas:** Pesquise faixas de música por nome e obtenha resultados com detalhes como nome da faixa, artista, duração e imagem do álbum.
- **Interface Responsiva:** O design é adaptado para diferentes tamanhos de tela, garantindo uma boa experiência em dispositivos móveis e desktop.
- **Exibição de Resultados:** Os resultados são exibidos de forma visualmente atraente, com imagens dos álbuns e informações relevantes.

## Tecnologias Utilizadas

- **Python**: Backend do projeto, utilizando Django para estruturação do projeto e gerenciamento de dados.
- **HTML/CSS**: Estrutura e estilo das páginas web.
- **JavaScript**: Funcionalidade dinâmica na interface.
- **API Spotify Scraper**: Fornece acesso aos dados das músicas e artistas. Disponível em [RapidAPI](https://rapidapi.com).

### Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/Elberscorrea/MusicFlow.git
   cd MusicFlow
   
2. Crie e ative um ambiente virtual:

   ```sh
   python -m venv .venv
   source .venv/bin/activate   # No Windows, use `.venv\Scripts\activate`

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt

4. Aplique as migrações:

   ```sh
   python manage.py migrate

5. Crie um superusuário para acessar o painel de administração:

   ```sh
   python manage.py createsuperuser

6. Execute o servidor de desenvolvimento:

   ```sh
   python manage.py runserver


## Contato

Elber Correa - elber.scorrea@gmail.com

Link do Projeto: https://github.com/Elberscorrea/MusicFlow


