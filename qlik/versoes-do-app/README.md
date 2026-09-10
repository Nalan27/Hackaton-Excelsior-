# Versões do app Qlik

Esta pasta armazena snapshots restauráveis do app Qlik em formato QVF.

## Organização

Cada entrega deve ficar em uma pasta própria, usando um número sequencial e a
task correspondente:

```text
01-task-09/
02-task-15/
03-task-21/
```

Dentro de cada pasta:

- salve o arquivo exportado com o nome `app.qvf`;
- preencha o `README.md` da versão;
- não altere snapshots anteriores; crie uma nova pasta para cada entrega.

Os arquivos QVF são armazenados com Git LFS, conforme a configuração presente
na raiz do repositório.

## Adicionando uma versão

Após copiar o QVF para a pasta correspondente, verifique se o Git LFS o
reconheceu:

```powershell
git lfs ls-files
git status
```
