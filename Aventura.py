#!/usr/bin/python
# -*- coding: UTF-8 -*-
import telebot
from telebot import types

TOKEN = './Token'

bot = telebot.TeleBot(TOKEN)

################################################################################
# VARIABLES AUXILIARES
################################################################################
# imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
situacion={}   # Lugar en que se encuentra el jugador en la red de decisiones
mens_mostrados={}    # Guarda un listado de los mensajes mostrados para cada usuario para poder borrarlos después

################################################################################
# LITERALES
################################################################################
escena = {
1   :   "_Los Buscaduendes es un juego de rol infantil de la editorial NosoloROL_\n\nEn esta pequeña aventura encarnarás a una avezada buscaduendes en una de sus muchas peripecias. Deberás tomar decisiones para lo que tendrás un teclado con diferentes opciones. Si en algún momento lo pierdes puedes recuperarlo pulsando el botón que hay a la izquierda del _clip_ (de adjuntar documentos).\nEscoge con cuidado, no todas te llevarán a la victoria y hay muchos peligros escondidos.\n\n*¡QUE COMIENCE LA AVENTURA!*",
2   :   "- ¡Despierta Sonrisitas! - oyes.\n\nTe llamas *Amelia* pero te apodan Sonrisitas porque en momentos de gran peligro, cuando nadie más sabe qué hacer, apareces con una amplia sonrisa y lo resuelves todo con el hechizo o poción adecuados.\n\n- ¡Vamos despierta! - vuelve a insistir la voz.\n\nAbres los ojos y miras. Es Rosita.\n\n- ¿Qué ocurre? Todavía es de noche - te quejas.\n\nPero Rosita no te ha escuchado. Ha salido y la oyes bajar rápida por las escaleras.\n\n- ¿Pero a qué vienen tantas prisas? - te preguntas.",
3   :   "Alcanzas a Rosita al final de las escaleras y salís juntas. Afuera ves el origen de tanto alboroto. *¡Os ha descubierto la Guardia del Reino!* Atónita ves cómo están atrapando a muchos de tus amigos y los que no, huyen al bosque.\n\n- ¡Si al menos tuviese mi libro de hechizos! - te lamentas\n\n¿Qué puedes hacer?",
4   :   "Te vistes con rapidez y guardas tus cosas en un zurrón. El ruido y los gritos son cada vez mayores. Miras por la ventana y ves carros llenos de buscaduendes encadenados. El resto parece que ha conseguido escapar al bosque.\nTe dispones a salir pero oyes pasos de guardias subiendo por las escaleras.\n\n*¡Deprisa, en poco tiempo llegarán a tu habitación!*",
5   :   "Corres lo más rápida que puedes sin mirar atrás. Después de un rato corriendo por el bosque te paras a escuchar si te alguien te sigue. Al poco escuchas unos pasos y un grito de auxilio. Intentando recuperar el aliento piensas qué hacer.",
6   :   "No eres de las que se quedan de brazos cruzados. Te lanzas a por un guardia que pasa cerca de tí. Por desgracia no tienes más que tu valor y tus puños. Consigues tirarlo al suelo pero pronto llegan otros a socorrerlo que te sujetan. Acabas encerrada con los demás en una de las carretas.\n\n- ¿Por qué habré sido tan impetuosa? Si al menos hubiese subido a coger mi varita mágica - te lamentas.\n\nNo sabes cuántos años pasarás en las mazmorras, pero estás segura que ya no volverá a haber más buscaduendes en el Reino...\n\n*FIN*",
7   :   "Escondida bajo la cama, oyes entrar a los guardias...",
8   :   "Sacas un pergamino de tu bolsa, te concentras como puedes y, entornando los ojos mascullas las palabras mágicas con miedo que te oigan.\n\n- *A dormir, a dormir, que los reyes van a venir* -\n\nLos guardias se quedan parados y de pronto caen dormidos al suelo.",
9   :   "Intentas escapar por el tejado. Por desgracia el rocío de la noche hace que las tejas resbaladizas. Pierdes el pie y caes como si de un tobogán se tratase. Terminas con una aparatosa caída. Cuando despiertas, varias horas después, no es el chichón lo que más te duele, si no la certeza de no poder volver a ver a tus amigos.\n\n*FIN*",
10  :   "Escapas lo más rápida que puedes pero terminas tropezando con tronco caído. Intentas levantarte pero te has torcido el tobillo y solo puedes cojear.\n\nTardas una eternidad en salir del bosque y encontrar a alguien que te ayude. Y para entonces no hay nada que hacer. Todos tus amigos están en las mazmorras de la Guardia del Reino y no puedes hacer nada por ayudarles.\n\n*FIN*",
11  :   "Ves a un guardia tirando de Rosita de un pie. Ella se resiste agarrándose a la raiz de un árbol que sale del suelo. El guardia te ve acercarte y desenvaina su espada con un gruñido de fastidio",
12  :   "Cierras los ojos y te quedas quieta. Despueś de un rato dejas de oir sus pasos y respiras aliviada. Pero en ese instante una mano te agarra el tobillo y te saca de la cama. Gimes y te revuelves pero solo consigues que sus risas sean más fuertes. Fuiste demasiado ingenua y ya nada te podrá librar tus grilletes ni de tu triste destino.\n\n*FIN*",
13  :   "Has salido de la habitación pero todavía corres peligro. Bajas con cuidado las escaleras y sales afuera. Ves alejarse los carros. Echas a correr pero te llevan ventaja y tienes que parar a recuperar el aliento.\n\nTe sorprende un *grito de auxilio* en el bosquecillo",
14  :   "Te preparas para ir en busca del mago Faustino, es un largo viaje y tienes que estar bien preparada.",
15  :   "Atas a los guardias y les echas un jarro de agua fria por la cabeza. Despiertan resoplando y te miran sorprendidos.",
16  :   "El guardia se abalanza hacia tí blandiendo su espada. Metes la mano en tu bolsa. Tienes el tiempo justo de lanzar tu trampa de mocos pegajosos.\n\nLanzas el frasco y... ¡CHOF! Sonríes al ver al guardia atrapado sin apenas poder moverse por un enorme moco verde.\n\nVes los carros alejarse al final del camino, todavía puedes intentar alcanzarlos ¿Qué haces?",
17  :   "Decides que es mejor no perder de vista los carros. Echas a correr desesperada. Amanece después de varias horas corriendo y caminando sin parar. Has perdido completamente el rastro. Te sientas y te lamentas de no haber podido ser de más ayuda.\n\n*FIN*",
18  :   "*VARIOS DÍAS DESPUÉS...*\n\nHan pasado varios días desde el ataque. El camino ha sido difícil pero por fin has llegado al barrio Salsipuedes. No estás segura cómo llegar al escondite de Faustino. Hay tantas casas y tan apretadas que no logras orientarte.\n\n¿Qué haces?",
19  :   "El guardia es más cobardica de lo que imaginabas. Solo has tenido que amenazarle con convertirle en cobaya y ya ha empezado a cantar. Por lo visto todo ha sido el malvado plan de un mago llamado *Faustino*. Está buscando cierta *máscara* custodiada por uno de vosotros y ha sobornado a los guardias para que os atacasen.\n\nParece que vive en el barrio Salsipuedes, pero no sabe en qué casa.\n\n- Esto no quedará así, ese mago malvado tendrá su merecido - prometes.",
20  :   "No te fías de nadie. Crees que es más seguro moverte por tu cuenta. Das vueltas y vueltas pero no consigues orientarte. Te sientas desesperada.\n\n- A este paso no solo no encontraré su casa, si no que tampoco conseguiré salir del barrio -",
21  :   "Decides preguntar a un duende doméstico que pasa con un montón de sartenes. Está tan absorto que da un respingo cuando le preguntas y se le caen todas al suelo. Te disculpas y le ayudas a recogerlas. Te mira extrañado.\n\n- *Me suena tu cara* - dice - *¿eres de por aquí?*",
22  :   "Después de muchas vueltas llegas a las afueras. Solo hay cuatro casas dispersas en medio de cultivos de calabaza. Una está *en ruinas*, pero puede que haya alguien dentro porque sale un poco de humo de su interior.\nOtra tiene una curiosa *forma de seta* y de la que no paran de entrar y salir duendes jardineros.\nOtra está *peligrosamente torcida* y en su puerta está sentado un *viejo mago con cara de pocos amigos* fumando de una larga pipa que le llega hasta los pies.\nLa última está hecha un desastre, las calabazas de su huerto están todas chamuscadas, al igual que las ventanas. De hecho, mientras miras *una explosión que hace temblar la casa* al tiempo que de la chimenea sale una nube morada con chispas doradas.\n\n¿Cuál decides investigar primero?",
23  :   "En un inusual acto de confianza decides contarle toda la verdad. Te escucha sorprendido...",
24  :   "Te haces la interesante.\n\n- Sí, soy del barrio. Es normal que te suene mi cara vengo mucho por aquí - le dices haciéndote la chulita.\n\n- Eso me parecía - responde él con cara de enfadado - *¿Y todavía tienes la cara de volver después de robarnos?* -\n\nTe quedas de piedra. Intentas explicarle que se está equivocando de persona, pero ya es tarde. Está llamando a gritos a los guardias que vienen corriendo. Pronto estás rodeada y sin escapatoria. No solo no podrás liberar a tus amigos, si no que pagarás los platos rotos de otra que se te parecía\n\n*FIN*",
25  :   "Puede que ese mago esté escondido en esa casa en ruinas. Seguro que allí nadie le buscará. Te acercas con cuidado y entras. Parece que no hay nadie. Ves los restos de una hoguera todavía humeante. Hay huellas de pies pequeños.\n\n- ¡Ay! - gritas.\n\nUn trasgo te ha mordido el brazo. Lo apartas de un manotazo y sacas tu varita mágica. Pero un nutrido grupo de trasgos aparecen a tu alrededor gruñendo y babeando ¡Estás rodeada!\n\nTe despiertas dolorida varias horas después. Buscas pero no hay rastro del mago, ha escapado. Has perdido la única pista que tenías y ya no podrás ayudar a tus amigos.\n\n*FIN*",
26  :   "Estás segura que es esta casa, pero hay tantos duendes entrando y saliendo que decides esperar a que anochezca y se vayan a cenar. Una campanilla suena avisándoles y todos entran en la casa.\n\n Te acercas sigilosa. Te asomas por una de las ventanas y ves una gran mesa llena de duendes sentados mientras otros traen platos de la cocina.\n\nPuedes intentar entrar por la puerta trasera o trepar hasta un ventanuco abierto del piso de arriba.",
27  :   "Te acercas decidida a la casa torcida. El anciano te observa huraño.\n\n- ¿*Tú también* vienes a revolver mis cosas? Pues entra, uno más no importa.\n\nTe extraña la reacción del viejo mago pero te asomas al interior. Un nutrido grupo de guardias rebusca en su interior. Uno de ellos te mira y abre sus ojos como platos.\n\n- *¡Eh, a esa la ví donde los Buscaduendes!* -\n\nTe has metido en la boca del lobo. Intentas escapar pero te atrapan.\n\n- ¿Cómo he podido ser tan descuidada? - te lamentas. Pero ya es tarde.\n\n*FIN*",
28  :   "Te acercas con sigilo a la casa. Escuchas la voz de una bruja en el interior. Asomándote a la ventana, ves a una brujita con gafas echando cosas a un caldero.\n\n- *Pluma de urraca,* - dice - *peluca de rana, suspiro de mochuelo* y... ¿*risa de unicornio*? ¡Vaya, no me queda! Bah, voy a echar *risa de murciélago* que será lo mismo... -.\n\n*BUUUUUM*\n\nLa explosión te alcanza y te deja los pelos de punta y chispitas multicolores. *¡Pero lo peor es que no recuerdas nada de nada!* Miras a tu alrededor asombrada. No sabes quién eres ni qué haces allí, pero el día es precioso así que te tumbas a tomar el sol. No volverás a ver a tus amigos pero, *sin memoria* tampoco les echarás de menos.\n\n*FIN*",
29  :   "Entras a un almacén. Oyes un barullo de voces, pasos y ruido de platos y cubiertos al otro lado. Puedes investigar, pero *está muy oscuro*.",
30  :   "Al otro lado hay a un mago en medio de un cuarto lleno de libros. Examina una extraña *máscara de madera* mientras consulta un enorme libro.\n\n- *Asarat Metrión Sintós* - entona\n\nLa máscara emite un brillo verdoso. Hace un gesto para ponérsela, pero se oye un estruendo del piso inferior y vuelve a dejarla sobre la mesa. Se levanta *dándote la espalda*...",
31  :   "Tu varita se ilumina y ves un enorme tesoro de gemas y monedas. Nunca has visto tal riqueza junta... ¡y sin protección!\n\nPero un gruñido detás de tí te saca del error. Te giras y compruebas que acabas de despertar a una *Tarasca*, un dragon todavía pequeño pero temible.",
32  :   "Te mueves a tientas en la oscuridad pero terminas tirando un montón de cacerolas. Por suerte notas los travesaños de una escalera y subes antes de que un duende entre extrañado por el ruido.\n\nEstás en un cuarto en la planta alta. Oyes un *murmullo al otro lado de una puerta*. Te acercas sigilosa y echas un vistazo.",
33  :   "- Estos duendes ¿Qué habrán liado esta vez? - dice gruñendo y sale de la habitación.\n\nEntras y te acercas a la máscara. Todavía brilla, notas que es muy poderosa.\n\n- Así que es esto lo que buscaba... - musitas - *¿Y ahora qué hago?* -.",
34  :   "El suelo cruje cuando lo pisas. Faustino se gira sorprendido, no tiene su varita a mano, solo la máscara. Duda un momento... y *se la pone en la cara*.\n\nRayos cegadores de luz verde salen de la máscara y te proteges con el brazo. El mago gime y se retuerce y finalmente *comienza a reir*. Te apunta con su brazo y tu cuerpo deja de obedecerte. Ves impotente aparecer docenas de duendes como sonámbulos acercándosete.\n\n- No sabía que la máscara era tan poderosa. *Debí haber esperado un poco mas* - te lamentas\n\n*FIN*",
35  :   "Sorprendentemente el dragón te olisquea como si le resultases familiar. Incluso ronronea frotando su cabeza contra tí.\n\nEstás atónita pero te repones. Ves una escalera y decides subir.\n\nArriba hay una puerta y oyes un murmullo al otro lado. Te acercas sigilosa y miras por el hueco de la cerradura.",
36  :   "Entonas las palabras mágicas una y otra vez mientras le miras a los ojos. Parpadea aturdida y retrocede tambaleándose. Termina cayéndose con una respiración profunda. Sonríes aliviada.\n\nSubes por una escalera a un cuarto del piso de arriba. Te acercas sigilosa y *miras por la cerradura*.",
37  :   "Tomas la máscara y escapas por la ventana. No has podido liberar a tus amigos pero ese maldito mago no conseguirá lo que desea.\n\nTe has convertido en la *guardiana de la máscara* y pasarás el resto de tu vida vagando, siempre perseguida por Faustino y otros como él que ansían su poder.\n\n*FIN*",
38  :   "- ¡Qué poderosa es! - dices al coger la máscaras - Con ella le derrotaría con solo chascar los dedos -.\n\nLa tentación es demasiado grande... y *te la pones en la cara*...",
39  :   "Al cabo de unos minutos el mago vuelve a la habitación. Abre los ojos como platos cuando te ve sonriente ojeando su libro y *con la máscara en la mano*...",
40  :   "*VARIOS AÑOS DESPUÉS*\n\nSin duda la máscara era poderosa pero el precio fue alto. *Venciste a Faustino*... y al resto de magos que se te opusieron. Pero a costa de tu mente. *Dominada por la máscara* recorres el reino sembrando el terror y controlando a todo duende que se topa contingo.\n\n*FIN*",
41  :   "",
42  :   "Llevas a Faustino a las autoridades.\n\n- Pasará sus días entre rejas - prometen.\n\nPor supuesto los buscaduendes sois declarados inocentes y todos *os piden perdón* muy compungidos. Sobre todo la Guardia Real que ha recibido una fuerte regañina. Y donáis el tesoro de Faustino a los niños pobres que dan saltos de alegría.\n\n*Todos se maravillan* de lo fuerte y valiente que has sido.\n\n*FIN DE LA AVENTURA*"
}
opciones = {
1   :   [[2,"Comenzar"]],
2   :   [[3,"Salgo yo también corriendo"],[4,"Me asomo por la ventana"]],
3   :   [[5,"Huyo al bosque con Rosita"],[4,"Vuelvo a coger mis cosas"],[6,"Me enfrento a los guardias"]],
4   :   [[7,"Me escondo bajo la cama"],[8,"Preparo un hechizo"],[9,"Escapo por la ventana"]],
5   :   [[10,"Sigo corriendo"],[11,"Me acerco a ayudar"]],
6   :   [[2,"Volver a intentarlo"]],
7   :   [[12,"Espero a que se vayan"],[13,"Intento salir sin que me vean"],[8,"Lanzo un hechizo"]],
8   :   [[13,"Aprovecho a escapar"],[15,"Interrogo a los guardias"]],
9   :   [[2,"Volver a intentarlo"]],
10  :   [[2,"Volver a intentarlo"]],
11  :   [[16,"Me enfrento al guardia",10,"Corro para salvar mi pellejo"]],
12  :   [[2,"Volver a intentarlo"]],
13  :   [[11,"Me acerco a ayudar"],[17,"Sigo corriendo"]],
14  :   [[18,"Continuar"]],
15  :   [[14,"Continuar"]],
16  :   [[17,"Persigo a los carros"],[19,"Interrogo al guardia"]],
17  :   [[2,"Volver a intentarlo"]],
18  :   [[21,"Pregunto a alguien"],[20,"No me arriesgo y sigo buscando"]],
19  :   [[18,"Continuar"]],
20  :   [[22,"Mejor sigo buscando sin ponerme en peligro"],[21,"Desisto y pregunto"]],
21  :   [[23,"Le digo la verdad"],[24,"Le miento para que no me descubra"]],
22  :   [[25,"Busco en la casa en ruinas"],[26,"Miro en la casa-seta"],[27,"Voy a la casa torcida"],[28,"A la de la explosión"]],
23  :   [[22,"Continuar"]],
24  :   [[2,"Volver a intentarlo"]],
25  :   [[2,"Volver a intentarlo"]],
26  :   [[29,"Entro por la puerta trasera"],[30,"Trepo por la enredadera"]],
27  :   [[2,"Volver a intentarlo"]],
28  :   [[2,"Volver a intentarlo"]],
29  :   [[31,"Alumbro con mi varita"],[32,"Mejor a oscuras para que no me vean"]],
30  :   [[33,"Espero a que se vaya"],[34,"Aprovecho a entrar"]],
31  :   [[35,"La intento tranquilizar"],[36,"La ataco con un hechizo"]],
32  :   [[30,"Continuar"]],
33  :   [[37,"Escapo con la máscara"],[38,"Me la pongo"],[39,"La guardo y me enfrento al mago"]],
34  :   [[2,"Volver a intentarlo"]],
35  :   [[30,"Continuar"]],
36  :   [[30,"Continuar"]],
37  :   [[1,"Volver al inicio"]],
38  :   [[40,"Continuar"]],
39  :   [[41,"Continuar"]],
40  :   [[1,"Volver al inicio"]],
41  :   [[42,"Continuar"]],
42  :   [[1,"¡ENHORABUENA!\nVolver al inicio"]]
}
imagen = {
1   :   False,
2   :   False,
3   :   False,
4   :   False,
5   :   False,
6   :   False,
7   :   False,
8   :   False,
9   :   False,
10  :   False,
11  :   False,
12  :   False,
13  :   False,
14  :   False,
15  :   False,
16  :   False,
17  :   False,
18  :   False,
19  :   False,
20  :   False,
21  :   False,
22  :   False,
23  :   False,
24  :   False,
25  :   False,
26  :   False,
27  :   False,
28  :   False,
29  :   False,
30  :   False,
31  :   False,
32  :   False,
33  :   False,
34  :   False,
35  :   False,
36  :   False,
37  :   False,
38  :   False,
39  :   False,
40  :   False,
41  :   False,
42  :   False
}
audio = {
1   :   False,
2   :   False,
3   :   False,
4   :   False,
5   :   False,
6   :   False,
7   :   False,
8   :   False,
9   :   False,
10  :   False,
11  :   False,
12  :   False,
13  :   False,
14  :   False,
15  :   False,
16  :   False,
17  :   False,
18  :   False,
19  :   False,
20  :   False,
21  :   False,
22  :   False,
23  :   False,
24  :   False,
25  :   False,
26  :   False,
27  :   False,
28  :   False,
29  :   False,
30  :   False,
31  :   False,
32  :   False,
33  :   False,
34  :   False,
35  :   False,
36  :   False,
37  :   False,
38  :   False,
39  :   False,
40  :   False,
41  :   False,
42  :   False
}

