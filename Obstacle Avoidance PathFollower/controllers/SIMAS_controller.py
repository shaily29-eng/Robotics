"""Controlador para o robo SIMAS feito para o projeto final de TI502 em 2021."""

#Por Antônio Hideoto Borges Kotsubo (19162), Ian de Almeida Pinheiros (19179) e Matheus Seiji Luna Noda (19190)

# Imports
from controller import Robot
import socket, _thread

print("Iniciando")
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 16 #int(robot.getBasicTimeStep())

# Pega e printa o nome do robo
nome = robot.getName()
print("Nome do robo: ", nome)

# Ativa os sensores de infravermelhor
ls_dir = robot.getDevice("ls_dir")
ls_dir.enable(timestep)
ls_meio = robot.getDevice("ls_meio")
ls_meio.enable(timestep)
ls_esq = robot.getDevice("ls_esq")
ls_esq.enable(timestep)

# Ativa a camera
camera = robot.getDevice("camera")
camera.enable(timestep)

# Ativa os motores (rodas)
motor_esq = robot.getDevice("motor roda esquerda")
motor_dir = robot.getDevice("motor roda direita")

motor_esq.setPosition(float('+inf'))
motor_dir.setPosition(float('+inf'))

motor_esq.setVelocity(0.0)
motor_dir.setVelocity(0.0)

# Ativa os sensores de distancia
ir0 = robot.getDevice("ir0")
ir0.enable(timestep)

ir1 = robot.getDevice("ir1")
ir1.enable(timestep)

ir2 = robot.getDevice("ir2")
ir2.enable(timestep)

ir3 = robot.getDevice("ir3")
ir3.enable(timestep)

# Determina a velocidade máxima e velocidade de curva do robo
max_vel = -3.0
dis_vel = 2.0

# (booleano) Verifica se o valor passado representa uma area escura
def ehEscuro(value):
    if value > 16.5:
        return True
    else:
        return False

###############################
#     Conexao via socket      #
###############################
# Pega o IP do host atual
def get_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

# Pega a porta da conexao (80 HTTP)
def get_port():
    return 80

# Atribui a variaveis os valores da porta e do IP
https = get_ip()
hport = get_port()

# Tratamento de uma nova conexao aceita
def on_new_client(socket, addr):
    while True:
        # Recebe a mensagem enviada e verifica ela
        msg = socket.recv(1024)
        if msg.decode().__contains__("/8080/foto"):
            # Salva a imagem atual da camera e lê ela
            camera.saveImage("photo.jpg", 100)
            str = open("photo.jpg", "rb").read()
            # Atribui à mensagem de resposta os valores da imagem
            msg = getImage(str)
        else:
            break
        # Envia a mensagem de resposta
        socket.sendall(msg)

    # Fecha a conexao
    socket.close()
    return        

# Monta o header e o body da mensagem de resposta
def getImage(img_data):
    header = 'HTTP/1.1 200 OK\n'
    header += 'Content-Type: image/jpg\n\n'
    msg = header.encode('utf-8')
    msg += img_data
    return msg

# Estabelece a thread do servidor
def servidor(https, hport):
    print("entrou no servidor()")
    sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockHttp.bind((https, hport))
    except:
        sockHttp.bind(('', hport))
    
    # Ouve à porta estabelecida
    sockHttp.listen(1)
    
    while True:
        # A cada nova conexao aceita cria uma nova thread com o tratamento
        client, addr = sockHttp.accept()
        _thread.start_new_thread(on_new_client, (client,addr))

# Inicia a thread do servidor
_thread.start_new_thread(servidor, (https,hport))

##########################################
#               Main loop:               #
##########################################
# Variavel de direcao
estado = "reto"
# Variavel para outras verificaxoes
info_extra = ""
# Variavel para o controle das etapas de desvio de obstaculo
fora_da_linha = 0

# Loop dos passos do robo
while robot.step(timestep) != -1: 
    # Distancias dos sensores
    distFrente = ir1.getValue()
    distEsq    = ir2.getValue()
    # Variaveis booleanas que verificam a presenca ou ausencia de paredes proximas ao robo
    temParedeFrente = distFrente >= 300
    temParedeEsq    = distEsq    >= 300 

    # Valores numericos dos sensores de infravermelho
    vMeio = ls_meio.getValue()
    vDir  = ls_dir.getValue()
    vEsq  = ls_esq.getValue()

    # Execucao do estado atual caso ele seja de desvio
    if estado == "desviar":
        if fora_da_linha == 2 and ehEscuro(vMeio):
            fora_da_linha = 0
            estado = "retorno_a_linha"

        elif ehEscuro(vEsq) and fora_da_linha == 0:
            fora_da_linha = 1
        
        elif not ehEscuro(vEsq) and fora_da_linha == 1:
            fora_da_linha = 2

        elif temParedeFrente:
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(max_vel)
        elif temParedeEsq:
            info_extra = ""
            motor_dir.setVelocity(max_vel)
            motor_esq.setVelocity(max_vel)
        else:
            motor_dir.setVelocity(max_vel)
            motor_esq.setVelocity(0.0)        
        
    # Execucao das instrucoes do estado atual
    if estado == "reto":
        motor_dir.setVelocity(max_vel)
        motor_esq.setVelocity(max_vel)
    elif estado == "3_ls_direita":
        if ehEscuro(vEsq):
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(max_vel)
    elif estado == "90_esquerda":
        if ehEscuro(vMeio):
            motor_dir.setVelocity(max_vel)
            motor_esq.setVelocity(max_vel)
        elif not ehEscuro(vDir):
            motor_dir.setVelocity(max_vel)
            motor_esq.setVelocity(0.0)
        else:
            estado = "reto"
    elif estado == "90_direita":
        if ehEscuro(vMeio):
            motor_dir.setVelocity(max_vel)
            motor_esq.setVelocity(max_vel)
        elif not ehEscuro(vEsq):
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(max_vel)
        else:
            estado = "reto"
    elif estado == "entortar_esquerda":
        motor_dir.setVelocity(max_vel)
        motor_esq.setVelocity(dis_vel)
    elif estado == "entortar_direita":
        motor_dir.setVelocity(dis_vel)
        motor_esq.setVelocity(max_vel)
    
    if estado == "retorno_a_linha":
        motor_dir.setVelocity(0.0)
        motor_esq.setVelocity(max_vel)
        if ehEscuro(vEsq):
            estado = "reto"
            
    # Atualizacao de estado
    elif temParedeFrente or estado == "desviar":
        info_extra = estado
        estado = "desviar"                  # Robo deve desviar de um obstaculo
    elif ehEscuro(vMeio):
        if ehEscuro(vEsq):
            if ehEscuro(vDir):
                info_extra = estado
                estado = "3_ls_direita"     # Robo com 3 sensores ativos (escolhemos virar para a direita)
            else:
                info_extra = estado
                estado = "90_esquerda"      # Robo deve fazer uma curva de 90 graus para a direita
        else:
            if ehEscuro(vDir):
                info_extra = estado
                estado = "90_direita"   # Robo deve fazer uma curva de 90 graus para a esquerda
            else:
                info_extra = estado
                estado = "reto"         # Robo deve ir reto
    else:
        if ehEscuro(vEsq):
            info_extra = estado
            estado = "entortar_esquerda"    # Robo deve virar aos poucos para a esquerda
        else:
            if ehEscuro(vDir):
                info_extra = estado
                estado = "entortar_direita" # Robo deve virar aos poucos para a direita
            else:
                info_extra = "gap"
                estado = "reto"             # Robo deve ir reto e ignorar o buraco da trilha
                
        
