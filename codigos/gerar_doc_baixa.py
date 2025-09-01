import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
# As bibliotecas abaixo são necessárias para gerar .docx e .pdf
# Se não as tiver, instale com: pip install python-docx reportlab
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from org_baixa import OrganizacaoBaixas
class GerarDocBaixa:
    def __init__(self, master, nome_planilha_base, dados_selecionados):
        self.janela_mestra_gerarbaixa = master
        self.nome_planilha_base = nome_planilha_base
        self.dados_selecionados_para_gerar = dados_selecionados
        self.toplevel_gerarbaixa = None
        self.carregar_recursos_gerarbaixa()

    def carregar_recursos_gerarbaixa(self):
        """Carrega a imagem do brasão para esta tela."""
        try:
            imagem_brasao = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao_para_gerarbaixa = ImageTk.PhotoImage(imagem_brasao)
        except Exception as e:
            print(f"Erro ao carregar brasão para Gerar Doc Baixa: {e}")
            self.brasao_para_gerarbaixa = None

    def exibir_tela(self):
        """Cria e exibe a janela de geração de documentos de baixa."""
        self.toplevel_gerarbaixa = ttk.Toplevel(self.janela_mestra_gerarbaixa)
        self.toplevel_gerarbaixa.title("Gerar Documentos de Baixa")
        self.toplevel_gerarbaixa.geometry("800x750")
        self.toplevel_gerarbaixa.position_center()
        self.toplevel_gerarbaixa.transient(self.janela_mestra_gerarbaixa)
        self.toplevel_gerarbaixa.grab_set()

        # --- Cabeçalho ---
        style = ttk.Style()
        style.configure('Header.TFrame', background='#5bc0de')
        frame_cabecalho = ttk.Frame(self.toplevel_gerarbaixa, style='Header.TFrame', padding=(10, 10))
        frame_cabecalho.pack(fill=X)
        if self.brasao_para_gerarbaixa:
            lbl_brasao = ttk.Label(frame_cabecalho, image=self.brasao_para_gerarbaixa, style='Header.TFrame')
            lbl_brasao.pack(side=LEFT, padx=(5, 10))
        lbl_titulo = ttk.Label(frame_cabecalho, text="Gerar Documentos de Baixa", font=("Inconsolata", 16, "bold"), background='#5bc0de', foreground='black')
        lbl_titulo.pack(side=LEFT, expand=True)

        # --- Frame Principal ---
        frame_corpo = ttk.Frame(self.toplevel_gerarbaixa, padding=20)
        frame_corpo.pack(expand=True, fill=BOTH)

        # --- Seção de Revisão Final ---
        frame_revisao = ttk.Labelframe(frame_corpo, text="Revisão final", padding=15)
        frame_revisao.pack(fill=X, pady=(0, 20))
        
        # Prepara os textos para a revisão
        total_documentos = len(self.dados_selecionados_para_gerar)
        unidades = list(set(key[0] for key in self.dados_selecionados_para_gerar.keys()))
        servidores = list(set(key[1] for key in self.dados_selecionados_para_gerar.keys()))
        
        texto_unidades = ", ".join(unidades[:3]) + ("..." if len(unidades) > 3 else "")
        texto_servidores = ", ".join(servidores[:3]) + ("..." if len(servidores) > 3 else "")
        data_geracao = datetime.now().strftime("%d/%m/%Y")

        ttk.Label(frame_revisao, text=f"Total de documentos a gerar: {total_documentos}").pack(anchor=W)
        ttk.Label(frame_revisao, text=f"Unidades envolvidas: {texto_unidades}").pack(anchor=W)
        ttk.Label(frame_revisao, text=f"Servidores responsáveis: {texto_servidores}").pack(anchor=W)
        ttk.Label(frame_revisao, text=f"Planilha base: {self.nome_planilha_base}").pack(anchor=W)
        ttk.Label(frame_revisao, text=f"Data da geração: {data_geracao}").pack(anchor=W)

        # --- Seção de Campos Obrigatórios ---
        frame_campos = ttk.Labelframe(frame_corpo, text="Campos obrigatórios*", padding=15)
        frame_campos.pack(fill=X, pady=(0, 20))
        frame_campos.grid_columnconfigure(0, weight=1)
        frame_campos.grid_columnconfigure(1, weight=1)

        self.entry_num_processo = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_num_processo.insert(0, "Número do processo")
        self.entry_num_processo.grid(row=0, column=0, sticky=EW, padx=(0, 10))
        
        self.entry_destino_final = ttk.Entry(frame_campos, font=("Inconsolata", 11))
        self.entry_destino_final.insert(0, "Local de destino final")
        self.entry_destino_final.grid(row=1, column=0, sticky=EW, padx=(0, 10), pady=(10, 0))

        self.text_observacoes = tk.Text(frame_campos, height=4, font=("Inconsolata", 11))
        self.text_observacoes.insert("1.0", "Observações gerais\nIrrecuperável, encaminhado pra leilão")
        self.text_observacoes.grid(row=0, column=1, rowspan=2, sticky=NSEW)

        # --- Seção de Configurações ---
        frame_configs = ttk.Labelframe(frame_corpo, text="Configurações", padding=15)
        frame_configs.pack(fill=X)

        self.formato_var = tk.StringVar(value=".pdf")
        ttk.Label(frame_configs, text="Formato do documento:").pack(side=LEFT)
        ttk.Radiobutton(frame_configs, text=".pdf", variable=self.formato_var, value=".pdf").pack(side=LEFT, padx=5)
        ttk.Radiobutton(frame_configs, text=".docx", variable=self.formato_var, value=".docx").pack(side=LEFT, padx=5)
        
        frame_pasta = ttk.Frame(frame_corpo, padding=(0, 20))
        frame_pasta.pack(fill=X)
        ttk.Label(frame_pasta, text="Pasta de destino:").pack(anchor=W, pady=(10, 0))
        self.entry_pasta_destino = ttk.Entry(frame_pasta, font=("Inconsolata", 11))
        self.entry_pasta_destino.pack(side=LEFT, fill=X, expand=True, ipady=4)
        ttk.Button(frame_pasta, text="Selecionar...", command=self.selecionar_pasta_destino).pack(side=LEFT, padx=(5,0))

        # --- Rodapé ---
        frame_rodape = ttk.Frame(self.toplevel_gerarbaixa, padding=10)
        frame_rodape.pack(fill=X, side=BOTTOM)
        ttk.Button(frame_rodape, text="<- Voltar e revisar agrupamentos", command=self.voltar_e_revisar, bootstyle="light-outline").pack(side=LEFT)
        ttk.Button(frame_rodape, text="Confirmar e gerar Documentos", command=self.confirmar_geracao, bootstyle="info").pack(side=RIGHT)

    def selecionar_pasta_destino(self):
        """Abre uma caixa de diálogo para selecionar uma pasta."""
        caminho = filedialog.askdirectory(title="Selecione a pasta de destino")
        if caminho:
            self.entry_pasta_destino.delete(0, END)
            self.entry_pasta_destino.insert(0, caminho)

    def confirmar_geracao(self):
        """Valida os campos e pede confirmação final antes de gerar o arquivo."""
        pasta = self.entry_pasta_destino.get()
        if not pasta:
            Messagebox.show_error("Erro", "Por favor, selecione uma pasta de destino.")
            return

        resposta = Messagebox.yesno("Confirmar Geração", "Você confirma a geração dos documentos com as informações fornecidas?")
        if resposta:
            self._gerar_arquivo()

    def _gerar_arquivo(self):
        """Gera o arquivo de texto com base nos dados e configurações."""
        formato = self.formato_var.get()
        pasta = self.entry_pasta_destino.get()
        nome_arquivo = f"Documento de Baixa - {datetime.now().strftime('%Y-%m-%d')}{formato}"
        caminho_completo = os.path.join(pasta, nome_arquivo)

        # Monta o conteúdo do texto
        conteudo_final = ""
        for (unidade, servidor), bens in self.dados_selecionados_para_gerar.items():
            conteudo_final += f"Unidade: {unidade}\n"
            conteudo_final += f"Servidor: {servidor}\n"
            conteudo_final += "Tombos:\n"
            for bem in bens:
                conteudo_final += f"    {bem['tombo']} - {bem['descricao']}\n"
            conteudo_final += "\n" # Adiciona um espaço entre os grupos
        
        try:
            # Lógica para salvar nos diferentes formatos
            if formato == ".docx":
                doc = Document()
                doc.add_paragraph(conteudo_final)
                doc.save(caminho_completo)
            elif formato == ".pdf":
                c = canvas.Canvas(caminho_completo, pagesize=letter)
                textobject = c.beginText(40, 750) # Posição inicial do texto
                for line in conteudo_final.split('\n'):
                    textobject.textLine(line)
                c.drawText(textobject)
                c.save()
            else: # .txt ou qualquer outro
                with open(caminho_completo, 'w', encoding='utf-8') as f:
                    f.write(conteudo_final)

            Messagebox.ok("Sucesso", f"Documento gerado com sucesso em:\n{caminho_completo}")
        except Exception as e:
            Messagebox.show_error("Erro", f"Não foi possível gerar o arquivo:\n{e}")

    def voltar_e_revisar(self):
        """Fecha a janela atual e reabre a anterior."""
        self.toplevel_gerarbaixa.destroy()
        # A janela anterior (org_baixa) foi destruída, então precisamos recriá-la.
        # A melhor abordagem seria passar a janela de menu principal para recriar a partir dela.
        tela_anterior = OrganizacaoBaixas(self.janela_mestra_gerarbaixa.master, self.nome_planilha_base, self.dados_brutos_recebidos)
        tela_anterior.org_baixas()
