
import string
import unicodedata


def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = texto.translate(str.maketrans("", "", string.punctuation))

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto

def mostrar_menu():

    print("\n" + "=" * 40)
    print("       🌙 ESCOLA DE INGLÊS DA LUNA")
    print("=" * 40)

    print("\nO que vamos estudar hoje?")

    print("\n1. Aprender vocabulário")
    print("2. Fazer um quiz de inglês")
    print("3. Praticar conversação")
    print("4. Encerrar aula")

    escolha = input("\nDigite sua opção: ")

    return escolha



def iniciar_luna():

    print("\nOlá! Eu sou a Luna! 🌙")
    print("Sua tutora pessoal de inglês.")

    while True:

        escolha = mostrar_menu()

        if escolha == "1":
            print("\n📚 Vamos estudar vocabulário!")

        elif escolha == "2":
            print("\n✏️ Vamos começar um quiz de inglês!")

        elif escolha == "3":
            print("\n💬 Vamos praticar conversação!")

        elif escolha == "4":
            print("\nAté nossa próxima aula! Bons estudos! ❤️")
            break

        else:
            print("\nOpção inválida! Escolha uma opção de 1 a 4.")


if __name__ == "__main__":
    iniciar_luna()
