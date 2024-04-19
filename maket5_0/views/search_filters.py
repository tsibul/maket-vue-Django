def order_search_filter(orders, search_string):
    return orders.filter(
        name__icontains=search_string,
        address__icontains=search_string,
        customer_name__icontains=search_string,
        customer_address__icontains=search_string,
        customer_inn__icontains=search_string,

        manager__name__icontains=search_string,
        manager__mail__icontains=search_string,
        manager__phone__icontains=search_string,

        customer__name__icontains=search_string,
        customer__address__icontains=search_string,
        customer__mail__icontains=search_string,
        customer__phone__icontains=search_string,
        customer__inn__icontains=search_string,

        item__name__icontains=search_string,
        item__print_name__icontains=search_string,
    ).distinct()
