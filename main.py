from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time


app = Tk()
app.minsize(width = 1200, height = 900)
app.title("Lista de compras")
app.resizable(True, True)
app.state('zoomed')

#Barra de carregamento
def carregamento(valor):
    my_progress = ttk.Progressbar(app, orient = HORIZONTAL, length = 100, mode = 'determinate')
    my_progress.place(relx = 0.82, rely = 0.92)
    labelBar = Label(app)
    labelBar.place(relx = 0.839, rely = 0.90)
    for i in range(1,100):
        my_progress['value'] = i
        app.update_idletasks()
        labelBar.config(text = str(i) + "%")
        time.sleep(valor)
        
    my_progress['value'] = 100
    my_progress.place(relwidth = 0, relheight = 0)
    labelBar.place(relwidth = 0, relheight = 0)

#Função que mostra os dados no menu inicial
def mostrar():
    tv.delete(*tv.get_children())
    vquery = "SELECT T_COMPRA, N_VALOR, T_DETALHE FROM lista ORDER BY T_COMPRA"
    linhas = database.dql(vquery)
    for i in linhas:
        tv.insert("","end",value = i)
        
    
#Função que soma o preço dos produtos e mostra eles no menu inicial
def mostrarSoma():
    tv.delete(*tv.get_children())
    xquery = "SELECT N_VALOR FROM lista"
    linha = database.dql(xquery)
    total = np.array([])

    for j in linha:
        total = np.append(total, j, axis=0)
        
    res = sum(total)
    
    
        
    lsoma = LabelFrame(tv, background = "#000080", fg = "#F5F5F5")
    lsoma.place(rely = 0.96, relwidth = 1, relheight = 0.04)
    Label(lsoma, text = "Valor final R$: {:.2f}".format(res), background = "#000080", foreground = "#F5F5F5", anchor = E, font = ("verdana", 11, "bold"), relief="flat", borderwidth = 4, highlightcolor = "#000080").place(x = 0, y = 0, relwidth = 0.62)
    mostrar()
  

    
#Função que adiciona um novo produto 
def adicionar():
    def add():
        
        if addE.get() == "" or addV.get() == "":
            messagebox.showwarning("Aviso", "Você não informou o nome do produto ou o valor")
            
        else:
            try:
                vquery = "INSERT INTO lista (T_COMPRA, N_VALOR, T_DETALHE) VALUES ('"+addE.get()+"','"+addV.get()+"','"+txt_detalhes.get('1.0', END)+"')"
                database.dml(vquery)
                resp = messagebox.askyesno("Mensagem", "gostaria de adicionar outro produto ?")
                
                if resp == True:
                    adicionar()
                    
                else:
                    carregamento(0.001)
                    messagebox.showinfo("Mensagem", "Produto salvo")
                    lframe.place(relwidth = 1, relheight = 1)
                    lbf_add.place(relwidth = 0, relheight = 0)
                    
            except:
                messagebox.showerror("Erro", "Erro ao salvar os dados")
        mostrarSoma()
        
                
    
    lframe.place(x = 0, y = 0, relwidth = 0, relheight = 0)
    
    lbf_add = LabelFrame(app, text = "adicionar")
    lbf_add.place(relwidth = 1, relheight = 1)
    lb_add = Label(lbf_add, text = "Produto", font = ("arial", 15))
    lb_add.place(relx = 0.3, rely = 0.1)
    addE = Entry(lbf_add, font = ("arial", 15))
    addE.place(relx = 0.3, rely = 0.13, relheight = 0.03, relwidth = 0.4)
    
    lb_valor = Label(lbf_add, text = "Valor", font = ("arial", 15))
    lb_valor.place(relx = 0.3, rely = 0.16)
    addV = Entry(lbf_add, font = ("arial", 15))
    addV.place(relx = 0.3, rely = 0.19, relheight = 0.03, relwidth = 0.4)
    
    lb_detalhes = Label(lbf_add, text = "Detalhes", font = ("arial", 15))
    lb_detalhes.place(relx = 0.3, rely = 0.22)
    txt_detalhes = Text(lbf_add, font = ("arial", 15))
    txt_detalhes.place(relx = 0.3, rely = 0.25, relheight = 0.3, relwidth = 0.4)
    
    #Função para voltar ao menu inicial
    def voltar():
        lbf_add.place(relwidth = 0, relheight = 0)
        lframe.place(relwidth = 1, relheight = 1)

                                
        
    btn_voltaradd = Button(lbf_add, text = "Voltar", bd = 4, bg = "#FF0000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = voltar)
    btn_voltaradd.place(relx = 0.3, rely = 0.6)
    btn_add_produto = Button(lbf_add, text = "Adicionar", bd = 4, bg = "#32CD32", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = add)
    btn_add_produto.place(relx = 0.332, rely = 0.6)
    
#função para apagar um produto
def selecionadoDel():
    try:
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, "values")
        res = messagebox.askyesno("Mensagem", "Deseja apagar este item ?")
        if res == True:
            vquery = "DELETE FROM lista where T_COMPRA = '"+valores[0]+"'"
            database.dml(vquery)
            messagebox.showinfo("Mensagem", "Produto apagado")
            mostrarSoma()
    except:
        messagebox.showinfo("Mensagem", "Selecione um item")    
  
