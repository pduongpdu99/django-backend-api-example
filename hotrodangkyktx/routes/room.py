from django.urls import re_path as url
from django.urls import path
import hotrodangkyktx.api.room as room 

urlpatterns = [
	path('all/', room.get_all, name="room api - get all"),
	path('add/', room.add, name="room api - add data"),
	path('update/', room.update, name="room api - update data"),
	path('find/<str:name>', room.find, name="room api - find data by pk"),
	path('delete/<str:name>', room.delete, name="room api - delete data by pk"),
	url('paginate', room.paginate, name="room api - paginate data by limit, page,...."),
]