################################################################################
# LITERALES
################################################################################
# Comienzo del juego
@bot.message_handler(commands=['start'])
def comenzar(m):
    cid = m.chat.id
    uid = m.from_user.id
    mid = m.message_id
    mens_mostrados[uid] = []

    display_option(1, cid, uid, mid)  # Muestra el teclado con las opciones

# Recuperar la posición del usuario
def get_user_step(uid):
    if uid in list(situacion):
        return situacion[uid]
        print("situacion_get_step: ", situacion)
    else:
        return 0

# Revisar la respuestas
@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) > 0)
def tto_mensaje_entrante(m):
    cid = m.chat.id
    uid = m.from_user.id
    mid = m.message_id
    text = m.text

    bot.send_chat_action(cid, 'typing')

    for i in opciones[situacion[uid]]:
        destino = i[0]
        seleccion = i[1]
        if text[0] == seleccion[0]:
            # bot.delete_message(cid, m.message_id -1)
            display_option(destino, cid, uid, mid)

            break
    else:
        bot.delete_message(cid, mid)   # Borra el mensaje previo
        m = bot.send_message(cid, "Opción errónea. Inténtalo de nuevo", reply_markup=imageSelect)

        # Guarda el mensaje
        mens_mostrados[uid].append(m.message_id)

