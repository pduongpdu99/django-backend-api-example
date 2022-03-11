from django.urls import re_path as url
from django.urls import path
import hotrodangkyktx.api.history as history 

urlpatterns = [
	path('all/', history.get_all, name="history api - get all"),
	path('add/', history.add, name="history api - add data"),
	path('update/', history.update, name="history api - update data"),
	path('find/<str:eventname>', history.find, name="history api - find data by pk"),
	path('delete/<str:eventname>', history.delete, name="history api - delete data by pk"),
	url('paginate', history.paginate, name="history api - paginate data by limit, page,...."),
]