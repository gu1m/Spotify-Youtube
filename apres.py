# importando bibliotecas
import pandas as pd
import plotly.express as px
import statistics as sts 
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

# lendo arquivos
df = pd.read_csv("df.csv")

# tirando todos os dados que não tem dados completos
df = df.dropna()


# configurando página
st.set_page_config(
    page_title="Dataframe Spotify/Youtube",
    page_icon="bar_chart:",
    layout="wide"
    
)
st.header("Dataframe Spotify/Youtube")

st.markdown("""---""")


# configurações da barra lateral
opcoes = ["Geral","Individual","Comparação"]
indi_geral = st.sidebar.selectbox("Escolha quais dados serão analisados", opcoes)

# se ecolher Individual
if indi_geral == "Individual":

    # vendo o total de músicas no Dataframe
    total_musicas = len(df["Track"])

    # analisando o total de artistas no Dataframe
    data = df.drop_duplicates(subset="Artist", keep='first')
    total_artistas = len(data["Artist"])

    col1,col2,col3 = st.columns(3)

    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)

    # colocando area de digitação para o usuario digitar a musica ou o artista para ser analisado
    keyword = st.text_input("Digite o nome de um artista")
    clicado = st.button("search")
    st.markdown("""---""")

    # verificando se há algo escrito no espaço para digitar
    if keyword is not None and len(str(keyword)) > 0:
        # se o usuario escolher para analisar musica
        dado = df.loc[df["Track"].isin ([keyword])]  
        # se o usuario escolher para analisar artista

        st.header("Dados Individuais do Artista Selecionado")

        st.write("Artista pesquisado")
        
        # encontrando o Artista no Dataframe
        dado = df.loc[df["Artist"].isin ([keyword])]

        # se o dado não for encontrado aparecerá a mensagem abaixo
        if dado.empty:
            st.subheader("Cantor não catalogado")

        # se o dado for encontrado irá proceder o algoritmo abaixo
        else:
            
            # encontrando o Artista no Dataframe
            dado = df.loc[df["Artist"].isin ([keyword])]

            # vendo o total de músicas que o Artista tem
            total_art_mus = len(dado["Track"])
                    
            
            # amostra de dados do artista
            st.write(dado)

            # analisando a media de likes do artista
            media_likes = sts.mean(dado["Likes"])
            col000,col001 = st.columns(2)
            col001.metric("A media de likes deste artista é:", round(media_likes,2))
            col000.metric("O total de musicas deste artista é:",total_art_mus)

            # realizando as estatisicas do artista 
            media_views = round(sts.mean(dado["Views"]),2)
            media_ene = round(sts.mean(dado["Energy"]),2)
            media_danc = round(sts.mean(dado["Danceability"]),2)
            media_stream = round(sts.mean(dado["Stream"]),2)
            total_visu = sum(dado["Views"])
            total_strea =  sum(dado["Stream"])

            # deixando a interface mais amigavel
            col10,col22,col33 = st.columns(3)
            col10.metric("Média de Views do Artista", media_views)
            col22.metric("Média de Energia", media_ene)
            col33.metric("A media de Danceabilidade", media_danc)

            col222,col004,col003 = st.columns(3)

            col222.metric("A media de vezes tocado no spotify", media_stream)
            col004.metric("O total de visualizações no Youtube:", total_visu)
            col003.metric("O total de vezes tocadas no Spotify:", total_strea)

            st.markdown("""---""")

            # espaço para o usuario pesquisar uma música dentro dos dados do artista selecionado
            keyword2 = st.text_input("Digite o nome de uma música do artista selecionado")
            clicado2 = st.button("search ")

            if keyword2 is not None and len(str(keyword2)) > 0:
                 # encontrando o nome da música nos dados do Artista
                dado_music = dado.loc[dado["Track"].isin ([keyword2])]
                
                # se a música não estiver catalogada
                if dado_music.empty:
                    st.subheader("Música não catalogada")
                
                # se a música estiver catalogada 
                else:
                    st.write(dado_music)

                    # pegando as informações da música
                    views_mu = sts.mode(dado_music["Views"])
                    dance  = sts.mode(dado_music["Danceability"])
                    Likes = sts.mode (dado_music["Likes"])
                    link = dado_music["Url_youtube"]

                    # deixando as informções mais visiveis para o usúario
                    col111,col222,col333 = st.columns(3)
                    col111.metric("O total de views desta música é:", views_mu)
                    col222.metric("A danceabilidade desta música é de:", dance)

                    col333.metric("O total de likes dessa música foi de", Likes)
                    
                    
                    col02, col444 = st.columns(2)

                    with col444:
                        st.markdown(f"{link}") 

                    
                    total_stream_spo = dado_music["Stream"]
                    col02.metric("O total de vezes tocadas no Spotify:", total_stream_spo)
            
            st.markdown("""---""")

            # Gráficos do artista 
            st.subheader("Gráficos e dados gerais do artista")

            # realizando os graficos individuais do artista
            data1 = df.loc[df["Artist"].isin ([keyword])]

            # neste histograma pode-se perceber o numero de musicas em correlação a popularidade
            fig07 =go.Histogram(x = data1.Stream, name="Spotify",marker=dict(line=dict(width=8,color="#d6ceaa"),color="#d6ceaa"))
            fig2 = go.Histogram(x = data1.Views, name="Youtube",marker=dict(line=dict(width=8,color="#5e2f46"),color="#5e2f46"))
            data4 = [fig07,fig2]
            layout = go.Layout(title="Representação do números de músicas em relação ao número de Views/Stream")
            figure = go.Figure(data = data4, layout= layout)
            figure.update_layout(xaxis_title="Views/Stream",yaxis_title="Total de Músicas")

            # neste plotbox pode ver a correlação de Danceabilidade e Views/Stream
            fig08 = go.Scatter(x=data1.Views, y=data1.Danceability, name="Youtube",mode="markers", marker=dict(line=dict(width=5,color="#eab05e"),color="#eab05e"))
            fig008 = go.Scatter(x=data1.Stream, y=data1.Danceability, name="Spotify",mode="markers",marker=dict(line=dict(width=5,color="#fdeecd"),color="#fdeecd"))
            data5 = [fig08,fig008]
            layout2 = go.Layout(title="Correlacionando a visibilidade da música com a danciabilidade")
            figure2= go.Figure(data = data5, layout = layout2)
            figure2.update_layout(xaxis_title="Views/Stream",yaxis_title="Danceabilidade")
            
            # neste plotbox pode ver a correlação de Energia e Views/Stream
            fig09 = go.Scatter(x=data1.Views, y=data1.Energy, name="Youtube",mode="markers", marker=dict(line=dict(width=8,color="#7e949e"),color="#7e949e"))
            fig009 = go.Scatter(x=data1.Stream, y=data1.Energy, name="Spotify",mode="markers", marker=dict(line=dict(width=8,color="#c4ceb0"),color="#c4ceb0"))
            data6 = [fig09,fig009]
            layout3 = go.Layout(title="Correlacionando a Energia da música com a visibilidade")
            figure3 = go.Figure(data = data6, layout = layout3)
            figure3.update_layout(xaxis_title="Views/Stream",yaxis_title="Energia")

            #neste plotbox pode ver o Tempo_ms em correlação com a Views/Stream
            fig10 = go.Scatter(x=data1.Views, y=data1.Duration_ms, name="Youtube",mode="markers", marker=dict(line=dict(width=8,color="#5e2f46"),color="#5e2f46"))
            fig100 = go.Scatter(x=data1.Stream, y=data1.Duration_ms, name="Spotify",mode="markers", marker=dict(line=dict(width=8,color="#829d74"),color="#829d74"))
            data7 = [fig10,fig100]
            layout4 = go.Layout(title="Correlacionando a Duração com a visibilidade da música")
            figure4 = go.Figure(data= data7, layout= layout4)
            figure4.update_layout(xaxis_title="Views/Stream",yaxis_title="Duração")

            # nesta matriz é apresentado a correlação entre os dados do dataframe
            data2 = data1.drop("Unnamed: 0", axis=1)
            fig11 = data2.corr(numeric_only=True)

            # aqui colocamos na variavel data1 a musica mais famosa do artista selecionado
            data1 = data1.nlargest(1, 'Views')[["Track","Likes","Views","Stream"]]
            st.write("A música mais famosa do artista no Youtube", data1)

            data1 = data1.nlargest(1, 'Stream')[["Track","Likes","Views","Stream"]]
            st.write("A música mais famosa do artista no Spotify", data1)


            st.markdown("""---""")
            #graficos em relação ao artista
            col0,col00 = st.columns(2)

            # aqui plotamos os graficos de fato no dashboard de forma organizada 
            with col0:
                st.write(figure)
                st.write("""O grafico a seguir análisa para cada música o numero de visualições""")
                st.markdown("""---""")

            with col00:
                st.write(figure2)
                st.markdown("""---""")

            col99, col90 = st.columns(2)

            with col99:
                st.write(figure3)
                st.markdown("""---""")

            with col90:
                st.write(figure4)
                st.markdown("""---""")   

            fig11.style.background_gradient(cmap='cividis')
            st.write("Matriz de Correlação entre os dados do Dataframe")
            st.write(fig11)
            st.write("""Este gráfico apresenta a dependência entre os dados do gráfico em relação a eles mesmos""")

