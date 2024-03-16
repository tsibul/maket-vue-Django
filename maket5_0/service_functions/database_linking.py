from django.db import models as models_rec


def linking_filter(model1, model2, model2_id):
    linking = find_linking_model(model1, model2)
    linking1 = cut_linking_pass(linking[0])
    linking2 = cut_linking_pass(linking[1])
    item2 = linking2[0][0].objects.get(id=model2_id)
    for i in range(len(linking2) - 1):
        item2 = getattr(item2, linking2[i + 1][1])
    item1 = [item2]
    for i in range(len(linking1) - 2, -1, -1):
        param_name = linking1[i + 1][1]
        kwargs = {f'{param_name}__in': item1}
        item1 = list(linking1[i][0].objects.filter(**kwargs).filter(deleted=False))
    return item1


def find_linking_model(model1, model2, field_name1=None, field_name2=None, visited1=None, visited2=None, path1=None,
                       path2=None):
    """

    :param model1:start model 1
    :param model2: start model 2
    :param field_name1: field of 1 model for connection
    :param field_name2: field of 2 model for connection
    :param visited1: set of visited models on road from model1
    :param visited2: set of visited models on road from model2
    :param path1: list of models connecting
    :param path2: list of models connecting
    :return:
    """
    if visited1 is None:
        visited1 = set()
    if visited2 is None:
        visited2 = set()
    if path1 is None:
        path1 = []
    if path2 is None:
        path2 = []

    visited1.add((model1, field_name1))
    path1.append((model1, field_name1))

    visited2.add((model2, field_name2))
    path2.append((model2, field_name2))

    if (model1, field_name1) == (model2, field_name2):
        return path1, path2

    fields1 = model1._meta.get_fields()
    fields2 = model2._meta.get_fields()

    for field1 in fields1:
        if isinstance(field1, models_rec.ForeignKey):
            related_model = field1.related_model
            if related_model not in visited1:
                linking_path1, linking_path2 = find_linking_model(related_model, model2, field1.name, field_name2,
                                                                  visited1, visited2, path1, path2)
                if linking_path1:
                    return linking_path1, linking_path2

    for field2 in fields2:
        if isinstance(field2, models_rec.ForeignKey):
            related_model = field2.related_model
            if related_model not in visited2:
                linking_path1, linking_path2 = find_linking_model(model1, related_model, field_name1, field2.name,
                                                                  visited1, visited2, path1, path2)
                if linking_path2:
                    return linking_path1, linking_path2

    visited1.remove((model1, field_name1))
    visited2.remove((model2, field_name2))
    return None


def cut_linking_pass(linking_path):
    """
    Make linking path without repeats
    :param linking_path:
    :return:
    """
    result_path = []
    for elem in linking_path:
        if elem not in result_path:
            result_path.append(elem)
    return result_path
