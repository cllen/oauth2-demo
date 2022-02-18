import abc

class BaseMiniOrm(metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def get(self,**kwargs):
		pass

	@abc.abstractmethod
	def save(self,**kwargs):
		pass

	@abc.abstractmethod
	def update(self,instance,**kwargs):
		pass

	@abc.abstractmethod
	def first(self):
		pass