# se o usuario escolher geral 
elif indi_geral == "Geral":
    # aqui apresentei o head do dataframe para o usuario visualizar os dados que estamos lidando
    st.header("Dados Gerais do Dataframe")
    # visualizando o total de musicas e artistas no dataframe
    total_musicas = len(df["Track"])
    data = df.drop_duplicates(subset="Artist", keep='first')
    total_artistas = len(data["Artist"])

    # colocando na interface o numero de artistas e musicas no dataframe
    col1,col2,col3 = st.columns(3)
    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)
    
    
    
    st.write("""Amostra de Dados""")
    st.write(df.head())
    
    col999, col000 =st.columns(2)
    
    with col999:
        # vendo qual o artista mais popular no dataframe
        st.write("""Música mais popular no Youtube:""")
        df.nlargest(1, 'Views')[['Track','Artist',"Views"]]
        st.write("""Música mais popular no Spotify:""")
        df.nlargest(1, 'Stream')[['Track','Artist',"Stream"]]
    
    
    media_dance = round(sts.mean(df["Danceability"]),2)
        
    col000.metric("A media de danciabilidade do Dataframe:",media_dance)

    st.markdown("""---""")
    # começando a plotar os graficos
    col01, col02 = st.columns(2)
   
    # O primeiro grafico representa a media de visualizações do Df em relação ao numero de músicas
    with col01:
        fig06 =go.Box(x=df.Views, name="Youtbe", marker=dict(color="#2b818c"))
        fig005 = go.Box(x=df.Stream,name="Spotify", marker=dict(color="#211c33"))
        data8 = [fig06,fig005]
        layout5 = go.Layout(title="Box plot das Views/Stream com o total de Musicas")
        figure5 = go.Figure(data=data8, layout=layout5)
        figure5.update_layout(xaxis_title="Views/Stream",yaxis_title="Total de Músicas")
        st.write(figure5)
        st.markdown("""---""")

    # O segundo grafico apresenta a correlção entre a danceabilidade e a visibilidade da música
    with col02:
        fig = go.Scatter(x=df.Views, y=df.Danceability, name="Youtube", mode='markers', marker=dict(color="#c02942"))
        fig0 = go.Scatter(x=df.Stream, y=df.Danceability, name="Spotify", mode='markers', marker=dict(color="#ecd078"))

        data8 = [fig, fig0]
        layout6 = go.Layout(title="Gráfico de disperção sobre Visibilidade da música em relação a Danceabilidade")
        figure6 = go.Figure(data=data8, layout=layout6)
        figure6.update_layout(xaxis_title="Views/Stream",yaxis_title="Danceabilidade")

        st.write(figure6)
        st.markdown("""---""")
    
    # O Terceiro grafico apresenta a visibilidade da música em relação a o quanto a música é viva
    col03, col04 = st.columns(2)

    with col03:
        fig2 = go.Scatter(x=df.Liveness, y=df.Views, name="Youtube",mode="markers", marker=dict(color="#87758f"))
        fig20 = go.Scatter(x=df.Liveness, y=df.Stream, name="Spotify",mode="markers", marker=dict(color="#2a091c"))
        data9 = [fig2,fig20]
        layout7 = go.Layout(title="Gráfico de disperção sobre a visibilidade da música em relação a o quanto a música é viva")
        figure7 = go.Figure(data=data9, layout=layout7)
        figure7.update_layout(xaxis_title="Views/Streams",yaxis_title="Liveness")
        st.write(figure7)
        st.markdown("""---""")

    # O quarto grafico apresenta a correlação entre o duração da música e visibilidade da música
    with col04:
        fig3 = go.Scatter(x=df.Views, y=df.Duration_ms, name="Youtube",mode="markers" ,marker=dict(color="#e5ddcb"))
        fig30 = go.Scatter(x=df.Stream, y=df.Duration_ms, name="Spotify",mode="markers", marker=dict(color="#a7c5bd"))
        data10 = [fig3, fig30]
        layout8 = go.Layout(title="Gráfico de disperção sobre a visibilidade da música em relação a Duração")
        figure8 = go.Figure(data=data10,layout=layout8)
        figure8.update_layout(xaxis_title="Views/Streams",yaxis_title="Duração")
        st.write(figure8)
        st.markdown("""---""")
    
    col756, col456 = st.columns(2)
    # O quinto grafico apresenta a correlação entre a Energia e a visibilidade da música
    with col756:
        fig4 = go.Scatter(x=df.Views, y=df.Energy, name="Youtube",mode="markers", marker=dict(color="#87758f"))
        fig40 = go.Scatter(x=df.Stream, y=df.Energy, name="Spotify",mode="markers", marker=dict(color="#a7c5bd"))
        data11 = [fig4,fig40]
        figure9 = go.Layout(title="Box plot sobre a visibilidade da música em relação a Energia")
        figure123 = go.Figure(data=data11,layout=figure9)
        figure123.update_layout(xaxis_title="Views/Streams",yaxis_title="Energia")
        st.write(figure123)
        
        st.markdown("""---""")
        
    
    with col456:
        data3 = df.drop("Unnamed: 0", axis=1)
        fig11 = data3.corr(numeric_only = True)
        fig11.style.background_gradient(cmap='cividis')
        st.write("Matriz de Correlação entre os dados do Dataframe")
        st.write(fig11)
        st.write("""Este gráfico apresenta a dependência entre os dados do gráfico em relação a eles mesmos""")

