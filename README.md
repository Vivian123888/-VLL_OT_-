# Otimizador de Grade Curricular — Engenharia de Produção

Aplicação web estática para planejamento de disciplinas da matriz 2026.

## Publicar no GitHub Pages

1. Abra **Settings** do repositório.
2. Selecione **Pages** no menu lateral.
3. Em **Build and deployment**, escolha **Deploy from a branch**.
4. Selecione a branch **main**, pasta **/(root)**, e clique em **Save**.
5. Aguarde a publicação e use o endereço exibido em Pages.

A aplicação está em `index.html` e não exige Google Colab, servidor ou banco de dados.

## Utilização

- Marque as disciplinas já concluídas.
- Defina o número máximo de períodos e o limite de disciplinas por período.
- Marque **Considerar conflitos de horário** somente quando quiser usar os horários históricos.
- Clique em **Gerar plano de estudos**.
- Use **Salvar grade em PDF** e escolha **Salvar como PDF** no destino de impressão do navegador.
- Opcionalmente baixe um CSV ou salve sua seleção no navegador.

## Observações

A aplicação usa uma **heurística**, não um algoritmo de otimização exata: a grade encontrada não é necessariamente a de menor duração. Requisitos de créditos acumulados são verificados antes de cada período. As ofertas e horários devem ser validados junto à coordenação; horários vazios não indicam disponibilidade confirmada.

As disciplinas concluídas são armazenadas somente no navegador do aluno quando ele clica em **Salvar seleção neste navegador**.