#Função para mostrar os detalhes do produto selecionado  
def detalhes():
    carregamento(0.00001)
    try:
        itemSelecionadoDet = tv.selection()[0]
        valor = tv.item(itemSelecionadoDet, "values")
        lf_det = LabelFrame(app, text = valor[0])
        lf_det.place(relwidth = 1, relheight = 1)
        Label(lf_det, text = "Nome: " + valor[0], font = ("arial", 15)).place(relx = 0.25, rely = 0.1)
        Label(lf_det, text = "Preço: " + valor[1], font = ("arial", 15)).place(relx = 0.25, rely = 0.2)
        Label(lf_det, text = "Detalhes: " + valor[2], font = ("arial", 15)).place(relx = 0.25, rely = 0.3)
        lframe.place(relwidth = 0, relheight = 0)
    
    except:
        messagebox.showinfo("Mensagem", "Selecione um item")
    
    #Função para voltar ao menu inicial
    def voltar():
        lf_det.place(relwidth = 0, relheight = 0)
        lframe.place(relwidth = 1, relheight = 1)
            
    #Função para alterar os dados do produto
    def atualizar():
        
        def atualizarDados():
            try:
                carregamento(0.001)
                vquery = "UPDATE lista set T_COMPRA = '"+addE.get()+"', N_VALOR = '"+addV.get()+"', T_DETALHE = '"+txt_detalhes.get('1.0', END)+"' WHERE T_COMPRA = '"+valor[0]+"' "
                database.dml(vquery)
                mostrar()
                messagebox.showinfo("Mensagem", "Dados atualizados")
                lf_att.place(relwidth = 0, relheight = 0)
                lf_det.place(relwidth = 0, relheight = 0)
                lframe.place(relwidth = 1, relheight = 1)
                
            except:
                messagebox.showerror("Erro", "Houve um erro ao atualizar")
            
        lf_att = LabelFrame(app, text = "Atualizar contato")
        lf_att.place(relwidth = 1, relheight = 1)
        
        lb_add = Label(lf_att, text = "Produto", font = ("arial", 15))
        lb_add.place(relx = 0.3, rely = 0.1)
        addE = Entry(lf_att, font = ("arial", 15))
        addE.insert(0, valor[0])
        addE.place(relx = 0.3, rely = 0.13, relheight = 0.03, relwidth = 0.4)
        
        lb_valor = Label(lf_att, text = "Valor", font = ("arial", 15))
        lb_valor.place(relx = 0.3, rely = 0.16)
        addV = Entry(lf_att, font = ("arial", 15))
        addV.place(relx = 0.3, rely = 0.19, relheight = 0.03, relwidth = 0.4)
        addV.insert(0, valor[1])
        
        lb_detalhes = Label(lf_att, text = "Detalhes", font = ("arial", 15))
        lb_detalhes.place(relx = 0.3, rely = 0.22)
        txt_detalhes = Text(lf_att, font = ("arial", 15))
        txt_detalhes.insert(1.0, valor[2])
        txt_detalhes.place(relx = 0.3, rely = 0.25, relheight = 0.3, relwidth = 0.4)
        
        def voltar():
            lf_att.place(relwidth = 0, relheight = 0)
            lf_det.place(relwidth = 1, relheight = 1)
        
        btn_att2 = Button(lf_att, text = "Atualizar",  bd= 4, bg = "#32CD32", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = atualizarDados)
        btn_att2.place(relx = 0.332, rely = 0.6)
        btn_voltar_att = Button(lf_att, text = "Voltar", bd= 4, bg = "#FF0000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = voltar)
        btn_voltar_att.place(relx = 0.3, rely = 0.6)
        
    btn_att = Button(lf_det, text = "Atualizar", bd= 4, bg = "#32CD32", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = atualizar)
    btn_att.place(relx = 0.30, rely = 0.55)
    btn_voltarDet = Button(lf_det, text = "Voltar", bd= 4, bg = "#FF0000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = voltar)
    btn_voltarDet.place(relx = 0.27, rely = 0.55)
    
#Funçaõ para mostrar os gráficos
def grafico():
    
    lframe.place(relwidth = 0, relheight = 0)
    
    lgrafico = ttk.Notebook(app)
    lgrafico.place(relwidth = 1, relheight = 1)
    
    #Gráfico em barra
    barChart = Frame(lgrafico)
    lgrafico.add(barChart, text = "Gráfico")
    
    vquery = "SELECT T_COMPRA, N_VALOR FROM lista"
    dados = database.dql(vquery)
    
    fig1 = plt.Figure(figsize=(8,9), dpi = 60)
    canva = FigureCanvasTkAgg(fig1, barChart)
    canva.get_tk_widget().place(relwidth = 1, relheight = 1)
    ax = fig1.add_subplot(111)
    
    #Gráfico em formato de pizza
    pieChart = Frame(lgrafico)
    lgrafico.add(pieChart, text = "Pie chart")
    
    fig2 = plt.Figure(figsize=(8,9), dpi = 60)
    canva = FigureCanvasTkAgg(fig2, pieChart)
    canva.get_tk_widget().place(relwidth = 1, relheight = 1)
    ax2 = fig2.add_subplot(111)
    nome = np.array([])
    valor = np.array([])
    resPie = np.array([])
    legenda = np.array([], dtype = "S")
    cont = 1
    for i, j in dados:
        nome = np.append(nome, i)
        valor = np.append(valor, j)

    rect1 = ax.bar(nome, valor) 
    
    for i in range(len(dados)):
        if cont % 2 ==0:
            rect1[i].set_color("red")
        else:
            rect1[i].set_color("blue")
        cont += 1 
    ax.set_title("Valores x Produtos")
    ax.set_xlabel("Produtos")
    ax.set_ylabel("Valores R$")
    
    #Função que mostra os valores dos produtos no topo da sua barra no gráfico em barra
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rect1)
    
        
    for x, z in dados:
        legenda = np.append(legenda, x)
        valorAtual = np.array([z])
        resPie = np.append(resPie, valorAtual, axis=0)
        ax2.axis('equal')
    ax2.set_title("Porcentagem que cada produto usa no orçamento total")
    ax2.pie(resPie, autopct = '%1.2f%%', startangle = 90)
    ax2.legend(labels = legenda, title = "Produtos")
    
    #Função para voltar ao menu inicial
    def voltar():
        lgrafico.place(relwidth = 0, relheight = 0)
        lframe.place(relwidth = 1, relheight = 1)

    
    btn_voltarDet = Button(lgrafico, text = "Voltar", bg = "#FF0000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = voltar)
    btn_voltarDet.place(relx = 0.1, rely = 0.1)

    
    
#Menu inicial
lframe = LabelFrame(app, text = "Home", font = ("verdana", 9, "bold"))
lframe.place(relwidth = 1, relheight = 1)

tv = ttk.Treeview(lframe, columns = ('Produto', 'Preço'), show = 'headings')
style = ttk.Style(app)
style.theme_use("clam")
style.configure("Treeview")
scroll = Scrollbar(tv, orient = "vertical")
scroll.pack(fill=Y, side=RIGHT, expand=FALSE)


tv.column('Produto', minwidth = 0, width = 500)
tv.column('Preço', minwidth = 0, width = 500)

tv.heading("Produto", text = "Produto")
tv.heading("Preço", text = "Preço")

tv.place(relx = 0.1, rely = 0.1, relwidth=0.8, relheight=0.8)
mostrarSoma()


btn = Button(lframe, text = "Adicionar",bd = 4, bg = "#32CD32", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = adicionar)
btn.place(relx=0.91, rely=0.15, relwidth=0.06)

btn_delete = Button(lframe, text = "Apagar",bd = 4, bg = "#000000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = selecionadoDel)
btn_delete.place(relx=0.91, rely=0.18, relwidth=0.06)

btn_detalhes = Button(lframe, text = "Detalhes",bd = 4, bg = "#000000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = detalhes)
btn_detalhes.place(relx=0.91, rely=0.21, relwidth=0.06)

btn_grafico = Button(lframe, text = "Gráfico",bd = 4, bg = "#000000", fg = "#FFFAFA", font = ("verdana", 9, "bold"), command = grafico)
btn_grafico.place(relx=0.91, rely=0.24, relwidth=0.06)


app.mainloop()
