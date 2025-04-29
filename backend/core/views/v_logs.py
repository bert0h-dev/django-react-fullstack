import csv
import io
import openpyxl
import json
import xml.etree.ElementTree as ET

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.models import AccessLog
from core.filters import AccessLogFilter
from core.responses import api_success
from core.messages import MSG_LOGS, MSG_SUCCESS
from core.permissions import IsAdminOrStaff
from core.decorators import log_view_action
from core.utils.models import get_model_name
from core.utils.mixins import ListOnlyMixin
from core.serializers.s_logs import AccessLogSerializer

User = get_user_model()

@extend_schema_view(
  list=extend_schema(
    summary="Listar registros de acceso",
    description="Permite listar registros de acceso de usuarios. Solo accesible a administradores o staff.",
    parameters=[
      OpenApiParameter(name='user', description='ID del usuario', required=False, type=int),
      OpenApiParameter(name='method', description='Método HTTP', required=False, type=str),
      OpenApiParameter(name='status_code', description='Código de respuesta HTTP', required=False, type=int),
      OpenApiParameter(name='path', description='Ruta contiene', required=False, type=str),
      OpenApiParameter(name='action', description='Acción realizada', required=False, type=str),
      OpenApiParameter(name='created_at__date', description='Desde fecha y hora (YYYY-MM-DDTHH:SS)', required=False, type=str),
      OpenApiParameter(name='created_at__lte', description='Hasta fecha y hora (YYYY-MM-DDTHH:SS)', required=False, type=str),
    ]
  ),
  retrieve=extend_schema(
    summary="Detalle de registro de acceso",
    description="Ver detalle del log específico."
  )
)
class AccessLogListView(ListOnlyMixin, ReadOnlyModelViewSet):
  queryset = AccessLog.objects.select_related('user').all()
  serializer_class = AccessLogSerializer
  permission_classes = [IsAdminOrStaff]
  filter_backends = [DjangoFilterBackend]
  filterset_class = AccessLogFilter

  # Configuracion de mixin
  log_list_action = MSG_LOGS["log_list"]
  success_list = MSG_SUCCESS["log_list"]

  def get_queryset(self):
    return AccessLog.objects.select_related('user').all()
  
  @log_view_action(
    MSG_LOGS["log_details"], 
    object_getter=lambda self, request, kwargs: self.get_object().action,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_success(data=serializer.data, message=MSG_SUCCESS["log_details"], status=status.HTTP_200_OK)

@extend_schema(
  summary="Exportar registros de acceso",
  description="Permite exportar registros de acceso en formato CSV, Excel, JSON o XML. Se pueden aplicar filtros.",
  parameters=[
    OpenApiParameter(name='format', description='Formato: csv, xlsx, json, xml', required=False, type=str),
    OpenApiParameter(name='user', description='ID del usuario', required=False, type=int),
    OpenApiParameter(name='method', description='Método HTTP', required=False, type=str),
    OpenApiParameter(name='status_code', description='Código de respuesta HTTP', required=False, type=int),
    OpenApiParameter(name='action', description='Acción contiene', required=False, type=str),
    OpenApiParameter(name='path', description='Path contiene', required=False, type=str),
    OpenApiParameter(name='created_at__gte', description='Desde fecha (YYYY-MM-DDTHH:MM)', required=False, type=str),
    OpenApiParameter(name='created_at__lte', description='Hasta fecha (YYYY-MM-DDTHH:MM)', required=False, type=str),
  ],
  responses={200: None}
)
class AccessLogExportView(APIView):
  permission_classes = [IsAdminOrStaff]
  filter_backends = [DjangoFilterBackend]
  filterset_class = AccessLogFilter

  @log_view_action(MSG_LOGS["log_export"])
  def get(self, request, format=None):
    queryset = AccessLog.objects.select_related('user').all()
    for backend in list(self.filter_backends):
      queryset = backend().filter_queryset(request, queryset, self)

    export_format = request.query_params.get('format', 'csv').lower()

    if export_format == 'xlsx':
      return self.export_excel(queryset)
    elif export_format == 'json':
      return self.export_json(queryset)
    elif export_format == 'xml':
      return self.export_xml(queryset)
    else:
      return self.export_csv(queryset)
  
  def export_csv(self, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="access_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Método', 'Path', 'Acción', 'Código', 'Mensaje', 'IP', 'User Agent', 'Fecha'])

    for log in queryset:
      writer.writerow([
        log.user.email if log.user else 'N/A',
        log.method,
        log.path,
        log.action,
        log.status_code,
        log.message,
        log.ip_address,
        log.user_agent,
        log.created_at.strftime('%Y-%m-%d %H:%M:%S')
      ])

    return response

  def export_excel(self, queryset):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Access Logs'

    headers = ['Usuario', 'Método', 'Path', 'Acción', 'Código', 'Mensaje', 'IP', 'User Agent', 'Fecha']
    worksheet.append(headers)

    for log in queryset:
      worksheet.append([
        log.user.email if log.user else 'N/A',
        log.method,
        log.path,
        log.action,
        log.status_code,
        log.message,
        log.ip_address,
        log.user_agent,
        log.created_at.strftime('%Y-%m-%d %H:%M:%S')
      ])

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
      output,
      content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="access_logs.xlsx"'
    return response

  def export_json(self, queryset):
    logs = []
    for log in queryset:
      logs.append({
        'usuario': log.user.email if log.user else 'N/A',
        'metodo': log.method,
        'path': log.path,
        'accion': log.action,
        'codigo': log.status_code,
        'mensaje': log.message,
        'ip': log.ip_address,
        'user_agent': log.user_agent,
        'fecha': log.created_at.strftime('%Y-%m-%d %H:%M:%S')
      })

    response = HttpResponse(json.dumps(logs, indent=4, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="access_logs.json"'
    return response
  
  def export_xml(self, queryset):
    root = ET.Element('AccessLogs')
    for log in queryset:
      log_element = ET.SubElement(root, 'AccessLog')
      ET.SubElement(log_element, 'Usuario').text = log.user.email if log.user else 'N/A'
      ET.SubElement(log_element, 'Metodo').text = log.method
      ET.SubElement(log_element, 'Path').text = log.path
      ET.SubElement(log_element, 'Accion').text = log.action
      ET.SubElement(log_element, 'Codigo').text = str(log.status_code)
      ET.SubElement(log_element, 'Mensaje').text = log.message or ''
      ET.SubElement(log_element, 'IP').text = log.ip_address or ''
      ET.SubElement(log_element, 'UserAgent').text = log.user_agent or ''
      ET.SubElement(log_element, 'Fecha').text = log.created_at.strftime('%Y-%m-%d %H:%M:%S')

    xml_data = ET.tostring(root, encoding='utf-8')
    response = HttpResponse(xml_data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="access_logs.xml"'
    return response