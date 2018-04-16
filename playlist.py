class playlist:
	def __init__(self,id,name,singer):
		self._id=id
		self._name=name
		self._singer=singer
	def get_id(self):
		return self._id
	def get_name(self):
		return self._name
	def get_creator(self):
		return self._singer
	def get_playlist_link(self):
		return "http://music.163.com/api/playlist/detail?id={}&upd".format(self._id)