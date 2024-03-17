from itertools import pairwise

def datefmt(value, format="%d-%m-%Y"):
    return value.strftime(format)

def embed_yt(vd, is_theory):
    kind = "ytplaylist" if vd.get("playlist",False) else "youtube"
    title = vd.get(
        "title", 
        f"Capítulo {vd['chapter']} - {'Video' if is_theory else 'Ejercicio'} {vd['num']}"
    )
    return f'{{{{< {kind} id="{vd["id"]}" title="{title}" >}}}}'


def expand_list(ej_list):
    res = set()
    for ej in ej_list:
        if isinstance(ej, int):
            ej = (ej,ej)
        expanded = list(range(ej[0],ej[1]+1))
        res |= set(expanded)
    return sorted(list(res))

def compile_list(expanded_list):
    if len(expanded_list)==0:
        return []
    res = []
    start = expanded_list[0]
    finish = expanded_list[0]
    for prev, num in pairwise(expanded_list + [None]):
        if num is not None and num == prev+1:
            # keep expanding window
            finish = num
        else:
            # window broke
            # tie up last one
            # if start is previous and already broke, it's not a window
            win = start if start == prev else (start, finish)
            res.append(win)
            # start new one
            start = num
    return res

def format_one(chapter, ex):
    def n(ex):
        return f"{chapter}.{ex}"
    return f"**{n(ex[0])}** al **{n(ex[1])}**" if isinstance(ex, tuple) else f"**{n(ex)}**"

def compile_ejs(ej_list):
    # recompile ej by chapter
    ej_list = {
        chapter: compile_list(expand_list(ejs)) 
        for chapter, ejs in ej_list.items()
    }
    # join multiple chapters by colon, exercises by comma
    return ". ".join([
        ",".join(format_one(ch, ex) for ex in exs)
        for ch, exs in ej_list.items()
    ]) + "."
