# docchat-llm
---------

## O que é?
Aplicativo simples feito para o teste e consumo básico de modelos LLM Text-to-Text. O aplicativo atua como uma interface de chat local, e realiza o download de modelos conforme inputado pelo usuário, utilizando-se deste para responder a prompts também inputados pelo usuário. 

## Como usar? 
Execute os comandos abaixo via terminal de comando, de dentro da pasta onde clonou o repositório.
1. Instale os pacotes necessários
```
  pip install -r requirements.txt
```
2. Entre na pasta src, abra via terminal e execute o aplicativo
```
  python app.py
```

## Como eu baixo um modelo para usar?
1. Crie uma conta no chat abaixo:
https://huggingface.co/
2. Procure algum modelo text-to-text
3. Copie o nome do repositório
Como por exemplo: meta-llama/Llama-3.2-1B-Instruct
4. Gere uma key de acesso indo em perfil > Settings > Access Keys
5. Abra o aplicativo, no menu superior vá em Modelo > Atualizar/Baixar modelo e siga os passos
6. Após o download ser concluído reinicie o aplicativo

Pronto, agora é só usar!

## O que é o Hugging face?
https://huggingface.co/huggingface

O Hugging Face é um site colaborativo onde diversas empresas postam seus modelos de aprendizado de máquina com qualidade mínima para produção. Lá se encontram os mais variados tipos de modelos open-source, desde os modelos Llama da META (Facebook) e muitas outras organizações. Além do modelo text-to-text usado neste app, existem outros inúmeros tipos de modelos disponíveis, que vão desde criação de imagens e videos, a sintetização de texto para audio. Tire um tempo para dar uma explorada!

## Qual a vantagem de rodar o aplicativo localmente?
LLM's rodados localmente não possuem acesso algum a rede externa, assim seu conteúdo não é compartilhado com terceiros, e ainda permite a customização do modelo, como por exemplo o retreinamento em outros tipos de arquivos locais. 
## O aplicativo serve só para chat? 
O aplicativo também terá a função de utilizar a opção RAG (pesquisa em documentos) dos modelos, e também a utilização de outros tipos de modelos de modelos. **Ainda em desenvolvimento**.
