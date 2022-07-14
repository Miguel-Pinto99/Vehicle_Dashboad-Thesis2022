#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from dashboard.msg import Can_msg
from dashboard.msg import Warning_msg


def callback(msg):
    #Receive and store data in variables
    autonomia_perc = msg.autonomia_perc
    autonomia_km = msg.autonomia_km
    contador_km = msg.contador_km
    velocidade = msg.velocidade
    temperatura_ac = msg.temperatura_ac
    intensidade_ac = msg.intensidade_ac
    mudanca = msg.mudanca
    porta_condutor = msg.porta_condutor
    porta_outras = msg.porta_outras
    parabrisas_frente = msg.parabrisas_frente
    parabrisas_atras = msg.parabrisas_atras
    btn_tmax = msg.btn_tmax
    btn_imax = msg.btn_imax
    alerta_cintop = msg.alerta_cintop
    alerta_cintoc = msg.alerta_cintoc
    pisca_dir = msg.pisca_dir
    pisca_esq = msg.pisca_esq
    medios = msg.medios
    maximos = msg.maximos
    carregador = msg.carregador

    #Publish function
    pub = rospy.Publisher('warning_messages', Warning_msg, queue_size=10)
    warn=Warning_msg()

    #Generate warnings and build message
    if carregador is True and (mudanca != "Park" or velocidade != 0):
        warn.carregar = True
    else:
        warn.carregar = False


    if (porta_condutor or porta_outras) is True and velocidade >= 10 :
        warn.porta = True
    else:
        warn.porta = False


    if (alerta_cintop or alerta_cintoc) is True and velocidade >= 10 :
        warn.cinto = True
    else:
        warn.cinto = False


    if autonomia_km <= 30 and intensidade_ac != 0:
        warn.ac = True
    else:
        warn.ac = False


    if mudanca == "Reverse":
        warn.reverse = True
    else:
        warn.reverse = False

    if autonomia_perc <= 15:
        warn.autonomia = True
    else:
        warn.autonomia = False


    warn.limite_velocidade = False
    warn.proximidade=False

    #Publish warnings
    pub.publish(warn)
    print(warn)

def main():

    #Initialize node
    rospy.init_node('warning_node', anonymous=True)
    #Subscribe topic
    rospy.Subscriber("can_messages", Can_msg,callback)
    rospy.spin()

if __name__ == '__main__':
    main()
