from django.template import Library
 
register = Library()
 
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})

@register.filter(name='addstyle')
def addstyle(field, addstyle):
    return field.as_widget(attrs={'style': addstyle})