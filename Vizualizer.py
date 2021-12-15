import dominate
from dominate.tags import *
import colorsys


def conv_steps_all(steps):
    all = []
    for step in steps:
        for spot in step:
            all.append(spot)
    return all

def lighten_color(color, amount):
    #https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    h = color.lstrip('#')
    c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    #https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib/49601444
    c = colorsys.rgb_to_hls(*c)
    c = colorsys.hls_to_rgb(c[0], c[1] + amount, c[2])
    return '%02x%02x%02x' % c

def to_html(grid, steps, path, filename):
    gridsize = (len(grid), len(grid[0]))
    converted_steps = conv_steps_all(steps)

    num_steps = len(steps)
    styleString = "table {width: 500px;margin: 2em auto;}th, td {border: solid 1px lightgrey;padding: 0.5em;}\n"


    for i in range(num_steps):
        animstring = f"""@keyframes color{i} [
                0% [background-color: #f1f1f1]
                100% [background-color: hsl(217, 74%, {(i/num_steps)*100}%)]
            ]\n"""
        styleString += animstring.replace('[', '{').replace(']', '}')
        animstring = f"""@keyframes color{i}path [
                0% [background-color: #f1f1f1]
                100% [background-color: hsl(60, 100%, {(i/num_steps)*100}%)]
            ]\n"""
        styleString += animstring.replace('[', '{').replace(']', '}')

        styleString += f".cell{i}"
        styleString += "{"
        styleString += f"""
            animation-name: color{i};
            animation-duration: 0.5s;
            animation-delay: {0.5 * (i+1)}s;
            animation-fill-mode: forwards;    
        """
        styleString += '}\n'
        tempstring = f""" .cell{i}path[
            animation-name: color{i}, color{i}path;
            animation-duration: 0.5s, 0.5s;
            animation-delay: {0.5 * (i+1)}s, {(0.5 * (i+ num_steps +1)) }s;
            animation-fill-mode: forwards;
            ]\n
        """
        styleString += tempstring.replace('[', '{').replace(']', '}')

    doc = dominate.document()
    with doc.head:
        style(styleString)


    table_grid = table()
    for row in grid:
        row_grid = tr()
        for ele in row:
            element = td()
            if ele == ["obstacle"]:
                element += img(src="brick-wall.jpg", width=50, height=50)
            row_grid += element
        table_grid += row_grid

    counter = 0
    for step in steps:
        for pair in step:
            table_grid.children[pair[0]].children[pair[1]]["class"] = f"cell{counter}"
            if pair in path:
                if pair == path[0]:
                    table_grid.children[pair[0]].children[pair[1]].add("Begin")
                elif pair == path[-1]:
                    table_grid.children[pair[0]].children[pair[1]].add("End")
                table_grid.children[pair[0]].children[pair[1]]["class"] = f"cell{counter}path"
        counter += 1


    doc += table_grid
    file = open(filename, "w")
    file.write(doc.render())
    file.close()
    pass

