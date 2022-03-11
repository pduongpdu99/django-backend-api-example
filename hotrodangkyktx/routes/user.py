from django.urls import re_path as url
from django.urls import path
import hotrodangkyktx.api.user as user 

urlpatterns = [
	path('all/', user.get_all, name="user api - get all"),
	path('add/', user.add, name="user api - add data"),
	path('update/', user.update, name="user api - update data"),
	path('find/<str:role>', user.find, name="user api - find data by pk"),
	path('delete/<str:role>', user.delete, name="user api - delete data by pk"),
	url('paginate', user.paginate, name="user api - paginate data by limit, page,...."),
]