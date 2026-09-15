# Versões do app Qlik

Esta pasta armazena snapshots restauráveis do app Qlik em formato QVF.

## Organização

Cada entrega deve ficar em uma pasta própria, usando um número sequencial e a
task correspondente:

```text
01-task-09/
02-task-10/
03-task-11/
04-task-12/
```

Dentro de cada pasta:

- baixe o app do Qlik no formato QVF usando a opção **com dados**;
- salve o arquivo exportado com o nome `app.qvf`;
- preencha o `README.md` da versão;
- não altere snapshots anteriores; crie uma nova pasta para cada entrega.

O download com dados é obrigatório para que cada snapshot preserve o estado
completo do app e possa ser visualizado após a importação sem depender de uma
recarga imediata das fontes externas.

Os arquivos QVF são armazenados com Git LFS, conforme a configuração presente
na raiz do repositório.

## Adicionando uma versão

Após copiar o QVF para a pasta correspondente, verifique se o Git LFS o
reconheceu:

```powershell
git lfs ls-files
git status
```
