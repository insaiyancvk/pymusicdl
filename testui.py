'''from inspect import cleandoc
import itertools
import py_cui


class App:
    character_gen = itertools.cycle(("X", "-", "█", "[", "#"))

    def __init__(self, root_: py_cui.PyCUI):
        self.root = root_

        # Default configuration
        self.default = self.root.add_slider("Default", 0, 0, column_span=2, min_val=-50, max_val=50)

        # controls
        self.title_button = self.root.add_button("Toggle title", 1, 0, command=self.default.toggle_title)
        self.border_button = self.root.add_button("Toggle border", 1, 1, command=self.default.toggle_border)
        self.value_button = self.root.add_button("Toggle value", 1, 2, command=self.default.toggle_value)
        self.character_button = self.root.add_button("Cycle char", 2, 0, command=self.cycle_characters)
        self.align_button = self.root.add_button("Change alignment", 2, 1, command=self.cycle_height)
        self.step_slider = self.root.add_slider("Step size", 2, 2, min_val=1, init_val=2, max_val=10)
        self.spacer = self.root.add_text_block("Spacer", 0, 2)

        # setups
        self.root.set_on_draw_update_func(self.set_step)
        self.height_cycle = itertools.cycle(
            (
                self.default.align_to_top,
                self.default.align_to_middle,
                self.default.align_to_bottom,
            )
        )

        help_text = """
                    Press a button to make a change.
                    You can change character freely,
                    but for demonstration purpose,
                    I've set it to cycle it here.
                    """

        help_text = cleandoc(help_text)
        self.spacer.set_text(help_text)

    def cycle_characters(self):
        self.default.set_bar_char(next(self.character_gen))

    def cycle_height(self):
        next(self.height_cycle)()

    def set_step(self):
        self.default.set_slider_step(self.step_slider.get_slider_value())


if __name__ == '__main__':
    root = py_cui.PyCUI(3, 3)
    root.set_title("Slider playground")
    s = App(root)
    root.start()'''

"""Example of using py_cui to create a simple Command line TODO list in under 150 lines of code
@author:    Jakub Wlodek
@created:   12-Aug-2019
"""

