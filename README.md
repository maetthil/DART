# Data Analysis Reporting Tool

O DART (Data Analysis Reporting Tool) é uma ferramenta desenvolvida com o objetivo de ajudar a realizar a exploração e documentar a qualidade de um conjunto de dados de maneira interativa.

## Como usar
Para construir a imagem em docker use:
```bash
docker build -t dart .
```
Para exportar o relatório junto com uma página HTML estática use o script export_analysis:
```console
usage: .\export_analysis [image_tag] [data_dir]

Constrói o relatório em dois formatos, HTML e pdf, os arquivos serão escritos em um diretório chamado export/ 

positional arguments:
  image_tag      especifique a tag da imagem do dart
  data_dir       especifique o diretório onde está o arquivo yaml com a descrição do conjunto de dados
```