def display_option(op, cid, uid, mid=False):
    situacion[uid] = op  # Actualiza el lugar en que se encuentra el jugador
    text = escena[op]    # Recupera el texto a mostrar
    imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True) # Crea el teclado a mostrar (en vacío)

    # Borra los mensajes previamente mostrados para que se escriba el siguiente
    if mid:
        bot.delete_message(cid, mid)   # Borra el mensaje escrito por el usuario

        for i in mens_mostrados[uid]:
            bot.delete_message(cid, i)

        mens_mostrados[uid] = []

    # Añade las nuevas opciones al teclado
    for i in opciones[op]:
        imageSelect.add(i[1])

    # Envía audio
    if imagen[op]:
        m = bot.send_photo(cid,open(imagen[op], "rb"), text, reply_markup=imageSelect, parse_mode="Markdown")
    elif audio[op]:
        m = bot.send_audio(cid, open(audio[op], "rb"), text, reply_markup=imageSelect, parse_mode="Markdown")
    else:
        m = bot.send_message(cid, text, reply_markup=imageSelect, parse_mode="Markdown")

    # Guarda el id del mensaje en el diccionario
    # l = mens_mostrados[uid]
    # l.append(m.message_id)
    # mens_mostrados[uid] = l
    mens_mostrados[uid].append(m.message_id)

bot.polling()
