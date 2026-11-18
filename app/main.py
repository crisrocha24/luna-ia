
import string


def iniciar_luna():

    print("=" * 45)
    print("       🌙 OLÁ! EU SOU A LUNA")
    print("=" * 45)

    nome = input("\nComo você se chama? ").strip().rstrip(string.punctuation)

    print(f"\nPrazer em conhecer você, {nome}!")

    print("\nEu sou sua tutora pessoal de inglês.")
    print("Vamos aprender inglês juntas, passo a passo!")

    resposta = input("\nComo está seu dia hoje? ").strip().lower()

    if resposta in ["ótimo", "otimo", "excelente", "maravilhoso"]:
        print("\nQue maravilha! Fico feliz por você! 😊")

    elif resposta in ["bem", "bom", "legal"]:
        print("\nQue bom! Vamos aproveitar para aprender inglês!")

    elif resposta in ["mal", "ruim", "péssimo", "pessimo"]:
        print("\nSinto muito. Espero que seu dia melhore! ❤️")

    else:
        print("\nEntendi! Obrigada por compartilhar comigo.")

    print("\nNossa expressão de hoje:")
    print("Hello! = Olá!")

    print("\nAté nossa próxima aula! 🌙")


if __name__ == "__main__":
    iniciar_luna()

