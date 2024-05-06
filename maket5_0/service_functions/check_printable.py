from maket5_0.models import PrintType


def check_printable(print_item):
    printable = True
    if not print_item.print_type:
        print_type = PrintType.objects.filter(name=print_item.type).first()
        if print_type:
            print_item.print_type = print_type
            printable = print_type.printable
            print_item.save()
    else:
        printable = print_item.print_type.printable
    return printable
