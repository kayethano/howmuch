from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from howmuch.messages.forms import MessageForm
from howmuch.messages.functions import *
from howmuch.messages.models import Conversation, Message
from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, PrestigeLikeBuyer, PrestigeLikeSeller

#Envia un mensaje a la conversation via ajax
@login_required(login_url = '/login/')
def send(request, conversationID):
    conversation = get_object_or_404(Conversation, pk=conversationID)
    #Verificacion de usuario
    verify_user(request.user, conversation)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            update_status_conversation(request.user, conversation)
            newMessage = form.save(commit=False)
            newMessage.owner = request.user
            newMessage.conversation = conversation
            newMessage.save()
            html_response = '<div class="wrapper-div row span8"><div class="span2"><img src="%s"></div> <div class="span4">%s</diV> </div>' % (newMessage.owner.profile.get_profile_picture_100x100(), newMessage.message)
            #create unread conversations
            return HttpResponse(html_response)

@login_required(login_url = '/login/')
def view_conversation(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    #Se verifica que quien publica el mensaje en la conversation sea el buyer o seller
    verify_user(request.user, conversation)
    #Si vienes de una notificacion, realizar las verificaciones y actualizar a True el status de la notificacion
    update_status_notification(request)
    #Verifica si es comprador y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversation
    if conversation.assignment.is_buyer(request.user):
        update_status_messages_buyer(conversation)
    #Verifica si es vendedor y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversation
    if conversation.assignment.is_seller(request.user):
        update_status_messages_seller(conversation)
    allmessages = Message.objects.filter(conversation = conversation).order_by('date')
    return render_to_response('messages/conversation.html', {'messages' : allmessages, 'conversation' : conversation }, context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def inbox(request):
    conversations = Conversation.objects.filter(Q(assignment__owner = request.user) | Q(assignment__article__owner = request.user)).order_by('-last_message')
    return render_to_response('messages/inbox.html',{'conversations' : conversations}, context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def getInfoBuyer(request,conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    if conversation.assignment.is_inside(request.user):
        buyer = conversation.assignment.get_buyer()
        return render_to_response('messages/infoBuyer.html', {'conversation' : conversation, 'buyer' : buyer},
            context_instance = RequestContext(request))
    else:
        return render_to_response('messages/infoBuyer.html', {'errors' : True },
            context_instance = RequestContext(request))
    

@login_required(login_url = '/login/')
def getInfoSeller(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    if conversation.assignment.is_inside(request.user):
        seller = conversation.assignment.get_seller()
        return render_to_response('messages/infoSeller.html', {'conversation' : conversation, 'seller' : seller},
            context_instance = RequestContext(request))
    else:
        return render_to_response('messages/infoSeller.html', {'errors' : True },
            context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def getInfoConfirmPay(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    confirmPay = get_object_or_404(ConfirmPay, assignment = conversation.assignment )
    if conversation.assignment.is_inside(request.user):
        return render_to_response('messages/infoConfirmPay.html', {'confirmPay' : confirmPay},
            context_instance = RequestContext(request))
    else:
        return render_to_response('messages/infoConfirmPay.html', {'errors' : True },
            context_instance = RequestContext(request))
    
@login_required(login_url = '/login/')
def getInfoConfirmDelivery(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    confirmDelivery = get_object_or_404(ConfirmDelivery, assignment = conversation.assignment )
    if conversation.assignment.is_inside(request.user):
        return render_to_response('messages/infoConfirmDelivery.html', {'confirmDelivery' : confirmDelivery},
            context_instance = RequestContext(request))
    else:
        return render_to_response('messages/infoConfirmDelivery.html', {'errors' : True },
            context_instance = RequestContext(request))

@login_required(login_url='/login/')
def getInfoCritique(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    try:
        critique = PrestigeLikeBuyer.objects.get(to = request.user, assignment = conversation.assignment)
    except PrestigeLikeBuyer.DoesNotExist:
        try:
            critique = PrestigeLikeSeller.objects.get(to = request.user, assignment = conversation.assignment)
        except PrestigeLikeSeller.DoesNotExist:
            return render_to_response('messages/infoCritique.html', {'errors' : True },
                context_instance = RequestContext(request))
    return render_to_response('messages/infoCritique.html', {'critique' : critique }, 
            context_instance = RequestContext(request))