elif indi_geral == "Comparação":
    
    # vendo o total de músicas no Dataframe
    total_musicas = len(df["Track"])

    # analisando o total de artistas no Dataframe
    data = df.drop_duplicates(subset="Artist", keep='first')
    total_artistas = len(data["Artist"])

    col1,col2,col3 = st.columns(3)

    col1.metric("Total de músicas", total_musicas)
    col3.metric("Número de artistas", total_artistas)

    col005, col006 = st.columns(2)

    with col005:
        # colocando area de digitação para o usuario digitar a musica ou o artista para ser analisado
        keyword3 = st.text_input("Digite o nome de um artista  ")
        clicado3 = st.button("search  ")
        st.markdown("""---""")
    
    with col006:
        # colocando area de digitação para o usuario digitar a musica ou o artista para ser analisado
        keyword4 = st.text_input("Digite o nome de um artista   ")
        clicado4 = st.button("search   ")
        st.markdown("""---""")

    # deixando a interface mais amigavel 
    col007, col008 = st.columns(2)
    # vendo se há algo escrito no input
    if keyword3 is not None and len(str(keyword3)) > 0:
        
        # localizando o artista
        dado_comp1 = df.loc[df["Artist"].isin ([keyword3])]  
        
        # se o artista não for localizado
        if dado_comp1.empty:
            with col007:
                st.subheader("Artista não catalogada") 
        
        # se o artista for localizado
        else:
            with col007:
                st.write(dado_comp1)

                col010 , col020 = st.columns(2)
                col200, col210 = st.columns(2)
                col237, col129 = st.columns(2)


                total_views_comp1 = sum(dado_comp1["Views"])
                total_stream_comp1 = sum(dado_comp1["Stream"])
                media_energy_comp1 = round(sts.mean(dado_comp1["Energy"]),2)
                media_dance_comp1 = round(sts.mean(dado_comp1["Danceability"]),2)

                col010.metric("O total de views desse artista:", total_views_comp1)
                col020.metric("O total de stream desse artista:", total_stream_comp1)

                col200.metric("A media de Energia desse artista:", media_energy_comp1)
                col210.metric("A media de danceabilidade do artista:", media_dance_comp1)

                with col237:
                    st.write(f"A música mais famosa de {keyword3} no Youtube:")
                    dado_comp1.nlargest(1, 'Views')[['Track','Artist',"Views"]]
                
                with col129:
                    st.write(f"A música mais famosa de {keyword3} no Spotify:")
                    dado_comp1.nlargest(1, 'Stream')[['Track','Artist',"Views"]]
                
                st.markdown("---")
    
    
    # vendo se há algo escrito no input
    if keyword4 is not None and len(str(keyword4)) > 0:
        # localizando o artista
        dado_comp2 = df.loc[df["Artist"].isin ([keyword4])]

        # se o artista não for localizado
        if dado_comp2.empty:
            with col008:
                st.subheader("Artista não catalogada")
        
        
        # se o artista for localizado
        else:
            with col008:
                st.write(dado_comp2)

                col011 , col021 = st.columns(2)
                col201, col211 = st.columns(2)
                col232, col124 = st.columns(2)
                
                total_views_comp2 = sum(dado_comp2["Views"])
                total_stream_comp2 = sum(dado_comp2["Stream"])
                media_energy_comp2 = round(sts.mean(dado_comp2["Energy"]),2)
                media_dance_comp2 = round(sts.mean(dado_comp2["Danceability"]),2)

                col011.metric("O total de views desse artista:", total_views_comp2)
                col021.metric("O total de stream desse artista:", total_stream_comp2)

                col201.metric("A media de Energia desse artista:", media_energy_comp2)
                col211.metric("A media de danceabilidade do artista:", media_dance_comp2)

                with col232:
                    st.write(f"A música mais famosa de {keyword4} no Youtube:")
                    dado_comp2.nlargest(1, 'Views')[['Track','Artist',"Views"]]
                
                with col124:
                    st.write(f"A música mais famosa de {keyword4} no Spotify:")
                    dado_comp2.nlargest(1, 'Stream')[['Track','Artist',"Views"]]
                
                st.markdown("---")

    #plotando os gráficos 

        col909, col239 = st.columns(2)

        with col909:
            fig34 = go.Histogram(x=dado_comp1.Views, name=keyword3, marker=dict(color="#5ac7aa"))
            fig43 = go.Histogram(x=dado_comp2.Views, name=keyword4,marker=dict(color="#9adcb9"))
            

            data12 = [fig34,fig43]
            layout9 = go.Layout(title="Total de músicas em relação ao total de views no Youtube")
            figure10 = go.Figure(data=data12, layout=layout9)
            figure10.update_layout(xaxis_title="Views",yaxis_title="Total de Músicas")
            st.write(figure10)
            st.markdown("""---""")
        
        with col239:
            fig34 = go.Histogram(x=dado_comp1.Stream, name=keyword3, marker=dict(color="#5ac7aa"))
            fig43 = go.Histogram(x=dado_comp2.Stream, name=keyword4,marker=dict(color="#9adcb9"))
            

            data12 = [fig34,fig43]
            layout9 = go.Layout(title="Total de músicas em relação ao total de Streams no Spotify")
            figure10 = go.Figure(data=data12, layout=layout9)
            figure10.update_layout(xaxis_title="Streams",yaxis_title="Total de Músicas")
            st.write(figure10)
            st.markdown("""---""")
        
        col332, col123 = st.columns(2)

        with col332:
            fig = go.Scatter(x=dado_comp1.Views, y=dado_comp1.Danceability, name=keyword3,mode="markers", marker=dict(color="#c02942"))
            fig0 = go.Scatter(x=dado_comp2.Views, y=dado_comp2.Danceability, name=keyword4,mode="markers",marker=dict(color="#ecd078"))

            data8 = [fig, fig0]
            layout6 = go.Layout(title="Box plot sobre Visibilidade da música em relação a Danceabilidade no Youtube")
            figure6 = go.Figure(data=data8, layout=layout6)
            figure6.update_layout(xaxis_title="Views",yaxis_title="Danceabilidade")

            st.write(figure6)
            st.markdown("""---""")
        
        with col123:
            fig = go.Scatter(x=dado_comp1.Stream, y=dado_comp1.Danceability, name=keyword3,mode="markers", marker=dict(color="#c02942"))
            fig0 = go.Scatter(x=dado_comp2.Stream, y=dado_comp2.Danceability, name=keyword4,mode="markers",marker=dict(color="#ecd078"))

            data8 = [fig, fig0]
            layout6 = go.Layout(title="Box plot sobre Visibilidade da música em relação a Danceabilidade no Spotify")
            figure6 = go.Figure(data=data8, layout=layout6)
            figure6.update_layout(xaxis_title="Streams",yaxis_title="Danceabilidade")

            st.write(figure6)
            st.markdown("""---""")

        col342, col356 = st.columns(2)

        with col342:
            fig4 = go.Scatter(x=dado_comp1.Views, y=dado_comp1.Energy, name=keyword3,mode="markers", marker=dict(color="#87758f"))
            fig40 = go.Scatter(x=dado_comp2.Views, y=dado_comp2.Energy, name=keyword4,mode="markers", marker=dict(color="#a7c5bd"))
            data11 = [fig4,fig40]
            layout10 = go.Layout(title="Box plot sobre a visibilidade da música em relação a Energia no Youtube")
            figure11= go.Figure(data=data11,layout=layout10)
            figure11.update_layout(xaxis_title="Views",yaxis_title="Energia")
            st.write(figure11)
            st.markdown("""---""")
        
        with col356:
            fig4 = go.Scatter(x=dado_comp1.Stream, y=dado_comp1.Energy, name=keyword3,mode="markers", marker=dict(color="#87758f"))
            fig40 = go.Scatter(x=dado_comp2.Stream, y=dado_comp2.Energy, name=keyword4,mode="markers", marker=dict(color="#a7c5bd"))
            data11 = [fig4,fig40]
            figure9 = go.Layout(title="Box plot sobre a visibilidade da música em relação a Energia no Spotify")
            figure11= go.Figure(data=data11,layout=figure9)
            figure11.update_layout(xaxis_title="Stream",yaxis_title="Energia")
            st.write(figure11)
            st.markdown("""---""")


        
        
        





