

import string
import unicodedata
import json
import io
import asyncio
import tempfile
import os
import pygame
import edge_tts
from html import unescape

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote


# ==========================================
# CONFIGURACAO DE VOZ
# ==========================================

VOZ_PORTUGUES = "pt-BR-FranciscaNeural"
VOZ_INGLES = "en-US-JennyNeural"


# ==========================================
# NORMALIZAR TEXTO
# ==========================================

def normalizar_texto(texto):

    texto = texto.lower().strip()
    texto = texto.translate(
        str.maketrans("", "", string.punctuation)
    )
    texto = unicodedata.normalize("NFD")

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


# ==========================================
# TRADUZIR INGLES PARA PORTUGUES
# ==========================================

def traduzir_texto(texto):

    endereco = (
        "https://api.mymemory.translated.net/get?q="
        + quote(texto)
        + "&langpair=en|pt"
    )

    requisicao = Request(
        endereco,
        headers={"User-Agent": "LunaEnglishTutor/1.0"}
    )

    try:

        with urlopen(requisicao, timeout=15) as resposta:

            dados = json.loads(
                resposta.read().decode("utf-8")
            )

        traducao = dados.get(
            "responseData", {}
        ).get("translatedText", "")

        if traducao:
            return unescape(traducao)

    except Exception as erro:

        print("\nNão consegui obter a tradução:", erro)

    return "Tradução indisponível no momento."


# ==========================================
# MOSTRAR LEGENDA
# ==========================================

def mostrar_legenda(texto):

    print("\n🇺🇸 Inglês:")
    print(texto)

    print("\n🇧🇷 Português:")
    print(traduzir_texto(texto))


# ==========================================
# FALAR COM A VOZ DA LUNA
# ==========================================

async def gerar_fala(texto, voz, arquivo):

    comunicacao = edge_tts.Communicate(
        texto,
        voz
    )

    await comunicacao.save(arquivo)


def falar(texto, idioma="pt"):

    voz = VOZ_PORTUGUES if idioma == "pt" else VOZ_INGLES

    arquivo = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        ) as temporario:

            arquivo = temporario.name

        asyncio.run(
            gerar_fala(texto, voz, arquivo)
        )

        pygame.mixer.init()
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

    except Exception as erro:

        print("\nNão consegui reproduzir a voz:", erro)

        try:
            pygame.mixer.quit()
        except Exception:
            pass

    finally:

        if arquivo and os.path.exists(arquivo):

            try:
                os.remove(arquivo)
            except OSError:
                pass


# ==========================================
# BUSCAR VOCABULARIO
# ==========================================

def buscar_vocabulario(palavra):

    endereco = (
        "https://api.dictionaryapi.dev/api/v2/entries/en/"
        + quote(palavra)
    )

    requisicao = Request(
        endereco,
        headers={"User-Agent": "LunaEnglishTutor/1.0"}
    )

    try:

        with urlopen(requisicao, timeout=15) as resposta:

            dados = json.loads(
                resposta.read().decode("utf-8")
            )

        entrada = dados[0]

        palavra_encontrada = entrada.get("word", palavra)

        print("\n======================================")
        print("\nPalavra:", palavra_encontrada)

        falar(palavra_encontrada, "en")

        pronuncia = entrada.get(
            "phonetic",
            "Não disponível"
        )

        print("\nPronúncia:", pronuncia)

        if pronuncia != "Não disponível":
            falar("The pronunciation is " + pronuncia, "en")

        for significado in entrada.get("meanings", []):

            classe = significado.get(
                "partOfSpeech",
                "Não informada"
            )

            print("\n======================================")
            print("\nClasse gramatical:", classe)

            for definicao in significado.get(
                "definitions", []
            )[:3]:

                texto_definicao = definicao.get(
                    "definition", ""
                )

                if texto_definicao:

                    mostrar_legenda(texto_definicao)

                    falar(texto_definicao, "en")

                exemplo = definicao.get("example")

                if exemplo:

                    mostrar_legenda(exemplo)

                    falar(exemplo, "en")

        mensagem_final = (
            "Great! We finished this vocabulary lesson."
        )

        mostrar_legenda(mensagem_final)
        falar(mensagem_final, "en")

        print("\nConsulta concluída! 🌙")

    except HTTPError as erro:

        print("\nErro na consulta ao dicionário:", erro.code)
        falar("I could not find this word.", "en")

    except URLError as erro:

        print("\nErro de conexão:", erro.reason)
        falar("There was a connection problem.", "en")

    except Exception as erro:

        print("\nOcorreu um erro:", erro)


# ==========================================
# MENU PRINCIPAL
# ==========================================

def mostrar_menu():

    print("\n======================================")
    print("       🌙 LUNA - ENGLISH TUTOR")
    print("======================================")

    print("\n1. Aprender vocabulário")
    print("2. Fazer um quiz de inglês")
    print("3. Praticar conversação")
    print("4. Encerrar aula")

    print("\n======================================")


# ==========================================
# INICIAR LUNA
# ==========================================

def iniciar_luna():

    saudacao = "Olá! Eu sou a Luna. Vamos aprender inglês juntas?"

    print("\n" + saudacao)
    falar(saudacao, "pt")

    while True:

        mostrar_menu()

        opcao = input("\nDigite sua opção: ").strip()

        if opcao == "1":

            palavra = input(
                "\nDigite uma palavra em inglês: "
            ).strip()

            if palavra:
                buscar_vocabulario(palavra)
            else:
                print("\nVocê não digitou nenhuma palavra.")

        elif opcao == "2":

            mensagem = "O módulo de quiz será desenvolvido em breve!"
            print("\n" + mensagem)
            falar(mensagem, "pt")

        elif opcao == "3":

            mensagem = "O módulo de conversação será desenvolvido em breve!"
            print("\n" + mensagem)
            falar(mensagem, "pt")

        elif opcao == "4":

            mensagem = "Até a próxima aula! Bons estudos!"
            print("\n" + mensagem)
            falar(mensagem, "pt")
            break

        else:

            print("\nOpção inválida. Tente novamente.")


# ==========================================
# EXECUTAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    iniciar_luna()
