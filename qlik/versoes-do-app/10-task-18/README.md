# Snapshot 10 — Task 18

Aplicativo Qlik Cloud exportado após a criação da **Tela 5 — Vulnerabilidade e
repasses (H3)** e a revisão da tabela da **Tela 3 — Cobertura e lacunas (H4)**.
É o sucessor do [snapshot 09](../09-task-16/README.md).

## Arquivo e evidências

- Arquivo: [`app.qvf`](./app.qvf).
- Exportação informada pelo usuário: **18/09/2026**, Qlik Cloud, **com dados**.
- Tamanho verificado: **425.984 bytes**.
- SHA-256 verificado: `BC7418FAE5F64247C6C65AEDF466D81413518FE3020763180707DCF2C5DC9B11`.
- Armazenamento: Git LFS, pela regra `*.qvf` em `.gitattributes`.
- Capturas: [Tela 5](../../../docs/evidencias/task-18/README.md) e
  [Tela 3 atualizada](../../../docs/evidencias/task-16/README.md).

As capturas da Tela 3 mostram a tabela simples com código IBGE e classificações
visíveis, além dos KPIs **478 / 334 / 144** sem seleção e **144 / 0 / 144** com
`afetado_sem_registro` selecionado. A captura da Tela 5 mostra gráfico,
tabela e nota de método. O script de análise da Task 18 verifica a conciliação
dos saldos e o recorte de **333 municípios com IDH-M** entre os **334 com
repasses**.

O tamanho e o hash identificam o QVF recebido; **a reimportação e a abertura
das telas ainda não foram confirmadas**. Essa validação deve ser registrada
antes de tratar o snapshot como restaurado.

## Restauração

Faça upload de `app.qvf` no Qlik Cloud como um novo aplicativo e abra, com as
seleções limpas, as Telas 3 e 5. Confira também a Visão Geral (334 municípios
com repasse), o mapa geográfico e a Tela 4, que já tiveram problemas de campos
ou visualizações após alterações no modelo. Para executar outra recarga,
disponibilize as fontes da conexão `DataFiles` descritas no
[snapshot 09](../09-task-16/README.md) e confira o script de carga.

O QVF inclui os dados carregados no momento da exportação; após upload, as
conexões com as fontes podem precisar ser configuradas novamente para uma
recarga. Os limites da comparação de IDH-M e repasses estão em
[`docs/task-18-vulnerabilidade-repasses.md`](../../../docs/task-18-vulnerabilidade-repasses.md).
