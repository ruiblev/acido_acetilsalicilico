import streamlit as st
import streamlit.components.v1 as components
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Simulador de Síntese - Ácido Acetilsalicílico",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS PERSONALIZADO ---
def inject_custom_css():
    st.markdown("""
        <style>
            /* Tipografia e cores globais */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            
            /* Melhoria visual para botões do Streamlit */
            .stButton > button {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
                border-color: transparent;
                color: white;
            }
            .stButton > button:active {
                transform: translateY(0);
            }
            
            /* Card Effect for Containers */
            .card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            }
            
            /* Títulos */
            h1, h2, h3 {
                color: #1e293b;
                font-weight: 700;
            }
            
            /* Alerta personalizado */
            .instruction-box {
                background: #f8fafc;
                border-left: 4px solid #3b82f6;
                padding: 15px 20px;
                border-radius: 0 8px 8px 0;
                color: #334155;
                margin-bottom: 20px;
                font-size: 1.05rem;
            }
        </style>
    """, unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'mode' not in st.session_state:
    st.session_state.mode = 'estudo'
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'pratico_phase' not in st.session_state:
    st.session_state.pratico_phase = 'prep'

def get_prep_block(step):
    mapping = {
        1: 1, 
        2: 2, 3: 2, 
        4: 3, 5: 3, 
        6: 4, 7: 4, 
        8: 5, 9: 5, 
        10: 6, 11: 6, 12: 6
    }
    return mapping.get(step, 1)

def next_step():
    current_block = get_prep_block(st.session_state.step)
    st.session_state.step += 1
    next_block = get_prep_block(st.session_state.step)
    if st.session_state.mode == 'pratico' and current_block != next_block:
        st.session_state.pratico_phase = 'prep'

def previous_step():
    current_block = get_prep_block(st.session_state.step)
    st.session_state.step = max(1, st.session_state.step - 1)
    prev_block = get_prep_block(st.session_state.step)
    if st.session_state.mode == 'pratico' and current_block != prev_block:
        st.session_state.pratico_phase = 'prep'

def set_mode():
    if st.session_state.radio_mode == 'Modo Prático-Experimental':
        st.session_state.mode = 'pratico'
    else:
        st.session_state.mode = 'estudo'

# --- DICIONÁRIOS DO MODO PRÁTICO ---
# Todas as ações possíveis (corretas + distratores)
ALL_ACTIONS = [
    "Pesar cerca de 2 g de ácido salicílico num erlenmeyer",
    "Adicionar 5 mL de anidrido acético e 4 gotas de ácido sulfúrico",
    "Aquecer em banho de água (50-60 °C) e adicionar 2 mL de água destilada",
    "Adicionar 20 mL de água fria e arrefecer em banho de gelo",
    "Filtração em vácuo",
    "Secagem"
]

# Todos os materiais possíveis
ALL_MATERIALS = [
    "2 Copos de precipitação de 600 mL",
    "Anidrido acético (líquido)",
    "Balança",
    "Bomba de vácuo com Kitasato e Guko",
    "Erlenmeyer de 100 mL",
    "Espátula",
    "Estufa",
    "Funil de Büchner",
    "Funil de pós",
    "Gelo",
    "Papel de filtro",
    "Pinça",
    "Pipeta de 2 mL",
    "Pipeta de 5 mL",
    "Placa de aquecimento",
    "Pompete/macrocontrolador",
    "Proveta de 25 mL",
    "Termómetro",
    "Vareta de vidro",
    "Vidro de relógio",
    "Ácido salicílico (sólido)",
    "Ácido sulfúrico 96% (frasco conta-gotas)",
    "Água destilada (esguicho)"
]

# Ação correta por bloco (1 - 6)
PRATICO_CORRECT_ACTIONS = {
    1: "Pesar cerca de 2 g de ácido salicílico num erlenmeyer",
    2: "Adicionar 5 mL de anidrido acético e 4 gotas de ácido sulfúrico",
    3: "Aquecer em banho de água (50-60 °C) e adicionar 2 mL de água destilada",
    4: "Adicionar 20 mL de água fria e arrefecer em banho de gelo",
    5: "Filtração em vácuo",
    6: "Secagem"
}

# Materiais essenciais necessários por bloco (1 - 6)
PRATICO_CORRECT_MATERIALS = {
    1: ["Balança", "Erlenmeyer de 100 mL", "Espátula", "Funil de pós", "Ácido salicílico (sólido)"],
    2: ["Erlenmeyer de 100 mL", "Anidrido acético (líquido)", "Pipeta de 5 mL", "Pompete/macrocontrolador", "Ácido sulfúrico 96% (frasco conta-gotas)"],
    3: ["Erlenmeyer de 100 mL", "Placa de aquecimento", "2 Copos de precipitação de 600 mL", "Termómetro", "Água destilada (esguicho)", "Pipeta de 2 mL", "Pompete/macrocontrolador", "Vareta de vidro"],
    4: ["Erlenmeyer de 100 mL", "Proveta de 25 mL", "2 Copos de precipitação de 600 mL", "Gelo", "Água destilada (esguicho)"],
    5: ["Erlenmeyer de 100 mL", "Funil de Büchner", "Bomba de vácuo com Kitasato e Guko", "Papel de filtro", "Água destilada (esguicho)", "Vareta de vidro"],
    6: ["Vidro de relógio", "Espátula", "Papel de filtro", "Estufa", "Pinça", "Balança"]
}


# --- NAVEGAÇÃO / HEADER Principal ---
def header():
    st.title("🧪 Síntese do Ácido Acetilsalicílico")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.radio("Modo de Simulação:", 
                 ['Modo de Estudo', 'Modo Prático-Experimental'], 
                 index=0 if st.session_state.mode == 'estudo' else 1,
                 key='radio_mode', 
                 on_change=set_mode, 
                 horizontal=True)
                 
    with col2:
        if st.button("Reiniciar Simulador", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
    progress = st.session_state.step / 12
    st.progress(progress if progress <= 1 else 1.0)
    st.caption(f"Etapa {st.session_state.step} de 12{' - Fase de Preparação' if (st.session_state.mode == 'pratico' and st.session_state.pratico_phase == 'prep' and st.session_state.step <= 12) else ''}")
    st.divider()

# --- ETAPAS DO PROCEDIMENTO ---

def etapa_1():
    st.subheader("Etapa 1: Pesagem do Ácido Salicílico")
    st.markdown("""
        <div class="instruction-box">
            Meça cerca de <strong>2 g</strong> de ácido salicílico num erlenmeyer de 100 mL.
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Coloque o erlenmeyer na balança e utilize o botão abaixo para deitar o ácido salicílico lentamente. Pare quando atingir 2,00 g.")
    # CSS para esconder o botão "Avançar_Hidden"
    st.markdown("""
        <style>
            div[data-testid="stButton"] > button:contains("Avançar_Hidden") {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Path to index.html
    html_path = os.path.join(os.path.dirname(__file__), "components", "weighing_scale", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=600)
    
    # Hidden button triggered by JavaScript inside the iframe
    st.button("Avançar_Hidden", key="btn_avancar", on_click=next_step)
def etapa_2():
    st.subheader("Etapa 2: Adição do Anidrido Acético")
    st.markdown("""
        <div class="instruction-box">
            Meça, com uma pipeta, <strong>5 mL</strong> de anidrido acético na <i>hotte</i> e verta para o erlenmeyer.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "pipette", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=550)
    st.button("Avançar_Hidden", key="btn_avancar_2", on_click=next_step)
    
    st.button("Retroceder", on_click=previous_step)

def etapa_3():
    st.subheader("Etapa 3: Adição do Ácido Sulfúrico")
    st.markdown("""
        <div class="instruction-box">
            Adicione <strong>4 gotas</strong> de ácido sulfúrico 96% (m/m).
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "dropper", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=500)
    st.button("Avançar_Hidden", key="btn_avancar_3", on_click=next_step)
    
    st.button("Retroceder", on_click=previous_step)

def etapa_4():
    st.subheader("Etapa 4: Aquecimento a 50-60 °C")
    st.markdown("""
        <div class="instruction-box">
            Aqueça o erlenmeyer em banho de água a 50-60 °C durante 10 minutos, agitando até dissolver todo o ácido salicílico.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "hotplate", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    st.markdown("<style>div[data-testid='stTextInput'] { display: none; }</style>", unsafe_allow_html=True)
    st.text_input("Temp_Hidden", key="hotplate_temp", label_visibility="collapsed")
    
    components.html(html_string, height=600)
    st.button("Avançar_Hidden", key="btn_avancar_4", on_click=next_step)
    
    st.button("Retroceder", on_click=previous_step)

def etapa_5():
    st.subheader("Etapa 5: Adição de Água Destilada")
    st.markdown("""
        <div class="instruction-box">
            Adicione <strong>2 mL</strong> de água destilada, continuando o aquecimento e a agitação.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "water_add", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read().replace("{{AMOUNT}}", "2 mL")
    
    components.html(html_string, height=550)
    st.button("Avançar_Hidden", key="btn_avancar_5", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_6():
    st.subheader("Etapa 6: Adição de Água Fria")
    st.markdown("""
        <div class="instruction-box">
            Retire o erlenmeyer do banho de água e adicione mais <strong>20 mL</strong> de água fria.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "water_add", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read().replace("{{AMOUNT}}", "20 mL")
    
    components.html(html_string, height=550)
    st.button("Avançar_Hidden", key="btn_avancar_6", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_7():
    st.subheader("Etapa 7: Arrefecimento em Banho de Gelo")
    st.markdown("""
        <div class="instruction-box">
            Arrefeça em banho de gelo para obter cristais de ácido acetilsalicílico.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "ice_bath", "index.html")
    import random
    temp_str = st.session_state.get('hotplate_temp', '55')
    try:
        base_temp = float(temp_str)
    except:
        base_temp = 55.0
        
    reduced_temp = int(base_temp * random.uniform(0.7, 0.8)) # 20% a 30% inferior
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "ice_bath", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read().replace("{{TEMP}}", str(reduced_temp))
    
    components.html(html_string, height=500)
    st.button("Avançar_Hidden", key="btn_avancar_7", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_8():
    st.subheader("Etapa 8: Filtração a Vácuo")
    st.markdown("""
        <div class="instruction-box">
            Filtre por vácuo os cristais obtidos, medindo previamente a massa do papel de filtro.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "filtration", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=650)
    st.button("Avançar_Hidden", key="btn_avancar_8", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_9():
    st.subheader("Etapa 9: Lavagem dos Cristais")
    st.markdown("""
        <div class="instruction-box">
            Lave os cristais na placa de filtro com pequenas porções de água fria por duas vezes.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "washing", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=650)
    st.button("Avançar_Hidden", key="btn_avancar_9", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_10():
    st.subheader("Etapa 10: Transferência")
    st.markdown("""
        <div class="instruction-box">
            Transfira cuidadosamente o papel de filtro e cristais para um vidro de relógio previamente tarado.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "transfer", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=600)
    st.button("Avançar_Hidden", key="btn_avancar_10", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_11():
    st.subheader("Etapa 11: Secagem Quente")
    st.markdown("""
        <div class="instruction-box">
            Coloque o vidro de relógio na estufa a 90 °C para remover o excesso de humidade.
        </div>
    """, unsafe_allow_html=True)
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "oven", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read()
    
    components.html(html_string, height=500)
    st.button("Avançar_Hidden", key="btn_avancar_11", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def etapa_12():
    st.subheader("Etapa 12: Pesagem Final")
    st.markdown("""
        <div class="instruction-box">
            Determine a massa dos cristais finalmente secos na balança para descobrir o seu rendimento.
        </div>
    """, unsafe_allow_html=True)
    
    import random
    if 'final_mass' not in st.session_state:
        temp_str = st.session_state.get('hotplate_temp', '55')
        try:
            temp = float(temp_str)
        except:
            temp = 55.0
            
        base_yield = 2.609 # Rendimento teórico de 2.0g de ác. salicílico
        
        if 50 <= temp <= 60:
            error_factor = random.uniform(0.90, 0.99) # 1% a 10% erro
        else:
            error_factor = random.uniform(0.80, 0.90) # 10% a 20% erro
            
        st.session_state.final_mass = round(base_yield * error_factor, 4)
        
    final_mass_str = f"{st.session_state.final_mass:.4f}"
    
    html_path = os.path.join(os.path.dirname(__file__), "components", "weighing_final", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_string = f.read().replace("{{MASS}}", final_mass_str)
    
    components.html(html_string, height=500)
    st.button("Avançar_Hidden", key="btn_avancar_12", on_click=next_step)
    st.button("Retroceder", on_click=previous_step)

def render_prep_phase():
    prep_block = get_prep_block(st.session_state.step)
    
    st.subheader(f"Preparação da Fase Laboratorial {prep_block} de 6")
    st.markdown("Para avançar para a execução da(s) próxima(s) etapa(s) no Modo Prático-Experimental, **selecione a ação principal** e **todo o material** necessário.")
    
    import random
    
    # Initialize separate shuffle states to avoid reshuffling on every interaction
    if 'shuffled_actions' not in st.session_state or st.session_state.get('last_prep_block') != prep_block:
        # Filter action list: Remove actions completed in previous blocks to simulate progression
        past_correct_actions = [PRATICO_CORRECT_ACTIONS[i] for i in range(1, prep_block)]
        available_actions = [act for act in ALL_ACTIONS if act not in past_correct_actions]
        
        st.session_state.shuffled_actions = random.sample(available_actions, len(available_actions))
        st.session_state.sorted_materials = ALL_MATERIALS
        st.session_state.last_prep_block = prep_block
        
    selected_action = st.selectbox(
        "Qual é a próxima ação a realizar?", 
        ["Selecione uma opção..."] + st.session_state.shuffled_actions
    )
    
    st.markdown("### Seleção de Material")
    selected_materials = st.multiselect(
        "Selecione o(s) material(is) necessário(s) para este processo:", 
        st.session_state.sorted_materials
    )
    
    if st.button("Validar Escolhas", type="primary"):
        correct_action = PRATICO_CORRECT_ACTIONS[prep_block]
        correct_materials = set(PRATICO_CORRECT_MATERIALS[prep_block])
        selected_materials_set = set(selected_materials)
        
        errors = []
        if selected_action == "Selecione uma opção...":
            errors.append("Por favor, selecione uma ação.")
        elif selected_action != correct_action:
            errors.append("❌ A ação escolhida não é a correta para esta(s) etapa(s).")
            
        if selected_materials_set != correct_materials:
            missing = correct_materials - selected_materials_set
            extra = selected_materials_set - correct_materials
            if missing:
                errors.append(f"❌ Faltam selecionar {len(missing)} material(is) essencial(is).")
            if extra:
                errors.append(f"❌ Foram selecionados {len(extra)} material(is) desnecessário(s) ou incorreto(s).")
                
        if not errors:
            if prepare_next_steps_message := "✅ Escolhas corretas! A iniciar simulação da etapa...":
                st.success(prepare_next_steps_message)
            st.session_state.pratico_phase = 'exec'
            st.rerun()
        else:
            for e in errors:
                st.error(e)

# --- CONTROLADOR PRINCIPAL ---
def main():
    inject_custom_css()
    header()
    
    # Modo Prático - Fase de Preparação (Apenas passos 1 a 12)
    if st.session_state.step <= 12 and st.session_state.mode == 'pratico' and st.session_state.pratico_phase == 'prep':
        render_prep_phase()
    else:
        # Execução das simulações visuais e conclusão
        if st.session_state.step == 1:
            etapa_1()
        elif st.session_state.step == 2:
            etapa_2()
        elif st.session_state.step == 3:
            etapa_3()
        elif st.session_state.step == 4:
            etapa_4()
        elif st.session_state.step == 5:
            etapa_5()
        elif st.session_state.step == 6:
            etapa_6()
        elif st.session_state.step == 7:
            etapa_7()
        elif st.session_state.step == 8:
            etapa_8()
        elif st.session_state.step == 9:
            etapa_9()
        elif st.session_state.step == 10:
            etapa_10()
        elif st.session_state.step == 11:
            etapa_11()
        elif st.session_state.step == 12:
            etapa_12()
        else:
            st.subheader("Conclusão do Procedimento & Análise")
            st.success("Parabéns! Completaste a síntese do ácido acetilsalicílico no simulador inteiramente interactivo! Regista agora a massa isolada no relatório.")
            st.balloons()
            
            st.markdown("---")
            st.markdown("### Cálculo do Rendimento (η)")
            st.markdown(
                "Sabendo que a massa de Ácido Salicílico (limitante) inicialmente pesada na Etapa 1 foi de **2,00 g**, "
                "insira abaixo a **Percentagem de Rendimento (%)** que obteve nos seus cálculos, utilizando a massa experimental observada ao final da Etapa 12."
            )
            
            with st.form("rendimento_form"):
                user_yield = st.number_input("O seu rendimento calculado (%)", min_value=0.0, max_value=150.0, step=0.1, format="%.1f")
                submit_yield = st.form_submit_button("Verificar Resultados")
                
                if submit_yield:
                    # Theoretical yield for 2.00g of salicylic acid is ~2.609 g of ASA
                    massa_teorica = 2.609 
                    massa_experimental = st.session_state.get('final_mass', 0.0)
                    
                    # Math: (experimental / theoretical) * 100
                    if massa_experimental > 0:
                        real_yield_percent = (massa_experimental / massa_teorica) * 100
                    else:
                        real_yield_percent = 0.0
                    
                    st.markdown(f"**Massa Teórica Esperada:** {massa_teorica:.3f} g")
                    st.markdown(f"**Massa Experimental Obtida:** {massa_experimental:.4f} g")
                    st.markdown(f"**Rendimento Real Calculado:** {real_yield_percent:.1f} %")
                    
                    # Tolerância para arredondamentos
                    diff = abs(user_yield - real_yield_percent)
                    
                    if diff <= 0.5:
                        st.success("✅ Excelente! Os seus cálculos de rendimento estão corretos. O valor aproxima-se perfeitamente da realidade experimental gerada.")
                    elif diff <= 2.0:
                        st.warning("⚠️ Sucesso Parcial. Os seus cálculos estão próximos, mas verifique os seus arredondamentos e as casas decimais usadas na fórmula teórica.")
                    else:
                        st.error("❌ Os resultados não correspondem. Por favor, reveja como calculou a massa molar do limitante e os seus fatores estequiométricos.")
            
            st.button("Reiniciar Simulador", on_click=lambda: st.session_state.clear())

if __name__ == "__main__":
    main()
