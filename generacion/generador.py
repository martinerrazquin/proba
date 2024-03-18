from itertools import pairwise
from pathlib import Path
from yaml import safe_load
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
import datetime
import argparse

def datefmt(value, format="%d/%m/%Y"):
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

def feriadofmt(feriado_dict):
    res = "Feriado por "
    if feriado_dict.get('puente') is not None:
        res += f"*Puente* de **{feriado_dict['puente']}** "
    return res + f"**{feriado_dict['motivo']}**."

def hydrate_video(kind, chapter, video, data_src):
    data = data_src[kind][chapter][video].copy()
    data['is_theory'] = kind == 'teoricos'
    data['chapter'] = chapter
    data['num'] = video
    return data

def unpack_hydrate(vids_dict, data_src):
    return {
        kind:[
            hydrate_video(kind,chapter,num, data_src) 
            for chapter,vidlist in x.items() 
            for num in vidlist
        ] 
        for kind, x in vids_dict.items()
    }

def hydrate_class(class_dict, videos_dict, week, day):
    ## base-level data
    class_dict['week'] = week
    class_dict['day'] = day

    # hydrating videos + formatting them
    if 'videos' not in class_dict:
        return
    class_dict['videos'] = unpack_hydrate(class_dict['videos'], videos_dict)

    # build topics from theory videos
    # Warning: a complementary, yet theory video may have no topics
    if 'teoricos' not in class_dict['videos']:
        return
    class_dict['temas'] = sum(
        (x.get('topics',[]) for x in class_dict['videos']['teoricos']), 
        []
    )

def apply_dates(weeks_dict, firstdates_dict):
    dates = firstdates_dict.copy()
    period = datetime.timedelta(weeks=1)
    for n_week, week_classes in sorted(weeks_dict.items(), key=lambda t: t[0]):
        for n_class, class_dict in week_classes.items():
            class_dict['fecha'] = dates[n_class]
            dates[n_class] += period


def read_yaml(path):
    with open(path) as f:
        data = safe_load(f)
    return data

def apply_next_prev(classes):
    def fmt(class_dict):
        return f"{class_dict['week']}_{class_dict['day']}"

    for prev_c, next_c in pairwise(classes):
        prev_c['next'] = fmt(next_c)
        next_c['prev'] = fmt(prev_c)

def process_data(classes_data, videos_data):
    class_weeks = classes_data['semanas']

    # apply dates
    apply_dates(class_weeks, classes_data['primerdia'])
    
    # hydrate
    for n_week, week_classes in class_weeks.items():
        for n_day, class_dict in week_classes.items():
            hydrate_class(
                class_dict, 
                videos_data, 
                week=n_week, 
                day=n_day
            )
    
    # flatten
    classes = sum((
        [week_d[n_day] for n_day in sorted(week_d.keys())]
        for _, week_d in sorted(class_weeks.items(), key=lambda kv:kv[0])
    ), [])

    # apply next/prev
    apply_next_prev(classes)

    return classes

def make_class(output_folder_path, clase_template, clase_data):
    def fmt(class_dict):
        return f"{class_dict['week']}_{class_dict['day']}.md"
    fname = str(output_folder_path / fmt(clase_data))
    with open(fname, 'wt') as f:
        f.write(clase_template.render(**clase_data))

FILTERS_NAMES = {
    'datefmt': datefmt,
    'embedyt': embed_yt,
    'feriadofmt': feriadofmt,
    'compileejs': compile_ejs
}

def setup(template_folder="generacion/templates"):
    env = Environment(
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape()
    )

    for name, f in FILTERS_NAMES.items():
        env.filters[name] = f
    
    return env

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("-i","--crono", type=Path,
        default=Path("./generacion/cronogramas"))
    parser.add_argument("-d","--data", type=Path,
        default=Path("./generacion/data"))
    parser.add_argument("-o","--output", type=Path, 
        default=Path("./content/clases"))
    parser.add_argument("-t", "--templates", type=Path,
        default=Path("./generacion/templates"))

    args = parser.parse_args()
    
    print(str(args.templates))
    env = setup(str(args.templates))

    t = env.get_template('clase.md')

    cronograma = read_yaml(args.crono / (args.name+".yaml"))
    videos = read_yaml(args.data / "videos.yaml")

    clases = process_data(cronograma, videos)

    for clase in clases:
        print(f"W{clase['week']: <2}, D{clase['day']: <2}...",end="\t")
        make_class(args.output, t, clase)
        print("done")  
