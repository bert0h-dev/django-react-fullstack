# core.utils.models.py

def get_model_name(instance):
  model = instance.__class__
  return f"{model._meta.app_label}.{model._meta.model_name}"