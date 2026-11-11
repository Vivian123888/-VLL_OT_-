import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
import itertools
import pandas as pd

# Base de disciplinas ENGENHARIA DE PRODUÇÃO
disciplinas = {
    'Cálculo I': {'horarios': {215, 217, 413, 415, 615, 617}, 'requisitos': [], 'dificuldade': 5, 'créditos': 4},
    'Introdução à Engenharia': {'horarios': {415, 417}, 'requisitos': [], 'dificuldade': 2, 'créditos': 2},
    'Geometria Analítica e Vetorial': {'horarios': set(), 'requisitos': [], 'dificuldade': 4, 'créditos': 4},
    'Programação I': {'horarios': {213, 215, 513, 515}, 'requisitos': [], 'dificuldade': 3, 'créditos': 3},
    'Química': {'horarios': {313, 315, 613, 615}, 'requisitos': [], 'dificuldade': 3, 'créditos': 3},
    'Expressão Gráfica': {'horarios': {313, 315, 513, 515}, 'requisitos': [], 'dificuldade': 2, 'créditos': 3},
    'Administração I': {'horarios': {213, 215}, 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Cálculo II': {'horarios': {213, 215, 413, 415, 613, 615}, 'requisitos': ['Cálculo I'], 'dificuldade': 5, 'créditos': 4},
    'Física I': {'horarios': {415, 417, 615, 617}, 'requisitos': ['Cálculo I'], 'dificuldade': 4, 'créditos': 4},
    'Física Experimental I': {'horarios': {515, 517}, 'requisitos': ['Cálculo I'], 'dificuldade': 2, 'créditos': 1},
    'Programação II': {'horarios': {215, 217, 315, 317}, 'requisitos': ['Programação I'], 'dificuldade': 4, 'créditos': 3},
    'Álgebra Linear': {'horarios': {313, 315, 515, 517}, 'requisitos': ['Geometria Analítica e Vetorial'], 'dificuldade': 3, 'créditos': 4},
    'Cálculo III': {'horarios': {318, 320, 518, 520}, 'requisitos': ['Cálculo II'], 'dificuldade': 5, 'créditos': 4},
    'Física II': {'horarios': {418, 420, 618, 620}, 'requisitos': ['Física I'], 'dificuldade': 5, 'créditos': 4},
    'Introdução às Equações Diferenciais Ordinárias': {'horarios': set(), 'requisitos': ['Cálculo II'], 'dificuldade': 4, 'créditos': 2},
    'Economia I': {'horarios': {218, 220, 222}, 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Física Experimental II': {'horarios': {613, 615}, 'requisitos': ['Física I', 'Física Experimental I'], 'dificuldade': 3, 'créditos': 1},
    'Probabilidade e Estatística': {'horarios': {415, 417, 515, 517}, 'requisitos': ['Cálculo I'], 'dificuldade': 3, 'créditos': 4},
    'Cálculo Numérico': {'horarios': {315, 317, 515, 517}, 'requisitos': ['Álgebra Linear', 'Programação I', 'Introdução às Equações Diferenciais Ordinárias'], 'dificuldade': 3, 'créditos': 3},
    'Fundamentos de Engenharia de Segurança': {'horarios': {513, 515}, 'requisitos': ['Introdução à Engenharia'], 'dificuldade': 2, 'créditos': 2},
    'Ciência dos Materiais': {'horarios': set(), 'requisitos': ['Química'], 'dificuldade': 4, 'créditos': 4},
    'Física III': {'horarios': {215, 217, 415, 417}, 'requisitos': ['Cálculo II'], 'dificuldade': 5, 'créditos': 4},
    'Física Experimental III': {'horarios': {413, 415}, 'requisitos': ['Física II', 'Física Experimental II'], 'dificuldade': 3, 'créditos': 1},
    'Métodos Estatísticos': {'horarios': {418, 422}, 'requisitos': ['Probabilidade e Estatística', 'Álgebra Linear'], 'dificuldade': 4, 'créditos': 3},
    'Engenharia de Dados e Conhecimento': {'horarios': set(), 'requisitos': ['Programação II', 'Probabilidade e Estatística'], 'dificuldade': 4, 'créditos': 3},
    'Fenômenos de Transporte': {'horarios': {318, 320, 518, 520}, 'requisitos': ['Cálculo II', 'Física II'], 'dificuldade': 4, 'créditos': 4},
    'Engenharia do Meio Ambiente': {'horarios': {213, 215}, 'requisitos': ['Economia I'], 'dificuldade': 2, 'créditos': 2},
    'Contabilidade Gerencial': {'horarios': {318, 320, 322}, 'requisitos': ['Economia I'], 'dificuldade': 3, 'créditos': 3},
    'Eletricidade Aplicada': {'horarios': {518, 520, 522}, 'requisitos': ['Física III'], 'dificuldade': 4, 'créditos': 4},
    'Engenharia de Métodos': {'horarios': {618, 620, 622}, 'requisitos': ['Administração I'], 'dificuldade': 4, 'créditos': 3},
    'Mecânica Técnica': {'horarios': {313, 315, 513, 515}, 'requisitos': ['Ciência dos Materiais'], 'dificuldade': 4, 'créditos': 4},
    'Planejamento e Controle da Produção': {'horarios': {418, 420, 422}, 'requisitos': ['Administração I'], 'dificuldade': 4, 'créditos': 3},
    'Metodologia Científica': {'horarios': {413, 415}, 'requisitos': ['Introdução à Engenharia'], 'dificuldade': 2, 'créditos': 2},
    'Pesquisa Operacional I': {'horarios': {418, 420, 422}, 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 4, 'créditos': 4},
    'Engenharia Econômico-Financeira': {'horarios': {218, 220, 222}, 'requisitos': ['Economia I'], 'dificuldade': 3, 'créditos': 3},
    'Ergonomia': {'horarios': {518, 520, 522, 524}, 'requisitos': ['Fundamentos de Engenharia de Segurança', 'Mecânica Técnica'], 'dificuldade': 3, 'créditos': 3},
    'Mecânica dos Materiais': {'horarios': {315, 317}, 'requisitos': ['Mecânica Técnica'], 'dificuldade': 4, 'créditos': 4},
    'Pesquisa Operacional II': {'horarios': {418, 420, 422}, 'requisitos': ['Pesquisa Operacional I'], 'dificuldade': 4, 'créditos': 3},
    'Estratégia de Organizações': {'horarios': {518, 520, 522}, 'requisitos': ['Administração I'], 'dificuldade': 4, 'créditos': 4},
    'Engenharia da Qualidade': {'horarios': {618, 620, 622}, 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 4, 'créditos': 4},
    'Projeto do Produto': {'horarios': {518, 520, 522}, 'requisitos': ['Ergonomia'], 'dificuldade': 4, 'créditos': 3},
    'Arranjo Físico Industrial': {'horarios': {318, 320, 322}, 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 3, 'créditos': 4},
    'Gestão da Manutenção': {'horarios': {518, 520, 522}, 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 4, 'créditos': 4},
    'Gestão de Projetos': {'horarios': {218, 220, 222}, 'requisitos': ['Engenharia de Métodos'], 'dificuldade': 4, 'créditos': 3},
    'Metodologias Qualitativas e Quantitativas': {'horarios': set(), 'requisitos': ['Métodos Estatísticos'], 'dificuldade': 3, 'créditos': 3},
    'Logística e Transportes': {'horarios': {318, 320, 322}, 'requisitos': ['Arranjo Físico Industrial'], 'dificuldade': 4, 'créditos': 4},
    'Estágio Supervisionado': {'horarios': set(), 'requisitos': ['80 créditos acumulados'], 'dificuldade': 3, 'créditos': 8},
    'Tópicos Especiais II - Produção': {'horarios': set(), 'requisitos': ['Planejamento e Controle da Produção'], 'dificuldade': 3, 'créditos': 4},
    'Tópicos Especiais I - Finanças': {'horarios': set(), 'requisitos': ['Engenharia Econômico-Financeira'], 'dificuldade': 3, 'créditos': 4},
    'Tópicos Especiais III - Metodologia': {'horarios': set(), 'requisitos': ['Administração I'], 'dificuldade': 3, 'créditos': 4},
    'Projeto Final I': {'horarios': {622}, 'requisitos': ['100 créditos acumulados'], 'dificuldade': 4, 'créditos': 4},
    'Projeto Final II': {'horarios': {624}, 'requisitos': ['Projeto Final I'], 'dificuldade': 5, 'créditos': 4},
    'Optativa Livre II': {'horarios': set(), 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
    'Optativa Livre I': {'horarios': set(), 'requisitos': [], 'dificuldade': 3, 'créditos': 4},
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
    linhas = [{'Período': i, 'Disciplina': d, 'Créditos': base[d]['créditos'],
               'Dificuldade': base[d]['dificuldade']}
              for i, periodo in enumerate(plano, 1) for d in periodo]
    df = pd.DataFrame(linhas)
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Grade', index=False)
        df.groupby('Período', as_index=False).agg(
            Disciplinas=('Disciplina', 'count'),
            Créditos=('Créditos', 'sum')).to_excel(
                writer, sheet_name='Resumo', index=False)
    return caminho

checkboxes = [widgets.Checkbox(value=False, description=d,
             layout=widgets.Layout(width='500px')) for d in disciplinas]
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
display(widgets.VBox(checkboxes, layout=widgets.Layout(max_height='300px', overflow='auto')))
display(slider_periodos, slider_limite, checkbox_horarios, botao_gerar, output)