'''import py_cui
import os
import logging

class SimpleTodoList:

    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        # The scrolled list cells that will contain our tasks in each of the three categories
        self.todo_scroll_cell =         self.master.add_scroll_menu('TODO',         0, 0, row_span=5, column_span=2)
        self.in_progress_scroll_cell =  self.master.add_scroll_menu('In Progress',  0, 2, row_span=7, column_span=2)
        self.done_scroll_cell =         self.master.add_scroll_menu('Done',         0, 4, row_span=7, column_span=2)

        # Textbox for entering new items
        self.new_todo_textbox = self.master.add_text_box('TODO Item', 5, 0, column_span=2)

        # buttons for rest of control
        self.mark_in_progress = self.master.add_button('Mark in Progress', 7, 0, column_span=2,    command=self.mark_as_in_progress)
        self.mark_in_progress = self.master.add_button('Mark As Done',     7, 2, column_span=2,    command=self.mark_as_done)
        self.remove_todo =      self.master.add_button('Remove TODO Item', 6, 1, pady = 1,         command=self.remove_item)
        self.new_todo_add =     self.master.add_button('Add TODO Item',    6, 0, pady =1,          command=self.add_item)
        self.save_todo_button = self.master.add_button('Save',             7, 4, column_span=2,    command=self.save_todo_file)

        # add some custom keybindings
        self.new_todo_textbox.add_key_command(          py_cui.keys.KEY_ENTER, self.push_and_reset)
        self.todo_scroll_cell.add_key_command(          py_cui.keys.KEY_ENTER, self.mark_as_in_progress)
        self.in_progress_scroll_cell.add_key_command(   py_cui.keys.KEY_ENTER, self.mark_as_done)
        self.read_todo_file()


    def push_and_reset(self):
        """Adds item and clears textbox. called when textbox is in focus mode and enter is pressed
        """

        self.add_item()
        self.new_todo_textbox.clear()


    def read_todo_file(self):
        """Read a saved todo file
        """

        todo = []
        in_progress = []
        done = []
        if os.path.exists('TODO.txt'):
            todo_fp = open('TODO.txt', 'r')
            state = 0
            line = todo_fp.readline()
            while line:
                line = line.strip()
                if state == 0:
                    if line == '__IN_PROGRESS__':
                        state = 1
                    elif len(line) > 1:
                        todo.append(line)
                elif state == 1:
                    if line == '__DONE__':
                        state = 2
                    elif len(line) > 1:
                        in_progress.append(line)
                elif state == 2:
                    if len(line) > 1:
                        done.append(line)
                line = todo_fp.readline()
            todo_fp.close()
        self.todo_scroll_cell.add_item_list(todo)
        self.in_progress_scroll_cell.add_item_list(in_progress)
        self.done_scroll_cell.add_item_list(done)


    def add_item(self):
        """Add a todo item
        """

        self.todo_scroll_cell.add_item('{}'.format(self.new_todo_textbox.get()))


    def remove_item(self):
        """Remove a todo item
        """

        self.todo_scroll_cell.remove_selected_item()


    def mark_as_in_progress(self):
        """Mark a todo item as inprogress. Remove it from todo scroll list, add it to in progress list, or show error popup if no tasks
        """

        in_prog = self.todo_scroll_cell.get()
        if in_prog is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as in progress')
            return
        self.todo_scroll_cell.remove_selected_item()
        self.in_progress_scroll_cell.add_item(in_prog)


    def mark_as_done(self):
        """Mark a inprogress item as done. Remove it from inprogress scroll list, add it to done list, or show error popup if no tasks
        """

        done = self.in_progress_scroll_cell.get()
        if done is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as done')
            return
        self.in_progress_scroll_cell.remove_selected_item()
        self.done_scroll_cell.add_item(done)


    def save_todo_file(self):
        """Save the three lists in a specific format
        """

        if os.path.exists('TODO.txt'):
            os.remove('TODO.txt')
        todo_fp = open('TODO.txt', 'w')
        todo_items = self.todo_scroll_cell.get_item_list()
        in_progress_items = self.in_progress_scroll_cell.get_item_list()
        done_items = self.done_scroll_cell.get_item_list()
        for item in todo_items:
            todo_fp.write(item + '\n')
        todo_fp.write('__IN_PROGRESS__' + '\n')
        for item in in_progress_items:
            todo_fp.write(item + '\n')
        todo_fp.write('__DONE__' + '\n')
        for item in done_items:
            todo_fp.write(item + '\n')
        todo_fp.close()
        self.master.show_message_popup('Saved', 'Your TODO list has been saved!')


# Create the CUI, pass it to the wrapper object, and start it
root = py_cui.PyCUI(8, 6)
root.set_title('CUI TODO List')
#root.enable_logging(logging_level=logging.DEBUG)
s = SimpleTodoList(root)
root.start()'''

import py_cui

class MultiWindowDemo:

    def __init__(self, root: py_cui.PyCUI):

        # Root PyCUI window
        self.root = root

        # Collect current CUI configuration as a widget set object
        self.widget_set_A = self.root.create_new_widget_set(3,3)

        # Add a button the the CUI
        self.widget_set_A.add_button('Open 2nd Window', 1, 1, command = self.open_set_B)

        # apply the initial widget set
        self.root.apply_widget_set(self.widget_set_A)

        # Create a second widget set (window). This one will have a 5x5 grid, not 3x3 like the original CUI
        self.widget_set_B = self.root.create_new_widget_set(5, 5)

        # Add a text box to the second widget set
        self.text_box_B = self.widget_set_B.add_text_box('Enter something', 0, 0, column_span=2)
        self.text_box_B.add_key_command(py_cui.keys.KEY_ENTER, self.open_set_A)


    def open_set_A(self):
        # Fired on the ENTER key in the textbox. Use apply_widget_set to switch between "windows"
        self.root.apply_widget_set(self.widget_set_A)


    def open_set_B(self):
        # Fired on button press. Use apply_widget_set to switch between "windows"
        self.root.apply_widget_set(self.widget_set_B)


# Create CUI object, pass to wrapper class, and start the CUI
root = py_cui.PyCUI(3, 3)
wrapper = MultiWindowDemo(root)
root.start()