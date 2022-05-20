from msilib.schema import Class
from posixpath import split
from django import template

register = template.Library()


@register.simple_tag

def rmsp(st):
    return st.split(":::")

