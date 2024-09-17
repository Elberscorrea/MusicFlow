# MusicFlow 🎵

MusicFlow é um projeto inspirado no Spotify que oferece uma interface para explorar e gerenciar músicas. Utilizando a API Spotify Scraper, o MusicFlow permite buscar faixas, visualizar detalhes dos artistas e muito mais.

## Funcionalidades 🚀

- **Busca de Músicas**: Encontre suas músicas favoritas usando a API Spotify Scraper.
- **Visualização de Artistas**: Veja detalhes dos artistas, incluindo imagem, nome e título.
- **Interface Responsiva**: Design adaptado para diferentes tamanhos de tela.

## Requisitos 🛠️

Antes de rodar o projeto, certifique-se de que você tem os seguintes requisitos:

1. **Python 3.8+**: Certifique-se de ter o Python 3.8 ou superior instalado em sua máquina.
2. **Pip**: O gerenciador de pacotes do Python deve estar instalado para instalar as dependências.

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


