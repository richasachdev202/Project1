import ipywidgets as widgets
from IPython.display import display

# Store expression
expression = ""

# Display box
display_box = widgets.Text(
    value='',
    placeholder='0',
    description='',
    layout=widgets.Layout(width='100%', height='50px')
)

# Functions
def on_button_click(b):
    global expression
    
    if b.description == "C":
        expression = ""
    elif b.description == "=":
        try:
            expression = str(eval(expression))
        except:
            expression = "Error"
    else:
        expression += b.description
    
    display_box.value = expression

# Create buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

button_widgets = []

for label in buttons:
    btn = widgets.Button(
        description=label,
        layout=widgets.Layout(width='60px', height='40px')
    )
    btn.on_click(on_button_click)
    button_widgets.append(btn)

# Arrange in grid
grid = widgets.GridBox(
    button_widgets,
    layout=widgets.Layout(
        grid_template_columns="repeat(4, 70px)",
        grid_gap="10px"
    )
)

# Display UI
display(display_box, grid)
