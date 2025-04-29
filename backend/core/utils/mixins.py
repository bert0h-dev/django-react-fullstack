from core.responses import api_success
from core.decorators import log_view_action

class ListOnlyMixin:
  log_list_action = None  # Cada ViewSet debe definir su propio log}
  success_list = None # Cada ViewSet dede definir su propio mensaje de api_success

  @log_view_action(lambda self, request, kwargs: self.log_list_action)
  def list(self, request, *args, **kwargs):
    queryset = super().filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return api_success(data=self.get_paginated_response(serializer.data).data, message=self.message_list)

    serializer = self.get_serializer(queryset, many=True)
    return api_success(data=serializer.data, message=self.message_list)