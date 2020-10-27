import json
from typing import List
from constantes import CODIFICACAO
from excecoes import TipoMensagemInvalida
from enum import Enum, unique


@unique
class TipoPermitidosDeMensagem(Enum):
    movimentacao = "movimentacao"
    desistencia = "desistencia"
    chat = "chat"
    vencedor = "vencedor"
    conexao_estabelecida = "conexao_estabelecida"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TipoPermitidosDeMensagem))


class Mensagem:
    def __init__(self, tipo: str, conteudo: str, remetente: str):
        self._eh_um_tipo_valido(tipo_mensagem=tipo)
        self._conteudo: str = conteudo
        self._tipo: str = tipo
        self._remetente: str = remetente

    def __str__(self):
        return f"tipo: {self._tipo}, conteudo: {self._conteudo}, remetente: {self.remetente}"

    @property
    def remetente(self) -> str:
        return self._remetente

    @property
    def conteudo(self) -> str:
        return self._conteudo

    @conteudo.setter
    def conteudo(self, novo_valor) -> None:
        self._conteudo = novo_valor

    @property
    def tipo(self) -> str:
        return self._tipo

    @conteudo.setter
    def conteudo(self, novo_valor) -> None:
        self._conteudo = novo_valor

    def _eh_um_tipo_valido(self, tipo_mensagem: str):
        if tipo_mensagem in TipoPermitidosDeMensagem.list():
            return True

        raise TipoMensagemInvalida(
            f"Esse tipo de mensagem é inválida. Tipos permitidos: {TipoPermitidosDeMensagem.list()}"
        )

    def converter_bytes_para_json_e_setar_valores_da_classe(self, json_em_bytes: bytes):
        json_em_texto = json_em_bytes.decode(CODIFICACAO).replace("'", '"')
        resultado = json.loads(json_em_texto)

        self._eh_um_tipo_valido(resultado.get("tipo"))
        self._conteudo = resultado.get("conteudo")
        self._tipo = resultado.get("tipo")
        self._remetente = resultado.get("remetente")

    def converter_msg_em_bytes_para_enviar(self) -> bytes:
        msg = {
            "tipo": self._tipo,
            "conteudo": self._conteudo,
            "remetente": self.remetente,
        }
        return json.dumps(msg).encode(CODIFICACAO)
