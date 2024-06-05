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


def film_search_filter(film_list, search_string):
    return film_list