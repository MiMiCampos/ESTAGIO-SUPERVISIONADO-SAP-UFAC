import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import hashlib
from PIL import Image, ImageTk
from utils.path_helper import resource_path

class GerenciadorUsuarios:
    def __init__(self, master, db_controller, dados_usuario_logado):
        self.janela_mestra = master
        self.db = db_controller
        self.usuario_logado = dados_usuario_logado
        self.toplevel = None
        self.tabela = None
        self.brasao = None
        self._carregar_recursos()

    def _carregar_recursos(self):
        """Carrega a imagem do brasão."""
        try:
            brasao_img = Image.open("imagens/brasao_UFAC.png").resize((50, 50))
            self.brasao = ImageTk.PhotoImage(brasao_img)
        except Exception as e:
            print(f"Erro ao carregar imagem do brasão para Gerenciador: {e}")
            self.brasao = None

    def exibir_tela(self):
        if self.toplevel and self.toplevel.winfo_exists():
            self.toplevel.lift()
            return

        self.toplevel = ttk.Toplevel(self.janela_mestra)
        self.toplevel.title("Gerenciamento de Usuários")
        # self.toplevel.geometry("800x600")
        # self.toplevel.position_center()
        
        screen_width = self.toplevel.winfo_screenwidth()
        screen_height = self.toplevel.winfo_screenheight()
        self.toplevel.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.toplevel.transient(self.janela_mestra)

        frame_cabecalho = ttk.Frame(self.toplevel, bootstyle='info', padding=(10, 5))
        frame_cabecalho.pack(fill=X)

        if self.brasao:
            lbl_brasao = ttk.Label(frame_cabecalho, image=self.brasao, bootstyle='info')
            lbl_brasao.pack(side=LEFT, padx=10)

        lbl_titulo = ttk.Label(frame_cabecalho, text="Gerenciamento de Usuários", font=("Inconsolata", 16, "bold"), bootstyle='inverse-info', foreground='black')
        lbl_titulo.pack(expand=True)

        frame_corpo = ttk.Frame(self.toplevel, padding=20)
        frame_corpo.pack(expand=True, fill=BOTH)

        colunas = ('id', 'nome', 'cpf', 'perfil')
        self.tabela = ttk.Treeview(frame_corpo, columns=colunas, show='headings', bootstyle="info")
        self.tabela.heading('id', text='ID')
        self.tabela.heading('nome', text='Nome Completo')
        self.tabela.heading('cpf', text='CPF')
        self.tabela.heading('perfil', text='Perfil')
        self.tabela.column('id', width=50, anchor=CENTER)
        self.tabela.column('nome', width=250)
        self.tabela.column('cpf', width=150, anchor=CENTER)
        self.tabela.column('perfil', width=100, anchor=CENTER)
        self.tabela.pack(expand=True, fill=BOTH)
        self._popular_tabela()

        frame_rodape = ttk.Frame(self.toplevel, padding=(10, 15))
        frame_rodape.pack(fill=X, side=BOTTOM)
        
        btn_voltar = ttk.Button(frame_rodape, text="<- Voltar", command=self.toplevel.destroy, bootstyle="primary-outline")
        btn_voltar.pack(side=LEFT, padx=(10, 0)) # Adicionado padding à esquerda
        
        btn_excluir = ttk.Button(frame_rodape, text="Excluir", command=self._deletar_usuario_selecionado, bootstyle="danger")
        # Espaçamento de 10px da borda direita da janela
        btn_excluir.pack(side=RIGHT, padx=(0, 10))
        
        btn_editar = ttk.Button(frame_rodape, text="Editar", command=self._abrir_janela_edicao_selecionado, bootstyle="info")
        # Espaçamento de 10px para o botão à sua direita (Excluir)
        btn_editar.pack(side=RIGHT, padx=(0, 10))

        btn_adicionar = ttk.Button(frame_rodape, text="Novo Usuário", command=lambda: self._abrir_janela_edicao(), bootstyle="success")
        # Espaçamento de 10px para o botão à sua direita (Editar)
        btn_adicionar.pack(side=RIGHT, padx=(0, 10))

    def _popular_tabela(self):
        """Limpa e preenche a tabela com os dados mais recentes do banco."""
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        
        usuarios = self.db.listar_usuarios()
        for usuario in usuarios:
            self.tabela.insert('', END, values=(usuario['id_usuario'], usuario['nome_completo'], usuario['cpf'], usuario['perfil']))

    def _abrir_janela_edicao_selecionado(self):
        item_selecionado_id = self.tabela.focus()
        if not item_selecionado_id:
            Messagebox.show_warning("Nenhum usuário selecionado", "Por favor, selecione um usuário na lista para editar.")
            return
        
        dados_item = self.tabela.item(item_selecionado_id)
        dados_usuario = {
            'id_usuario': dados_item['values'][0],
            'nome_completo': dados_item['values'][1],
            'cpf': dados_item['values'][2],
            'perfil': dados_item['values'][3]
        }
        self._abrir_janela_edicao(dados_usuario)

    def _deletar_usuario_selecionado(self):
        item_selecionado_id = self.tabela.focus()
        if not item_selecionado_id:
            Messagebox.show_warning("Nenhum usuário selecionado", "Por favor, selecione um usuário na lista para excluir.")
            return

        id_usuario_para_deletar = int(self.tabela.item(item_selecionado_id)['values'][0])
        
        if id_usuario_para_deletar == self.usuario_logado['id_usuario']:
            Messagebox.show_error("Ação Inválida", "Você não pode excluir o seu próprio usuário.")
            return

        nome_usuario = self.tabela.item(item_selecionado_id)['values'][1]
        resposta = Messagebox.yesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o usuário '{nome_usuario}'?\nEsta ação não pode ser desfeita.")

        if resposta == "Sim":
            if self.db.deletar_usuario(id_usuario_para_deletar):
                Messagebox.ok("Sucesso", "Usuário excluído com sucesso.")
                self._popular_tabela()
                
    def _abrir_janela_edicao(self, dados_usuario=None):
        """Abre uma janela para adicionar ou editar um usuário."""
        modo_edicao = dados_usuario is not None
        titulo = "Editar Usuário" if modo_edicao else "Adicionar Novo Usuário"

        dialog = ttk.Toplevel(self.toplevel)
        dialog.title(titulo)
        dialog.transient(self.toplevel)
        dialog.grab_set()
        dialog.position_center()
        
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(expand=True, fill=BOTH)
        frame.grid_columnconfigure(1, weight=1)

        style = ttk.Style()
        style.configure('Form.TEntry', padding=(0, 4))
        style.configure('Form.TCombobox', padding=(0, 4))

        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0, sticky=W, pady=5, padx=(0,10))
        
        lista_servidores = self.db.get_todos_servidores()
        combo_nome_servidor = ttk.Combobox(frame, values=lista_servidores, width=40, style='Form.TCombobox')
        combo_nome_servidor.grid(row=0, column=1, sticky=EW, pady=(0, 10))

        ent_nome_estagiario = ttk.Entry(frame, style='Form.TEntry', width=40)
        ent_nome_estagiario.grid(row=0, column=1, sticky=EW, pady=(0, 10))
        ent_nome_estagiario.grid_remove() 
        
        ttk.Label(frame, text="CPF:").grid(row=1, column=0, sticky=W, pady=5, padx=(0,10))
        ent_cpf = ttk.Entry(frame, style='Form.TEntry', width=40)
        ent_cpf.grid(row=1, column=1, sticky=EW, pady=(0, 10))

        # --- Função para formatar o CPF ---
        def _formatar_cpf_dialog(event=None):
            texto_atual = ent_cpf.get()
            numeros = "".join(filter(str.isdigit, texto_atual))
            numeros = numeros[:11]

            formatado = ""
            if len(numeros) > 9:
                formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
            elif len(numeros) > 6:
                formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
            elif len(numeros) > 3:
                formatado = f"{numeros[:3]}.{numeros[3:]}"
            else:
                formatado = numeros
            
            ent_cpf.delete(0, END)
            ent_cpf.insert(0, formatado)
            ent_cpf.icursor(END)

        # --- Conecta a função ao campo de CPF ---
        ent_cpf.bind("<KeyRelease>", _formatar_cpf_dialog)

        lbl_senha = ttk.Label(frame, text="Senha:")
        lbl_senha.grid(row=2, column=0, sticky=W, pady=5, padx=(0,10))
        ent_senha = ttk.Entry(frame, show="*", style='Form.TEntry', width=40)
        ent_senha.grid(row=2, column=1, sticky=EW, pady=(0, 10))
        
        if modo_edicao:
            lbl_senha.config(text="Nova Senha (opcional):")

        ttk.Label(frame, text="Perfil:").grid(row=3, column=0, sticky=W, pady=5, padx=(0,10))
        combo_perfil = ttk.Combobox(frame, values=['Servidor', 'Estagiário'], state='readonly', style='Form.TCombobox', width=38)
        combo_perfil.grid(row=3, column=1, sticky=EW, pady=(0, 10))
        combo_perfil.set('Servidor')

        def _on_perfil_changed(event=None):
            if combo_perfil.get() == 'Servidor':
                ent_nome_estagiario.grid_remove()
                combo_nome_servidor.grid()
            else:
                combo_nome_servidor.grid_remove()
                ent_nome_estagiario.grid()
        
        combo_perfil.bind("<<ComboboxSelected>>", _on_perfil_changed)

        if modo_edicao:
            combo_perfil.set(dados_usuario['perfil'])
            combo_perfil.config(state='disabled')
            
            if dados_usuario['perfil'] == 'Servidor':
                combo_nome_servidor.set(dados_usuario['nome_completo'])
                ent_nome_estagiario.grid_remove()
            else:
                ent_nome_estagiario.insert(0, dados_usuario['nome_completo'])
                combo_nome_servidor.grid_remove()
                ent_nome_estagiario.grid()

            ent_cpf.insert(0, dados_usuario['cpf'])

        frame_botoes = ttk.Frame(frame)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        def _salvar_usuario():
            perfil = combo_perfil.get()
            nome = ""
            if perfil == 'Servidor':
                nome = combo_nome_servidor.get().strip()
            else:
                nome = ent_nome_estagiario.get().strip()

            cpf = ent_cpf.get().strip()
            senha = ent_senha.get().strip() # Captura a senha, mesmo que seja vazia

            if not all([nome, cpf, perfil]):
                Messagebox.show_warning("Campos Obrigatórios", "Nome, CPF e Perfil são obrigatórios.")
                return

            if not modo_edicao and not senha:
                Messagebox.show_warning("Senha Obrigatória", "A senha é obrigatória para novos usuários.")
                return

            id_para_ignorar = dados_usuario['id_usuario'] if modo_edicao else None
            if self.db.cpf_existe(cpf, id_para_ignorar):
                Messagebox.show_error("CPF Duplicado", "Este CPF já está cadastrado no sistema.")
                return

            if modo_edicao:
                # Tentativa de atualizar nome, CPF e perfil
                sucesso_atualizacao = self.db.atualizar_usuario(dados_usuario['id_usuario'], nome, cpf, perfil)
                
                sucesso_senha = True # Assume sucesso se não houver senha para atualizar
                if senha: # Se uma nova senha foi fornecida
                    if len(senha) < 6: # Adicione uma validação mínima para a senha
                        Messagebox.show_warning("Senha Fraca", "A nova senha deve ter no mínimo 6 caracteres.")
                        return
                    nova_senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                    sucesso_senha = self.db.atualizar_senha_usuario(dados_usuario['id_usuario'], nova_senha_hash)
                    
                    if not sucesso_senha:
                        Messagebox.show_error("Erro", "Não foi possível atualizar a senha do usuário.")
                        return # Sai da função se a senha falhar

                if sucesso_atualizacao and sucesso_senha: # Verifica ambos os sucessos
                    Messagebox.ok("Sucesso", "Usuário atualizado com sucesso.")
                    dialog.destroy()
                    self._popular_tabela()
                elif not sucesso_atualizacao:
                    Messagebox.show_error("Erro", "Não foi possível atualizar os dados do usuário (nome/CPF/perfil).")

            else: # Modo de adição de novo usuário
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                if self.db.cadastrar_usuario(nome, cpf, senha_hash, perfil):
                    Messagebox.ok("Sucesso", "Usuário cadastrado com sucesso.")
                    dialog.destroy()
                    self._popular_tabela()
                else:
                    Messagebox.show_error("Erro", "Não foi possível cadastrar o novo usuário.")

        btn_salvar = ttk.Button(frame_botoes, text="Salvar", command=_salvar_usuario, bootstyle="success")
        btn_salvar.pack(side=LEFT, padx=10)

        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=dialog.destroy, bootstyle="danger-outline")
        btn_cancelar.pack(side=LEFT, padx=10)