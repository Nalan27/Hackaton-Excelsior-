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

### Erro `Connection not found: Hackaton:DataFiles (space not found)`

Esse erro aparece na **recarga** quando o script importado ainda aponta para o
espaço `Hackaton`, inexistente ou inacessível no ambiente de destino. Ele não
prova que os dados já incluídos no QVF ou as telas foram perdidos. Para recarregar:

1. Confirme em qual espaço está o aplicativo e disponibilize nele os cinco CSVs
   de `data/processed/`: `dim_municipio.csv`, `fato_repasses.csv`,
   `dim_calendario.csv`, `intervalo_primeiro_repasse.csv` e
   `cobertura_municipal.csv`.
2. No Editor da carga de dados, procure **todas** as referências
   `lib://Hackaton:DataFiles/`. Se os arquivos estão no espaço pessoal de quem
   recarrega, use `lib://DataFiles/`. Se estão no mesmo espaço compartilhado do
   app, use `lib://:DataFiles/`; para outro espaço compartilhado, use seu nome
   exato, por exemplo `lib://NomeDoEspaco:DataFiles/`.
3. Confira nomes e pastas dos arquivos antes de carregar. Após a recarga,
   valide o modelo e os indicadores das Telas 3 e 5. Não adicione uma segunda
   carga de `cobertura_municipal.csv` pelo Gerenciador de dados.

O script versionado em [`qlik/load_data.qvs`](../../load_data.qvs) usa
`lib://DataFiles/`; a referência ao espaço `Hackaton` foi observada no erro de
recarga de outro ambiente. Consulte as [regras de caminhos do Qlik](https://help.qlik.com/pt-BR/cloud-services/Subsystems/Hub/Content/Sense_Hub/Scripting/LoadData/connect-data-sources-data-load-editor.htm)
e a [documentação sobre upload de aplicativos](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Apps/uploading-apps.htm).
