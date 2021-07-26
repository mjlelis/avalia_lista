import pandas as pd
import streamlit as st


with st.form(key='questionario'):
    score_aderencia = st.slider(label='Socre Aderência:', min_value=0, max_value=5, value=0, step=1,
                                        format='%f')
    st.write('Observações sobre sua avaliação que extrapolam as prguntas acima.')
    obs = st.text_area("Conclusão da Avaliação:", "Sua observação")

    submeter = st.form_submit_button("Submeter Avaliação")
    # resultados = pd.read_csv('dfs/resultados.csv')

    if submeter:
        dados_resultados = {
            'score': [score_aderencia],
            'obss' : [obs]
        }
        df_r = pd.DataFrame(dados_resultados)
        df_r.to_csv('dfs/resultados.csv', mode="a", index=False, header=False)
