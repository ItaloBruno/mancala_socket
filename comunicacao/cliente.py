import socket
import sys
import _thread


endereco_ip = sys.argv[1]
porta = int(sys.argv[2])
id_cliente = int(sys.argv[3])
conexoes_ativas = []


def enviar_mensagem_ao_servidor():
    while True:
        messagem = input("\ndigite uma mensagem: ")
        print(f"Enviando: {messagem}")
        conexao.send(messagem.encode())


def receber_mensagem_do_servidor():
    while True:
        try:
            # recebendo mensagem do servidor
            dados = conexao.recv(2048)
        except:
            print("A conexão com o servidor foi encerrada!")
            _thread.interrupt_main()
            break

        if not dados:
            print("A conexão com o servidor foi encerrada!")
            _thread.interrupt_main()
            break

        else:
            print(f"Mensagem recebida do servidor: {dados.decode()}")


def criar_cliente(host='localhost', port=8080):
    # Criando um socket TCP/IP
    conexa_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Realizando mapeamento entre o socket e a porta
    infos_servidor = (host, port)

    print(f"Conectando no host {infos_servidor[0]} na porta {infos_servidor[1]}")
    conexa_cliente.connect(infos_servidor)
    print("Conectado!")

    return conexa_cliente


if __name__ == '__main__':
    conexao = criar_cliente(host=endereco_ip, port=porta)

    _thread.start_new_thread(enviar_mensagem_ao_servidor, ())
    _thread.start_new_thread(receber_mensagem_do_servidor, ())

    while True:
        continue
