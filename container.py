import pinject

from application import test_repository

obj_graph = pinject.new_object_graph(modules=[test_repository])
