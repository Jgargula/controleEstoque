# -*- coding: utf-8 -*-
import re
from functools import partial


from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView


from Views.mainClientes import Ui_ct_MainClientes
from Views.formClientes import Ui_ct_FormClientes
from Crud.CrudClientes import CrudClientes


class MainClientes(Ui_ct_MainClientes, Ui_ct_FormClientes):

    def mainclientes(self, frame):
        super(MainClientes, self).setMainClientes(frame)
        self.frameMainClientes.show()

        # Icones Botoes
        self.IconeBotaoMenu(self.bt_BuscaClientes,
                            self.resourcepath('Images/search.png'))
        self.IconeBotaoMenu(self.bt_PrintRelatCliente,
                            self.resourcepath('Images/gtk-print.png'))
        self.IconeBotaoForm(self.bt_AddNovoClientes,
                            self.resourcepath('Images/addCliente.svg'))

        # Botao Adicionar Cliente / FormClientes
        self.bt_AddNovoClientes.clicked.connect(self.FormClientes)

        # Tamanho colunas tabela
        self.tb_Clientes.blockSignals(True)
        self.tb_Clientes.setColumnHidden(0, True)
        self.tb_Clientes.setColumnWidth(1, 40)
        self.tb_Clientes.setColumnWidth(2, 350)
        self.tb_Clientes.setColumnWidth(3, 235)
        self.tb_Clientes.setColumnWidth(4, 265)
        self.tb_Clientes.setColumnWidth(5, 40)

        # Populando Tabela
        self.TabelaClientes()

        # Busca CLiente por nome
        self.tx_BuscaClientes.textEdited.connect(self.TabelaClientes)

        # Botao imprimir
        self.bt_PrintRelatCliente.clicked.connect(self.imprimirCliente)

    # Dados Tabela

    def TabelaClientes(self):
        lista = CrudClientes()
        busca = self.tx_BuscaClientes.text()
        lista.ListaClientesTabela(busca)
        i = 0

        while self.tb_Clientes.rowCount() > 0:
            self.tb_Clientes.removeRow(0)

        if len(lista.nomeCliente) >= 1:
            while i < len(lista.nomeCliente):
                self.tb_Clientes.insertRow(i)
                self.TabelaStatus(self.tb_Clientes, i, 0,
                                  self.StatusEntrega(1))
                self.TabelaID(self.tb_Clientes, i, 1, lista.idCliente[i])
                self.TabelaNomeTelefone(self.tb_Clientes, i, 2,
                                        lista.nomeCliente[i],
                                        lista.apelidoCliente[i])
                self.TabelaNomeTelefone(self.tb_Clientes, i, 3,
                                        self.formatoNumTelefone(
                                            lista.celularCliente[i]),
                                        self.formatoNumTelefone(
                                            lista.telefoneCliente[i]))
                self.TabelaNomeTelefone(self.tb_Clientes, i, 4,
                                        lista.emailCliente[i], "")
                # Sinal click tabela
                self.botaoTabela(self.tb_Clientes, i, 5, partial(
                    self.SelectCliente, lista.idCliente[i]), "#005099")
                i += 1
            pass

    # Seleciona Cliente por ID
    def SelectCliente(self, valor):
        id = valor
        self.FormClientes()
        self.tx_Id.setText(str(id))
        busca = CrudClientes()
        busca.SelectClienteID(id)
        self.tx_NomeFantasia.setText(busca.nomeCliente)
        self.tx_RazaoSocial.setText(busca.apelidoCliente)
        self.tx_cnpj.setText(busca.cpfCliente)
        self.tx_InscEstadual.setText(busca.rgCliente)
        self.tx_Celular.setText(busca.celularCliente)
        self.tx_Telefone.setText(busca.telefoneCliente)
        self.tx_Email.setText(busca.emailCliente)
        self.tx_Obs.setText(busca.obsCliente)
        self.tx_Cep.setText(busca.cepCliente)
        self.tx_Endereco.setText(busca.enderecoCliente)
        self.tx_Numero.setText(busca.numCliente)
        self.tx_Bairro.setText(busca.bairroCliente)
        self.tx_Cidade.setText(busca.cidadeCliente)
        self.tx_Estado.setText(busca.estadoCliente)

        for row in range(self.tb_Historico.rowCount()):
            self.tb_Historico.removeRow(row)

        total = '0.00'
        for row in range(len(busca.dataEntrega)):
            # print row
            self.tb_Historico.insertRow(row)
            self.conteudoTabela(
                self.tb_Historico, row, 0, str(busca.dataEmissao[row]))
            self.conteudoTabela(
                self.tb_Historico, row, 1, str(busca.dataEntrega[row]))
            self.conteudoTabela(
                self.tb_Historico, row, 2, str(busca.Total[row]))

            total = float(busca.Total[row]) + float(total)

        self.lb_TotalHistorico.setText(format(float(total), ".2f"))
        pass

    # Frame Formulário Produtos
    def FormClientes(self):
        # self.DesativaBotaoProdutos()
        self.LimpaFrame(self.ct_containerClientes)
        super(MainClientes, self).setFormClientes(self.ct_containerClientes)
        self.fr_FormClientes.show()

        # ICone Botoes
        self.IconeBotaoMenu(self.bt_Salvar,
                            self.resourcepath('Images/salvar.png'))
        self.IconeBotaoMenu(self.bt_Voltar,
                            self.resourcepath('Images/cancelar.png'))
        self.IconeBotaoMenu(self.bt_BuscaCep,
                            self.resourcepath('Images/find.png'))

        # Checando se existe ID válido
        self.IdCheckCliente()

        # Tamanho tabela Histórico
        self.tb_Historico.setColumnWidth(0, 100)
        self.tb_Historico.setColumnWidth(1, 100)
        self.tb_Historico.setColumnWidth(2, 100)
        self.tb_Historico.setColumnHidden(3, True)

        # Botão Voltar
        self.bt_Voltar.clicked.connect(self.janelaClientes)
        # Botao Salvar
        self.bt_Salvar.clicked.connect(self.VerificaInputClientes)

        # Buscar Cep
        self.bt_BuscaCep.clicked.connect(self.buscarCepCliente)
        self.tx_Cep.returnPressed.connect(self.buscarCepCliente)

        pass

    # checando campo Id se é Edicao ou Novo Cliente
    def IdCheckCliente(self):
        if not self.tx_Id.text():
            busca = CrudClientes()
            self.tx_Id.setText(str(busca.lastIDCliente()))
        pass

    # Valida Inputs
    def VerificaInputClientes(self):
        if not self.tx_NomeFantasia.text():
            self.tx_NomeFantasia.setFocus()
        elif not self.tx_Celular.text():
            self.tx_Celular.setFocus()
        else:
            self.CadCliente()

    def CadCliente(self):
        INSERI = CrudClientes()
        INSERI.idCliente = self.tx_Id.text()
        INSERI.nomeCliente = self.tx_NomeFantasia.text().upper()
        INSERI.apelidoCliente = self.tx_RazaoSocial.text().upper()
        INSERI.cpfCliente = re.sub(
            '[^[0-9]', '', self.tx_cnpj.text())
        INSERI.rgCliente = re.sub(
            '[^[0-9]', '', self.tx_InscEstadual.text())

        INSERI.celularCliente = re.sub(
            '[^[0-9]', '', self.tx_Celular.text())
        INSERI.telefoneCliente = re.sub(
            '[^[0-9]', '', self.tx_Telefone.text())
        INSERI.emailCliente = self.tx_Email.text()
        INSERI.obsCliente = self.tx_Obs.text().upper()
        INSERI.cepCliente = re.sub(
            '[^[0-9]', '', self.tx_Cep.text())
        INSERI.enderecoCliente = self.tx_Endereco.text().upper()
        INSERI.numCliente = self.tx_Numero.text()
        INSERI.bairroCliente = self.tx_Bairro.text().upper()
        INSERI.cidadeCliente = self.tx_Cidade.text().upper()
        INSERI.estadoCliente = self.tx_Estado.text().upper()
        INSERI.CadCliente()

        self.janelaClientes()

        pass

        # Imprimindo

    def imprimirCliente(self):
        self.documento = QWebEngineView()

        headertable = ["Cod", "Nome ", "Telefone", "Email"]
        buscaFornecedor = CrudClientes()
        buscaFornecedor.ListaClientesTabela('')
        html = self.renderTemplate(
            "clientes.html",
            estilo=self.resourcepath('Template/estilo.css'),
            titulo="LISTAGEM CLIENTES",
            headertable=headertable,
            codcliente=buscaFornecedor.idCliente,
            nomeCliente=buscaFornecedor.nomeCliente,
            telefoneFornecedor=buscaFornecedor.celularCliente,
            emailFornecedor=buscaFornecedor.emailCliente
        )

        self.documento.load(QUrl("file:///" +
                                 self.resourcepath("report.html")))
        self.documento.loadFinished['bool'].connect(self.previaImpressao)
