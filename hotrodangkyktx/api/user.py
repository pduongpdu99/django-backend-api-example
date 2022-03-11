from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from ..models import User
import json, datetime

# private method


def __is_field_valid(body_keys, model_keys):
    for key in body_keys:
        if key not in model_keys:
            return False
    return True


# select all
@csrf_exempt
def get_all(request):
    """select data

    Args:
        non argument

    Returns:
        dataset by model
    """
    if request.method in ['GET']:
        fields = list(map(lambda item: item.name, User._meta.fields))
        data =[]
        
        for item in User.objects.all().order_by('role').values(*fields):
            # process all value to string
            for field in fields:
                if item[field] is datetime.datetime:
                    item[field] = datetime.datetime.strptime(item[field], "%Y-%m-%d %H:%M:%S")
                
                if item[field] is not str:
                    item[field] = str(item[field])
            
            data.append(item);
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    return HttpResponse([])

@csrf_exempt
# insert query
def add(request):
    """insert data

    Args:
        request (MODEL): MODEL, which is the input of client expect

    Returns:
        insert data from MODEL into database
    """

    if request.method in ['POST']:
        try:
            # declare result variable
            results = {}

            # loads body from client request
            body = json.loads(request.body.decode('utf-8'))

            # field validation
            body_keys = list(body)
            fields = list(map(lambda item: item.name, User._meta.fields))

            # set value from fields of model
            for field in fields:
                if field in list(body):
                    results[field] = body[field]
                else:
                    results[field] = None

            # check field isn't in model
            if not __is_field_valid(body_keys, fields):
                return HttpResponse("Field invalid with model")

            # check that's exist in database
            vals = User.objects.filter(
                role=results[User._meta.pk.name]).values()

            if len(vals) > 0:
                return HttpResponse("It's exist")
            else:
                # not exist
                user_new = User(*dict(results).values())
                user_new.save(),
                return HttpResponse(json.dumps(results, ensure_ascii=False))
        except Exception as error:
            print(error)
            pass
    return HttpResponse("Method invalid")


@csrf_exempt
# update query
def update(request):
    """update data

    Args:
        request (MODEL): MODEL, which is the input of client expect

    Returns:
        update data from MODEL into database
    """
    if request.method in ['PUT']:
        try:
            body = json.loads(request.body.decode('utf-8'))

            # field validation
            body_keys = list(body)
            fields = list(map(lambda item: item.name, User._meta.fields))

            if not __is_field_valid(body_keys, fields):
                return HttpResponse("Field invalid with model")

            query = User.objects.filter(role=body[User._meta.pk.name])
            index = query.values().first()

            def get_value(index_name):
                return body[index_name] if (index_name in list(body) and body[index_name] != None) else index.get(index_name)

            if query.exists():
                # update
                query.update(
                    name=get_value('name'),
					phonenumber=get_value('phonenumber'),
					address=get_value('address'),
					nationality=get_value('nationality'),
					idcard=get_value('idcard'),
					birth=get_value('birth'),
					sex=get_value('sex'),
					roomid=get_value('roomid')
                )
                return HttpResponse(json.dumps(body, ensure_ascii=False))
            else:
                return HttpResponse("It is not exist")
        except Exception as error:
            print(error)
            pass
    return HttpResponse("Method invalid")


@csrf_exempt
# delete query
def delete(request, role):
    """delete data by primary key

    Args:
        request (id): id (primary key) that's presentation of entry

    Returns:
        delete record
    """
    if request.method in ['DELETE']:
        try:
            # field validation
            query = User.objects.filter(role=role)
            if query.exists():
                query.delete()
                return HttpResponse("'{pk_id}' deleted".format(pk_id=role))
            else:
                return HttpResponse("")
        except Exception as error:
            print(error)
            pass

    return HttpResponse("Method invalid")


@csrf_exempt
# find query
def find(request, pk_id):
    """find data by primary key

    Args:
        request (id):  id (primary key) that's presentation of entry

    Returns:
        data by id
    """
    if request.method in ['GET']:
        fields = list(map(lambda item: item.name, User._meta.fields))
        return HttpResponse(dict(item) for item in User.objects.filter(role=pk_id).values(*fields))
    return HttpResponse("Http method is invalid")


@csrf_exempt
# paginate
def paginate(request):
    """paginate: load data by limit and page

    Args:
        request (limit): the record's amount
        request (page): page index

    Returns:
        limit: the record's amount
        page: page index
        results: load data by limit and page
        total_results: all possible data in the database
        total_page: number page with limit and page current
    """
    if request.method in ["GET"]:
        try:
            _page = request.GET.get("page")
            _limit = request.GET.get("limit")
            _argument = dict(request.GET)

            # remove limit and page field from argument
            _argument.pop('limit')
            _argument.pop('page')

            # arguments process
            for key in _argument.keys():
                _argument[key] = "".join(_argument[key])

            # validate
            if _page == None or _limit == None:
                return HttpResponse("Paginate is invalid")

            # filter process
            _limit = int(_limit)
            _page = int(_page)

            _obj_all = User.objects.filter(**_argument).all()
            user_list = _obj_all.order_by('role').values()
            paginator = Paginator(
                user_list, _limit, allow_empty_first_page=False)
            page_obj = paginator.get_page(_page)

            # get result
            _num_page = paginator.num_pages
            _amount = len(_obj_all.values())

            _results = [dict(item) for item in page_obj]
            if _page > _num_page:
                _results = []

            data = {
                "limit": _limit,
                "page": _page,
                "results": _results,
                "total_page": _num_page,
                "total_result": _amount,
            }
            return HttpResponse(str(data).replace('\'', '"'))
        except Exception as error:
            print(error)
            pass
    else:
        return HttpResponse("Http method is invalid")