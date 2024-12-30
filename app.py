import tkinter as tk
import tkinter.ttk as ttk
from recipe_db_service import get_meal_categories, filter_by_category, lookup_meal_by_id

# Globals
search_tags = []
cat_rc = [1,1]
meals = {}
found_meals = []
meals_rc = [1,1]
selected_meals = []
ingredient_tags = set()
ing_rc = [1,1]

# Functions
def get_search_tags():
    active_tags = [tag.cget('text') for tag in search_tags if tag.toggled.get() == 1]
    # for tag in search_tags:
    #     tag.toggled.set(0)
    return active_tags


def reset_last_search():
    global meals, found_meals
    meals = {}
    for mealItem in found_meals:
        mealItem.frame.destroy()
    found_meals = []
    for tag in search_tags:
        tag.toggled.set(0)


def search():
    # reset_last_search()
    search_term=search_var.get()
    active_tags = get_search_tags()
    print("The search term is : " + search_term)
    print(active_tags)
    for tag in active_tags:
        meals.update(filter_by_category(tag))
    print(meals)
    for meal in meals:
        create_found_meal_item(meal, meals[meal])
    search_var.set("")


class TagButton(tk.Checkbutton):
    def __init__(self, search_word: str, master: tk.Misc):
        self.toggled = tk.IntVar()
        super().__init__(master,
        text=search_word,
        variable=self.toggled,
        indicatoron=False,
        command=self.on_toggle)

    def on_toggle(self):
        print("Button toggled:", self.toggled.get())


class MealItem():
    def __init__(self, meal_name: str, mealid: int, master: tk.Misc, button_txt="+", command=None):
        if not command:
            command=self.select_meal
        self.meal_details = None
        self.meal_name = meal_name
        self.mealid = mealid
        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame,
                       text=meal_name)
        self.label.grid(row=1,column=1)
        self.button = tk.Button(self.frame,
                       text=button_txt,
                       command=command)
        self.button.grid(row=1,column=2)
        self.frame.grid(row=meals_rc[0],column=meals_rc[1])
        meals_rc[0] += 1

    def select_meal(self):
        self.frame.destroy()
        found_meals.remove(self)
        self.__init__(self.meal_name, self.mealid, selected_meals_frame,"-",self.deselect_meal)
        if not self.meal_details:
            self.meal_details = lookup_meal_by_id(self.mealid)
        for val in self.meal_details:
            if val.startswith("strIngredient") and self.meal_details[val]:
                create_tag_button(self.meal_details[val], ing_rc, ingredient_tags_frame)
                ingredient_tags.update(self.meal_details[val])

    def deselect_meal(self):
        self.frame.destroy()
        selected_meals.remove(self)


def create_tag_button(search_word: str, tag_rc: list, master: tk.Misc):
    new_tag = TagButton(search_word, master)
    new_tag.grid(row=tag_rc[0],column=tag_rc[1])
    if tag_rc[1] < 4:
        tag_rc[1] += 1
    else:
        tag_rc[0] += 1
        tag_rc[1] = 1

    search_tags.append(new_tag)

def create_found_meal_item(meal_name: str, mealid: int):
    meal_item = MealItem(meal_name, mealid, found_meals_frame)
    if meal_item.meal_name not in [meal.meal_name for meal in found_meals]:
        found_meals.append(meal_item)

# Create main window
root = tk.Tk()
root.geometry('400x700')
root.title("Recipe Brainstormer")
search_var = tk.StringVar()
tabControl = ttk.Notebook(root)


# Create tab1
tab1 = ttk.Frame(tabControl)

    # Create a Canvas and Scrollbar for tab1
canvas = tk.Canvas(tab1)
scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

    # Configure the canvas
scrollable_frame.bind("<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

    # grid canvas and scrollbar
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)

    # Create tabs for tag selections
tags_notebook = ttk.Notebook(scrollable_frame)
tags_notebook.grid(row=3, column=1, padx=10, pady=10)
inc_tag_tab = ttk.Frame(tags_notebook)
# inc_tag_tab.config(Background="black")
exc_tag_tab = ttk.Frame(tags_notebook)


    # Add frames inside the scrollable_frame
selected_meals_frame = ttk.Frame(scrollable_frame)
selected_meals_frame.grid(row=1, column=1)

search_frame = ttk.Frame(scrollable_frame)
search_frame.grid(row=2, column=1)

category_tags_frame = ttk.Frame(inc_tag_tab)#scrollable_frame)
category_tags_frame.grid(row=3, column=1)

ingredient_tags_frame = ttk.Frame(inc_tag_tab)#scrollable_frame)
ingredient_tags_frame.grid(row=4, column=1, pady=10)

found_meals_frame = ttk.Frame(scrollable_frame)
found_meals_frame.grid(row=5, column=1)

    # Create search box & button
search_box = ttk.Entry(search_frame, textvariable=search_var)
search_box.grid(row=1, column=1)
search_btn = tk.Button(search_frame, text='Search', command=search)
search_btn.grid(row=1, column=2)
reset_btn = tk.Button(search_frame, text='Reset', command=reset_last_search)
reset_btn.grid(row=1, column=3)

tags_notebook.add(inc_tag_tab, text="Inclusive Tags")
tags_notebook.add(exc_tag_tab, text="Exclusive Tags")
tabControl.add(tab1, text='Recipe search')

# Create tab2
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='My recipes')

# Create tab3
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='Shopping list')

# Pack components
tabControl.pack(expand=1, fill="both")

for cat in get_meal_categories():
    create_tag_button(cat, cat_rc, category_tags_frame)

# for meal in selected_meals:
#     get_ingredients

root.mainloop()