from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.db.models import Prefetch
from rest_framework.decorators import action
from tgbots.views import Update

from supports.models import SupportChatMessage, Ticket
from supports.serializers import TicketRetrieveSerializer, TicketSerializer
from tgbots.models import TelegramAccount
from tgbots.views import ReplyMarkup, SendMessage

# Create your views here.
class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Ticket.objects.prefetch_related('user', 'staff')
        if self.action == 'list':
            return qs.filter(user=self.request.user)
        if self.action in ['retrieve', 'close_ticket']:
            ticket_messages = SupportChatMessage.objects.prefetch_related('author')
            prefetched_ticket_messages = Prefetch('ticket_messages', ticket_messages)
            return qs.prefetch_related(prefetched_ticket_messages)
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TicketRetrieveSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        ticket = Ticket.objects.create(user=request.user)
        SupportChatMessage.objects.create(author=request.user, text=request.data.get('text'), ticket=ticket)
        bosses = TelegramAccount.objects.filter(account__groups__name='support_boss')
        text = render_to_string('boss_new_ticket.html', {'ticket':ticket})
        for boss in bosses:
            reply_markup = ReplyMarkup(ticket=ticket).get_markup('boss_got_new_ticket')
            SendMessage(boss.tg_id, text, reply_markup).send()  
        return Response(TicketSerializer(ticket, context={'request':request}).data, status=200)
    
    @action(['patch'], detail=True)
    def close_ticket(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.status = 3
        ticket.save()
        who_close_ticket = 'Технической Поддержкой' if request.user.is_staff else 'Пользователем'
        message = 'Заявка закрыта ' + who_close_ticket
        message = SupportChatMessage.objects.create(author=request.user, text=message, ticket=ticket)
        Update({'items':None}).send_message_to_support_chat(message, ticket)
        Update({'items':None}).send_command_to_support_chat('close_ticket', ticket)
        return Response(TicketRetrieveSerializer(ticket, context={'request':request}).data, status=200)