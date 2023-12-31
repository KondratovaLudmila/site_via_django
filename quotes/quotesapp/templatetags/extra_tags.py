from django import template

register = template.Library()

def toptenrate(max, top_ten):    
    sizes = []
    first = top_ten[0].quotes_count or 1
    for item in top_ten:
        tag = {"name": item.name,
               "id": item.id,
               "quotes": item.quotes_count,
               "font": int(max*item.quotes_count/first)}
        sizes.append(tag)
    return sizes
    

register.filter("toptenrate", toptenrate)