import datetime

from django.db.models import Q


def order_search_filter(orders, search_string):
    return orders.filter(
        Q(order_number__icontains=search_string) |
        # address__icontains=search_string,
        Q(customer_name__icontains=search_string) |
        Q(customer_address__icontains=search_string) |
        Q(customer_inn__icontains=search_string) |

        Q(manager__name__icontains=search_string) |
        Q(manager__mail__icontains=search_string) |
        Q(manager__phone__icontains=search_string) |

        Q(customer__name__icontains=search_string) |
        Q(customer__address__icontains=search_string) |
        Q(customer__mail__icontains=search_string) |
        Q(customer__phone__icontains=search_string) |
        Q(customer__inn__icontains=search_string) |

        Q(orderitem__name__icontains=search_string) |
        Q(orderitem__print_name__icontains=search_string)
    ).distinct()


def film_search_filter(film_list, search_string, sh_deleted):
    try:
        date_object = datetime.datetime.strptime(search_string, '%d.%m.%y').date()
    except ValueError:
        date_object = None
    try:
        film_no = int(search_string)
    except ValueError:
        film_no = None

    if film_no and film_no < 100:
        return film_list.filter(film_number__icontains=film_no)
    else:
        return film_list.filter(
            (Q(date=date_object) if date_object else Q()) |
            (Q(date_sent=date_object) if date_object else Q()) |

            (Q(groupinfilm__group__maket__order__order_number__icontains=search_string) |
             Q(groupinfilm__group__maket__order__customer__name__icontains=search_string) |
             Q(groupinfilm__group__name__icontains=search_string) |
             (Q(groupinfilm__group__maket__order__order_date=date_object) if date_object else Q())
             ) &
            (Q(groupinfilm__status=True) if not sh_deleted else Q())

        ).distinct()
