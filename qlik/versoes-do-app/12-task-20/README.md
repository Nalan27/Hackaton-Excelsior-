# Snapshot 12 — Task 20

Aplicativo Qlik final após a revisão de usabilidade da **Task 20**. É o
sucessor do [snapshot 11](../11-task-19/README.md).

## Arquivo e identificação

- Arquivo: [`app.qvf`](./app.qvf).
- Exportação informada pelo usuário: **21/09/2026**, no Qlik Cloud, com a
  opção **com dados**.
- Responsável: usuário responsável pela revisão no Qlik.
- Tamanho verificado: **589.824 bytes**.
- SHA-256 verificado:
  `F4BB66B6DA6A437348A8599258E861714304E59135115E79D3FA8095346045F4`.
- Armazenamento: Git LFS, pela regra `*.qvf` em `.gitattributes`.
- Evidência detalhada: [revisão da Task 20](../../../docs/evidencias/task-20/README.md).
- Capturas finais das Telas 0 a 6: [`docs/evidencias/resumo-final`](../../../docs/evidencias/resumo-final/README.md).

O arquivo ficou menor que o snapshot anterior porque foram excluídas pastas
de desenvolvimento. Após a recarga, o usuário confirmou sete pastas públicas,
nesta ordem: Visão Geral; Distribuição geográfica; Evolução mensal dos
repasses; Cobertura e lacunas; Concentração dos repasses; Vulnerabilidade e
repasses; Resumo e recomendações. Os snapshots anteriores preservam as pastas
removidas.

## Correção do modelo associativo

O app usa uma carga híbrida: `fato_repasses` é carregada na seção Main;
`dim_municipio` e `intervalo_primeiro_repasse`, na seção gerada
automaticamente; e `cobertura_municipal`, em uma seção própria. Nesta versão,
`cobertura_municipal` passou a carregar `chave_municipal` sem `Text()`, de
modo compatível com as outras três tabelas do app ativo.

A recarga concluída em 21/09/2026 buscou 133 linhas de calendário, 658
movimentações, 497 linhas de cobertura e 334 linhas em cada tabela municipal
e de intervalo. O Qlik informou zero erros forçados e zero chaves sintéticas.
Nos retestes, tanto `município` quanto `municipio_cobertura` passaram a
propagar as seleções por todas as telas.

O script de referência [`qlik/load_data.qvs`](../../load_data.qvs) segue uma
estratégia manual diferente: ele aplica `Text()` à chave em todas as tabelas.
As duas abordagens mantêm o tipo da chave consistente dentro do respectivo
modelo e não devem ser combinadas parcialmente.

## Validação funcional

O usuário percorreu as sete telas, sem filtros e com os seguintes recortes,
após a correção e a recarga:

- Porto Alegre, selecionado pelos dois campos municipais;
- julho de 2024;
- marcador Top 20;
- Aceguá, sem movimentações na base;
- Pinto Bandeira, sem IDH-M na fonte;
- recurso Judiciário, seguido da limpeza da seleção.

Os valores de controle e os estados vazios coincidiram com a documentação da
Task 20. As capturas finais arquivadas confirmam as sete pastas públicas, as
sete telas sem filtros e os principais casos de controle.

## Restauração

Faça upload de `app.qvf` no Qlik Cloud como um novo aplicativo. Com as
seleções limpas, confirme que as sete pastas públicas e os dados aparecem sem
recarga. Esse teste de reimportação do arquivo exportado ainda não foi
registrado.

Se for necessário recarregar, disponibilize os cinco CSVs de
`data/processed/` na conexão `DataFiles` e preserve uma única estratégia para
o tipo de `chave_municipal`. Como este QVF contém uma seção gerada pelo
Gerenciador de dados, não sincronize tabelas com o script sem antes conferir
as seções automáticas e as renomeações da carga.

O tamanho e o hash identificam exatamente o arquivo versionado. Eles não
comprovam, isoladamente, que os dados e todos os objetos foram incorporados;
essa garantia depende da exportação com dados informada pelo usuário e do
teste de reimportação descrito acima.
