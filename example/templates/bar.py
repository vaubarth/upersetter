{% for import in bar.content.imports %}import {{import}}
{% endfor %}

{{bar.content.var}} = 'one'
print({{bar.content.var}})