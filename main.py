from storage.json_store import ensure_len
import sys
from storage.json_store import CACHE_FILE, MAX_LEN, update_cache
from commands.list import list_task
from commands.add import add_task
from commands.delete import delete_task
from commands.help import help_task
from commands.update import update_task_priority
from commands.undo import undo_task
from commands.flush import flush_task_list

commands = {   # Dictionary containing the functions and argument types of the commands
    "add" : {
        "func" : add_task,
        "args" : ["str"],
        },
    "list" : {
        "func" : list_task,
        "args" : [],
        },        
    "delete" : {
        "func" : delete_task,
        "args" : ["int"],
        },
    "help" : {
        "func" : help_task,
        "args" : [],
        },
    "update" : {
        "func" : update_task_priority,
        "args" : ["int", "int"]
        },

    "undo" : {
        "func" : undo_task,
        "args" : [],
        },

    "flush" : {
        "func" : flush_task_list,
        "args" : []
        }
    }

action_commands = ["add", "delete", "update", "flush"]


def main():
    if len(sys.argv)<2:
        print("No command provided")  # Checks for the command's existence
        return

    name = sys.argv[1].lower()   # Command's name taken from CLI
    command = commands.get(name) # Extracting the corresponding command name from the dictionary
    


    if not command:
        print("Unknown command") # if the provided command name isnt in the command list, throws error
        help_task()
        return

    args = sys.argv[2:]    # Storing the arguments
    expected_arg_types = command["args"] # Storing the argument types

    if len(args) != len(expected_arg_types):
        print(f"{name} expects {len(expected_arg_types)} argument(s)") # Checks for the exact length of the arguments of the command provided
        help_task()
        return

    parsed_args = []  # Empty list to contain the parsed arguments

    for value, arg_type in zip(args, expected_arg_types):  #  Pairs up the arguments with their respective data types
        if arg_type == "int":                              # Since CLI takes only string inputs, this block checks and converts the integer inputs from string to integer
            try:
                parsed_args.append(int(value))             
            except ValueError:
                print("Invalid number")
                help_task()
                return
        else:
            parsed_args.append(value)            # Store all the converted or not arguments in the list

    if name in action_commands:
        ensure_len(CACHE_FILE, MAX_LEN)
        update_cache()

    command["func"](*parsed_args)                # Stylish way of dynamically calling the functions from the dictionary, 
                                                 # command["func"] extracts thefunction name and (*parsed_args) passes the arguments through the called function

if __name__ == "__main__":
    main()
                


