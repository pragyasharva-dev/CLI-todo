import sys
from commands.list import list_task
from commands.add import add_task
from commands.delete import delete_task
from commands.help import help_task

commands = {
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
    }


def main():
    if len(sys.argv)<2:
        print("No command provided")
        return

    name = sys.argv[1].lower()
    command = commands.get(name)

    if not command:
        print("Unknown command")
        help_task()
        return

    args = sys.argv[2:]
    expected_arg_types = command["args"]

    if len(args) != len(expected_arg_types):
        print(f"{name} expects {len(expected_arg_types)} argument(s)")
        help_task()
        return

    parsed_args = []

    for value, arg_type in zip(args, expected_arg_types):
        if arg_type == "int":
            try:
                parsed_args.append(int(value))
            except ValueError:
                print("Invalid number")
                help_task()
                return
        else:
            parsed_args.append(value)

    command["func"](*parsed_args)


if __name__ == "__main__":
    main()
                


