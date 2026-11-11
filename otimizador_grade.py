import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
import itertools
import pandas as pd

# Base de disciplinas ENGENHARIA DE PRODUÇÃO
disciplinas = {
    'Cálculo I': {'periodo': 1, 'horarios': {215, 217, 413, 415, 615, 617}, 'requisitos': [], 'dificuldade': 5, 'créditos': 4},
    'Química': {'periodo': 1, 'horarios': {313, 315, 613, 615}, 'requisitos': [], 'dificuldade': 3, 'créditos': 3},
    'Programação Estruturada': {'periodo': 1, 'horarios': {213, 215, 513, 515}, 'requisitos': [], 'dificuldade': 3, 'créditos': 3},
    'Geometria Analítica e Vetorial': {'periodo': 1, 'horarios': set(), 'requisitos': [], 'dificuldade': 4, 'créditos': 4},
    'Introdução à Engenharia de Produção': {'periodo': 1, 'horarios': {415, 417}, 'requisitos': [], 'dificuldade': 2, 'créditos': 2},
    'Expressão Gráfica': {'periodo': 1, 'horarios': {313, 315, 513, 515}, 'requisitos': [], 'dificuldade': 2, 'créditos': 3},
    'Cálculo II': {'periodo': 2, 'horarios': {213, 215, 413, 415, 613, 615}, 'requisitos': ['Cálculo I'], 'dificuldade': 5, 'créditos': 4},
    'Álgebra Linear': {'periodo': 2, 'horarios': {313, 315, 515, 517}, 'requisitos': ['Geometria Analítica e Vetorial'], 'dificuldade': 3, 'créditos': 4},
    'Programação II': {'periodo': 2, 'horarios': {215, 217, 315, 317}, 'requisitos': ['Programação Estruturada'], 'dificuldade': 4, 'créditos': 3},
    'Administração': {'periodo': 2, 'horarios': {213, 215}, 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Física I': {'periodo': 2, 'horarios': {415, 417, 615, 617}, 'requisitos': ['Cálculo I'], 'dificuldade': 4, 'créditos': 4},
    'Física Experimental I': {'periodo': 2, 'horarios': {515, 517}, 'requisitos': ['Cálculo I'], 'dificuldade': 2, 'créditos': 1},
    'Cálculo III': {'periodo': 3, 'horarios': {318, 320, 518, 520}, 'requisitos': ['Cálculo II'], 'dificuldade': 5, 'créditos': 4},
    'Economia': {'periodo': 3, 'horarios': {218, 220, 222}, 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Prob. e Estatística': {'periodo': 3, 'horarios': {415, 417, 515, 517}, 'requisitos': ['Cálculo I'], 'dificuldade': 3, 'créditos': 4},
    'Cálculo Numérico': {'periodo': 3, 'horarios': {315, 317, 515, 517}, 'requisitos': ['Álgebra Linear', 'Programação Estruturada', 'Introd. Equações Diferenciais Ordinárias'], 'dificuldade': 3, 'créditos': 3},
    'Física II': {'periodo': 3, 'horarios': {418, 420, 618, 620}, 'requisitos': ['Física I'], 'dificuldade': 5, 'créditos': 4},
    'Física Experimental II': {'periodo': 3, 'horarios': {613, 615}, 'requisitos': ['Física I', 'Física Experimental I'], 'dificuldade': 3, 'créditos': 1},
    'Fundamentos de Segurança do Trabalho': {'periodo': 3, 'horarios': {513, 515}, 'requisitos': ['Introdução à Engenharia de Produção'], 'dificuldade': 2, 'créditos': 2},
    'Introd. Equações Diferenciais Ordinárias': {'periodo': 3, 'horarios': set(), 'requisitos': ['Cálculo II'], 'dificuldade': 4, 'créditos': 2},
    'Fenômenos de Transporte': {'periodo': 4, 'horarios': {318, 320, 518, 520}, 'requisitos': ['Cálculo II', 'Física II'], 'dificuldade': 4, 'créditos': 4},
    'Ciências dos Materiais': {'periodo': 4, 'horarios': set(), 'requisitos': ['Química'], 'dificuldade': 4, 'créditos': 4},
    'Métodos Estatísticos': {'periodo': 4, 'horarios': {418, 422}, 'requisitos': ['Prob. e Estatística', 'Álgebra Linear'], 'dificuldade': 4, 'créditos': 3},
    'Engenharia de Dados e Conhecimento': {'periodo': 4, 'horarios': set(), 'requisitos': ['Programação II', 'Prob. e Estatística'], 'dificuldade': 4, 'créditos': 3},
    'Ciências do Ambiente': {'periodo': 4, 'horarios': {213, 215}, 'requisitos': ['Economia'], 'dificuldade': 2, 'créditos': 2},
    'Física III': {'periodo': 4, 'horarios': {215, 217, 415, 417}, 'requisitos': ['Cálculo II'], 'dificuldade': 5, 'créditos': 4},
    'Física Experimental III': {'periodo': 4, 'horarios': {413, 415}, 'requisitos': ['Física II', 'Física Experimental II'], 'dificuldade': 3, 'créditos': 1},
    'Mecânica Técnica': {'periodo': 5, 'horarios': {313, 315, 513, 515}, 'requisitos': ['Ciências dos Materiais'], 'dificuldade': 4, 'créditos': 4},
    'Metodologia Científica': {'periodo': 5, 'horarios': {413, 415}, 'requisitos': ['Introdução à Engenharia de Produção'], 'dificuldade': 2, 'créditos': 2},
    'Contabilidade Gerencial': {'periodo': 5, 'horarios': {318, 320, 322}, 'requisitos': ['Economia'], 'dificuldade': 3, 'créditos': 3},
    'Planejamento e Controle da Produção': {'periodo': 5, 'horarios': {418, 420, 422}, 'requisitos': ['Administração'], 'dificuldade': 4, 'créditos': 3},
    'Eng. de Métodos e Processos': {'periodo': 5, 'horarios': {618, 620, 622}, 'requisitos': ['Administração'], 'dificuldade': 4, 'créditos': 3},
    'Eletricidade Aplicada': {'periodo': 5, 'horarios': {518, 520, 522}, 'requisitos': ['Física III'], 'dificuldade': 4, 'créditos': 4},
    'Mecânica dos Materiais I': {'periodo': 6, 'horarios': {315, 317}, 'requisitos': ['Mecânica Técnica'], 'dificuldade': 4, 'créditos': 4},
    'Pesquisa Operacional I': {'periodo': 6, 'horarios': {418, 420, 422}, 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 4, 'créditos': 4},
    'Eng. Econômica Financeira': {'periodo': 6, 'horarios': {218, 220, 222}, 'requisitos': ['Economia'], 'dificuldade': 3, 'créditos': 3},
    'Ergonomia': {'periodo': 6, 'horarios': {518, 520, 522, 524}, 'requisitos': ['Fundamentos de Segurança do Trabalho', 'Mecânica Técnica'], 'dificuldade': 3, 'créditos': 3},
    'Engenharia da Qualidade': {'periodo': 7, 'horarios': {618, 620, 622}, 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 4, 'créditos': 4},
    'Pesquisa Operacional II': {'periodo': 7, 'horarios': {418, 420, 422}, 'requisitos': ['Pesquisa Operacional I'], 'dificuldade': 4, 'créditos': 3},
    'Projeto do Produto': {'periodo': 7, 'horarios': {518, 520, 522}, 'requisitos': ['Ergonomia'], 'dificuldade': 4, 'créditos': 3},
    'Planejamento de Instalações': {'periodo': 7, 'horarios': {318, 320, 322}, 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 3, 'créditos': 4},
    'Estratégia de Organizações': {'periodo': 7, 'horarios': {518, 520, 522}, 'requisitos': ['Administração'], 'dificuldade': 4, 'créditos': 4},
    'Gestão da Manutenção de Ativos': {'periodo': 8, 'horarios': {518, 520, 522}, 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 4, 'créditos': 4},
    'Gestão de Projetos': {'periodo': 8, 'horarios': {218, 220, 222}, 'requisitos': ['Eng. de Métodos e Processos'], 'dificuldade': 4, 'créditos': 3},
    'Metodologias Quantitativas e Qualitativas': {'periodo': 8, 'horarios': set(), 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 3, 'créditos': 3},
    'Gestão da Cadeia de Suprimentos': {'periodo': 8, 'horarios': {318, 320, 322}, 'requisitos': ['Planejamento de Instalações'], 'dificuldade': 4, 'créditos': 4},
    'Estágio Supervisionado': {'periodo': 8, 'horarios': set(), 'requisitos': ['80 créditos acumulados'], 'dificuldade': 3, 'créditos': 8},
    'Tópicos Especiais em Produção': {'periodo': 9, 'horarios': set(), 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 3, 'créditos': 4},
    'Tópicos Especiais em Finanças': {'periodo': 9, 'horarios': set(), 'requisitos': ['Eng. Econômica Financeira'], 'dificuldade': 3, 'créditos': 4},
    'Tópicos Especiais em Mercadologia': {'periodo': 9, 'horarios': set(), 'requisitos': ['Administração'], 'dificuldade': 3, 'créditos': 4},
    'Projeto Final I': {'periodo': 9, 'horarios': {622}, 'requisitos': ['100 créditos acumulados'], 'dificuldade': 4, 'créditos': 4},
    'Optativa Livre I': {'periodo': 10, 'horarios': set(), 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Projeto Final II': {'periodo': 10, 'horarios': {624}, 'requisitos': ['Projeto Final I'], 'dificuldade': 5, 'créditos': 4},
    'Optativa Livre II': {'periodo': 10, 'horarios': set(), 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
}
MAX_DISCIPLINAS_POR_PERIODO = 7
MAX_SOLUCOES = 5

import re
from functools import lru_cache

def validar_base(base):
    for nome, info in base.items():
        for requisito in info['requisitos']:
            if re.fullmatch(r'\d+\s+créditos acumulados', requisito):
                continue
            if requisito not in base:
                raise ValueError(f'{nome}: requisito desconhecido: {requisito}')

def pode_cursar(disciplina, feitas, disciplinas_dict):
    creditos = sum(disciplinas_dict[d]['créditos'] for d in feitas)
    for requisito in disciplinas_dict[disciplina]['requisitos']:
        m = re.fullmatch(r'(\d+)\s+créditos acumulados', requisito)
        if m:
            if creditos < int(m.group(1)):
                return False
        elif requisito not in feitas:
            return False
    return True

def tem_conflito(disciplina, horarios_ocupados, disciplinas_dict):
    return bool(disciplinas_dict[disciplina]['horarios'] & horarios_ocupados)

def calcular_dificuldade_distribuida(plano, disciplinas_dict):
    valores = [sum(disciplinas_dict[d]['dificuldade'] for d in periodo) for periodo in plano if periodo]
    media = sum(valores) / len(valores) if valores else 0
    return sum(abs(v - media) for v in valores)

def alocar_disciplinas(disciplinas_dict, max_periodos, ja_feitas,
                       considerar_horarios=False, max_disciplinas=MAX_DISCIPLINAS_POR_PERIODO):
    """Heurística de planejamento; encontra grades viáveis, sem garantir ótimo global."""
    validar_base(disciplinas_dict)
    feitas = set(ja_feitas)
    if feitas - disciplinas_dict.keys():
        raise ValueError('Há disciplinas concluídas não cadastradas.')
    dependentes = {d: set() for d in disciplinas_dict}
    for d, info in disciplinas_dict.items():
        for requisito in info['requisitos']:
            if requisito in dependentes:
                dependentes[requisito].add(d)

    @lru_cache(None)
    def profundidade(d):
        # As dependências devem ser acíclicas.
        return _profundidade(d, frozenset())

    def _profundidade(d, vistos):
        if d in vistos:
            raise ValueError(f'Ciclo de pré-requisitos: {d}')
        return 1 + max((_profundidade(x, vistos | {d}) for x in dependentes[d]), default=-1)

    ordem = sorted(disciplinas_dict, key=lambda d: (
        -profundidade(d), -len(dependentes[d]),
        -disciplinas_dict[d]['dificuldade'], d))
    plano = []
    for _ in range(max_periodos):
        if len(feitas) == len(disciplinas_dict):
            break
        candidatas = [d for d in ordem if d not in feitas and pode_cursar(d, feitas, disciplinas_dict)]
        selecionadas, ocupados = [], set()
        for d in candidatas:
            if len(selecionadas) >= max_disciplinas:
                break
            if considerar_horarios and tem_conflito(d, ocupados, disciplinas_dict):
                continue
            selecionadas.append(d)
            if considerar_horarios:
                ocupados.update(disciplinas_dict[d]['horarios'])
        if not selecionadas:
            break
        plano.append(selecionadas)
        feitas.update(selecionadas)
    return [plano] if len(feitas) == len(disciplinas_dict) else []

def exportar_excel(plano, base, caminho='grade_otimizada.xlsx'):
    linhas = [{'Período': i, 'Disciplina': d,
               'Dificuldade': base[d]['dificuldade']}
              for i, periodo in enumerate(plano, 1) for d in periodo]
    df = pd.DataFrame(linhas)
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Grade', index=False)
        df.groupby('Período', as_index=False).agg(
            Disciplinas=('Disciplina', 'count')).to_excel(
                writer, sheet_name='Resumo', index=False)
    return caminho

checkboxes = []
grupos_periodos = []
for periodo in range(1, 11):
    itens = [
        widgets.Checkbox(value=False, description=d,
                         layout=widgets.Layout(width='500px'))
        for d, info in disciplinas.items() if info['periodo'] == periodo
    ]
    checkboxes.extend(itens)
    if itens:
        grupos_periodos.append(widgets.VBox(
            [widgets.HTML(value=f'<h4>{periodo}º período</h4>'), *itens],
            layout=widgets.Layout(margin='0 0 10px 0')
        ))
slider_periodos = widgets.IntSlider(value=12, min=1, max=20, description='Períodos:')
slider_limite = widgets.IntSlider(value=7, min=1, max=9, description='Máx. matérias:')
checkbox_horarios = widgets.Checkbox(value=False, description='Considerar conflitos de horário')
botao_gerar = widgets.Button(description='📅 Gerar Plano de Estudos', button_style='success')
output = widgets.Output()

def ao_clicar(botao):
    with output:
        clear_output()
        ja_feitas = [cb.description for cb in checkboxes if cb.value]
        try:
            solucoes = alocar_disciplinas(
                disciplinas, slider_periodos.value, ja_feitas,
                considerar_horarios=checkbox_horarios.value,
                max_disciplinas=slider_limite.value)
            if not solucoes:
                display(Markdown('⚠️ Nenhuma solução completa encontrada. Aumente os períodos '
                                 'ou o limite de disciplinas, ou desative os conflitos de horário.'))
                return
            plano = solucoes[0]
            display(Markdown(f'### ✅ Grade encontrada em {len(plano)} períodos'))
            df = pd.DataFrame({
                f'Período {i+1}': pd.Series(periodo)
                for i, periodo in enumerate(plano)})
            display(df)
            caminho = exportar_excel(plano, disciplinas)
            display(Markdown(f'📁 Arquivo Excel gerado: **{caminho}**'))
            try:
                from google.colab import files
                files.download(caminho)
            except ImportError:
                pass
        except Exception as erro:
            display(Markdown(f'⚠️ Erro: {erro}'))

botao_gerar.on_click(ao_clicar)
display(Markdown('## 📘 Otimizador de Plano de Estudos — Matriz 2026'))
display(Markdown('### Marque as disciplinas já concluídas:'))
display(widgets.VBox(grupos_periodos, layout=widgets.Layout(max_height='350px', overflow='auto')))
display(slider_periodos, slider_limite, checkbox_horarios, botao_gerar, output)
