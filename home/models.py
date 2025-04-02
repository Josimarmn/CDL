import locale
from decimal import Decimal
from django.db import models
from datetime import date
import hashlib
from django.core.validators import RegexValidator

#Produtos => Cursos
#Clientes => Alunos
#Pedidos  => Matrícula

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()
    
    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14,verbose_name="C.P.F")
    contato = models.CharField(max_length=20,verbose_name="Contato")
    #datanasc = models.DateField(verbose_name="Data de Nascimento")
    class Meta:
        db_table = 'home_cliente'
    
    @classmethod
    def total_clientes(cls):
        """Retorna o total de clientes cadastrados"""
        return cls.objects.count()
    #@property
    #def datanascimento(self):
    #    """Retorna a data de nascimento no formato DD/MM/AAAA"""
    #    if self.datanasc:
    #        return self.datanasc.strftime('%d/%m/%Y')
    #    return None

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10,decimal_places=2,blank=False)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    img_base64=models.TextField(blank=True)
   
    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde':0})
        return estoque_item

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()   
    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'

class Pedido(models.Model):

    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)
    valor_total_impostos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_icms = models.DecimalField(max_digits=10, decimal_places=2)
    valor_ipi = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pis = models.DecimalField(max_digits=10, decimal_places=2)
    valor_confins = models.DecimalField(max_digits=10, decimal_places=2)
    total_alunos = models.IntegerField(null=True)
    total_curso01 = models.IntegerField(null=True)
    total_curso02 = models.IntegerField(null=True)
    total_curso03 = models.IntegerField(null=True)
    total_curso04 = models.IntegerField(null=True)
    total_curso05 = models.IntegerField(null=True)
    total_curso06 = models.IntegerField(null=True)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def chave_acesso(self):
        """
        Gera uma chave de acesso única baseada no ano, ID do pedido e um hash SHA-256.
        """
        # Concatenando o ano (do campo data_pedido) com o ID do pedido
        ano = self.data_pedido.strftime('%Y')  # Pega o ano da data do pedido
        dados = f"{ano}{self.id}"  # Concatenando ano e ID do pedido

        # Criando o hash SHA-256
        chave = hashlib.sha256(dados.encode('utf-8')).hexdigest()

        # Retorna a chave composta por ano + ID + hash
        return f"{ano}{self.id}{chave.upper()}"  # Retorna em maiúsculas para padronizar

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None
    
    @property    
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total

    
    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido, """
        return self.itempedido_set.count()  
    

    @property    
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)    
    
    #Calcula o total de todos os pagamentos do pedido
    @property
    def total_pago(self):
        total = sum(pagamento.valor for pagamento in self.pagamentos.all())
        return total    
    
    @property
    def debito(self):
        return self.total-self.total_pago
    


    @property
    def valor_icms(self):
        icms = Decimal('0.18') * self.total
        return icms.quantize(Decimal('0.01'))  # Arredonda para 2 casas decimais
    
    @property
    def valor_ipi(self):
        ipi = Decimal('0.05') * self.total
        return ipi.quantize(Decimal('0.01'))  # Arredonda para 2 casas decimais
    
    @property
    def valor_pis(self):
        pis = Decimal('0.0165') * self.total
        return pis.quantize(Decimal('0.01'))  # Arredonda para 2 casas decimais

    @property
    def valor_confins(self):
        cofins = Decimal('0.076') * self.total
        return cofins.quantize(Decimal('0.01'))  # Arredonda para 2 casas decimais

    @property
    def valor_total_impostos(self):
        # Somando os valores dos impostos e arredondando o total
        return (self.valor_icms + self.valor_ipi + self.valor_pis + self.valor_confins).quantize(Decimal('0.01'))
    @property
    def valor_final(self):
        # Somando os valores dos impostos e arredondando o total
        return (self.valor_icms + self.valor_ipi + self.valor_pis + self.valor_confins + self.total).quantize(Decimal('0.01'))

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"  

    @property    
    def subtotal(self):
        """Calcula o subtotal de todos os itens no pedido, formatado como moeda local"""
        return self.qtde * self.preco

class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MMaa"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None