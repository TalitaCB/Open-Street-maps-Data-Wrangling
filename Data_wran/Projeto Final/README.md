ud032
=====
Detalhes do Projeto
Este projeto está conectado com o curso de Tratamento de Dados. Você precisa escolher entre dois bancos de dados para este projeto: SQL e MongoDB. Para uma explicação das diferenças entre esses dois bancos de dados, acesse este módulo. Há instruções separadas abaixo que são relevantes para a escolha de cada banco de dados.

Aqui está o que você deve fazer:

Primeiro Passo - Complete os Exercícios de Programação
Tenha certeza de que todos os exercícios de programação estão resolvidos corretamente na Lição "Estudo de Caso: Dados do OpenStreetMap" no curso que você escolheu (MongoDB ou SQL). Esta é a última lição nesta seção.

Segundo Passo - Revise a Rúbrica e a Amostra de Projeto
A Rúbrica de Projeto será utilizada para avaliar seu projeto. Ele precisa atender às especificações para todos os critérios listados. Aqui estão exemplos de como o seu relatório final deve parecer:

Amostra de Projeto de SQL

Amostra de Projeto de MongoDB

Terceiro Passo - Escolha sua Região no Mapa
Escolha qualquer área do mundo dohttps://www.openstreetmap.org, e baixe o banco de dados do OSM em XML. O banco de dados deve ter pelo menos 50MB em tamanho (descomprimido). Nós recomendamos utilizar um dos seguintes métodos para baixar banco de dados:

Baixe uma área pré-selecionada do metrô em Map Zen.
Utilize o API do Overpass para baixar uma área quadrada personalizada. Explicações sobre a sintaxe podem ser encontras na Wikipédia. De maneira geral, você vai querer utilizar as seguintes consultas:(node(minimum_latitude, minimum_longitude, maximum_latitude, maximum_longitude);<;);out meta; por exemplo, (node(51.249,7.148,51.251,7.152);<;);out meta; a opção meta está incluída assim como os elementos que contém timestamp e informações de usuário. Você pode usar a Ferramenta de Exportação do Open Street Maps para encontrar as coordenadas da sua caixa de delimitação. Nota: Você não poderá utilizar a Ferramenta de Exportação para, de fato, baixar os dados, a área necessária para este projeto é muito grande.
Quarto Passo - Processe seu Conjunto de Dados
É recomendando que você inicie com os exercícios práticos do seu curso escolhido e modifique-os para se adequar ao conjunto de dados escolhido. Conforme você vai entendendo os dados, tome nota dos problemas encontrados ao longo do caminho assim como os problemas com o conjunto de dados. Você vai precisar deles quando for escrever seu relatório de projeto.

Dica: Talvez você queira começar primeiro olhando para uma pequena amosta da da sua região quando auditá-la, assim a iteração na sua investigação será feita com mais facilidade. Veja o código nas notas abaixo para ver como isso é feito.

SQL
Limpe e audite completamente o seu conjunto de dados, os converta do formato XML para CSV. Então importe e limpe os arquivos .csv em um banco de dados SQL utilizando este modelo ou um modelo customizado da sua escolha.

MongoDB
Limpe e audite completamente o seu conjunto de dados, os converta do formato XML para JSON. Então importe e limpe o arquivo .json em um banco de dados MongoDB.

Quinto Passo - Investigue seu Banco de Dados
Depois de construir seus banco de dados local, você vai investigar seus dados realizando consultas. Tenha certeza de documentar essas consultas e seus resultados no documento de envio descrito abaixo. Veja a Rúbrica de Projeto para mais informações em relação as expectativas de consulta.

Sexto Passo - Documente o Seu Trabalho
Crie um documento (pdf, html) que direciona diretamenta às seções a seguir da Rúbrica de Projeto.

Problemas encontrados no seu mapa
Visão geral dos Dados
Outras ideias em relação aos conjuntos de dados
Tente incluir fragmentos de código e tags com problemas (veja Amostra de Projeto de MongoDB ou Amostra de Projeto de SQL) e visualizações em seu relatório, se forem aplicáveis.
Utilize o código a seguir para obter uma amostra sistemática de elementos da sua região do OSM original. Tente mudar o valor de k, desta forma, o seu resultado SAMPLE_FILE termina em diferentes tamanhos. Ao começar, tente utilizar um valor de k maior, então mude para um valor de k intermediário antes de processar todo seu conjunto de dados.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "some_osm.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
