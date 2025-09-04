import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import openpyxl
from datetime import datetime

class EdicaoPlanilha:
    def __init__(self, master, nome_planilha, caminho_arquivo_aberto=None, dados_iniciais=None, db_controller=None, id_desfazimento=None):
        self.janela_mestra = master
        self.nome_da_planilha_atual = nome_planilha
        self.caminho_arquivo_atual = caminho_arquivo_aberto
        self.dados_carregados = dados_iniciais
        
        self.db = db_controller
        self.id_desfazimento_atual = id_desfazimento
        
        self.toplevel_edicao = None
        self.numero_ordem_atual = 1
        self.carregar_recursos_edicao()

    def carregar_recursos_edicao(self):
        """Carrega as imagens necessárias (apenas o brasão) para a tela de edição."""
        try:
            imagem_brasao_edicao = Image.open("imagens/brasao_UFAC.png").resize((40, 40))
            self.brasao_para_edicao = ImageTk.PhotoImage(imagem_brasao_edicao)
        except Exception as e:
            print(f"Erro ao carregar imagem do brasão para tela de edição: {e}")
            self.brasao_para_edicao = None

    def exibir_tela(self):
        """Cria e exibe a janela principal para edição da planilha."""
        if self.toplevel_edicao and self.toplevel_edicao.winfo_exists():
            self.toplevel_edicao.lift()
            return

        self.toplevel_edicao = ttk.Toplevel(self.janela_mestra)
        self.toplevel_edicao.title("Editando Planilha de Desfazimento")
        self.toplevel_edicao.geometry("1200x700")
        self.toplevel_edicao.transient(self.janela_mestra)
        self.toplevel_edicao.position_center()
        self.toplevel_edicao.grab_set()

        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        style.configure( 'custom.TButton', font=("Inconsolata", 14), borderwidth=1, padding=(10, 10), background='white', foreground='#5bc0de')
        style.map('custom.TButton', bordercolor=[('!active', '#adb5bd'), ('active', '#5bc0de')], background=[('active', "#ececec"), ('!active', 'white')], relief=[('pressed', 'solid'), ('!pressed', 'solid')])

        frame_cabecalho_edicao = ttk.Frame(self.toplevel_edicao, style='Header.TFrame', padding=(10, 5))
        frame_cabecalho_edicao.pack(fill=X, side=TOP)

        if self.brasao_para_edicao:
            label_brasao_edicao = ttk.Label(frame_cabecalho_edicao, image=self.brasao_para_edicao, style='Header.TFrame')
            label_brasao_edicao.pack(side=LEFT, padx=(5, 10))

        label_titulo_edicao = ttk.Label(frame_cabecalho_edicao, text="Planilha de Desfazimento", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        label_titulo_edicao.pack(side=LEFT, expand=True, pady=5)

        frame_botoes_inferiores = ttk.Frame(self.toplevel_edicao, padding=10)
        frame_botoes_inferiores.pack(fill=X, side=BOTTOM)

        frame_corpo_edicao = ttk.Frame(self.toplevel_edicao, padding=(20, 20))
        frame_corpo_edicao.pack(expand=True, fill=BOTH)

        frame_input_tombos = ttk.Frame(frame_corpo_edicao)
        frame_input_tombos.pack(fill=X, pady=(0, 15))

        label_instrucao_tombo = ttk.Label(frame_input_tombos, text="Digite o número do tombo:", font=("Inconsolata", 12))
        label_instrucao_tombo.pack(side=LEFT, padx=(0, 10))

        self.entry_numero_tombo = ttk.Entry(frame_input_tombos, font=("Inconsolata", 12), width=30)
        self.entry_numero_tombo.pack(side=LEFT, fill=X, expand=True)
        self.entry_numero_tombo.bind("<Return>", lambda event: self.adicionar_item_planilha())

        botao_adicionar_tombo = ttk.Button( frame_input_tombos, text="Adicionar", bootstyle="info",style='custom.TButton', command=self.adicionar_item_planilha)
        botao_adicionar_tombo.pack(side=LEFT, padx=(10, 0))

        label_titulo_relatorio = ttk.Label(frame_corpo_edicao, text=self.nome_da_planilha_atual, font=("Inconsolata", 12, "bold"))
        label_titulo_relatorio.pack(fill=X, pady=(0, 5))

        colunas = ('ordem', 'tombo', 'descricao', 'data_aq', 'doc_fiscal', 'unidade', 'classificacao', 'destino')
        self.tabela_desfazimento = ttk.Treeview(frame_corpo_edicao, columns=colunas, show='headings', bootstyle="info")
        
        headings = ['Nº DE ORDEM', 'TOMBO', 'DESCRIÇÃO DO BEM', 'DATA DA AQUISIÇÃO', 'DOCUMENTO FISCAL', 'UNIDADE RESPONSÁVEL', 'CLASSIFICAÇÃO', 'DESTINAÇÃO']
        widths = [100, 100, 350, 120, 120, 200, 120, 120]
        for col, head, w in zip(colunas, headings, widths):
            self.tabela_desfazimento.heading(col, text=head)
            self.tabela_desfazimento.column(col, width=w, anchor=CENTER if col in ['ordem', 'tombo'] else W)

        scrollbar_vertical = ttk.Scrollbar(frame_corpo_edicao, orient=VERTICAL, command=self.tabela_desfazimento.yview)
        self.tabela_desfazimento.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)
        self.tabela_desfazimento.pack(expand=True, fill=BOTH)

        botao_voltar_edicao = ttk.Button(frame_botoes_inferiores, text="<- Voltar", command=self.toplevel_edicao.destroy, style='custom.TButton', bootstyle="light-outline")
        botao_voltar_edicao.pack(side=LEFT)
        
        botao_gerar_planilha = ttk.Button(frame_botoes_inferiores, text="Gerar Planilha", command=self.gerar_planilha_final, bootstyle="success", style='custom.TButton')
        botao_gerar_planilha.pack(side=RIGHT, padx=(0, 10))
        
        botao_salvar_edicao = ttk.Button(frame_botoes_inferiores, text="Salvar", command=self.salvar_alteracoes, style='custom.TButton', bootstyle="info")
        botao_salvar_edicao.pack(side=RIGHT, padx=(0, 10))

        botao_editar_item = ttk.Button(frame_botoes_inferiores, text="Editar", command=self.editar_item_selecionado, style='custom.TButton', bootstyle="info-outline")
        botao_editar_item.pack(side=RIGHT, padx=(0, 10))

        self._popular_tabela_com_dados_carregados()

    def _popular_tabela_com_dados_carregados(self):
        """Verifica se há dados carregados e os insere na tabela."""
        if self.dados_carregados:
            for linha in self.dados_carregados:
                self.tabela_desfazimento.insert('', END, values=linha)
            if self.dados_carregados:
                self.numero_ordem_atual = len(self.dados_carregados) + 1
    
    def adicionar_item_planilha(self):
        """Busca o tombo no banco, o associa ao desfazimento e o adiciona na tabela da interface."""
        if not self.db:
            Messagebox.show_error("Erro Crítico", "A conexão com o banco de dados não foi estabelecida.")
            return

        if self.id_desfazimento_atual is None:
            Messagebox.show_error("Erro de Processo", "Não há um processo de desfazimento ativo. \n\n"
                                  "Se está a continuar uma edição, certifique-se que o ficheiro foi salvo anteriormente pelo sistema.")
            return

        numero_tombo = self.entry_numero_tombo.get().strip()
        if not numero_tombo:
            Messagebox.show_warning(title="Atenção", message="Por favor, digite um número de tombo.")
            return

        for item_id in self.tabela_desfazimento.get_children():
            item_values = self.tabela_desfazimento.item(item_id)['values']
            if str(item_values[1]) == numero_tombo:
                Messagebox.show_warning("Tombo Duplicado", f"O tombo '{numero_tombo}' já foi adicionado a esta planilha.")
                self.entry_numero_tombo.delete(0, END)
                return

        bem_data = self.db.get_bem_by_tombo(numero_tombo)
        
        if not bem_data:
            Messagebox.show_warning("Tombo não encontrado", f"O bem de tombo '{numero_tombo}' não foi encontrado no banco de dados.")
            return

        id_desfazimento_no_banco = bem_data.get('id_desfazimento')
        if id_desfazimento_no_banco is not None and id_desfazimento_no_banco != self.id_desfazimento_atual:
            Messagebox.show_warning("Bem em Uso", f"O tombo '{numero_tombo}' já está associado a outro processo de desfazimento.")
            return

        if id_desfazimento_no_banco is None:
            sucesso = self.db.associar_bem_a_desfazimento(numero_tombo, self.id_desfazimento_atual)
            if not sucesso: return

        data_aq_formatada = bem_data['data_aquisicao'].strftime('%d/%m/%Y') if bem_data.get('data_aquisicao') else 'N/A'

        valores_linha = (
            self.numero_ordem_atual,
            bem_data.get('tombo', 'N/A'),
            bem_data.get('descricao', 'N/A'),
            data_aq_formatada,
            bem_data.get('nota_fiscal', 'N/A'),
            bem_data.get('nome_unidade', 'N/A'),
            'Irrecuperável', 'Alienação/Leilão'
        )

        self.tabela_desfazimento.insert('', END, values=valores_linha)
        self.numero_ordem_atual += 1
        self.entry_numero_tombo.delete(0, END)

    def editar_item_selecionado(self):
        """Abre uma janela para editar o item selecionado."""
        item_selecionado_id = self.tabela_desfazimento.focus()
        if not item_selecionado_id:
            Messagebox.show_warning(title="Atenção", message="Nenhum item selecionado para editar.")
            return
        
        valores_atuais = self.tabela_desfazimento.item(item_selecionado_id)['values']
        janela_edicao_item = ttk.Toplevel(self.toplevel_edicao)
        janela_edicao_item.title("Editar Item")
        janela_edicao_item.transient(self.toplevel_edicao)
        janela_edicao_item.grab_set()
        frame_edicao_campos = ttk.Frame(janela_edicao_item, padding=15)
        frame_edicao_campos.pack(expand=True, fill=BOTH)
        campos_entrada = {}
        colunas_nomes = ['Nº ORDEM', 'TOMBO', 'DESCRIÇÃO', 'DATA AQUISIÇÃO', 'DOC. FISCAL', 'UNIDADE', 'CLASSIFICAÇÃO', 'DESTINO']
        for i, nome_coluna in enumerate(colunas_nomes):
            lbl = ttk.Label(frame_edicao_campos, text=f"{nome_coluna}:")
            lbl.grid(row=i, column=0, sticky=W, pady=5)
            ent = ttk.Entry(frame_edicao_campos, width=40)
            ent.grid(row=i, column=1, sticky=EW, pady=5)
            ent.insert(0, valores_atuais[i])
            campos_entrada[i] = ent
        def salvar_edicao():
            novos_valores = [campos_entrada[i].get() for i in range(len(colunas_nomes))]
            self.tabela_desfazimento.item(item_selecionado_id, values=novos_valores)
            janela_edicao_item.destroy()
        botao_salvar_edicao_item = ttk.Button(frame_edicao_campos, text="Salvar Alterações", command=salvar_edicao, bootstyle="success")
        botao_salvar_edicao_item.grid(row=len(colunas_nomes), column=0, columnspan=2, pady=15)

    def _salvar_dados_no_arquivo(self, caminho):
        """Lógica interna para salvar os dados da tabela no ficheiro Excel."""
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Relatório de Desfazimento"
            cabecalho = [self.tabela_desfazimento.heading(c)['text'] for c in self.tabela_desfazimento['columns']]
            sheet.append(cabecalho)
            for item_id in self.tabela_desfazimento.get_children():
                sheet.append(self.tabela_desfazimento.item(item_id)['values'])
            workbook.save(caminho)
            return True
        except Exception as e:
            Messagebox.show_error(title="Erro ao Salvar", message=f"Ocorreu um erro ao salvar o ficheiro:\n{e}")
            return False

    # --- MUDANÇA PRINCIPAL: Conecta o salvamento ao banco de dados ---
    def salvar_alteracoes(self):
        """Salva as alterações no ficheiro atual e no banco de dados."""
        if not self.caminho_arquivo_atual:
            Messagebox.show_error(title="Erro", message="Nenhum ficheiro associado a esta planilha.")
            return

        if self._salvar_dados_no_arquivo(self.caminho_arquivo_atual):
            total_tombos = len(self.tabela_desfazimento.get_children())
            self.db.salvar_ou_atualizar_planilha_finalizada(
                id_desfazimento=self.id_desfazimento_atual,
                nome_planilha=self.nome_da_planilha_atual,
                caminho=self.caminho_arquivo_atual,
                total_tombos=total_tombos
            )
            Messagebox.ok(title="Sucesso", message="Os dados foram salvos.")

    # --- MUDANÇA PRINCIPAL: Conecta o salvamento ao banco de dados ---
    def gerar_planilha_final(self):
        """Salva as alterações no ficheiro atual e no banco de dados, com uma mensagem final."""
        if not self.caminho_arquivo_atual:
            Messagebox.show_error(title="Erro", message="Nenhum ficheiro associado a esta planilha.")
            return
            
        if self._salvar_dados_no_arquivo(self.caminho_arquivo_atual):
            total_tombos = len(self.tabela_desfazimento.get_children())
            self.db.salvar_ou_atualizar_planilha_finalizada(
                id_desfazimento=self.id_desfazimento_atual,
                nome_planilha=self.nome_da_planilha_atual,
                caminho=self.caminho_arquivo_atual,
                total_tombos=total_tombos
            )
            mensagem = f"Planilha gerada com sucesso em:\n{self.caminho_arquivo_atual}"
            Messagebox.ok(title="Sucesso", message=mensagem)