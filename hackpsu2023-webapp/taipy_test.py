from taipy.gui import Gui, notify
from PIL import Image


text = ''


page = """
# Eye disease *type*


Types: <|{text}|>


<|Normal|button|on_action=on_button_action|>
<|Cataract|button|on_action=on_button_action|>
<|Glaucoma|button|on_action=on_button_action|>
<|Diabetes|button|on_action=on_button_action|>
"""


# Dictionary to map category names to image paths
image_paths = {
    'Normal': "./N/2332_left.jpg",
    'Cataract': "./C/_0_4015166.jpg",
    'Glaucoma': "./G/1213_left.jpg",
    'Diabetes': "./D/1000_right.jpg",
}

def on_button_action(state):
    notify(state, 'info', f'The text is {state}')
   
    # Get the image path based on the selected category
    image_path = image_paths.get(state, "")
   
    if image_path:
        # Open and display the image
        img = Image.open(image_path)
        img.show()


def on_change(state, var_name, var_value):
    if var_name == 'text' and var_value == 'Reset':
        state.text = ''
        return


Gui(page).run()
