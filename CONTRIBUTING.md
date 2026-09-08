# 🤝 Como contribuir

Este projeto é desenvolvido em equipe. Para manter o código organizado, siga estas orientações.

## 1. Atualize seu repositório

Antes de começar uma tarefa:

```bash
git checkout main
git pull origin main
```

## 2. Crie uma branch

Não faça alterações diretamente na `main`.

Crie uma branch para sua tarefa:

```bash
git checkout -b feature/nome-da-tarefa
```

Exemplos:

```bash
git checkout -b feature/login
git checkout -b feature/pagamentos
git checkout -b fix/corrigir-validacao
```

## 3. Faça suas alterações

Desenvolva sua tarefa e teste o código antes de enviar.

Depois, adicione as alterações:

```bash
git add .
```

Faça o commit:

```bash
git commit -m "feat: adiciona sistema de login"
```

Tipos de commit sugeridos:

* `feat:` nova funcionalidade
* `fix:` correção de bug
* `docs:` alteração na documentação
* `style:` alterações visuais ou de formatação
* `refactor:` melhoria no código sem adicionar funcionalidade

## 4. Envie sua branch

```bash
git push origin feature/nome-da-tarefa
```

## 5. Abra um Pull Request

No GitHub:

1. Abra um Pull Request da sua branch para a `main`.
2. Explique brevemente o que foi feito.
3. Peça para outro integrante revisar.
4. Após a aprovação, faça o merge.
5. Exclua a branch.

## ⚠️ Regras importantes

* Não trabalhar diretamente na `main`.
* Sempre atualizar a `main` antes de criar uma nova branch.
* Cada tarefa deve ter sua própria branch.
* Faça commits pequenos e com mensagens claras.
* Teste o código antes de abrir um Pull Request.
* Não faça merge do código de outro integrante sem revisar.

## 💬 Comunicação

Se houver dúvidas sobre uma tarefa ou alteração que possa afetar o código de outro integrante, converse com a equipe antes de realizar a mudança.

Assim evitamos conflitos e mantemos o projeto organizado. 🚀