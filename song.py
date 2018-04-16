class song:
	def __init__(self,id,name,singer):
		self._id=id
		self._name=name
		self._singer=singer
	def get_id(self):
		return self._id
	def get_name(self):
		return self._name
	def get_singer(self):
		return self._singer
	def get_comments_link(self):
		return "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token=".format(self._id)