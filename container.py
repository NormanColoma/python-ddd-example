import pinject

from application.test_repository import TestRepository

class RepositoryBindingSpec(pinject.BindingSpec):
	def provide_repository(self):
		return TestRepository()


obj_graph = pinject.new_object_graph(binding_specs=[RepositoryBindingSpec()])
